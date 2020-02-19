from raytracing import *
from numpy import *
import matplotlib.pyplot as plt

# Les valeurs en variables pour que ce soit simple
fobj = 45
dObj = 45
f2 = 150
d2 = 75
f3 = 33
d3 = 45

# On construit le chemin optique a partir de la lampe
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
path.display(onlyChiefAndMarginalRays=True) # Vous verrez le montage


# On calcule le profil d'intensité en propageant plein de rayons
# qui suivent la distribution en cos^2 theta du probleme.
nRays = 1000000 # Vous pouvez augmenter pour obtenir une meilleure reponse
inputRays = RandomLambertianRays(yMax=10/2, maxCount=nRays)
outputRays = Rays()

for ray in inputRays:
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        outputRays.append(lastRay) # Si pas bloqué, on le garde

    inputRays.displayProgress()


outputRays.display()
