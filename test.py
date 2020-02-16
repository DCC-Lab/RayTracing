from raytracing import *
from numpy import *
import matplotlib.pyplot as plt

fobj = 5
f2 = 200
f3 = 200

path = ImagingPath()
path.append(Space(d=f3))
path.append(Lens(f=f3, diameter=100))
path.append(Space(d=f3))
path.append(Space(d=f2))
path.append(Lens(f=f2, diameter=100))
path.append(Space(d=f2))
path.append(Space(d=fobj))
path.append(Lens(f=fobj, diameter=5))
path.append(Space(d=fobj))

rayHeights = []
for ray in LambertianRays(yMax=2.5,M=100, N=100, I=100):
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        rayHeights.append(lastRay.y)

_ = plt.hist(rayHeights, bins=10,density=True)
plt.title("Intensity profile")
plt.show()

#print(totalNumberRays)
