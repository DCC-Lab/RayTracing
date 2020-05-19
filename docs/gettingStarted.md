# Getting Started

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

This will show you a few examples of things you can do:

```shell
python -m raytracing
```

or request help with:

```
python -m raytracing -h
```

In your code, (such as the `test.py` or `demo.py`  files included in the [source](https://pypi.org/project/raytracing/)), you would do this:

```python
from raytracing import *

path = ImagingPath()
path.append(Space(d=100))
path.append(Lens(f=50, diameter=25))
path.append(Space(d=120))
path.append(Lens(f=70))
path.append(Space(d=100))
path.display()
```

You can also call display() on an element to see the cardinal points, principal planes, BFL and FFL. You can do it with any single `Matrix` element but also with `MatrixGroup`.

```python
from raytracing import *

thorlabs.AC254_050_A().display()
eo.PN_33_921().display()
```

Finally, an addition as of 1.2.0 is the ability to obtain the intensity profile of a given source from the object plane at the exit plane of an OpticalPath. This is in fact really simple: by tracing a large number of rays, with the number of rays at y and θ being proportionnal to the intensity, one can obtain the intensity profile by plotting the histogram of rays reaching a given height at the image plane. `Rays` are small classes that return a `Ray` that satisfies the condition of the class.  Currently, there is `UniformRays`,`RandomUniformRays` `LambertianRays` and `RandomLambertianRays` (a Lambertian distribution follows a cosθ distribution, it is a common diffuse surface source).  They appear like iterators and can easily be used like this example script:

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