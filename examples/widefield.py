'''
In any imaging system, lens diameters are of great importance as
they dictate the position of the Aperture Stop(AS) and Field Stop(FS). 
We recall that the AS controls the light acceptance and that a 
poorly placed FS causes vignetting.

The following code shows a simple imaging system with three different
paths containing different lens diameter.

(a). The first one shows that if both lenses are too small, 
     the AS is the first lens and the FS is the second lens.
     We get vignetting on the final image, since the FS is poorly 
     placed at a lens instead of the detector's camera. 
(b). The second one shows that the second lens is smaller 
     than the first one, so the FS is at the camera but 
     AS is on the second lens, which is suboptimal.
(c). The last one shows that both lenses are big enough to make the first 
     lens the AS and the detector's camera the FS.
'''

import envexamples
from raytracing import *

path = ImagingPath()
path.label="(a) Vignetting with FS poorly placed because of second lens diameter"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=15, label="First lens"))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=15, label="Second lens"))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)


path = ImagingPath()
path.label="(b) Suboptimal AS at second lens, but without vignetting"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=40, label="First lens"))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=15, label="Second lens"))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)


path = ImagingPath()
path.label="(c) Optimal AS at first lens and FS at Camera"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=25, label="First lens"))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=25, label="Second lens"))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))
path.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
