import matplotlib.pyplot as plt

class Ray:
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

	@classmethod
	def fanGroup(self, yMin, yMax, M, minRadian, maxRadian, N):
		rays = []
		for j in range(M):
			for i in range(N):
				theta = minRadian + i*(maxRadian-minRadian)/(N-1)
				y = yMin + j*(yMax-yMin)/(M-1)
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
			print "Unrecognized right side element in multiply: ", rightSide			

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

		if abs(rightSideRay.y) > self.apertureDiameter/2:			
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
		halfHeight = 4
		if self.apertureDiameter != float('Inf'):
			halfHeight = self.apertureDiameter/2

		plt.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25,length_includes_head=True)
		plt.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',head_length=0.25, head_width=0.25, length_includes_head=True)

class Space(Matrix):
	def __init__(self, d):	
		super(Space, self).__init__(A=1, B=float(d), C=0,D=1, physicalLength=d)

class Aperture(Matrix):
	def __init__(self, diameter):	
		super(Aperture, self).__init__(A=1, B=0, C=0,D=1, physicalLength=0, apertureDiameter=diameter)
	def drawAt(self, z, axes):
		halfHeight = self.apertureDiameter/2

		plt.arrow(z, halfHeight+1, 0,-1, width=0.1, fc='k', ec='k',head_length=0.05, head_width=1,length_includes_head=True)
		plt.arrow(z, -halfHeight-1, 0, 1, width=0.1, fc='k', ec='k',head_length=0.05, head_width=1, length_includes_head=True)


class OpticalPath(object):
	def __init__(self):
		self.name = "Ray tracing"
		self.elements = []
		self.objectHeight = 1.0   # object height (full). FIXME: Python 2.7 requires 1.0, not 1 (float)
		self.objectPosition = 0.0 # always at z=0 for now. FIXME: Python 2.7 requires 1.0, not 1 (float)
		self.fanAngle = 0.5       # full fan angle for rays
		self.fanNumber = 10        # number of rays in fan
		self.rayNumber = 3        # number of rays in height

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
		fig, axes = plt.subplots(figsize=(10, 7))
		axes.set(xlabel='Distance', ylabel='Height', title=self.name, aspect='equal')
		axes.set_ylim([-5,5]) # FIXME: obtain limits from plot.  Currently 5cm either side
		self.drawRayTraces(axes)
		self.drawObject(axes)
		self.drawOpticalElements(axes)
		plt.ioff()
		plt.show()
		fig.savefig(self.name + ".png")

	def drawObject(self, axes):
		plt.arrow(self.objectPosition, -self.objectHeight/2, 0, self.objectHeight, width=0.1, fc='b', ec='b',head_length=0.25, head_width=0.25,length_includes_head=True)

	def drawOpticalElements(self, axes):		
		z = 0
		for element in self.elements:
			element.drawAt(z, axes)
			z += element.L

	def drawRayTraces(self, axes):
		color = ['b','r','g']

		halfHeight = self.objectHeight/2
		halfAngle = self.fanAngle/2

		rayFan = Ray.fanGroup(yMin=-halfHeight, yMax=halfHeight, M=self.rayNumber,minRadian=-halfAngle, maxRadian=halfAngle, N=self.fanNumber)
		rayFanSequence = self.propagateMany(rayFan)

		lastHeight = float('+Inf')
		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForDisplay(raySequence)
			if len(y) == 0:
				continue # nothing to plot, ray was fully blocked

			rayInitialHeight = y[0]
			binSize = self.objectHeight/(len(color)-1)
			colorIndex = int((rayInitialHeight-(-halfHeight-binSize/2))/binSize)
			axes.plot(x, y, color[colorIndex], linewidth=0.4)


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
			# else: # ray will simply stop drawing from here
			
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

	path = OpticalPath()
	path.name = "Demonstration: two lenses with aperture"
	path.objectHeight = 0.5
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=2))
	path.append(Aperture(diameter=3))
	path.append(Space(d=18))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=10))
	path.display()