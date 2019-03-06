import math as m
from raytracing import *
from raytracing.thorlabs import *

path = LaserPath()
path.label = "Demo #16: Gaussian beam and  vendor lenses"
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=50))
path.append(eo.PN_33_921())
path.append(Space(d=50))
path.append(eo.PN_88_593())
path.append(Space(180))
path.append(olympus.LUMPlanFL40X())
path.append(Space(10))
path.display(beam=GaussianBeam(w=0.001))
print(GaussianBeam(w=0.001))
