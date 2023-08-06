from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Unified OGC Api Python Client'
LONG_DESCRIPTION = 'Python package that provides a simple and consistent interface for working with OGC (Open Geospatial Consortium) services'

# Setting up
setup(
    name="PyOGC",
    version=VERSION,
    author="Ryanwalker277 (Anvansh)",
    author_email="<anvansh30mar@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests','pytest'],
    keywords=['python', 'video', 'OGC', 'API', 'client', 'unified', 'pyogc', 'pyogcclient'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)