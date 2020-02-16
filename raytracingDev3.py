from raytracing import *
from numpy import *
import matplotlib.pyplot as plt

# Les valeurs en variables pour que ce soit simple
fobj = 5
dObj = 5
f2 = 200
d2 = 50
f3 = 100
d3 = 50

# On construit le chemin optique a partir de la lampe
path = ImagingPath()
path.objectHeight = 5
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
nRays = 100000 # Vous pouvez augmenter pour obtenir une meilleure reponse
allRays = RandomLambertianRays(yMax=2.5,M=nRays)

# Les hauteurs des rayons a la sortie
rayHeights = [] 
i = 1
progressLog = 100

for ray in allRays:
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        rayHeights.append(lastRay.y) # Si pas bloqué, on le garde

    i += 1
    if i % progressLog == 0:
        progressLog *= 3
        if progressLog > nRays:
        	progressLog = nRays

        print("Progress {0}/{1} ({2:.0f}%) ".format(i, nRays,i/nRays*100))

plt.hist(rayHeights, bins=20,density=True)
plt.title("Profil d'illumination à l'objet")
plt.show()
