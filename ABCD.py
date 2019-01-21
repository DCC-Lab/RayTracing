import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Ray:
	y = 0
	theta = 0
	z = 0
	isBlocked = False

	def __init__(self, y=0, theta=0, z=0, isBlocked=False):	
		self.y = y
		self.theta = theta
		self.z = z
		self.isBlocked = isBlocked
	
	@classmethod
	def fan(self, y, minRadian, maxRadian, N):
		rays = []
		for i in range(N):
			theta = minRadian + i*(maxRadian-minRadian)/(N-1)
			rays.append(Ray(y,theta,0))

		return rays


class Matrix(object):
	A = 1
	B = 0
	C = 0
	D = 1

	L = 0 # Physical length
	apertureDiameter = float('+Inf') 

	def __init__(self, A, B, C, D, physicalLength, apertureDiameter=float('+Inf')):	
		self.A = float(A)
		self.B = float(B)
		self.C = float(C)
		self.D = float(D)
		self.L = float(physicalLength)
		self.apertureDiameter = apertureDiameter
		
		super(Matrix, self).__init__()		

	def __mul__(self, rightSide):
		if isinstance(rightSide, Matrix):
			return self.mul_matrix(rightSide)
		elif isinstance(rightSide, Ray):
			return self.mul_ray(rightSide)
		else:
			print "Unrecongnized right side element in multiply: ", rightSide			

	def mul_matrix(self, rightSideMatrix):
		a = self.A * rightSideMatrix.A + self.B * rightSideMatrix.C
		b = self.A * rightSideMatrix.B + self.B * rightSideMatrix.D
		c = self.C * rightSideMatrix.A + self.D * rightSideMatrix.C
		d = self.C * rightSideMatrix.B + self.D * rightSideMatrix.D
		l = self.L + rightSideMatrix.L

		return Matrix(a,b,c,d,physicalLength=l)

	def mul_ray(self, rightSideRay):
		outputRay = Ray()

		outputRay.y = self.A * rightSideRay.y + self.B * rightSideRay.theta
		outputRay.theta = self.C * rightSideRay.y + self.D * rightSideRay.theta
		outputRay.z = self.L + rightSideRay.z

		if rightSideRay.y > self.apertureDiameter/2 or rightSideRay.y < -self.apertureDiameter/2:			
			outputRay.isBlocked = True
		else:
			outputRay.isBlocked = rightSideRay.isBlocked		

		return outputRay

	def drawAt(self, z, axes):
		return


class Lens(Matrix):
	def __init__(self, f, diameter=float('+Inf')):	
		super(Lens, self).__init__(A=1, B=0, C=-1/float(f),D=1, physicalLength=0, apertureDiameter=diameter)

	def drawAt(self, z, axes):
		lensHalfHeight = 4
		if not np.isinf(self.apertureDiameter):
			lensHalfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, lensHalfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.5,length_includes_head=True)
		plt.arrow(z, 0, 0, -lensHalfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.5, length_includes_head=True)

class Space(Matrix):
	def __init__(self, d):	
		super(Space, self).__init__(A=1, B=float(d), C=0,D=1, physicalLength=d)

class OpticalPath(object):
	def __init__(self):
		self.elements = []
		self.objectHeight = 1
		self.objectPosition = 0 # always at z=0 for now
		self.fanNumber = 20
		self.name = "Ray tracing"

	def physicalLength(self):
		z = 0
		for element in self.elements:
			z += element.L
		return z

	def append(self, matrix):
		self.elements.append(matrix)

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

	def display(self):
		fig, axes = plt.subplots()
		axes.set(xlabel='Distance', ylabel='Height', title=self.name)
		self.drawRayTraces(axes)
		self.drawObject(axes)
		self.drawOpticalElements(axes)
		plt.ioff()
		plt.show()

	def drawObject(self, axes):
		plt.arrow(self.objectPosition, 0, 0, self.objectHeight, width=0.2, fc='b', ec='b',head_length=0.25, head_width=0.5,length_includes_head=True)

	def drawOpticalElements(self, axes):		
		z = 0
		for element in self.elements:
			element.drawAt(z, axes)
			z += element.L

	def drawRayTraces(self, axes):
		rayFan = Ray.fan(y=self.objectHeight,minRadian=-0.25, maxRadian=0.25, N=self.fanNumber)
		rayFanSequence = self.propagateMany(rayFan)

		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForDisplay(raySequence)
			axes.plot(x, y,'b', linewidth=0.4)

		rayFan = Ray.fan(y=0,minRadian=-0.25, maxRadian=0.25, N=self.fanNumber)
		rayFanSequence = self.propagateMany(rayFan)

		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForDisplay(raySequence)
			axes.plot(x, y,'r', linewidth=0.4)


	def rearrangeRaysForDisplay(self, rayList, removeBlockedRaysCompletely=True):
		x = []
		y = []
		for ray in rayList:
			if not ray.isBlocked:
				x.append(ray.z)
				y.append(ray.y)
			elif removeBlockedRaysCompletely:
				x = []
				y = []
			
		return (x,y)

if __name__ == "__main__":
	print("")
	path = OpticalPath()
	path.name = "Simple demonstration: one infinite lens"
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=10))
	path.display()

	path = OpticalPath()
	path.name = "Simple demonstration: two infinite lenses"
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=20))
	path.append(Lens(f=5))
	path.append(Space(d=10))
	path.display()

	path = OpticalPath()
	path.name = "Demonstration: two 1-inch lenses"
	path.objectHeight = 0.5
	path.append(Space(d=10))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=20))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=10))
	path.display()