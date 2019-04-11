from raytracing import *
from raytracing.thorlabs import *
from raytracing.eo import *
from raytracing.olympus import *

# PN_85_877().display()
# PN_85_877().flipOrientation().display()
# AC254_050_B().display()
# AC254_050_B().flipOrientation().display()
# XLUMPlanFLN20X().display()
# XLUMPlanFLN20X().flipOrientation().display()

cavity = LaserPath()
cavity.inputBeam = GaussianBeam(w=0.01)
cavity.append(Space(d=160))
cavity.append(Lens(f=50))
cavity.append(Space(d=160))
cavity.display()

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