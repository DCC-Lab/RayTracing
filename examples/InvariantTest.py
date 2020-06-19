import envexamples
from raytracing import *

path = ImagingPath() # second lens is smaller than the first one
path.append(System4f(f1=30, diameter1=20, f2=50, diameter2=10))
path.append(Aperture(diameter=10, label='Camera'))
print("Lagrange invariant of the system is {}".format(path.lagrangeInvariant()))
#path.display(onlyPrincipalAndAxialRays=False)

axialAngle = path.axialRay()
maxAngle = axialAngle.theta
print("The maximal possible angle is {}".format(maxAngle)) 
halfFOV = path.fieldOfView()/2

ray1 = Ray(theta = 0.16, y = 4) # change y to 0, 1, 2, 3, 4
ray2 = Ray(theta = 0, y = 3)
ray1Out = path.traceThrough(ray1)
ray2Out = path.traceThrough(ray2)

lagrange = path.lagrangeInvariant(ray1, ray2)
print("The lagrange invariant of those two rays is {}".format(lagrange))

if ray1Out.isBlocked:
    print("Ray 1 blocked")
if ray2Out.isBlocked:
	print("Ray 2 blocked")
if ray1Out.isNotBlocked and ray2Out.isNotBlocked:
    print("Not Blocked")

