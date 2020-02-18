from raytracing import *
from numpy import *
import matplotlib.pyplot as plt
import sys

# On construit le chemin optique a partir de la lampe
f = 50
path = ImagingPath()
path.append(Space(d=f))
path.append(Lens(f=f,diameter=100))
path.append(Space(d=f))

# On calcule le profil d'intensité en propageant plein de rayons
# qui suivent la distribution en cos^2 theta du probleme.
nRays = 100000 # Vous pouvez augmenter pour obtenir une meilleure reponse
rayDistribution = RandomLambertianRays(yMax=20, M=nRays)
histogram = Histogram(min=-100, max=100, binCount=50)

for ray in rayDistribution:
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        histogram.add(lastRay.y)

    # i += 1
    # if i % progressLog == 0:
    #     progressLog *= 3
    #     if progressLog > nRays:
    #         progressLog = nRays

#         print("Progress {0}/{1} ({2:.0f}%) ".format(i, nRays,i/nRays*100))

histogram.show(title="Profil d'intensité au plan focal")
