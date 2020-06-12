from .matrix import *
import matplotlib.pyplot as plt



class Axicon(Matrix):
	"""
	This class is an advanced module that describes an axicon lens, not part of the basic formalism.
	Using this class an axicon conical lens can be presented.
	Axicon lenses are used to obtain a line focus instead of a point.

	Parameters
	----------
	alpha : float
		alpha is the small angle in radians of the axicon
		(typically 2.5 or 5 degrees) corresponding to 90-apex angle
	n : float
		index of refraction.
		This value cannot be less than 1.0.
	diameter : float
		Aperture of the element. (default = +Inf)
		The diameter of the aperture must be a positive value.
	label : string
		The label of the axicon lens.

	"""

	def __init__(self, alpha, n, diameter=float('+Inf'), label=''):	

		self.n = n
		self.alpha = alpha
		super(Axicon, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter, label=label)

	def deviationAngle(self):
		""" This function provides deviation angle delta

		Returns
		-------
		delta : float
			the deviation angle

		See ALso
		--------
		https://ru.b-ok2.org/book/2482970/9062b7, p.48

		"""

		return (self.n-1.0)*self.alpha


	def focalLineLength(self, yMax=None):
		""" Provides the line length, assuming a ray at height yMax

		Parameters
		----------
		yMax : float
			the height of the ray (default=None)
			If no height is defined for the ray, then yMax would be set to the height of the axicon (apertureDiameter/2)

		Returns
		-------
		focalLineLength : float
			the length of the focal line

		See ALso
		--------
		https://ru.b-ok2.org/book/2482970/9062b7, p.48

		"""

		if yMax == None:
			yMax = self.apertureDiameter/2

		return yMax/(self.n-1.0)/self.alpha

	def mul_ray(self, rightSideRay):
		""" This function is used to calculate the output ray through an axicon.

		Parameters
		----------
		rightSideRay : object of ray class
			A ray with a defined height and angle.

		Returns
		-------
		outputRay : object of ray class
			the height and angle of the output ray.

		See Also
		--------
		raytracing.Matrix.mul_ray


		"""

		outputRay = super(Axicon, self).mul_ray(rightSideRay)

		if rightSideRay.y > 0:
			outputRay.theta += -self.deviationAngle()
		elif rightSideRay.y < 0:
			outputRay.theta +=  self.deviationAngle()
		# theta == 0 is not deviated
				
		return outputRay

	def mul_mat(self, rightSideMatrix):
		""" The final matrix of an optical path with an axicon can be calculated using this function.

		Parameters
		----------
		rightSideMatrix : object of matrix class
			The ABCD matrix of an element or an optical path.

		Notes
		-----
		For now the final matrix with an axicon in the path cannot be calculated.

		"""

		raise TypeError("Cannot calculate final matrix with axicon in path. \
			You can only propagate rays all rhe way through")

	def drawAt(self, z, axes):
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)


