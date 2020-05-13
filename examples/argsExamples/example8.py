from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''
    Demo #8: Virtual image at -2f with object at f/2
'''


def example():
    path = ImagingPath()
    path.label = "Demo #8: Virtual image at -2f with object at f/2"
    path.append(Space(d=2.5))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
