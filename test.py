import math as m
from raytracing import *
from raytracing.thorlabs import *

path = ImagingPath()
path.label = "Demo #16: Vendor Lenses"
path.append(Space(d=5))
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
path.displayGaussian(beam=GaussianBeam(w=1))

