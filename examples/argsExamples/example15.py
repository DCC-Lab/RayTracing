from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''
#DEMO 15 - Path with LUMPlanFL40X
'''


def example():
    path = ImagingPath()
    path.fanAngle = 0.0
    path.fanNumber = 1
    path.rayNumber = 15
    path.objectHeight = 10.0
    path.label = "Demo #15 Path with LUMPlanFL40X"
    path.append(Space(180))
    path.append(olympus.LUMPlanFL40X())
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
