import ABCD

class Axicon(ExtendedMatrix):
	def __init__(self, alpha, n, diameter=float('+Inf')):	
		self.n = n
		self.alpha = alpha

		super(Axicon, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)

	def 
	def drawAt(self, z, axes):
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)

