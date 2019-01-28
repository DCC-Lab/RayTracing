import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys
if sys.version_info[0] < 3:
    print("Warning: you should really be using Python 3. No guarantee this will work in 2.x")

"""A simple module for ray tracing with ABCD matrices.

Create an OpticalPath(), append matrices (optical elements).
and then display().
The  objectHeight, fanAngle, and fanNumber are used if the
field of view is not defined. You may adjust the values
to suit your needs.
"""


class Ray:
	"""A vector and a light ray as transformed by ABCD matrices

	The Ray() has a height (y) and an angle with the optical axis (theta).
	It also has a position (z) and a marker if it has been blocked.

	Simple class functions are defined to obtain a group of rays: fans
	originate from the same height but sweep a range of angles; fan groups 
	are fans originating from different heights; and a beam spans 
	various heights with a fixed angle.
	"""

	def __init__(self, y=0, theta=0, z=0, isBlocked=False):	
		# Ray matrix formalism
		self.y = y
		self.theta = theta

		# Position of this ray
		self.z = z

		# Aperture
		self.isBlocked = isBlocked

	@property
	def isNotBlocked(self):
		"""Opposite of isBlocked.  Convenience function for readability

		"""

		return not self.isBlocked

	@staticmethod
	def fan(self, y, radianMin, radianMax, N):
		"""A list of rays spanning from radianMin to radianMax to be used with Matrix().propagate()

		"""
		rays = []
		for i in range(N):
			theta = radianMin + i*(radianMax-radianMin)/(N-1)
			rays.append(Ray(y,theta,z=0))

		return rays

	@staticmethod
	def fanGroup(yMin, yMax, M, radianMin, radianMax, N):
		""" A list of rays spanning from yMin to yMax and radianMin to 
		radianMax to be used with Matrix().propagate()
		"""
		rays = []
		for j in range(M):
			for i in range(N):
				theta = radianMin + i*(radianMax-radianMin)/(N-1)
				y = yMin + j*(yMax-yMin)/(M-1)
				rays.append(Ray(y,theta,z=0))
		return rays

	@staticmethod
	def beam(yMin, yMax, M, radian):
		""" A list of rays spanning from yMin to yMax at a fixed
		angle to be used with Matrix().propagate()
		"""
		rays = []
		for i in range(M):
			y = yMin + i*(yMax-yMin)/(M-1)
			theta = radian
			rays.append(Ray(y,theta,z=0))
		return rays
		
	def __str__(self):
		""" String description that allows the use of print(Ray()) """

		description  = " /     \\ \n"
		description += "| {0:0.3f} |\n".format(self.y)
		description += "|       |\n"
		description += "| {0:0.3f} |\n".format(self.theta)
		description += " \\     /\n\n"

		description += "z = {0:0.3f}\n".format(self.z)
		if self.isBlocked:
			description += " (blocked)"

		return description



