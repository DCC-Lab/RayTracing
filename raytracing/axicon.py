from .matrix import *
import matplotlib.pyplot as plt

"""
Axicon: An advanced module that describes an axicon lens, not part of the basic formalism.

"""

class Axicon(Matrix):
	def __init__(self, alpha, n, diameter=float('+Inf'), label=''):	
		""" An element representing an axicon conical lens, used to obtain 
		a line focus instead of a point.

		alpha is the small angle in radians of the axicon 
		(typically 2.5 or 5 degrees) corresponding to 90-apex angle

		"""
		self.n = n
		self.alpha = alpha
		super(Axicon, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter, label=label)

	def deviationAngle(self):
		""" Provides deviation angle delta

		See Kloos, p.48

		"""

		return (self.n-1.0)*self.alpha


	def focalLineLength(self, yMax=None):
		""" Provides the line length, assuming a ray at height yMax

		See Kloos, p.48

		"""

		if yMax == None:
			yMax = self.apertureDiameter/2

		return yMax/(self.n-1.0)/self.alpha

	def mul_ray(self, rightSideRay):
		outputRay = super(Axicon, self).mul_ray(rightSideRay)

		if rightSideRay.y > 0:
			outputRay.theta += -self.deviationAngle()
		elif rightSideRay.y < 0:
			outputRay.theta +=  self.deviationAngle()
		# theta == 0 is not deviated
				
		return outputRay

	def mul_mat(self, rightSideMatrix):
		raise TypeError("Cannot calculate final matrix with axicon in path. \
			You can only propagate rays all rhe way through")

	def drawAt(self, z, axes):
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)


