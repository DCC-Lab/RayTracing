from raytracing import *
from numpy import *
import matplotlib.pyplot as plt
import sys
import os

# On construit le chemin optique a partir de la lampe
f = 50
path = ImagingPath()
path.append(Space(d=f))
path.append(Lens(f=f))
path.append(Space(d=f))

# On calcule le profil d'intensité en propageant plein de rayons
# qui suivent la distribution en cos^2 theta du probleme.
nRays = 1000000 # Vous pouvez augmenter pour obtenir une meilleure reponse
inputRays = RandomLambertianRays(yMax=1, maxCount=nRays)
outputRays = Rays()

childs = []
childPID = -1
while len(childs) < 8 and childPID != 0:
    childPID = os.fork()
    if childPID == 0:
        for (i,ray) in enumerate(inputRays):
            lastRay = path.traceThrough(ray)
            if lastRay.isNotBlocked:
                outputRays.append(lastRay)
            
            inputRays.displayProgress()

        outputRays.save("rays-{0}.dat".format(os.getpid()))
        exit(0)
    else:
        childs.append(childPID)

if childPID != 0:
    print("Waiting for childs for complete")
    os.waitpid(0, 0)
    print("Done")

    allRays = Rays()
    for pid in childs:
        allRays.load("rays-{0}.dat".format(pid), append=True)

    allRays.display("Output profile")


