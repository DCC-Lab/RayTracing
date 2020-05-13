
from raytracing import ImagingPath, Space, Lens, Aperture
from matplotlib import pyplot as plt

'''
    A retrofocus has a back focal length longer than the effective focal length. It comes from a diverging lens followed by a converging
    lens. We can always obtain the effective focal lengths and the back focal length of a system.
'''


def example():
    path = ImagingPath()
    path.fanAngle = 0.05
    path.append(Space(d=20))
    path.append(Lens(f=-10, label='Div'))
    path.append(Space(d=7))
    path.append(Lens(f=10, label='Foc'))
    path.append(Space(d=40))
    (focal, focal) = path.effectiveFocalLengths()
    bfl = path.backFocalLength()
    path.label = "Demo #10: Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}".format(focal, bfl)
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
