"""
To obtain and plot the intensity of a point source at the pinhole of a confocal microscope (with variable pinhole size)
 as a function of position of focal spot by sending a large number of rays in the system (changing the position of the
 focal spot provides an optical sectioning process).
"""
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *
import matplotlib.pyplot as plt

# Dictionary of pinhole factors with an empty list which will subsequently contain the transmission efficiency
# for each focal spot position
pinholeModifier = {1/3: [], 1: [], 3: []}

# list of all relative positions from the ideal focal spot position in nm
positions = [1000, 800, 500, 300, 150, 100, 50, 25, 0, -25, -50, -100, -150, -300, -500, -800, -1000]

for pinhole in pinholeModifier:

    finalRays = pinholeModifier[pinhole]
    # pinholeSize = 0.009374*pinhole  # Ideal size of the pinhole times a certain factor
    print(".")

    for z in positions:

        newPositions = 5 + (z*0.000001)  # Working distance of the objective + position
        #print(newPositions)
        nRays = 10000  # Number of total rays produced by the focal spot
        # Production of rays from a focal spot with a radius of 250 nm
        inputRays = RandomUniformRays(yMax=0.000250, yMin=-0.000250, maxCount=nRays)

        illumination = ImagingPath()
        illumination.append(Space(d=newPositions))
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
        pinholeSize = 0.009375 * pinhole
        #pinholeSize = illumination.imageSize()*pinhole  # Ideal size of the pinhole times a certain factor
        #print(pinholeSize)
        #print(illumination.imageSize())
        illumination.append(Aperture(diameter=pinholeSize))

        # Counts how many rays make it through the pinhole
        outputRays = illumination.traceManyThrough(inputRays, progress=False)
        finalRays.append(outputRays.count/inputRays.count)  # Calculates the transmission efficiency

    pinholeModifier[pinhole] = finalRays  # Incorporates the final list of transmission efficiencies into the dictionary

plt.plot(positions, pinholeModifier[1/3], label='Pinhole Size S/3', linestyle='dashed')
plt.plot(positions, pinholeModifier[1], label='Pinhole Size S')
plt.plot(positions, pinholeModifier[3], label='Pinhole Size 3S', linestyle='dotted')
plt.ylabel('Transmission efficiency')
plt.xlabel('Position of the focal spot (nm)')
plt.legend()
plt.show()
