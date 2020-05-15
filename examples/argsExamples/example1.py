from raytracing import ImagingPath, Space, Lens

'''Demo #1 - An object at z=0 (front edge) is used. It is shown in blue. The image (or any intermediate images) are shown in red.\n\
This will use the default objectHeight and fanAngle but they can be changed with:
path.objectHeight = 1.0
path.fanAngle = 0.5
path.fanNumber = 5
path.rayNumber = 3'''


path = ImagingPath()
path.label = "Demo #1: lens f = 5cm, infinite diameter"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()

