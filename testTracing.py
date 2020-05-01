from raytracing import *

f = 50
path = ImagingPath()
path.append(Space(d=f))
path.append(Lens(f=f, diameter=25))
path.append(Space(d=f))

nRays = 100000 # You can change this
inputRays = RandomUniformRays(yMax=0, maxCount=nRays) # at center
outputRays = Rays() # output histogram

for ray in inputRays:
    lastRay = path.traceThrough(ray)
    if lastRay.isNotBlocked:
        outputRays.append(lastRay)
    inputRays.displayProgress()

print("Number of rays sent: {0}".format(inputRays.count))
print("Number of rays received: {0}".format(outputRays.count))
print("Transmission efficiency: {0}".format(outputRays.count/inputRays.count))

outputRays.display("Output profile")

