import matplotlib.pyplot as plt

class Ray:
	def __init__(self, y=0, theta=0, z=0, isBlocked=False):	
		# Ray matrix formalism
		self.y = y
		self.theta = theta

		# Position of this ray
		self.z = z

		# Aperture
		self.isBlocked = isBlocked
	
	@classmethod
	def fan(self, y, radianMin, radianMax, N):
		rays = []
		for i in range(N):
			theta = radianMin + i*(radianMax-radianMin)/(N-1)
			rays.append(Ray(y,theta,0))

		return rays

	@classmethod
	def fanGroup(self, yMin, yMax, M, radianMin, radianMax, N):
		rays = []
		for j in range(M):
			for i in range(N):
				theta = radianMin + i*(radianMax-radianMin)/(N-1)
				y = yMin + j*(yMax-yMin)/(M-1)
				rays.append(Ray(y,theta,0))
		return rays



class Matrix(object):
	def __init__(self, A, B, C, D, physicalLength, apertureDiameter=float('+Inf')):	
		# Ray matrix formalism
		self.A = float(A)
		self.B = float(B)
		self.C = float(C)
		self.D = float(D)

		# Length of this element
		self.L = float(physicalLength)

		# Aperture
		self.apertureDiameter = apertureDiameter
		
		super(Matrix, self).__init__()		

	def __mul__(self, rightSide):
		if isinstance(rightSide, Matrix):
			return self.mul_matrix(rightSide)
		elif isinstance(rightSide, Ray):
			return self.mul_ray(rightSide)
		else:
			print("Unrecognized right side element in multiply: ", rightSide)			

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
		self.fanNumber = 10       # number of rays in fan
		self.rayNumber = 6        # number of rays from different height on object

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

	def save(self, filepath):
		fig, axes = plt.subplots(figsize=(10, 7))
		axes.set(xlabel='Distance', ylabel='Height', title=self.name, aspect='equal')
		axes.set_ylim([-5,5]) # FIXME: obtain limits from plot.  Currently 5cm either side
		self.drawRayTraces(axes)
		self.drawObject(axes)
		self.drawOpticalElements(axes)
		fig.savefig(filepath,dpi=600)

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

		rayFan = Ray.fanGroup(yMin=-halfHeight, yMax=halfHeight, M=self.rayNumber,radianMin=-halfAngle, radianMax=halfAngle, N=self.fanNumber)
		rayFanSequence = self.propagateMany(rayFan)

		for raySequence in rayFanSequence:
			(x,y) = self.rearrangeRaysForPlotting(raySequence)
			if len(y) == 0:
				continue # nothing to plot, ray was fully blocked

			rayInitialHeight = y[0]
			binSize = self.objectHeight/(len(color)-1)
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
	path.objectHeight = 2
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
	path.objectHeight = 0.5
	path.append(Space(d=10))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=20))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=10))
	path.display()
	# or 
	# path.save("Figure 3.png")

	path = OpticalPath()
	path.name = "Advanced demo: two lenses with aperture"
	path.objectHeight = 0.5
	path.append(Space(d=10))
	path.append(Lens(f=5))
	path.append(Space(d=2))
	path.append(Aperture(diameter=3))
	path.append(Space(d=18))
	path.append(Lens(f=5, diameter=2.5))
	path.append(Space(d=10))
	path.display()
	# or 
	# path.save("Figure 4.png")