import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *



path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=20))
path.append(Space(d=50))
path.append(Space(d=100))
path.append(Lens(f=100,diameter=20))
path.append(Space(d=100))


path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=30))
path.append(Space(d=50))
path.append(Space(d=100))
path.append(Lens(f=100,diameter=30))
path.append(Space(d=100))


path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=25))
path.append(Space(d=50))
path.append(Space(d=100))
path.append(Lens(f=100,diameter=25))
path.append(Space(d=100))

'''
plt.figure(1)

#1
plt.subplot2grid((2,2), (0,0))
plt.title('..')

#2
plt.subplot2grid((2,2), (0,1))
plt.title('..')

#3
plt.subplot2grid((2,2), (1,0), colspan = 2)
plt.title('..')


plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.3,
                    wspace=0.35)
plt.show()

