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


class Matrix(object):
	A = 1
	B = 0
	C = 0
	D = 1
	L = 0

	def __init__(self, A, B, C, D, physicalLength):	
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.L = physicalLength

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
		super(Lens, self).__init__(A=1, B=0, C=-1/f,D=1, physicalLength=0)

class Space(Matrix):
	def __init__(self, d):	
		super(Space, self).__init__(A=1, B=d, C=0,D=1, physicalLength=d)

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


def rearrangeRays(rayList):
	x = []
	y = []
	for ray in rayList:
		x.append(ray.z)
		y.append(ray.y)
	return (x,y)


M1 = Matrix(1,1,0,1, 1)
M2 = Matrix(1,2,0,1, 2)
M3 = M2*M1
L = Lens(10)

path = OpticalPath()
path.append(M1)
path.append(L)
path.append(M3)
path.append(Space(10))


r = Ray(y=1,theta=0.5,z=0)

rays = path.propagate(r)
for ray in rays:
	print(ray.z, ray.y)
(x,y) = rearrangeRays(rays)


print(M3.A)
print(M3.B)
print(M3.C)
print(M3.D)

rp = M3*r

print(rp.y)
print(rp.theta)

# # Data for plotting
# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set(xlabel='Distance', ylabel='Rayon',
       title='Trace de rayons')
ax.grid()

fig.savefig("test.png")
plt.show()
