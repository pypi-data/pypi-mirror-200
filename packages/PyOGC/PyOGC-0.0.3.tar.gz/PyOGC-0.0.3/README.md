# PyOGC

[![GitHub issues](https://img.shields.io/github/issues/RyanWalker277/PyOGC)](https://github.com/RyanWalker277/PyOGC/issues)
[![GitHub forks](https://img.shields.io/github/forks/RyanWalker277/PyOGC)](https://github.com/RyanWalker277/PyOGC/network)
[![GitHub stars](https://img.shields.io/github/stars/RyanWalker277/PyOGC)](https://github.com/RyanWalker277/PyOGC/stargazers)
[![GitHub license](https://img.shields.io/github/license/RyanWalker277/PyOGC)](https://github.com/RyanWalker277/PyOGC/blob/main/LICENSE)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) ![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square) ![GitHub contributors](https://img.shields.io/github/contributors-anon/RyanWalker277/PyOGC)
<br>

PyOGC is a Python package that provides a simple and consistent interface for working with OGC (Open Geospatial Consortium) services such as WMS, WFS, WCS, and Tiling Services.

PyOGC is built using modern Python development tools and practices, including Poetry for package management and Pytest for testing. It is designed to be easy to install and use, and to provide clear and comprehensive documentation.

# Installation

```
pip install PyOGC
```
# Usage

```
from PyOGC import landing
data = landing.metadata()

print(data)
```

Here is an example of how to use PyOGC to retrieve a tile matrix set:

```
from PyOGC.TilingSchemes.schemes import TilesAPI

api = TilesAPI()

# Get all available tile matrix sets
tile_matrix_sets = api.get_tile_matrix_sets()
print(tile_matrix_sets)

# Get a specific tile matrix set
tile_matrix_set = api.get_tile_matrix_set("CDB1GlobalGrid")
print(tile_matrix_set)
```
# Development

If you want to contribute to PyOGC or modify it to suit your needs, you can get started with the following steps:

## Clone the repository:

```
git clone <https://github.com/your_username/PyOGC.git>
```
Change into the directory: 
```
cd PyOGC
```
Create a new virtual environment: 
```
python3 -m venv venv
```
Activate the virtual environment: 
```
source venv/bin/activate
```
Install PyOGC and its dependencies: 
```
poetry install
```
Once you have installed PyOGC, you can run the tests to make sure everything is working as expected:
```
poetry run pytest
```
If you want to modify the tests or add new tests, you can find them in the `tests` directory. You can also run individual tests by specifying the test file and the test name:

```
poetry run pytest tests/test_ogc.py::test_get_capabilities
```
## Support++

This project needs your shiny star ⭐.  
Don't forget to leave a star ⭐️

![forthebadge made-with-python](https://forthebadge.com/images/badges/open-source.svg) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)


## Contributors

<!-- readme: contributors -start -->
<!-- readme: contributors -end -->

##

Made with ❤ by Anvansh ([@RyanWalker277](https://github.com/RyanWalker277))