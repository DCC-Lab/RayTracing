from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''An object at z=0 (front edge) is used. It is shown in blue. The image (or any intermediate images) are shown in red.\n\
This will use the default objectHeight and fanAngle but they can be changed with:
path.objectHeight = 1.0
path.fanAngle = 0.5
path.fanNumber = 5
path.rayNumber = 3'''


def example():
    path = ImagingPath()
    path.label = "Demo #1: lens f = 5cm, infinite diameter"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
