from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''# Demo #5: Simple microscope system
The aperture stop (AS) is at the entrance of the objective lens, and the tube lens, in this particular microscope, is
the field stop (FS) and limits the field of view. Because the field stop exists, we can use limitObjectToFieldOfView=True
when displaying, which will set the objectHeight to the field of view, but will still trace all the rays using our parameters.
'''


def example():
    path = ImagingPath()
    path.label = "Demo #5: Simple microscope system"
    path.fanAngle = 0.1  # full fan angle for rays
    path.fanNumber = 5  # number of rays in fan
    path.rayNumber = 5  # number of points on object
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=0.8, label='Obj'))
    path.append(Space(d=4 + 18))
    path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
    path.append(Space(d=18))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
