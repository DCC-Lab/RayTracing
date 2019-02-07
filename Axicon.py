from ABCD import *
import matplotlib.pyplot as plt

"""
Axicon: An advanced module that describes an axicon lens, not part of the basic formalism.

"""

class Axicon(Matrix):
	def __init__(self, alpha, n, diameter=float('+Inf'), label=''):	
		""" alpha is the small angle in radians of the axicon 
		(typically 2.5 or 5 degrees) corresponding to 90-apex angle

		"""
		self.n = n
		self.alpha = alpha
		super(Axicon, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)

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


if __name__ == "__main__":

	fa = 150  # Focal axicon lens
	f1 = 50.3 # Focal scan lens
	f2 = 180  # Focal tube lens
	F = 18    # Focal objective
	w = 1.2   # Beam half size DEF?

	cleoDesign = OpticalPath()
	cleoDesign.name = "Lightsheet axicon"
	cleoDesign.fanAngle = 0.0
	cleoDesign.rayNumber = 21
	cleoDesign.objectHeight = w*2.0

	axicon = Axicon(n=1.47, alpha=2.5*3.1416/180, diameter=20,label='Axicon')
	cleoDesign.append(Space(d=30))
	cleoDesign.append(axicon)
	cleoDesign.append(Space(d=fa))
	cleoDesign.append(Lens(f=fa, diameter = 25,label='Fourier lens'))
	cleoDesign.append(Space(d=fa))
	cleoDesign.append(Aperture(diameter=20,label='Galvo'))
	cleoDesign.append(Space(d=f1))
	cleoDesign.append(Lens(f=f1, diameter = 25,label='Scan lens'))
	cleoDesign.append(Space(d=f1+f2))
	cleoDesign.append(Lens(f=f2, diameter = 50,label='Tube lens'))
	cleoDesign.append(Space(d=f2))
	cleoDesign.append(Space(d=F))
	cleoDesign.append(Lens(f=F, diameter = 25,label='Objective'))	
	cleoDesign.append(Space(d=F+5))

	print("Deviation beta = {0:1.3f} rad".format(axicon.deviationAngle()))

	maxRay = Ray(y=w, theta=0) # Highest ray on axicon
	minRay = Ray(y=0.1, theta=0) # Lowest useful ray near the tip?

	maxOutputRay = cleoDesign.propagate(maxRay)[-1] # Last ray
	minOutputRay = cleoDesign.propagate(minRay)[-1] # Last ray

	startOfLine = minOutputRay.y/(minOutputRay.theta)
	endOfLine = maxOutputRay.y/(maxOutputRay.theta)

	print("Output beta_2 {0:1.2f}".format(abs(minOutputRay.theta)*180/3.1416))
	print("Final Line L = {0:1.3f} mm".format(abs(endOfLine-startOfLine)))

	cleoDesign.display()