class Matrix(object):
	"""A matrix and an optical element that can transform a ray or another matrix.

	The general properties (A,B,C,D) are defined here. The operator "*" is 
	overloaded to allow simple statements such as:

	M2 = M1 * ray  
	or 
	M3 = M2 * M1

	In addition apertures are considered and the physical length is 
	included to allow simple management of the ray tracing.
	"""

	def __init__(self, A, B, C, D, physicalLength=0, apertureDiameter=float('+Inf'), label=''):	
		# Ray matrix formalism
		self.A = float(A)
		self.B = float(B)
		self.C = float(C)
		self.D = float(D)

		# Length of this element
		self.L = float(physicalLength)

		# Aperture
		self.apertureDiameter = apertureDiameter
		
		self.label = label
		super(Matrix, self).__init__()		

	def __mul__(self, rightSide):
		"""Operator overloading allowing easy to read matrix multiplication 

		For instance, with M1 = Matrix() and M2= Matrix(), one can write M3 = M1*M2.
		With r = Ray(), one can apply the M1 transform to a ray with r = M1*r

		"""
		if isinstance(rightSide, Matrix):
			return self.mul_matrix(rightSide)
		elif isinstance(rightSide, Ray):
			return self.mul_ray(rightSide)
		else:
			raise TypeError("Unrecognized right side element in multiply: '{0}' cannot be multiplied by a Matrix".format(rightSide))			

	def mul_matrix(self, rightSideMatrix):
		""" Multiplication of two matrices.  Total length of the elements is calculated.
		Apertures are lost.

		"""

		a = self.A * rightSideMatrix.A + self.B * rightSideMatrix.C
		b = self.A * rightSideMatrix.B + self.B * rightSideMatrix.D
		c = self.C * rightSideMatrix.A + self.D * rightSideMatrix.C
		d = self.C * rightSideMatrix.B + self.D * rightSideMatrix.D
		l = self.L + rightSideMatrix.L

		return Matrix(a,b,c,d,physicalLength=l)

	def mul_ray(self, rightSideRay):
		""" Multiplication of a ray by a matrix.  New position of ray is updated by 
		the physical length of the matrix. If the ray is beyond the aperture diameter
		it is labelled as "isBlocked = True" but can still propagate.

		"""

		outputRay = Ray()
		outputRay.y = self.A * rightSideRay.y + self.B * rightSideRay.theta
		outputRay.theta = self.C * rightSideRay.y + self.D * rightSideRay.theta
		outputRay.z = self.L + rightSideRay.z

		if abs(rightSideRay.y) > self.apertureDiameter/2:			
			outputRay.isBlocked = True
		else:
			outputRay.isBlocked = rightSideRay.isBlocked		

		return outputRay

	def pointsOfInterest(self, z):
		""" Any points of interest for this matrix (focal points, principal planes etc...)
		"""
		return []

	def focalDistances(self):
		""" The equivalent focal distance calcuated from the power (C) of the matrix.

		Currently, it is assumed the index is n=1 on either side and both focal 
		distances are the same.
		"""

		focalDistance = -1.0/self.C #FIXME: Assumes n=1 on either side
		return (focalDistance, focalDistance)

	def focusPositions(self, z):
		""" Positions of both focal points on either side.

		Currently, it is assumed the index is n=1 on either side and both focal 
		distances are the same.
		"""
		(frontFocal, backFocal) = self.focalDistances()
		(p1, p2) = self.principalPlanePositions(z)
		return (p1-frontFocal, p2+backFocal)

	def principalPlanePositions(self, z):
		""" Positions of the input and output prinicpal planes.

		Currently, it is assumed the index is n=1 on either side.
		"""
		p1 = z + (1-self.D)/self.C #FIXME: Assumes n=1 on either side
		p2 = z + self.L + (1-self.A)/self.C #FIXME: Assumes n=1 on either side
		return (p1,p2)

	def drawAt(self, z, axes):
		""" Draw element on plot with starting edge at 'z'.

		"""
		halfHeight = self.displayHalfHeight()
		p = patches.Rectangle((z,-halfHeight), self.L, 2*halfHeight, color='k', fill=False, transform=axes.transData, clip_on=False)
		axes.add_patch(p)

	def drawLabels(self,z, axes):
		""" Draw element labels on plot with starting edge at 'z'.

		"""
		halfHeight = self.displayHalfHeight()
		center = z+self.L/2.0
		plt.annotate(self.label, xy=(center, 0.0), xytext=(center, halfHeight*1.1), xycoords='data', ha='center', va='bottom')

	def displayHalfHeight(self):
		""" A reasonable height for display purposes for an element, whether it is infinite or not.

		If the element is infinite, currently the half-height will be '4'.
		If not, it is the apertureDiameter/2.

		"""
		halfHeight = 4 # default half height is reasonable for display if infinite
		if self.apertureDiameter != float('+Inf'):
			halfHeight = self.apertureDiameter/2.0 # real half height
		return halfHeight

	def __str__(self):
		""" String description that allows the use of print(Matrix())

		"""
		description  = " /             \\ \n"
		description += "| {0:0.3f}   {1:0.3f} |\n".format(self.A, self.B)
		description += "|               |\n"
		description += "| {0:0.3f}   {1:0.3f} |\n".format(self.C, self.D)
		description += " \\             /\n"
		if self.C != 0:
			description += "\nf={0:0.3f}\n".format(-1.0/self.C)
		else:
			description += "\nf = +inf (afocal)\n"
		return description

class Lens(Matrix):
	"""Lens: a matrix representing a thin lens of focal f and finite diameter 

	"""

	def __init__(self, f, diameter=float('+Inf'), label=''):	
		super(Lens, self).__init__(A=1, B=0, C=-1/float(f),D=1, physicalLength=0, apertureDiameter=diameter,label=label)

	def drawAt(self, z, axes):
		halfHeight = self.displayHalfHeight()
		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)
		self.drawCardinalPoints(z, axes)

	def drawCardinalPoints(self, z, axes):
		(f1,f2) = self.focusPositions(z)
		axes.plot([f1,f2], [0,0], 'ko', color='k', linewidth=0.4)

	def pointsOfInterest(self,z):
		(f1,f2) = self.focusPositions(z)
		return [{'z':f1,'label':'$F_1$'},{'z':f2,'label':'$F_2$'}]


