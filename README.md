# RayTracing
This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops).  It makes use of ABCD matrices and does not consider aberrations (spherical or chromatic). It is not a package to do "Rendering in 3D with raytracing".  

The code has been developed first for teaching purposes and is used in my "[Optique](https://itunes.apple.com/ca/book/optique/id949326768?mt=11)" Study Notes (french only), but also for actual use in my research. I have made no attempts at making high performance code.  Readability and simplicity of usage is the key here. It is a single module with only a few files, and only `matplotlib` as a dependent module.

The module defines `Ray` ,  `Matrix`, `MatrixGroup` and `ImagingPath` as the main elements.  `Matrix` and `MatrixGroup` are either one or a sequence of many matrices into which `Ray` will propagate. `ImagingPath` is also a sequence of elements, with an object at the front edge.  Specific subclasses of `Matrix` exists: `Space`, `Lens`, `ThicklLens`, and `Aperture`. Finally, a ray fan is a collection of rays, originating from a given point with a range of angles.

## Installing

There are several ways to install the module:

1. Simplest: `pip install raytracing`
2. If you download the [source](https://pypi.org/project/raytracing/) of the module, then you can type: `python setup.py install`
3. From GitHub, you can get the latest version (including bugs) and then type `python setup.py install`
4. If you are completely lost, copying the folder `raytracing` (the one that includes `__init__.py`) from the source file into the same directory as your own script will work.

## Getting started

You need `matplotlib`, which is a fairly standard Python module. If you do not have it,  installing [Anaconda](https://www.anaconda.com/download/) is your best option. You should choose Python 3.7 or later.

The simplest way to import the package in your own scripts after installing it:

```python
from raytracing import *
```

This will import `Ray` , and several `Matrix` elements such as `Space`, `Lens`, `ThickLens`, `Aperture`, `DielectricInterface`, but also `MatrixGroup` (to group elements together) and `ImagingPath` (to ray trace with an object at the front edge) and a few predefined other such as `Objective` (to create a very thick lens that mimicks an objective).

You create an `ImagingPath`, which you then populate with optical elements such as Space, Lens or Aperture. You can then adjust the imaging path properties (object height for instance) and display in matplotlib.

This will show you a few examples of things you can do:

```shell
python -m raytracing
```

In your code, (such as the `test.py` or `demo.py`  files included in the [source](https://pypi.org/project/raytracing/)), you would do this:

```python
from raytracing import *

path = ImagingPath()
path.append(Space(d=10))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=12))
path.append(Lens(f=7))
path.append(Space(d=10))
path.display()
```

You may obtain help by typing (interactively): `help(Matrix)`, `help(Ray)`,`help(ImagingPath)`

```python
python
>>> help(Matrix)
Help on class Matrix in module raytracing.abcd:

class Matrix(builtins.object)
 |  Matrix(A, B, C, D, physicalLength=0, apertureDiameter=inf, label='')
 |  
 |  A matrix and an optical element that can transform a ray or another
 |  matrix.
 |  
 |  The general properties (A,B,C,D) are defined here. The operator "*" is
 |  overloaded to allow simple statements such as:
 |  
 |  ray2 = M1 * ray
 |  or
 |  M3 = M2 * M1
 |  
 |  The physical length is included in the matrix to allow simple management of
 |  the ray tracing. IF two matrices are multiplied, the resulting matrice
 |  will have a physical length that is the sum of both matrices.
 |  
 |  In addition finite apertures are considered: if the apertureDiameter
 |  is not infinite (default), then the object is assumed to limit the
 |  ray height to plus or minus apertureDiameter/2 from the front edge to the back
 |  edge of the element.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, A, B, C, D, physicalLength=0, apertureDiameter=inf, label='')
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __mul__(self, rightSide)
 |      Operator overloading allowing easy to read matrix multiplication
 |      
 |      For instance, with M1 = Matrix() and M2 = Matrix(), one can write
 |      M3 = M1*M2. With r = Ray(), one can apply the M1 transform to a ray
 |      with r = M1*r
 |  
 |  __str__(self)
 |      String description that allows the use of print(Matrix())
 |  
 |  backwardConjugate(self)
 |      With an image at the back edge of the element,
 |      where is the object ? Distance before the element by
 |      which a ray must travel to reach the conjugate plane at
 |      the back of the element. A positive distance means the
 |      object is "distance" in front of the element (or to the
 |      left, or before).
 |      
 |      M2 = M1*Space(distance)
 |      # M2.isImaging == True

```

## Examples

You can run the module directly with `python -m raytracing` or look at the [examples](https://github.com/DCC-Lab/RayTracing/tree/master/examples) directory.

You can run `demo.py` to see a variety of systems, `illuminator.py` to see a Kohler illuminator, and `invariant.py` to see an example of the role of lens diameters to determine the field of view.

![Figure1](assets/Figure1.png)
![Microscope](assets/Microscope.png)
![Illumination](assets/Illumination.png)

## Licence

This code is provided under the [MIT License](./LICENSE).