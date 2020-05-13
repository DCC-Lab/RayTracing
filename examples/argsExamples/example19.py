from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''Demo #19 - Calculation of cavity laser modes'''


def example():
    cavity = LaserPath(label="Laser cavity: round trip\nCalculated laser modes")
    cavity.isResonator = True
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))
    cavity.append(CurvedMirror(R=400))
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))
    fig, axes = plt.subplots(figsize=(10, 7))
    cavity.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    # Calculate all self-replicating modes (i.e. eigenmodes)
    (q1, q2) = cavity.eigenModes()
    print(q1, q2)
    # Obtain all physical (i.e. finite) self-replicating modes
    qs = cavity.laserModes()
    for q in qs:
        print(q)

    if __name__ == "__main__":
        cavity._showPlot()


if __name__ == "__main__":
    example()
