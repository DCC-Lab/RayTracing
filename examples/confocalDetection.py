import envexamples

from raytracing import *
import matplotlib.pyplot as plt

"""
To obtain and plot the intensity of a point source at the pinhole of a confocal microscope (with variable pinhole size)
 as a function of position of focal spot by sending a large number of rays in the system (changing the position of the
 focal spot provides an optical sectioning process).
"""

# Focal spot radius (Airy disk radius)
focalRadius = 0.000250
# Dictionary of pinhole factors with an empty list which will subsequently contain the transmission efficiency
# for each focal spot position
pinholeModifier = {1 / 3: [], 1: [], 3: []}
# list of all relative positions from the ideal focal spot position in nm
positions = [1000, 800, 500, 300, 150, 100, 50, 25, 0, -25, -50, -100, -150, -300, -500, -800, -1000]
# Number of total rays produced by the focal spot
nRays = 100000
# Production of rays from a focal spot with a radius determined by focalRadius
inputRays = RandomUniformRays(yMax=focalRadius, yMin=-focalRadius, maxCount=nRays)
# Focal length of the objective
objFocalLength = 5

def path(focalSpotPosition=objFocalLength): 
    illumination = ImagingPath()
    illumination.append(Space(d=focalSpotPosition))
    illumination.append(Lens(f=objFocalLength))
    illumination.append(Space(d=105))
    illumination.append(Lens(f=100))
    illumination.append(Space(d=100))
    illumination.append(System4f(f1=100, f2=75))
    illumination.append(System4f(f1=40, f2=50))  # Path finishes at the pinhole position

    return illumination

def optimalPinholeSize():
    """
    Finds the magnification of the optical path and use it to find the optimal pinhole size when the focal spot is at one
    focal length distance of the objective. 

    Return
    -------
        pinholeIdeal : Float
            Returns the optimal pinhole size
    """

    # Dictionnary of the position and magnification of all conjugate planes of the focal spot. 
    planes = path().intermediateConjugates()
    # The last conjugate plane is the pinhole. The magnification of this position is saved in mag. 
    mag = planes[-1][1]
    # Calculates the pinhole size that fits perfectly the focal spot diameter.
    pinholeIdeal = abs(mag * (focalRadius * 2))

    return pinholeIdeal


def illuminationPath(pinholeFactor=None, focalSpotPosition=None):
    """
    Determines the amount of rays emitted from the object that are detected at the pinhole plane. 

    Parameter
    ---------
        pinholeFactor : Float
            Factor changing the pinhole size according to the ideal pinhole size. 

        focalSpotPosition : float
            Position of the focal spot according to the objective (first lens)

    Returns
    -------
        illumination : object of ImagingPath class.
            Returns the illumination path
    """

    illumination = path(focalSpotPosition)

    pinholeSize = optimalPinholeSize() * pinholeFactor
    illumination.append(Aperture(diameter=pinholeSize))

    # Counts how many rays make it through the pinhole
    outputRays = illumination.traceManyThroughInParallel(inputRays, progress=False)

    return outputRays.count / inputRays.count


for pinhole in pinholeModifier:
    print("\nComputing transmission for pinhole size {0:0.1f}".format(pinhole))

    efficiencyValues = []
    for z in positions:
        print(".",end='')
        newPosition = 5 + (z * 0.000001)
        efficiency = illuminationPath(pinholeFactor=pinhole, focalSpotPosition=newPosition)
        efficiencyValues.append(efficiency)
    pinholeModifier[pinhole] = efficiencyValues

plt.plot(positions, pinholeModifier[1 / 3], 'k:', label='Small pinhole', linestyle='dashed')
plt.plot(positions, pinholeModifier[1], 'k-', label='Ideal pinhole')
plt.plot(positions, pinholeModifier[3], 'k--', label='Large pinhole', linestyle='dotted')
plt.ylabel('Transmission efficiency')
plt.xlabel('Position of the focal spot (nm)')
plt.legend()
plt.show()
