import ABCD

class ExtendedMatrix(Matrix):
	def __init__(self, A, B, C, D, E, F, physicalLength, apertureDiameter=float('+Inf')):	
		self.E = E
		self.F = F
		super(ExtendedMatrix, self).__init__(A, B, C,D, physicalLength, apertureDiameter)

	def __init__(self, matrix):	
		self.E = 0
		self.F = 0
		super(ExtendedMatrix, self).__init__(matrix.A, matrix.B, matrix.C,matrix.D, matrix.L, matrix.apertureDiameter)

	def __mul__(self, rightSide):
		matrix = super.__mul__(self, rightSide)

		if isinstance(rightSide, ExtendedMatrix):
			matrix = ExtendedMatrix(matrix)
			matrix.E = rightSide.E
			matrix.F = rightSide.F
		
		return matrix


class Axicon(ExtendedMatrix):
	def __init__(self, alpha, n, diameter=float('+Inf')):	
		self.E = 0
		self.F = (n-1)*alpha

		super(Axicon, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)

	def drawAt(self, z, axes):
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)

