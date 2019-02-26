from raytracing import *

path = MatrixGroup()
path.append(Lens(f=50))
path.append(Space(3))
path.append(lens)
path.append(Space(0.1))
path.append(lens)
path.append(Space(3))

