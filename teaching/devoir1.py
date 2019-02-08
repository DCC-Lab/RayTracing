# Devoir #1: Simple assignement for 1st-year students. 
import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from ABCD import *
import matplotlib.pyplot as plt

class DielectricInterface(Matrix):
	def __init__(self, n1, n2, R, diameter=float('+Inf')):
		# ... corrigez le code ici pour une interface dielectrique
		super(DielectricInterface, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)
	
class ThickLens(Matrix):
	def __init__(self, n, R1, R2, thickness, diameter=float('+Inf')):
		# ... corrigez le code ici le code pour une lentille epaisse
		super(ThickLens, self).__init__(A=1, B=0, C=-0,D=1, physicalLength=thickness, apertureDiameter=diameter)	


# Clairement, vous allez valider votre code d'une facon ou d'une autre...?
if __name__ == "__main__":
	path = OpticalPath()
	path.name = 'Devoir #1: faites une lentille epaisse et une interface dielectrique'
	path.append(Space(d=10))
	path.append(ThickLens(n=1.55, R1=float('+Inf'), R2=float('+Inf'), thickness=2))
	#...? autre chose
	path.append(Space(d=10))
	path.display()
