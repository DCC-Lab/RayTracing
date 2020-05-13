from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''Demo #4: Aperture behind lens
Notice the aperture stop (AS) identified after the lens, not at the lens. Again, since there is no field stop,
we cannot restrict the object to the field of view because it is infinite.'''


def example():
    path = ImagingPath()
    path.label = "Demo #4: Aperture behind lens"
    path.append(Space(d=10))
    path.append(Lens(f=5, diameter=3))
    path.append(Space(d=3))
    path.append(Aperture(diameter=3))
    path.append(Space(d=17))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
