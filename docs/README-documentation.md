# Raytracing Documentation

This document describes where the documentation is, how to write or update documentation for the Raytracing module and how to publish updated documentation through ReadTheDocs.

## Reading documentation

If you are a user of the raytracing package, you probably want to read the documentation online at https://raytracing.readthedocs.io/. There are useful information about the required python version, installation, description of the functions in the module, and several examples to show how this module is used.

## Writing documentation

If you are a developer, you may be interested in updating the documentation. The documentation is auto-generated with the Sphynx documentation module from the docstrings directly in the code. There are many different formats that can be used, but the one used in Raytracing is the [Numpy Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html) format. This format applied to the code looks like this:

```python
class Ray:
    """A vector and a light ray as transformed by ABCD matrices.

    The Ray() has a height (y) and an angle with the optical axis (theta).
    It also has a position (z) initially at z=0, the diameter of the aperture at that point
    when it propagated through, and a marker if it has been blocked by the
    aperture.

    Simple static functions are defined to obtain a group of rays: fans
    originate from the same height but sweep a range of angles; fan groups
    are fans originating from different heights.
    
    Parameters
    ----------
    y : float
        Initial height of the ray. Defaults to 0.
    theta : float
        Initial angle of the ray. Defaults to 0.

    Attributes
    ----------
    z : float
        Position of the ray along the optical axis. Initialized at 0.
    apertureDiameter : float
        The diameter of any blocking aperture at the present position z. Initialized at +Inf.
    isBlocked : bool
        Whether or not the ray was blocked by an aperture. Initialized to False.

    Returns
    -------
    output : data
        if there is an output for the function

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    Some similar functions

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a+b
    0
    
    """
   
    def __init__(self, y: float = 0, theta: float = 0):
        self.y = y
        self.theta = theta

        self.z: float = 0
        self.isBlocked: bool = False
        self.apertureDiameter: float = float("+Inf")
```

## Publishing documentation (maintainers only)

Maintainers of the package publish the documentation with each release. To create the documentation and publish it, follow the guidelines below.

### Requirements

These requirements are only for anyone who wants to publish the documentation, and are not necessary for the use of the Raytracing package.

```
pip install sphinx
pip install recommonmark
pip install sphinx_rtd_theme
```
Note that the package `recommonmark` adds Markdown support.

### Files controlling the format
|File|Usage|
|---|---|
|`conf.py`|Configure `html_theme` and `extensions`|
|`index.rst`|Main index page|
|`_templates/autoClass.rst`|Template used to auto-document classes|
|`_templates/autoFunction.rst`|Template used to auto-document functions|

*[FIXME: Information here on key files and their role in the Sphynx documentation system]*

Defined pages in the website are the content of the following files:

1. raytracing (`raytracing.rst`) : Simple introdution to the module and its classes.
2. gettingStarted (`gettingStarted.md`) : Description about the installation and updating the module.
3. reference (`reference.rst`) : Documentation of the module ( description of classes and functions)
4. examples (`raytracing.rst`) : Examples for introducing how to start using the module. 
5. contribute (`raytracing.rst`) : How to report issues and bugs.
6. FAQ (`raytracing.rst`)



### Build online
The online documentation can be updated directly from the [RayTracing project](https://readthedocs.org/projects/raytracing/) on ReadTheDocs by the project administrators (currently dccote, jlbegin and elaheparham) to match the release from PyPI. The build is currently set on the master branch.
To build a released version, an admistrator must go to the [Build](https://readthedocs.org/projects/raytracing/builds/) on ReadTheDocs, select the version and push Build Version. 

Remember before bulding online the new documentation version, you should check if all the documentations and examples are working properly. So, run `.../raytracing/tests/testsDocTestModule.py` and if there are no errors, the documentation is working properly. 
If there is an error you should go to the line that raises the error and fix it before publishing the new version.

### Build local

Anyone can build the documentation locally. From the docs directory, with the requirements installed in your python environment, type: 
```
make clean  # (optional, remove previous build) 
make html
```
Then you can open `_build/html/index.html`.

> For some reasons on my computer I have to leave the folder `docs` and call `docs/make html`

### Updating the documentation

>  The documentation files for all methods are auto-generated and maintained during build.

1. If new classes were added, update `reference.rst` (Optional) 

   > Simply follow the template and add new files (titles) or classes (items)

2. Go to https://readthedocs.org/projects/raytracing/ 

   > You need to be logged in as one of the maintainers. 

3. Click `Build version` (latest by default)

   > To build a specific branch, go to Versions and activate the desired branch in the list at the bottom (it might require a build of master to fetch for new branches). 