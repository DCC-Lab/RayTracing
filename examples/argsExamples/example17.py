from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''
Demo #17: Vendor Lenses
'''


def example():
    path = ImagingPath()
    path.label = "Demo #17: Vendor Lenses"
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=150))
    path.append(eo.PN_33_921())
    path.append(Space(d=50))
    path.append(eo.PN_88_593())
    path.append(Space(180))
    path.append(olympus.LUMPlanFL40X())
    path.append(Space(10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
