from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''
    Demo #7: Focussing through a dielectric slab
'''


def example():
    path = ImagingPath()
    path.label = "Demo #7: Focussing through a dielectric slab"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=3))
    path.append(DielectricSlab(n=1.5, thickness=4))
    path.append(Space(d=10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
