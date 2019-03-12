from raytracing import *
from raytracing.thorlabs import *

offset = 0
f1 = 150
f2 = 300
inputBeam = GaussianBeam(w=1)

path = LaserPath()
path.label = "Relay"
path.append(Space(d=f1))
path.append(Lens(f=f1, diameter=25))
path.append(Space(d=f1+f2+offset))
path.append(Lens(f=f2, diameter=25))
path.append(Space(d=f2+10*offset))
path.display(inputBeam=inputBeam)
print(path*inputBeam)

imag = path.ImagingPath()
imag.objectHeight = 3
imag.fanAngle = 0.15
imag.display()