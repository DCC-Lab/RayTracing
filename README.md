# RayTracing
This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops).  It makes use of ABCD matrices and does not consider aberrations (spherical or chromatic). It is not a package to do "Rendering in 3D with raytracing".  

The code has been developed first for teaching purposes and is used in my "[Optique](https://itunes.apple.com/ca/book/optique/id949326768?mt=11)" Study Notes (french only), but also for actual use in my research. I have made no attempts at making high performance code.  Readability and simplicity of usage is the key here. It is a single file with only `matplotlib` as a dependent module.

The module defines `Ray` ,  `Matrix` and `OpticalPath` as the main elements.  An optical path is a sequence of matrices into which rays will propagate. Specific subclasses of `Matrix` exists: `Space`, `Lens` and `Aperture`. Finally, a ray fan is a collection of rays, originating from a given point with a range of angles.

## Getting started
You need `matplotlib`, which is a fairly standard Python module. If you do not have it,  installing [Anaconda](https://www.anaconda.com/download/) is your best option. You should choose Python 3.7 or later.

You create an OpticalPath, which you then populate with optical elements such as Space, Lens or Aperture. You can then adjust the optical path properties (object height for instance) and display in matplotlib.

This will show you a few examples of things you can do:

```shell
python ABCD.py
python demo.py
```

In your code, (such as the `test.py` or `demo.py`  files), you would do this:

```python
import ABCD as rt

path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5, diameter=2.5))
path.append(rt.Space(d=12))
path.append(rt.Lens(f=7))
path.append(rt.Space(d=10))
path.display()
```

## Licence

This code is provided under the [MIT License](./LICENSE).