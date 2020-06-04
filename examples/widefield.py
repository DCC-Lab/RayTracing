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

# Counts the number of rays starting at the object makes it through the system.
# nRays if the total number of rays emitted from the object. 
def rayCount(nRays=10000, objectHalfHeight=5, path=ImagingPath()):

    # Production of rays from a focal spot with a radius of objectHalfHeight
    inputRays = RandomUniformRays(yMax=objectHalfHeight, yMin=objectHalfHeight, maxCount=nRays)
    outputRays = Rays()

    # Counts how many rays make it through the system
    for ray in inputRays:
        lastRay = path.traceThrough(ray)

        # if the ray passes through, it's added in outputRays
        if lastRay.isNotBlocked: 
            outputRays.append(lastRay)
    inputRays.displayProgress()

    print("Number of rays sent: {0}".format(inputRays.count))
    print("Number of rays received: {0}".format(outputRays.count))
    print("Transmission efficiency: {0}".format(outputRays.count/inputRays.count))
    

    return outputRays.display("Output profile")


# Defines the path. a and b are the diameter of the lenses.
def imagingPath(a=10, b=10, title=""):
    
    path = ImagingPath()
    path.label=title
    path.append(Space(d=50))
    path.append(Lens(f=50, diameter=a, label="First lens"))
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=b, label="Second lens"))
    path.append(Space(d=50))
    path.append(Aperture(diameter=10, label='Camera'))
    path.append(Space(d=50))
    
    return path


# Three paths with different sets of lenses diameter. 
path1 = imagingPath(a=15, b=15, title="Vignetting with FS poorly placed because of second lens diameter")
path1.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
rayCount(path=path1)

path2 = imagingPath(a=40, b=15, title="Suboptimal AS at second lens, but without vignetting")
path2.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
rayCount(path=path2)

path3 = imagingPath(a=25, b=25, title="Optimal AS at first lens and FS at Camera")
path3.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
rayCount(path=path3)
