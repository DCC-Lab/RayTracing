from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''
Demo #12: Thick diverging lens built from individual elements
'''


def example():
    path = ImagingPath()
    path.label = "Demo #12: Thick diverging lens built from individual elements"
    path.objectHeight = 20
    path.append(Space(d=50))
    path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
    path.append(Space(d=10, diameter=25, label='Lens'))
    path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
    path.append(Space(d=50))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
