import envexamples
from raytracing import *

nRays = 1000000 # Increase for better resolution
minHeight = -5
maxHeight = 5

# Lambertian: distribution proportional to cos theta
inputRays = RandomLambertianRays(yMin = minHeight, 
	                             yMax = maxHeight,
	                             maxCount = nRays)
inputRays.display()
