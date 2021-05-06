import envexamples
from raytracing import *

nRays = 1000000 # Increase for better resolution
minHeight = -5
maxHeight = 5
minTheta = -0.5 # rad
maxTheta = +0.5

# define a list of rays with uniform distribution
inputRays = RandomUniformRays(yMin = minHeight, 
	                          yMax = maxHeight,
	                          maxCount = nRays,
	                          thetaMax = maxTheta,
	                          thetaMin = minTheta)
inputRays.display()
