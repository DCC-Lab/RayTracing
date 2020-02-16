from raytracing import *
from numpy import *
import matplotlib.pyplot as plt

fobj = 5
dObj = 5

f2 = 200
d2 = 100

f3 = 100
d3 = 10

path = ImagingPath()
path.append(Space(d=f3))
path.append(Lens(f=f3, diameter=d3))
path.append(Space(d=f3))
path.append(Space(d=f2))
path.append(Lens(f=f2, diameter=d2))
path.append(Space(d=f2))
path.append(Space(d=fobj))
path.append(Lens(f=fobj, diameter=dObj))
path.append(Space(d=fobj))

rayHeights = []
nRays = 1000000
i = 0
progressLog = 100

allRays = RandomLambertianRays(yMax=2.5,M=nRays)

for ray in allRays:
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        rayHeights.append(lastRay.y)

    if i % progressLog == 0:
        progressLog *= 10
        print("Progress {0}/{1} ({2}%) ".format(i, nRays,i/nRays*100))
    i += 1

plt.hist(rayHeights, bins=40,density=True)
plt.title("Intensity profile")
plt.show()
