from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''Demo #2: Two lenses, infinite diameters
An object at z=0 (front edge) is used with default properties (see Demo #1).'''


def example():
    path = ImagingPath()
    path.label = "Demo #2: Two lenses, infinite diameters"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=20))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
