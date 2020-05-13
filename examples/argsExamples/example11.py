from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''
Demo #11: Thick diverging lens
'''


def example():
    path = ImagingPath()
    path.label = "Demo #11: Thick diverging lens"
    path.objectHeight = 20
    path.append(Space(d=50))
    path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
    path.append(Space(d=50))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