class Space(Matrix):
	"""Space: a matrix representing free space

	"""

	def __init__(self, d,label=''):	
		super(Space, self).__init__(A=1, B=float(d), C=0,D=1, physicalLength=d, label=label)
	def drawAt(self, z, axes):
		return

class Aperture(Matrix):
	"""Aperture: a matrix representing an aperture of finite diameter.

	If the ray is above the finite diameter, the ray is blocked.
	"""

	def __init__(self, diameter,label=''):	
		super(Aperture, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter, label=label)

	def drawAt(self, z, axes):
		halfHeight = self.apertureDiameter/2
		plt.arrow(z, halfHeight+1, 0,-1, width=0.1, fc='k', ec='k',head_length=0.05, head_width=1,length_includes_head=True)
		plt.arrow(z, -halfHeight-1, 0, 1, width=0.1, fc='k', ec='k',head_length=0.05, head_width=1, length_includes_head=True)


class OpticalPath(object):
	"""OpticalPath: the main class of the module, allowing calculations and ray tracing for an object at the beginning.

	Usage is to create the OpticalPath(), then append() elements and display().
	You may change objectHeight, fanAngle, fanNumber and rayNumber.
	"""

	def __init__(self):
		self.name = "Ray tracing"
		self.elements = []
		self.objectHeight = 1.0   # object height (full). FIXME: Python 2.7 requires 1.0, not 1 (float)
		self.objectPosition = 0.0 # always at z=0 for now. FIXME: Python 2.7 requires 1.0, not 1 (float)
		self.fanAngle = 0.5       # full fan angle for rays
		self.fanNumber = 10       # number of rays in fan
		self.rayNumber = 3        # number of rays from different heights on object
		
		# Display properties
		self.showElementLabels = True
		self.showPointsOfInterest = True
		self.showPointsOfInterestLabels = True
		self.showPlanesAcrossPointsOfInterest = True

	def append(self, matrix):
		self.elements.append(matrix)

	def transferMatrix(self, z = float('+Inf')):
		transferMatrix = Matrix(A=1, B=0, C=0, D=1)
		for element in self.elements: 
			if transferMatrix.L + element.L <= z: #FIXME: Assumes z falls on edge of element
				transferMatrix = element*transferMatrix
			else:
				break

		return transferMatrix

	def propagate(self, inputRay):
		ray = inputRay
		outputRays = [ray]
		for element in self.elements:
			ray = element*ray
			outputRays.append(ray)
		return outputRays

	def propagateMany(self, inputRays):
		output = []
		for inputRay in inputRays:
			ray = inputRay
			outputRays = [ray]
			for element in self.elements:
				ray = element*ray
				outputRays.append(ray)
			output.append(outputRays)
		return output

	def hasFiniteDiameterElements(self):
		for element in self.elements:
			if element.apertureDiameter != float('+Inf'):
				return True
		return False

	def chiefRay(self, y):
		( stopPosition, stopDiameter ) = self.apertureStop()
		transferMatrixToApertureStop = self.transferMatrix(z=stopPosition)
		A = transferMatrixToApertureStop.A
		B = transferMatrixToApertureStop.B
		return Ray(y=y, theta=-A*y/B)

	def marginalRays(self, y):
		( stopPosition, stopDiameter ) = self.apertureStop()
		transferMatrixToApertureStop = self.transferMatrix(z=stopPosition)
		A = transferMatrixToApertureStop.A
		B = transferMatrixToApertureStop.B

		thetaUp = (stopDiameter/2*0.98 - A * y )/ B ;
		thetaDown = (-stopDiameter/2*0.98 - A * y )/ B ;

		return (Ray(y=0, theta=thetaUp), Ray(y=0, theta=thetaDown))

	def apertureStop(self):
		# Aperture stop is the aperture that limits the system
		# Strategy: take ray height and divide by real aperture diameter.
		# Max ratio is the aperture stop.
		if not self.hasFiniteDiameterElements():
			return (None,float('+Inf'))
		else:
			ray = Ray(y=0, theta=0.1) # Any ray angle will do
			maxRatio = 0 
			apertureStopPosition = 0
			for element in self.elements:
				ray = element*ray
				ratio = ray.y/element.apertureDiameter
				if ratio > maxRatio:
					apertureStopPosition = ray.z
					apertureStopDiameter = element.apertureDiameter
					maxRatio = ratio

			return (apertureStopPosition, apertureStopDiameter)

	def fieldStop(self):
		# Field stop is the aperture that limits the image size (or field of view)
		# Strategy: take ray at various height from object and aim at center of pupil
		# (chief ray from that point) until ray is blocked
		# It is possible to have finite diameter elements but still an infinite
		# field of view and therefore no Field stop.

		if not self.hasFiniteDiameterElements():
			return (None,float('+Inf'))
		else:
			deltaHeight = 0.001
			fieldStopPosition = None
			fieldStopDiameter = float('+Inf')
			for i in range(10000):
				chiefRay = self.chiefRay(y=i*deltaHeight)
				outputRaySequence = self.propagate(chiefRay)
				for ray in reversed(outputRaySequence):
					if not ray.isBlocked:
						break
					else:
						fieldStopPosition = ray.z
						fieldStopDiameter = abs(ray.y) * 2.0

				if fieldStopPosition != None:
					return (fieldStopPosition,fieldStopDiameter)

			return (fieldStopPosition,fieldStopDiameter)

	def fieldOfView(self):
		# The field of view is the maximum object height visible until blocked by field stop
		# Strategy: take ray at various height from object and aim at center of pupil
		# (chief ray from that point) until ray is blocked.
		# It is possible to have finite diameter elements but still an infinite
		# field of view and therefore no Field stop.
		halfFieldOfView = float('+Inf')
		(stopPosition, stopDiameter) = self.fieldStop()
		if stopPosition == None:
			return halfFieldOfView

		transferMatrixToFieldStop = self.transferMatrix(z=stopPosition)
		deltaHeight = 0.001 #FIXME: This is not that great.
		for i in range(10000): #FIXME: When do we stop? Currently 10.0 (abritrary).
			height = i*deltaHeight
			chiefRay = self.chiefRay(y=height)
			outputRay = transferMatrixToFieldStop*chiefRay
			if abs(outputRay.y) > stopDiameter/2.0:
				halfFieldOfView = height
				break

		return halfFieldOfView*2.0

	def display(self):
		fig, axes = plt.subplots(figsize=(10, 7))
		axes.set(xlabel='Distance', ylabel='Height', title=self.name)
		axes.set_ylim([-5,5]) # FIXME: obtain limits from plot.  Currently 5cm either side
		
		fieldOfView = self.fieldOfView()
		if fieldOfView != float('+Inf'):
			self.objectHeight = fieldOfView

		self.drawRayTraces(axes, removeBlockedRaysCompletely=False)
		self.drawObject(axes)
		self.drawOpticalElements(axes)
		if self.showPointsOfInterest:
			self.drawPointsOfInterest(axes)

		plt.ioff()
		plt.show()

	def save(self, filepath):
		fig, axes = plt.subplots(figsize=(10, 7))
		axes.set(xlabel='Distance', ylabel='Height', title=self.name, aspect='equal')
		axes.set_ylim([-5,5]) # FIXME: obtain limits from plot.  Currently 5cm either side
		if self.fieldOfView() != float('+Inf'):
			self.objectHeight = self.fieldOfView()/2.0

		self.drawRayTraces(axes)
		self.drawObject(axes)
		self.drawOpticalElements(axes)
		if self.showPointsOfInterest:
			self.drawPointsOfInterest(axes)
		fig.savefig(filepath,dpi=600)

	def drawObject(self, axes):
		plt.arrow(self.objectPosition, -self.objectHeight/2, 0, self.objectHeight, width=0.1, fc='b', ec='b',head_length=0.25, head_width=0.25,length_includes_head=True)

	def drawPointsOfInterest(self, axes):
		pointsOfInterestLabels = {} # Regroup labels at same z
		zElement = 0
		for element in self.elements:
			pointsOfInterest = element.pointsOfInterest(zElement)

			for pointOfInterest in pointsOfInterest:
				zStr = "{0:3.3f}".format(pointOfInterest['z'])
				label = pointOfInterest['label']
				if zStr in pointsOfInterestLabels:
					pointsOfInterestLabels[zStr] = pointsOfInterestLabels[zStr]+", "+label
				else:
					pointsOfInterestLabels[zStr] = label
			zElement += element.L

		halfHeight = 4 #FIXME
		for zStr, label in pointsOfInterestLabels.items():
			z = float(zStr)
			plt.annotate(label, xy=(z, 0.0), xytext=(z, halfHeight*1.1), xycoords='data', ha='center', va='bottom')

		(apertureStopPosition, apertureStopDiameter) = self.apertureStop()
		if apertureStopPosition != None:
			plt.annotate('AS', xy=(apertureStopPosition, 0.0), xytext=(apertureStopPosition, halfHeight*1.1), xycoords='data', ha='center', va='bottom')		

		(fieldStopPosition, fieldStopDiameter) = self.fieldStop()
		if fieldStopPosition != None:
			plt.annotate('FS', xy=(fieldStopPosition, 0.0), xytext=(fieldStopPosition, halfHeight*1.1), xycoords='data', ha='center', va='bottom')		

	def drawOpticalElements(self, axes):		
		z = 0
		for element in self.elements:
			element.drawAt(z, axes)

			if self.showElementLabels:
				element.drawLabels(z,axes)
			z += element.L

	def drawRayTraces(self, axes, removeBlockedRaysCompletely=True):
		color = ['b','r','g']

		if self.fieldOfView() == float('+Inf'):
			halfAngle = self.fanAngle/2.0
			halfHeight = self.objectHeight/2.0
			rayGroup = Ray.fanGroup(yMin=-halfHeight, yMax=halfHeight, M=self.rayNumber,radianMin=-halfAngle, radianMax=halfAngle, N=self.fanNumber)
		else:
			halfHeight = self.objectHeight/2.0
			chiefRay = self.chiefRay(y=halfHeight-0.01)
			print(chiefRay)
			(marginalUp, marginalDown) = self.marginalRays(y=0)
			rayGroup = (chiefRay, marginalUp)

		rayGroupSequence = self.propagateMany(rayGroup)

		for raySequence in rayGroupSequence:
			(x,y) = self.rearrangeRaysForPlotting(raySequence, removeBlockedRaysCompletely)
			if len(y) == 0:
				continue # nothing to plot, ray was fully blocked

			rayInitialHeight = y[0]
			binSize = 2.0*halfHeight/(len(color)-1)
			colorIndex = int((rayInitialHeight-(-halfHeight-binSize/2))/binSize)
			axes.plot(x, y, color[colorIndex], linewidth=0.4)

	def rearrangeRaysForPlotting(self, rayList, removeBlockedRaysCompletely=True):
		x = []
		y = []
		for ray in rayList:
			if not ray.isBlocked:
				x.append(ray.z)
				y.append(ray.y)
			elif removeBlockedRaysCompletely:
				x = []
				y = []
			# else: # ray will simply stop drawing from here			
		return (x,y)


