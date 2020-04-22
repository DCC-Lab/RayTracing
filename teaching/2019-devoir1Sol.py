import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from ABCD import *
import matplotlib.pyplot as plt

class DielectricInterface(Matrix):
	def __init__(self, n1, n2, R, diameter=float('+Inf'),label=''):
		a = 1.0
		b = 0.0
		c = - (n2-n1)/(n2*R)
		d = n1/n2

		super(DielectricInterface, self).__init__(A=a, B=b, C=c,D=d, physicalLength=0, apertureDiameter=diameter,label=label)
	
class ThickLens(Matrix):
	def __init__(self, n, R1, R2, thickness, diameter=float('+Inf'),label=''):
		# ... corrigez le code ici le code pour une lentille epaisse
		t = thickness

		a = t*(1.0-n)/(n*R1) + 1
		b = t/n
		c = - (n - 1.0)*(1.0/R1 - 1.0/R2 + t*(n-1.0)/(n*R1*R2))
		d = t*(n-1.0)/(n*R2) + 1
		super(ThickLens, self).__init__(A=a, B=b, C=c,D=d, physicalLength=thickness, apertureDiameter=diameter,label=label)	

if __name__ == "__main__":
	# Clairement, vous allez valider votre code d'une facon ou d'une autre...?
	path = OpticalPath()
	path.name = 'Devoir #1: Interface plane'
	path.append(Space(d=10))
	path.append(DielectricInterface(n1=1.0, n2=1.55,R=float('+Inf'),label='Interface plane'))
	path.append(Space(d=10))
	path.display()

	path = OpticalPath()
	path.name = 'Devoir #1: Plaque de verre parallele'
	path.append(Space(d=10))
	path.append(DielectricInterface(n1=1.0, n2=1.55,R=float('+Inf'),label='Entree'))
	path.append(Space(d=2))
	path.append(DielectricInterface(n1=1.55, n2=1.0,R=float('+Inf'),label='Sortie'))
	path.append(Space(d=10))
	path.display()

	path = OpticalPath()
	path.name = 'Devoir #1: Lentille épaisse par morceau'
	path.append(Space(d=10))
	path.append(DielectricInterface(n1=1.0, n2=1.55,R=5.0,label='Entree'))
	path.append(Space(d=2))
	path.append(DielectricInterface(n1=1.55, n2=1.0,R=-5.0,label='Sortie'))
	path.append(Space(d=10))
	path.display()

	path = OpticalPath()
	path.name = 'Devoir #1: Lentille épaisse en bloc'
	path.append(Space(d=10))
	path.append(ThickLens(n=1.55, R1=5.0, R2=-5.0,thickness=2.0, label='Lentille epaisse'))
	path.append(Space(d=10))
	path.display()

	M1 = DielectricInterface(n1=1.0, n2=1.55,R=5.0,label='Entree')
	M2 = Space(d=2)
	M3 = DielectricInterface(n1=1.55, n2=1.0,R=-5.0,label='Sortie')
	lens1 = M3*M2*M1
	lens2 = ThickLens(n=1.55, R1=5.0, R2=-5.0,thickness=2.0, label='Lentille epaisse')
	if lens1.C != lens2.C:
		print("Erreur: diel + space != thicklens") 

