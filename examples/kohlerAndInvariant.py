import envexamples

from raytracing import *

'''
DESCRIPTION
'''

#print("The Lagrange Invariant of this system is {}".format(illumination1.lagrangeInvariant()))

def displayMultiple(paths: list,
                    limitObjectToFieldOfView=False,
                    onlyChiefAndMarginalRays=False,
                    removeBlockedRaysCompletely=False,
                    comments=None):
    fig, axes = plt.subplots(figsize=(10, 7))
    for path in paths:
        path.createRayTracePlot(axes=axes, limitObjectToFieldOfView=False,
                                onlyChiefAndMarginalRays=False,
                                removeBlockedRaysCompletely=False)
    # can only def callbacks for only one path
    axes.callbacks.connect('ylim_changed', paths[0].updateDisplay)
    axes.set_ylim([-paths[0].displayRange(axes) / 2 * 1.5, paths[0].displayRange(axes) / 2 * 1.5])
    paths[0]._showPlot()


# Source with Kohler illumination 
illumination1 = ImagingPath()
illumination1.fanNumber = 3
illumination1.fanAngle = 0.1
illumination1.design(rayColors = ["r","r","r"])

illumination1.append(Space(d=10))
illumination1.append(Lens(f=10, diameter=100, label="Collector"))
illumination1.append(Space(d=10+30))
illumination1.append(Lens(f=30, diameter=100, label="Condenser"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Objective"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Tube"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination1.append(Space(d=30+2))
illumination1.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination1.append(Space(d=2))
illumination1.display()




# Source without Kohler illumination 
illumination2 = ImagingPath()
illumination2.fanNumber = 3
illumination2.fanAngle = 0.1
illumination2.objectPosition = 20
illumination2.design(rayColors = ["b","b","b"])

illumination2.append(Space(d=30))
illumination2.append(Lens(f=30, diameter=100, label="Condenser"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Objective"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Tube"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination2.append(Space(d=30+2))
illumination2.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination2.append(Space(d=2))
illumination2.display()




# Sample imaging path 
illumination3 = ImagingPath()
illumination3.objectPosition = 80
illumination3.objectHeight = 5
illumination3.fanNumber = 1
illumination3.fanAngle = 0
illumination3.design(rayColors = ["g","g","g"])


illumination3.append(Space(d=10))
illumination3.append(Lens(f=10, diameter=100, label="Collector"))
illumination3.append(Space(d=10+30))
illumination3.append(Lens(f=30, diameter=100, label="Condenser"))
illumination3.append(Space(d=30+30))
illumination3.append(Lens(f=30, diameter=100, label="Objective"))
illumination3.append(Space(d=30+30))
illumination3.append(Lens(f=30, diameter=100, label="Tube"))
illumination3.append(Space(d=30+30))
illumination3.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination3.append(Space(d=30+2))
illumination3.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination3.append(Space(d=2))
illumination3.display()

#displayMultiple([illumination3, illumination1])
#displayMultiple([illumination3, illumination2])
