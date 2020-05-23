from raytracing import *

'''
Too small lenses in a 4f system causes vignetting. This code calculates accurate optical system parameters to avoid vignetting and obtain a good image size. 
'''

path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()



path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=35))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()



path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=100))
path.append(Lens(f=50,diameter=40))
path.append(Space(d=50))
path.append(Aperture(diameter=15,label='Camera'))
path.append(Space(d=50))
path.display()