# This is an example for the module.
# Don't modify this: create a new script that imports ABCD
# See test.py
if __name__ == "__main__":
	path = OpticalPath()
	path.name = "Simple demo: one infinite lens f = 5cm"
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=10))
	path.display()
	# or 
	#path.save("Figure 1.png")

	path = OpticalPath()
	path.name = "Simple demo: two infinite lenses with f = 5cm"
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=20))
	path.append(Lens(f=5))
	path.append(Space(d=10))
	path.display()
	# or 
	# path.save("Figure 2.png")

	path = OpticalPath()
	path.name = "Advanced demo: two lenses f = 5cm, with a finite diameter of 2.5 cm"
	path.append(Space(d=10))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=20))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=10))
	path.display()
	# or 
	# path.save("Figure 3.png")

	path = OpticalPath()
	path.name = "Microscope system"
	path.objectHeight = 0.1
	path.append(Space(d=4))
	path.append(Lens(f=4, diameter=0.8, label='Obj'))
	path.append(Space(d=4+18))
	path.append(Lens(f=18,diameter=5.0, label='Tube Lens'))
	path.append(Space(d=18))
	path.display()
	(r1,r2) = path.marginalRays(y=0)
	print(r1, r2)
	# or 
	# path.save("Figure 4.png")

	path = OpticalPath()
	path.name = "Advanced demo: two lenses with aperture"
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=2))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=2))
	path.append(Aperture(diameter=2.0))
	(r1,r2) = path.marginalRays(y=0)
	print(r1, r2)
	print(path.fieldOfView())
	path.display()
