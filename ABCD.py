import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Ray:
	y = 0
	theta = 0
	z = 0

	def __init__(self, y, theta, z):	
		self.y = y
		self.theta = theta
		self.z = z
	
	@classmethod
	def rayFan(self, y, minRadian, maxRadian, N):
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

	L = 0

	def __init__(self, A, B, C, D, physicalLength):	
		self.A = float(A)
		self.B = float(B)
		self.C = float(C)
		self.D = float(D)
		self.L = float(physicalLength)

		super(Matrix, self).__init__()		

	def __mul__(self, rightSide):
		if isinstance(rightSide, Matrix):
			return self.mul_matrix(rightSide)
		elif isinstance(rightSide, Ray):
			return self.mul_ray(rightSide)
		else:
			print "Error"			

	def mul_matrix(self, rightSideMatrix):
		a = self.A * rightSideMatrix.A + self.B * rightSideMatrix.C
		b = self.A * rightSideMatrix.B + self.B * rightSideMatrix.D
		c = self.C * rightSideMatrix.A + self.D * rightSideMatrix.C
		d = self.C * rightSideMatrix.B + self.D * rightSideMatrix.D

		l = self.L + rightSideMatrix.L

		return Matrix(a,b,c,d,physicalLength=l)

	def mul_ray(self, rightSideRay):
		y = self.A * rightSideRay.y + self.B * rightSideRay.theta
		theta = self.C * rightSideRay.y + self.D * rightSideRay.theta

		z = self.L + rightSideRay.z

		return Ray(y, theta, z)

class Lens(Matrix):
	def __init__(self, f):	
		super(Lens, self).__init__(A=1, B=0, C=-1/float(f),D=1, physicalLength=0)

class Space(Matrix):
	def __init__(self, d):	
		super(Space, self).__init__(A=1, B=float(d), C=0,D=1, physicalLength=d)

class OpticalPath(object):
	def __init__(self):
		self.elements = []

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
		fig, ax = plt.subplots()
		ax.set(xlabel='Distance', ylabel='Rayon', title='Trace de rayons')
		ax.grid()

		rayFan1 = Ray.rayFan(y=1,minRadian=-0.25, maxRadian=0.25, N=5)
		rayFanSequence = path.propagateMany(rayFan1)

		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForDisplay(raySequence)
			ax.plot(x, y,'b')

		rayFan2 = Ray.rayFan(y=0,minRadian=-0.25, maxRadian=0.25, N=5)
		rayFanSequence = path.propagateMany(rayFan2)

		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForDisplay(raySequence)
			ax.plot(x, y,'r')


		plt.show()


	def rearrangeRaysForDisplay(self, rayList):
		x = []
		y = []
		for ray in rayList:
			x.append(ray.z)
			y.append(ray.y)
		return (x,y)

path = OpticalPath()
path.append(Space(10))
path.append(Lens(10))
path.append(Space(10))
path.display()