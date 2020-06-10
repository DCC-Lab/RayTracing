import envexamples
from raytracing import *
nRays = 1000000 # Increase for better resolution
minHeight=0
maxHeight=50
minTheta=-1.5
maxTheta=1.5
# define a list of rays with uniform distribution
inputRays = RandomUniformRays(yMin=minHeight, yMax=maxHeight, maxCount=nRays, thetaMax=maxTheta, thetaMin=minTheta)
inputRays.display()
