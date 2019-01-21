# RayTracing
This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops).  It makes use of ABCD matrices and does not consider aberrations (spherical or chromatic). It is not a package to do "Rendering in 3D with raytracing".  

The code has been developed first for teaching purposes but also for actual use in my research. I have made no attempts at making high performance code.  Readability and simplicity of usage is the key here.

The code defines `Ray` ,  `Matrix` and `OpticalPath` as the main elements.  An optical path is a sequence of matrices into which rays will propagate. Specific subclasses of `Matrix` exists: `Space`, `Lens` and `Aperture`. Finally, a ray fan is a collection of rays, originating from a given point with a range of angles.

## Getting started
This will show you a few examples of things you can do:
```shell
python ABCD.py
```

In your code, (such as the `test.py` file), you would do this:

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

This code is provided under the MIT Licence.