try:
    from raytracing import *
except ImportError:
    raise ImportError('Raytracing module not found: "pip install raytracing"')

from raytracing import *
import matplotlib.pyplot as plt

pinholeModifier = [1/3, 1/2, 1, 2, 3]
finalRays = []
pinholeDiameter = []

for pinhole in pinholeModifier:

    pinholeSize = 0.009374*pinhole
    nRays = 10000  # Number of total rays produced by the source
    inputRays = RandomUniformRays(yMax=0.000250, yMin=-0.000250, maxCount=nRays)

    illumination = ImagingPath()
    illumination.append(Space(d=5))
    illumination.append(Lens(f=5, label="$objective$"))
    illumination.append(Space(d=105))
    illumination.append(Lens(f=100, label="$L1$"))
    illumination.append(Space(d=200))
    illumination.append(Lens(f=100, label="$L2$"))
    illumination.append(Space(d=175))
    illumination.append(Lens(f=75, label="$L3$"))
    illumination.append(Space(d=115))
    illumination.append(Lens(f=40, label="$L4$"))
    illumination.append(Space(d=40))
    illumination.append(Lens(f=50, label="$Lpinhole$"))
    illumination.append(Space(d=50))
    illumination.append(Aperture(diameter=pinholeSize))

    outputRays = illumination.traceManyThrough(inputRays, progress=False)
    finalRays.append(outputRays.count/inputRays.count)
    pinholeDiameter.append(pinholeSize)
    print('.')

plt.plot(pinholeDiameter,finalRays) 
plt.ylabel('Transmission efficiency')
plt.xlabel('Pinhole size (mm)')
plt.title("Transmission efficiency according to the pinhole size of a confocal microscope")
plt.show()