# RayTracing
Simple ray tracing library in Python

This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops).  
It makes use of ABCD matrices and does not consider aberrations (spherical or chromatic). It is not a package to do "Rendering in 3D with raytracing".  

## Getting started
This will show you a few examples:
```
python ABCD.py
```

In your code, (such as the `test.py` file), you would do this:

```
import ABCD as rt

path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5, diameter=2.5))
path.append(rt.Space(d=12))
path.append(rt.Lens(f=7))
path.append(rt.Space(d=10))
path.display()
```

