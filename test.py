from raytracing import *
from raytracing.thorlabs import *
from raytracing.eo import *
from raytracing.olympus import *

PN_85_877().display()
PN_85_877().flipOrientation().display()
AC254_050_B().display()
AC254_050_B().flipOrientation().display()
XLUMPlanFLN20X().display()
XLUMPlanFLN20X().flipOrientation().display()


irRetrofocus = MatrixGroup()
irRetrofocus.label = "Bliq Axicon Retrofocus"
irRetrofocus.append(PN_85_877())
irRetrofocus.append(Space(d=38.85))
irRetrofocus.append(AC254_050_B())
irRetrofocus.display()

offset = 0
f1 = 50
f2 = 100
inputBeam = GaussianBeam(w=1)

path = ImagingPath()
path.label = "Relay"
path.append(Space(d=f1))
path.append(Lens(f=f1, diameter=25))
path.append(Space(d=f1/2))
path.append(Aperture(diameter=2))
path.append(Space(d=f1/2))
path.append(Space(d=f2))
path.append(Lens(f=f2, diameter=25))
path.append(Space(d=f2+10*offset))
(m1, m2) = path.marginalRays()
chiefRay = path.chiefRay(path.objectHeight/2)

print(path*inputBeam)

imag = path.ImagingPath()
imag.objectHeight = 3
imag.fanAngle = 0.15
imag.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
print(imag.entrancePupil())
