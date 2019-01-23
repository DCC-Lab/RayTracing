import ABCD as rt


class DielectricInterface(rt.Matrix):
	def __init__(self, n1, n2, R, diameter=float('+Inf')):
		# ... corrigez le code ici pour une interface dielectrique
		super(DielectricInterface, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)
	
	def drawAt(self, z, axes):
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2
		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)

class ThickLens(rt.Matrix):
	def __init__(self, n, R1, R2, thickness, diameter=float('+Inf')):
		# ... corrigez le code ici le code pour une lentille epaisse
		super(ThickLens, self).__init__(A=1, B=0, C=-0,D=1, physicalLength=thickness, apertureDiameter=diameter)	

	def drawAt(self, z, axes):
		# Vous pouvez ameliorez le dessin si vous voulez, pas necessaire
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2
		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)


path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.ThickLens(n=1.55, R1=?, R2=?, thickness=2))
#...? autre chose
path.display()
