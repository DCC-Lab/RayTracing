try:
		from raytracing import *
except ImportError:
		raise ImportError('Raytracing module not found: "pip install raytracing"')

from raytracing import *
import numpy
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import signal
import os

list = [1/3, 1/2, 1, 2, 3]
finalRays = []
pinholeDiameter = []

for x in list:

	nRays = 10000 #Number of total rays produced by the source
	inputRays = RandomUniformRays(yMax=0.000250, yMin=-0.000250, maxCount=nRays)
	outputRays = Rays() # output histogram

	Lobj = Lens(f=5, label="$objective$")
	L1 = Lens(f=100, label="$L1$")
	L2 = Lens(f=100, label="$L2$")
	L3 = Lens(f=75, label="$L3$")
	L4 = Lens(f=40, label="$L4$")
	Lp = Lens(f=50, label="$Lpinhole$")

	pinholeSize = 0.009374*x

	illumination = ImagingPath()
	illumination.append(Space(d=5))
	illumination.append(Lobj)
	illumination.append(Space(d=105))
	illumination.append(L1)
	illumination.append(Space(d=200))
	illumination.append(L2)
	illumination.append(Space(d=175))
	illumination.append(L3)
	illumination.append(Space(d=115))
	illumination.append(L4)
	illumination.append(Space(d=40))
	illumination.append(Lp)
	illumination.append(Space(d=50))
	illumination.append(Aperture(diameter=pinholeSize))

	outputRays = illumination.traceManyThrough(inputRays, progress=False)
	finalRays.append(outputRays.count/inputRays.count)
	pinholeDiameter.append(pinholeSize)
	print('.')

plt.plot(pinholeDiameter,finalRays) 
plt.show(block=True)