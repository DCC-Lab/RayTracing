from raytracing import *

'''
In any imaging system, lens diameter is of great importance as it calculates Field Stop(FS) and Aperture Stop(AS). 
It is AS that controls light acceptance and poorly placed FS causes vignetting and it has an impact on image quality.

The following code shows a simple imaging system with three different paths containing different lens diameter.

(a). The first one shows that if both lenses are too small, the AS is the first lens and the FS is the second lens. 
    We get vignetting on the final image, since the FS is poorly placed at a lens instead of the detector's camera. 
(b). The second one shows that the second lens is smaller than the first one, so the AS is on the second lens, 
    FS as the camera.
(c). The last one shows that both lenses are big enough to make the first lens the AS and the detector's camera the FS.
'''

path = ImagingPath()
path.fanNumber = 3
path.objectHeight = 10
path.label="(a)"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=15))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=15))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display()


path = ImagingPath()
path.objectHeight = 10
path.fanNumber = 3
path.label="(b)"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=40))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=15))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display()


path = ImagingPath()
path.objectHeight = 10
path.fanNumber = 3
path.label="(c)"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=25))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=25))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display()
