# Raytracing Documentation

This document describes where the documentation is, how to write or update documentation for the Raytracing module and how to publish updated documentation through ReadTheDocs.

## Reading documentation

If you are a user of the raytracing package, you probably want to read the documentation online at https://raytracing.readthedocs.io/ 

## Writing documentation

If you are a developer, you may be interested in updating the documentation. The documentation is auto-generated with the Sphynx documentation module from the comments directly from the code (i.e. docstrings). There are many different formats that can be used, but the one used in Raytracing is the [Numpy Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html) format. 

## Publishing documentation (maintainers only)

Maintainers of the package publish the documentation with each release. To create the documentation and publish it, follow the guidelines below.

### Requirements

These requirements are only for anyone who wants to publish the documentation, and are not necessary for the use of the Raytracing package.

```
pip install sphinx
pip install recommonmark
pip install sphinx_rtd_theme
```
The package `recommonmark` adds Markdown support.

### Files controlling the format

*[FIXME: Information here on key files and their role in the Sphynx documentation system]*

### Build online
The online documentation can be updated directly from the [RayTracing project](https://readthedocs.org/projects/raytracing/) on ReadTheDocs by the project administrator (currently dccote) to match the release from PyPI.

### Build local

Anyone can build the documentation locally. From the docs directory, with appropriate tools installed, type: 
```
make html
```
Then you can open `_build/html/index.html`.

> For some reasons on my computer I have to leave the folder `docs` and call `docs/make html`

### Technical details

- When autogenerating the stub files from toctrees in `reference.rst`, note that sphinx-autogen requires to load a pythonpath to your project. 
  
    On windows the command is 
    ```
  $ set PYTHONPATH=C:\Path\to\project
  $ sphinx-autogen -t docs/_templates docs/reference.rst
  ```
    On Mac/Linux:
    ```
  PYTHONPATH=. sphinx-autogen -t docs/_templates docs/index.rst
    ```
