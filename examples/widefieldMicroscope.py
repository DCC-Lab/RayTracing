'''
DESCRIPTION


When the lenses in a 4f system are too small, we get vignetting. We show a simple imaging system with vignetting, Field Stop poorly placed at a lens instead of the image with fix in next figure.
Simple 4f system with lenses too small, shows vignetting 4f system with bigger lenses, show no more vignetting and good image size

'''

from raytracing import *



path = ImagingPath()
path.objectHeight = 15
path.append(Space(d=5))
path.append(Lens(f=5, diameter=25.4))
path.append(Space(d=10))
path.append(Lens(f=5, diameter=20))
path.append(Space(d=5))
path.append(Aperture(diameter=10,label='Camera'))
path.append(Space(d=5))

# print(path.imageSize())
path.display()


path = ImagingPath()
path.objectHeight = 15
path.append(Space(d=5))
path.append(Lens(f=5, diameter=25.4))
path.append(Space(d=10))
path.append(Lens(f=5, diameter=25.4))
path.append(Space(d=5))
path.append(Aperture(diameter=10,label='Camera'))
path.append(Space(d=5))

# print(path.imageSize())
path.display()

path = ImagingPath()
path.objectHeight = 15
path.append(Space(d=5))
path.append(Lens(f=5, diameter=20))
path.append(Space(d=10))
path.append(Lens(f=5, diameter=20))
path.append(Space(d=5))
path.append(Aperture(diameter=10,label='Camera'))
path.append(Space(d=5))

# print(path.imageSize())
path.display()