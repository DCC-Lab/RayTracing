# RayTracing

by the DCCLab group http://www.dcclab.ca, guided by Prof. [Daniel Côté](mailto:dccote@cervo.ulaval.ca?subject=Raytracing%20python%20module).

This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops).  It makes use of ABCD matrices and does not consider spherical aberrations but can compute chromatic aberrations for simple cases when the materials are known. Since it uses the ABCD formalism (or Ray matrices, or Gauss matrices) it can perform tracing of rays and gaussian laser beams. 

It is not a package to do "Rendering in 3D with raytracing".

The code has been developed first for teaching purposes and is used in my "[Optique](https://itunes.apple.com/ca/book/optique/id949326768?mt=11)" Study Notes (french only), but also for actual use in my research. As of January 21st, 2021, there is an extensive, freely accessible, peer-reviewed tutorial in Journal of Neurophotonics:

> ["Tools and tutorial on practical ray tracing for microscopy"](https://doi.org/10.1117/1.NPh.8.1.010801) 
>
> by V. Pineau Noël\*, S. Masoumi\*, E. Parham\*, G. Genest, L. Bégin, M.-A. Vigneault, D. C. Côté, 
> Neurophotonics, 8(1), 010801 (2021). 
> *Equal contributions.
> Permalink: https://doi.org/10.1117/1.NPh.8.1.010801

The published tutorial assumes version 1.3.x.  There are video [tutorials](https://www.youtube.com/playlist?list=PLUxTghemi4Ft0NzQwuufpU-EGgkmaInAf) (in english or french, with english subtitles when in french) on YouTube. We have made no attempts at making high performance code.  **Readability** and **simplicity of usage** are the key here. It is a module with a few files, and only `matplotlib` and `numpy` as dependent modules.

## Where do I get started?
   * If you want to use the module, keep reading.
   * If you have a suggestion or a bug report, go to [Issues](https://github.com/DCC-Lab/RayTracing/issues).
   * If you want to read and contribute to the code, go to the [Wiki](https://github.com/DCC-Lab/RayTracing/wiki) for general considerations. We plan to have a roadmap in the near future.

## Getting started
The module defines `Ray` , `Matrix`, `MatrixGroup` and `ImagingPath` as the main elements for tracing rays.  `Matrix` and `MatrixGroup` are either one or a sequence of many matrices into which `Ray` will propagate. `ImagingPath` is also a sequence of elements, with an object at the front edge.  Specific subclasses of `Matrix` exists: `Space`, `Lens`, `ThicklLens`, and `Aperture`. Finally, a ray fan is a collection of rays, originating from a given point with a range of angles.

We have tried to separate the calculation code (i.e. the matrices and subclasses) from the drawing code (figures and graphics). One can use the calculation code without any graphics calls.

If you want to perform calculations with coherent laser beams, then you use `GaussianBeam` and `LaserPath`. Everything is essentially the same, except that the formalism does not allow for the gaussian beam to be "blocked", hence any calculation of stops with aperture are not available in `LaserPath`. That part of the code is less developed, but it is nevertheless available.

## What's new?

To get information about what is new, currently the best place is the [release page on GitHub.](https://github.com/DCC-Lab/RayTracing/releases)

There is a **[Frequently Asked Questions](./FAQ.md)** page.

The article above is fully compatible with all 1.3.x versions.  As long as the API does not change, versions will be 1.3.x.



## Installing and upgrading

You need `matplotlib`, which is a fairly standard Python module. If you do not have it,  installing [Anaconda](https://www.anaconda.com/download/) is your best option. Python 3.6 or later is required. There are several ways to install the module:

1. Simplest: `pip install raytracing` or `pip install --upgrade raytracing`
   1. If you need to install `pip`, download [getpip.py](https://bootstrap.pypa.io/get-pip.py) and run it with `python getpip.py`
2. If you download the [source](https://pypi.org/project/raytracing/) of the module, then you can type: `python setup.py install`
3. From GitHub, you can get the latest version (including bugs, which are 153% free!) and then type `python setup.py install`
4. If you are completely lost, copying the folder `raytracing` (the one that includes `__init__.py`) from the source file into the same directory as your own script will work.
5. Watch the tutorial with subtitles [here.](https://www.youtube.com/playlist?list=PLUxTghemi4Ft0NzQwuufpU-EGgkmaInAf)

## Getting started

The simplest way to import the package in your own scripts after installing it:

```python
from raytracing import *
```

This will import `Ray` , `GaussianBeam`,  and several `Matrix` elements such as `Space`, `Lens`, `ThickLens`, `Aperture`, `DielectricInterface`, but also `MatrixGroup` (to group elements together),  `ImagingPath` (to ray trace with an object at the front edge), `LaserPath` (to trace a gaussian laser beam from the front edge) and a few predefined other such as `Objective` (to create a very thick lens that mimicks an objective).

You create an `ImagingPath` or a `LaserPath`, which you then populate with optical elements such as `Space`, `Lens` or `Aperture` or vendor lenses. You can then adjust the path properties (object height in `ImagingPath` for instance or inputBeam for `LaserPath`) and display in matplotlib. You can create a group of elements with `MatrixGroup` for instance a telescope, a retrofocus or any group of optical elements you would like to treat as a "group".  The Thorlabs and Edmund optics lenses, for instance, are defined as `MatrixGroups`.

This will show you a list of examples of things you can do (more on that in the Examples section):

```shell
python -m raytracing -l           # List examples
python -m raytracing -e all       # Run all of them
python -m raytracing -e 1,2,4,6   # Only run 1,2,4 and 6
python -m raytracing -t           # Run all the tests.  Some performance tests can take up to a minute, but they should all pass.
```

or request help with:

```
python -m raytracing -h
```

In your code, you would do this:

```python
from raytracing import *

path = ImagingPath()
path.append(Space(d=50))
path.append(Lens(f=50, diameter=25))
path.append(Space(d=120))
path.append(Lens(f=70))
path.append(Space(d=100))
path.display()
```

<img src="https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/simple.png" alt="simple" style="zoom:25%;" />

You can also call `display()` on an element to see the cardinal points, principal planes, BFL (back focal length, or the distance between the last interface and the focal point after the lens) and FFL (front focal length, or the distance between the focal point before the lens and the first interface). You can do it with any single `Matrix` element but also with `MatrixGroup`.

```python
from raytracing import *

thorlabs.AC254_050_A().display()
eo.PN_33_921().display()
```

![e0](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/e0.png)

![thorlabs](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/thorlabs.png)

Finally, an addition as of 1.2.0 is the ability to obtain the intensity profile of a given source from the object plane at the exit plane of an `OpticalPath`. This is in fact really simple: by tracing a large number of rays, with the number of rays at y and θ being proportionnal to the intensity, one can obtain the intensity profile by plotting the histogram of rays reaching a given height at the image plane. `Rays` are small classes that return a `Ray` that satisfies the condition of the class.  Currently, there is `UniformRays`,`RandomUniformRays` `LambertianRays` and `RandomLambertianRays` (a Lambertian distribution follows a cosθ distribution, it is a common diffuse surface source).  They appear like iterators and can easily be used like this example script:

```python
from raytracing import *
from numpy import *
import matplotlib.pyplot as plt

# Kohler illumination with these variables
fobj = 5
dObj = 5
f2 = 200
d2 = 50
f3 = 100
d3 = 50

# We build the path (i.e. not an Imaging path)
path = OpticalPath()
path.append(Space(d=f3))
path.append(Lens(f=f3, diameter=d3))
path.append(Space(d=f3))
path.append(Space(d=f2))
path.append(Lens(f=f2, diameter=d2))
path.append(Space(d=f2))
path.append(Space(d=fobj))
path.append(Lens(f=fobj, diameter=dObj))
path.append(Space(d=fobj))

# Obtaining the intensity profile
nRays = 1000000 # Increase for better resolution 
inputRays = RandomLambertianRays(yMax=2.5, maxCount=nRays)
inputRays.display("Input profile")
outputRays = path.traceManyThrough(inputRays, progress=True)
# On macOS and Linux, you can do parallel computations
# outputRays = path.traceManyThroughInParallel(inputRays, progress=True, processes=8) 
outputRays.display("Output profile")

```

and you will get the following ray histograms:

<img src="https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/inputProfile.png" alt="inputProfile" style="zoom:25%;" />

<img src="https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/outputProfile.png" alt="outputProfile" style="zoom:25%;" />

Finally, it is possible to obtain the chromatic aberrations for compound lenses (achromatic doublets from Thorlabs and Edmund optics, and singlet lens because the materials are known). The following command will give you the focal shift as a function of wavelength (as a graph or values):
```python
from raytracing import *

thorlabs.AC254_100_A().showChromaticAberrations()
wavelengths, shifts = thorlabs.AC254_100_A().focalShifts()
```

<img src="https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/chromaticaberrations.png" alt="chromatic" style="zoom:100%;" />

## Documentation

All the documentation is [available online](https://raytracing.readthedocs.io/). 

The class hierarchy for optical elements (with parameters and defaults) is:

![class](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/hierarchy.png)

You may obtain help by:

1. Reading the documentation for the code ([API reference](https://raytracing.readthedocs.io/en/latest/reference.html)).
   1. Core: 
      1. `Ray`: a ray for geometrical optics with a height and angle $y$ and $\theta$.
      2. `Rays`: ray distributions to ray trace an object through the optical system.
         1.  `UniformRays`, `RandomUniformRays`, `LambertianRays` and `RandomLambertianRays` are currently available.  See example above.
      3. `GaussianBeam`: a gaussian laser beam with complex radius of curvature $q$.
      4. `Matrix`: any 2x2 matrix.
      5. `MatrixGroup`: treats a group of matrix as a unit (draws it as a unit too)
      6. `ImagingPath`: A `MatrixGroup` with an object at the front for geometrical optics 
      7. `LaserPath`: A `MatrixGroup` with a laser beam input at the front or a Resonator.
   2. Optical elements: `Aperture`, `Space`, `Lens`, `DielectricInterface`, `DielectricSlab`, `ThickLens`
   3. Specialty lenses: Defines a general achromat and objective lens
   4. Thorlabs lenses: Achromat doublet lenses from Thorlabs.
   5. Edmund Optics lenses: Achromat doublet lenses from Edmund Optics
   6. Olympus objectives: A few objectives from Olympus.
   7. Glasses: A few glasses used by Thorlabs to make achromatic doublets. They all have a single function `n(wavelength)` that returns the index at that wavelength.  All data obtained from http://refractiveindex.info.
   8. Zemax ZMX file reader: to read text-based Zemax files of lenses.
2. typing (interactively): `help(Matrix)`,`help(MatrixGroup)` `help(Ray)`,`help(ImagingPath)` to get the API, 
3. look at the examples with `python -m raytracing` 
4. simply look at the code.

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

You can list several examples `python -m raytracing -l`:

```shell
All example code on your machine is found at: /somedirectory/on/your/machine
 1. ex01.py A single lens f = 50 mm, infinite diameter
 2. ex02.py Two lenses, infinite diameters
 3. ex03.py Finite-diameter lens
 4. ex04.py Aperture behind lens acting as Field Stop
 5. ex05.py Simple microscope system
 6. ex06.py Kohler illumination
 7. ex07.py Focussing through a dielectric slab
 8. ex08.py Virtual image at -f with object at f/2
 9. ex09.py Infinite telecentric 4f telescope
10. ex10.py Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}
11. ex11.py Thick diverging lens computed from the Lensmaker equation
12. ex12.py Thick diverging lens built from individual elements
13. ex13.py Obtain the forward and backward conjugates
14. ex14.py Generic objectives
15. ex15.py Model Olympus objective LUMPlanFL40X
16. ex16.py Commercial doublets from Thorlabs and Edmund
17. ex17.py An optical system with vendor lenses
18. ex18.py Laser beam and vendor lenses
19. ex19.py Cavity round trip and calculated laser modes
.... and more complete examples at /somedirectory/on/your/machine
```

 You can run them all with `python -m raytracing -e all` (see them all below) to get a flavour of what is possible (note: in the US, it will give you a flavor of what is possible instead). Notice the command will tell you where the directory with all the tests is on your machine. **You will find more complete examples** in that [examples](https://github.com/DCC-Lab/RayTracing/tree/master/raytracing/examples) directory, distributed with the module.  For instance, `illuminator.py` to see a Kohler illuminator, and `invariant.py` to see an example of the role of lens diameters to determine the field of view.



![ex01](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex01.png)

![ex02](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex02.png)

![ex03](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex03.png)

![ex04](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex04.png)

![ex05](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex05.png)

![ex06](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex06.png)

![ex07](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex07.png)

![ex08](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex08.png)

![ex09](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex09.png)

![ex10](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex10.png)

![ex11](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex11.png)

![ex12](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex12.png)

![ex14](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex14.png)

![ex15](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex15.png)

![ex16.1](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.1.png)

![ex16.2](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.2.png)

![ex16.3](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.3.png)

![ex17](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex17.png)

![ex18](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex18.png)

## Known limitations

There are no known bugs in the actual calculations, but there are bugs or limitations in the display:

1. It is not easy to put several labels on a graph without any overlap. We are still working on it.
2. It is also not easy to figure out what "the right size" should be for an arrow head, the font, the position of a label, the size of the "ticks" on the aperture.
3. Labelling focal points with appropriate secondary labels should be possible, maybe a superscript?
4. The y-scale is not always set appropriately when the elements have infinite diameters: the rays will go beyond the element drawn on the figure.

## Licence

This code is provided under the [MIT License](./LICENSE).
