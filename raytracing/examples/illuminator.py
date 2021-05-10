TITLE       = "Kohler illumination"
DESCRIPTION = """
"""

import envexamples
from raytracing import *

def exampleCode():
	path = ImagingPath()
	path.name = "Kohler illumination with 1 cm wide lamp and 0.5 NA"
	path.append(Space(d=40))
	path.append(Lens(f=40,diameter=25, label='Collector'))
	path.append(Space(d=40+25))
	path.append(Lens(f=25, diameter=75, label='Condenser'))
	path.append(Space(d=25))
	path.append(Space(d=9))
	path.append(Lens(f=9, diameter=8, label='Objective'))
	path.append(Space(d=9))
	path.showLabels=True
	print(path.fieldStop())
	print(path.fieldOfView())
	path.display(ObjectRays(diameter=20, H=3, T=3, halfAngle=0.5), onlyPrincipalAndAxialRays=True, limitObjectToFieldOfView=True)
	#path.saveFigure("Illumination.png", onlyPrincipalAndAxialRays=True, limitObjectToFieldOfView=True)

if __name__ == "__main__":
    exampleCode()
