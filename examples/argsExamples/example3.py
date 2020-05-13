from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''Demo #3: A finite lens
   An object at z=0 (front edge) is used with default properties (see Demo #1). Notice the aperture stop (AS)
   identified at the lens which blocks the cone of light. There is no field stop to restrict the field of view,
   which is why we must use the default object and cannot restrict the field of view. Notice how the default
   rays are blocked.'''


def example():
    path = ImagingPath()
    path.label = "Demo #3: Finite lens"
    path.append(Space(d=10))
    path.append(Lens(f=5, diameter=2.5))
    path.append(Space(d=3))
    path.append(Space(d=17))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
