
from raytracing import *

'''
In any imaging systems, lens diameter is of great importance as it calculates Field Stop(FS) and Aperture Stop(AS). It is AS that controls light acceptance and poorly placed FS causes vignetting and it has an impact on image quality.

The following code shows a simple imaging system with three different paths containing different lens diameter.

1. The first one shows that if both lenses are too small, the AS is the first lens and the FS is the second lens. We get  vignetting, since Field Stop is poorly placed at a lens instead of the image
2. The Second one shows that the second lens is smaller than the first one, so the AS is on the second lens, FS as the camera.
3. The last one shows that both lenses are big enough to make the first lens the AS and the “camera” as FS.
'''

path = ImagingPath()
path.objectHeight = 20
path.append(Space(d=50))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()



path = ImagingPath()
path.objectHeight = 20
path.append(Space(d=50))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=35))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()



path = ImagingPath()
path.objectHeight = 20
path.append(Space(d=50))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()




