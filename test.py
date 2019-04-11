from raytracing import *

cavity = LaserPath()
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))
cavity.append(CurvedMirror(R=400))
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))

(q1,q2) = cavity.eigenModes()
print(q1,q2)
qs = cavity.laserModes()
for q in qs:
	print(q)

cavity.inputBeam = qs[0]
cavity.display()