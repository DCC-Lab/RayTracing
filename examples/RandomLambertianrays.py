import envexamples
from raytracing import*
nRays = 1000000 # Increase for better resolution
minHeight=0
maxHeight=50
# define a list of rays with Lambertian distribution
inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight, maxCount=nRays)
inputRays.display()