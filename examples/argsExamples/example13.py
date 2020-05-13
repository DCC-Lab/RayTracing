from raytracing import ImagingPath, Space, Lens
from matplotlib import pyplot as plt

'''An object at z=0 (front edge) is used. It is shown in blue. The image (or any intermediate images) are shown in red.\n\
This will use the default objectHeight and fanAngle but they can be changed with:
path.objectHeight = 1.0
path.fanAngle = 0.5
path.fanNumber = 5
path.rayNumber = 3'''


def example():
    M1 = Space(d=10)
    M2 = Lens(f=5)
    M3 = M2 * M1
    print(M3.forwardConjugate())
    print(M3.backwardConjugate())

    if __name__ == "__main__":
        pass


if __name__ == "__main__":
    example()
