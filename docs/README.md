# Sphinx Documentation
You can now browse the documentation online at https://raytracing.readthedocs.io/ 

## Contribute
We need help to write the API documentation. 
Since the documentation pages are auto-generated from the doctrings, 
please follow the required [Google Docstring](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google)
 format. 

## Developer Notes
### Requirements
```
pip install sphinx
pip install recommonmark
pip install sphinx_rtd_theme
```
The package `recommonmark` adds Markdown support.

### Build online
The online documentation can be updated directly from the [RayTracing project](https://readthedocs.org/projects/raytracing/) on ReadTheDocs.

### Build local
This is done locally. The build is git-ignored. 
```
make html
```
Then you can open `_build/html/index.html`.

> For some reasons on my computer I have to leave the folder `docs` and call `docs/make html`

### Reminders
- When autogenerating the stub files from toctrees in reference.rst, note that sphinx-autogen requires to load a pythonpath to your project. 
    
    On windows the command is 
    ```
  $ set PYTHONPATH=C:\Path\to\project
  $ sphinx-autogen -t docs/_templates docs/reference.rst
  ```
    On Mac/Linux:
    ```
  PYTHONPATH=. sphinx-autogen -t docs/_templates docs/index.rst
  ```
