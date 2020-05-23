import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *

'''
Too small lenses in a 4f system causes vignetting. This code calculates accurate optical system parameters to avoid vignetting and obtain a good image size. 
'''

path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=20))
path.append(Space(d=100))
path.append(Lens(f=35,diameter=20))
path.append(Space(d=35))
path.append(Aperture(diameter=20,label='Camera'))
path.append(Space(d=35))
path.display()



path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=100))
path.append(Lens(f=35,diameter=25))
path.append(Space(d=35))
path.append(Aperture(diameter=20,label='Camera'))
path.append(Space(d=35))
path.display()



path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=100))
path.append(Lens(f=35,diameter=30))
path.append(Space(d=35))
path.append(Aperture(diameter=20,label='Camera'))
path.append(Space(d=35))
path.display()