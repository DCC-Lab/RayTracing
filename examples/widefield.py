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
import gc

# Defines the path. a and b are the diameter of the lenses.
def imagingPathPreset(a=10, b=10, title=""):
    
    path = ImagingPath()
    path.design(fontScale=1.7)
    path.label=title
    path.append(System4f(f1=50, diameter1=a, f2=50, diameter2=b))
    path.append(Aperture(diameter=10, label='Camera'))
    
    return path


# Input from the expected field of view
inputRays = RandomUniformRays(yMax = 5, 
                              yMin = -5,
                              thetaMin = -0.5,
                              thetaMax = +0.5,
                              maxCount=1000000)

if __name__ == "__main__":

    # Three paths with different sets of lens diameter. 
    path1 = imagingPathPreset(a=15, b=15, title="Vignetting with FS poorly placed because of second lens diameter")
    outputRays = path1.traceManyThrough(inputRays)
    efficiency = 100*outputRays.count/inputRays.count
    path1.display(interactive=False)
    outputRays.display("Output profile with vignetting {0:.0f}% efficiency".format(efficiency), showTheta=False)
    path1.reportEfficiency()

    gc.collect()

    path2 = imagingPathPreset(a=40, b=15, title="Suboptimal AS at second lens, but without vignetting")
    outputRays = path2.traceManyThrough(inputRays)
    efficiency = 100*outputRays.count/inputRays.count
    path2.display(interactive=False)
    outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)
    path2.reportEfficiency()

    gc.collect()

    path3 = imagingPathPreset(a=25, b=50, title="Better AS at first lens and FS at Camera")
    outputRays = path3.traceManyThrough(inputRays)
    efficiency = 100*outputRays.count/inputRays.count
    path3.display(interactive=False)
    outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)
    path3.reportEfficiency()
