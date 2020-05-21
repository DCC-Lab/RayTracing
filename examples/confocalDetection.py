from raytracing import *
import matplotlib.pyplot as plt

pinholeModifier = {1/3:[], 1:[], 3:[]}

for pinhole in pinholeModifier:

    finalRays = pinholeModifier[pinhole]
    pinholeSize = 0.009374*pinhole
    positions = [5.001000, 5.000800, 5.000500, 5.000300, 5.000150, 5.000100, 5.000050, 5.000025, 5, 4.999975, 4.999950, 4.999900, 4.999850, 4.999700, 4.999500, 4.999200, 4.999000]
    print('.')

    for z in positions:

        nRays = 10000  # Number of total rays produced by the source
        inputRays = RandomUniformRays(yMax=0.000250, yMin=-0.000250, maxCount=nRays)

        illumination = ImagingPath()
        illumination.append(Space(d=z))
        illumination.append(Lens(f=5))
        illumination.append(Space(d=105))
        illumination.append(Lens(f=100))
        illumination.append(Space(d=200))
        illumination.append(Lens(f=100))
        illumination.append(Space(d=175))
        illumination.append(Lens(f=75))
        illumination.append(Space(d=115))
        illumination.append(Lens(f=40))
        illumination.append(Space(d=90))
        illumination.append(Lens(f=50))
        illumination.append(Space(d=50))
        illumination.append(Aperture(diameter=pinholeSize))

        outputRays = illumination.traceManyThrough(inputRays, progress=False)
        finalRays.append(outputRays.count/inputRays.count)

    pinholeModifier[pinhole] = finalRays

plt.plot(positions, pinholeModifier[1/3], label='Pinhole Size S/3')
plt.plot(positions, pinholeModifier[1], label='Pinhole Size S')
plt.plot(positions, pinholeModifier[3], label='Pinhole Size 3S')
plt.ylabel('Transmission efficiency')
plt.xlabel('Position of the focal spot (mm)')
plt.legend()
plt.show()