# GeoPicTagReader

![GeoVisio logo](https://gitlab.com/geovisio/api/-/raw/develop/images/logo_full.png)

Python library to extract standardized metadata from geolocated pictures EXIF metadata.

[[_TOC_]]


## Features

This tool allows you to:

- Analyse various EXIF variables to extract standardized metadata for geolocated pictures applications


## Install

GeoPicTagReader can be installed using two methods:

- From [PyPI](https://pypi.org/project/geopictagreader/), the Python central package repository
- Using this [Git repository](https://gitlab.com/geovisio/geo-picture-tag-reader)

### From PyPI

Just launch this command:

```bash
pip install geopic_tag_reader
```

After this you should be able to use the CLI tool with the name `geopic-tag-reader`:

```bash
geopic-tag-reader --help
```

Alternatively, you can use [pipx](https://github.com/pypa/pipx) if you want all the script dependencies to be in a custom virtual env.

You need to [install pipx](https://pypa.github.io/pipx/installation/), then:

```bash
pipx install geopic_tag_reader
```

### From Git repository

Download the repository:

```bash
git clone https://gitlab.com/geovisio/geo-picture-tag-reader.git geopic_tag_reader
cd geopic_tag_reader/
```

To avoid conflicts, it's considered a good practice to create a _[virtual environment](https://docs.python.org/3/library/venv.html)_ (or virtualenv). To do so, launch the following commands:

```bash
# Create the virtual environment in a folder named "env"
python3 -m venv env

# Launches utilities to make environment available in your Bash
source ./env/bin/activate
```

Then, install the dependencies using pip:

```bash
pip install -e .
```

You can also install the `dev` dependencies if necessary (to have lints, format, tests, ...):

```bash
pip install -e .[dev]
```

Then, you can use the `geopic-tag-reader` command:
```bash
geopic-tag-reader --help
```


## Usage

This library can be used both from command-line or as Python module.

### As command-line

To see all available commands:

```bash
geopic-tag-reader --help
```

[Full documentation is also available here](./docs/CLI_USAGE.md).

### As Python library

In your own script, you can use:

```python
from geopic_tag_reader import reader
from PIL import Image

# Open an image with Pillow
img = Image.open("my_picture.jpg")

# Read EXIF metadata
metadata = reader.readPictureMetadata(img)

# Print results
print(metadata)
```

[Full documentation is also available here](./docs/API_USAGE.md).


## Development

### Tests

Tests are run using PyTest. You can simply run this command to launch tests:

```bash
pytest
```

### Documentation

High-level documentation is handled by [Typer](https://typer.tiangolo.com/). You can update the generated `USAGE.md` file using this command:

```bash
make docs
```

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Note that before opening a pull requests, you may want to check formatting and tests of your changes:

```bash
make ci
```


## License

Copyright (c) GeoVisio team 2023, [released under MIT license](./LICENSE).
