
from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''
    Demo #9: Infinite telecentric 4f telescope
'''


def example():
    path = ImagingPath()
    path.label = "Demo #9: Infinite telecentric 4f telescope"
    path.append(Space(d=5))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=5))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
