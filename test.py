from raytracing import *

cavity = LaserPath()
cavity.isResonator = True
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))
cavity.append(CurvedMirror(R=400))
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))

# Calculate all self-replicating modes (i.e. eigenmodes)
(q1,q2) = cavity.eigenModes()
print(q1,q2)

# Obtain all physical (i.e. finite) self-replicating modes
qs = cavity.laserModes()
for q in qs:
	print(q)

# Show
cavity.display()