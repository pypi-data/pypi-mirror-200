from PIL import Image, ExifTags
import xmltodict
import datetime
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class GeoPicTags:
    """Tags associated to a geolocated picture

    Attributes:
        lat (float): GPS Latitude (in WGS84)
        lon (float): GPS Longitude (in WGS84)
        ts (float): The capture date (as POSIX timestamp)
        heading (int): Picture heading (in degrees, North = 0°, East = 90°, South = 180°, West = 270°)
        type (str): The kind of picture (flat, equirectangular)
        make (str): The camera manufacturer name
        model (str): The camera model name
        focal_length (float): The camera focal length (in mm)
        exif (dict[str, str]): Raw EXIF tags from picture
    """

    lat: float
    lon: float
    ts: float
    heading: int
    type: str
    make: str
    model: str
    focal_length: float
    exif: Dict[str, str] = field(default_factory=lambda: {})


class PartialExifException(Exception):
    """Exception for partial / missing EXIF information from image"""

    def __init__(self, msg):
        super().__init__(msg)


def readPictureMetadata(picture):
    """Extracts metadata from picture file

    Args:
        picture (PIL.Image): Picture file

    Returns:
        GeoPicTags: Extracted metadata from picture
    """

    data = {}

    info = picture._getexif()
    if info:
        for tag, value in info.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = ExifTags.GPSTAGS.get(t, t)
                    data[sub_decoded] = value[t]
            else:
                data[decoded] = value

    # Read XMP tags
    for segment, content in picture.applist:
        if segment == "APP1":
            marker, body = content.split(b"\x00", 1)
            if marker == b"http://ns.adobe.com/xap/1.0/":
                body = body.strip(b"\00")
                description = xmltodict.parse(body)["x:xmpmeta"]["rdf:RDF"][
                    "rdf:Description"
                ]
                if isinstance(description, list):
                    # there can be several rdf:Description, if that's the case, we merge them all
                    description = {k: v for d in description for k, v in d.items()}
                data = data | description

    # Cleanup XMP tags with @
    for k in list(data):
        if k.startswith("@"):
            data[k[1:]] = data[k]
            del data[k]

    # Parse latitude/longitude
    if (
        isExifTagUsable(data, "GPSLatitude", tuple)
        and isExifTagUsable(data, "GPSLongitude", tuple)
        and isExifTagUsable(data, "GPSLatitudeRef")
        and isExifTagUsable(data, "GPSLongitudeRef")
    ):
        latRaw = data["GPSLatitude"]
        lat = (-1 if data["GPSLatitudeRef"] == "S" else 1) * (
            float(latRaw[0]) + float(latRaw[1]) / 60 + float(latRaw[2]) / 3600
        )

        lonRaw = data["GPSLongitude"]
        lon = (-1 if data["GPSLongitudeRef"] == "W" else 1) * (
            float(lonRaw[0]) + float(lonRaw[1]) / 60 + float(lonRaw[2]) / 3600
        )
    else:
        raise PartialExifException(
            "No GPS coordinates or broken coordinates in picture EXIF tags"
        )

    # Parse date/time
    if isExifTagUsable(data, "GPSTimeStamp", tuple) and isExifTagUsable(
        data, "GPSDateStamp"
    ):
        timeRaw = data["GPSTimeStamp"]
        dateRaw = data["GPSDateStamp"].replace(":", "-").replace("\x00", "")
        msRaw = (
            data["SubSecTimeOriginal"]
            if isExifTagUsable(data, "SubSecTimeOriginal", float)
            else "0"
        )
        d = datetime.datetime.combine(
            datetime.date.fromisoformat(dateRaw),
            datetime.time(
                int(timeRaw[0]),
                int(timeRaw[1]),
                int(timeRaw[2]),
                int(msRaw[:6].ljust(6, "0")),
                tzinfo=datetime.timezone.utc,
            ),
        )
    elif isExifTagUsable(data, "DateTimeOriginal"):
        dateRaw = data["DateTimeOriginal"].split(" ")[0].replace(":", "-")
        timeRaw = data["DateTimeOriginal"].split(" ")[1].split(":")
        msRaw = (
            data["SubSecTimeOriginal"]
            if isExifTagUsable(data, "SubSecTimeOriginal", float)
            else "0"
        )
        d = datetime.datetime.combine(
            datetime.date.fromisoformat(dateRaw),
            datetime.time(
                int(timeRaw[0]),
                int(timeRaw[1]),
                int(timeRaw[2]),
                int(msRaw[:6].ljust(6, "0")),
                tzinfo=datetime.timezone.utc,
            ),
        )
    else:
        raise PartialExifException("No date in picture EXIF tags")

    # Heading
    heading = None
    if isExifTagUsable(data, "GPano:PoseHeadingDegrees", float) and isExifTagUsable(
        data, "GPSImgDirection", float
    ):
        gpsDir = int(round(data["GPSImgDirection"]))
        gpanoHeading = int(round(float(data["GPano:PoseHeadingDegrees"])))
        if gpsDir > 0 and gpanoHeading == 0:
            heading = gpsDir
        elif gpsDir == 0 and gpanoHeading > 0:
            heading = gpanoHeading
        else:
            if gpsDir == gpanoHeading:
                heading = gpanoHeading
            else:
                raise PartialExifException(
                    "Contradicting heading values in EXIF PoseHeadingDegrees and GPSImgDirection tags"
                )
    elif isExifTagUsable(data, "GPano:PoseHeadingDegrees", float):
        heading = int(round(float(data["GPano:PoseHeadingDegrees"])))
    elif isExifTagUsable(data, "GPSImgDirection", float):
        heading = int(round(data["GPSImgDirection"]))

    # Make and model
    make = decodeMakeModel(data["Make"]).strip() if "Make" in data else None
    model = decodeMakeModel(data["Model"]).strip() if "Model" in data else None
    if model is not None and model is not None:
        model = model.replace(make, "").strip()

    return GeoPicTags(
        lat,
        lon,
        d.timestamp(),
        heading,
        data["GPano:ProjectionType"]
        if isExifTagUsable(data, "GPano:ProjectionType")
        else "flat",
        make,
        model,
        float(data["FocalLength"])
        if isExifTagUsable(data, "FocalLength", float)
        else None,
        data,
    )


def decodeMakeModel(value):
    """Python 2/3 compatible decoding of make/model field."""
    if hasattr(value, "decode"):
        try:
            return value.decode("utf-8").replace("\x00", "")
        except UnicodeDecodeError:
            return None
    else:
        return value.replace("\x00", "")


def isExifTagUsable(exif, tag, expectedType=str):
    """Is a given EXIF tag usable (not null and not an empty string)

    Args:
        exif (dict): The EXIF tags
        tag (str): The tag to check
        expectedType (class): The expected data type

    Returns:
        bool: True if not empty
    """

    try:
        if not tag in exif:
            return False
        elif not (expectedType == float or isinstance(exif[tag], expectedType)):
            return False
        elif not (
            expectedType != str or len(exif[tag].strip().replace("\x00", "")) > 0
        ):
            return False
        elif not (expectedType != float or float(exif[tag]) is not None):
            return False
        else:
            return True
    except ValueError:
        return False
