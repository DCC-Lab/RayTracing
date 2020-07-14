import envexamples
from raytracing import *

path = ImagingPath()
path.label = "Demo #5: Simple microscope system"
path.append(Space(d=4))
path.append(Lens(f=4, diameter=0.8, label='Obj'))
path.append(Space(d=4 + 18))
path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.figure.dpiFactor = 0.5  # try with 0, 0.5 and 1
path.display()