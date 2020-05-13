from raytracing import ImagingPath, Space, Lens, Objective
from matplotlib import pyplot as plt

'''
Demo #14 Path with generic objective
'''


def example():
    obj = Objective(f=10, NA=0.8, focusToFocusLength=60, backAperture=18, workingDistance=2, label="Objective")
    print("Focal distances: ", obj.focalDistances())
    print("Position of PP1 and PP2: ", obj.principalPlanePositions(z=0))
    print("Focal spots positions: ", obj.focusPositions(z=0))
    print("Distance between entrance and exit planes: ", obj.L)

    path = ImagingPath()
    path.fanAngle = 0.0
    path.fanNumber = 1
    path.rayNumber = 15
    path.objectHeight = 10.0
    path.label = "Demo #14 Path with generic objective"
    path.append(Space(180))
    path.append(obj)
    path.append(Space(10))
    fig, axes = plt.subplots(figsize=(10, 7))
    path.createRayTracePlot(axes=axes)
    plt.savefig('tempFig.pdf', dpi=600)

    if __name__ == "__main__":
        path._showPlot()


if __name__ == "__main__":
    example()
