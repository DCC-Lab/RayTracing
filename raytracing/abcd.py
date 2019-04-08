import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms
import math
import sys

if sys.version_info[0] < 3:
    print("Warning: you should really be using Python 3. \
        No guarantee this will work in 2.x")

"""A simple module for ray tracing with ABCD matrices.
https://github.com/DCC-Lab/RayTracing

Create an ImagingPath(), append matrices (optical elements or other
group of elements), and then display(). This helps determine of
course simple things like focal length of compound systems,
object-image, etc... but also the aperture stop, field stop, field
of view and any clipping issues that may occur.

When displaying the result with an ImagingPath(), the  objectHeight,
fanAngle, and fanNumber are used if the field of view is not
defined. You may adjust the values to suit your needs in ImagingPath().

The class hierarchy can be seen on http://webgraphviz.com with the
following description:

digraph G {

    subgraph mathview {
        "Matrix" -> "MatrixGroup"
        "MatrixGroup" -> ImagingPath
    }

    subgraph opticsview {
        "Element" -> "Group"
        "Group" -> ImagingPath
    }
}

To use the package, either:
1) pip install raytracing
or
2) copy to the raytracing package to the directory where you want to use it
or
3) python setup.py install from the source code directory
"""


""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0/math.pi
radPerDeg = math.pi/180.0


class Ray:
    """A vector and a light ray as transformed by ABCD matrices

    The Ray() has a height (y) and an angle with the optical axis (theta).
    It also has a position (z), the diameter of the aperture at that point
    when it propagated through, and a marker if it has been blocked by the
    aperture.

    Simple static functions are defined to obtain a group of rays: fans
    originate from the same height but sweep a range of angles; fan groups
    are fans originating from different heights.
    """

    def __init__(self, y=0, theta=0, z=0, isBlocked=False):
        # Ray matrix formalism
        self.y = y
        self.theta = theta

        # Position of this ray and the diameter of the aperture at that 
        # position
        self.z = z
        self.apertureDiameter = float("+Inf")
        self.isBlocked = isBlocked

    @property
    def isNotBlocked(self):
        """Opposite of isBlocked.  Convenience function for readability

        """

        return not self.isBlocked

    @staticmethod
    def fan(y, radianMin, radianMax, N):
        """A list of rays spanning from radianMin to radianMax to be used
        with Matrix.trace() or Matrix.traceMany()

        """
        if N >= 2:
            deltaRadian = float(radianMax - radianMin) / (N - 1)
        elif N == 1:
            deltaRadian = 0.0
        else:
            raise ValueError("N must be 1 or larger.")

        rays = []
        for i in range(N):
            theta = radianMin + float(i) * deltaRadian
            rays.append(Ray(y, theta, z=0))

        return rays

    @staticmethod
    def fanGroup(yMin, yMax, M, radianMin, radianMax, N):
        """ A list of rays spanning from yMin to yMax and radianMin to
        radianMax to be used with Matrix.trace() or Matrix.traceMany()
        """
        if N >= 2:
            deltaRadian = float(radianMax - radianMin) / (N - 1)
        elif N == 1:
            deltaRadian = 0.0
        else:
            raise ValueError("N must be 1 or larger.")

        if M >= 2:
            deltaHeight = float(yMax - yMin) / (M - 1)
        elif M == 1:
            deltaHeight = 0.0
        else:
            raise ValueError("M must be 1 or larger.")

        rays = []
        for j in range(M):
            for i in range(N):
                theta = radianMin + float(i) * deltaRadian
                y = yMin + float(j) * deltaHeight
                rays.append(Ray(y, theta, z=0))

        return rays

    def __str__(self):
        """ String description that allows the use of print(Ray()) """

        description = "\n /       \\ \n"
        description += "| {0:6.3f}  |\n".format(self.y)
        description += "|         |\n"
        description += "| {0:6.3f}  |\n".format(self.theta)
        description += " \\       /\n\n"

        description += "z = {0:4.3f}\n".format(self.z)
        if self.isBlocked:
            description += " (blocked)"

        return description

class GaussianBeam(object):
    """A gaussian laser beam using the ABCD formalism for propagation

    w is the 1/e beam size in electric field.
    R is the radius of curvature (positive means diverging)
    n is index in which the beam is. Necessary to compute beam size
    wavelength is in the same units
    """

    def __init__(self, w=None, R=float("+Inf"), n=1.0, wavelength=632.8e-6, z=0):
        # Gaussian beam matrix formalism
        if w is not None:
            self.q = 1/( 1.0/R - complex(0,1)*wavelength/n/(math.pi*w*w))
        else:
            self.q = None 

        self.wavelength = wavelength
        self.z = z
        self.n = n
        self.isClipped = False

    @property
    def R(self):
        invQReal = (1/self.q).real
        if invQReal == 0:
            return float("+Inf")

        return 1/invQReal

    @property
    def w(self):
        return math.sqrt( self.wavelength/self.n/(math.pi * (-1/self.q).imag))

    @property
    def wo(self):
        return math.sqrt( self.zo * self.wavelength/math.pi )

    @property
    def waist(self):
        return self.wo

    @property
    def waistPosition(self):
        return -self.q.real

    @property
    def zo(self):
        return self.q.imag

    @property
    def confocalParameter(self):
        return self.zo

    @property
    def rayleighRange(self):
        return self.zo

    def __str__(self):
        """ String description that allows the use of print(Ray()) """
        description = "Complex radius: {0:.3}\n".format(self.q)
        description += "z: {0:.3f}, ".format(self.z)
        description += "w(z): {0:.3f}, ".format(self.w)
        description += "R(z): {0:.3f}, ".format(self.R)
        description += "λ: {0:.1f} nm\n".format(self.wavelength*1e6)
        description += "zo: {0:.3f}, ".format(self.zo)
        description += "wo: {0:.3f}, ".format(self.wo)
        description += "wo position: {0:.3f} ".format(self.waistPosition)
        return description

class Matrix(object):
    """A matrix and an optical element that can transform a ray or another
    matrix.

    The general properties (A,B,C,D) are defined here. The operator "*" is
    overloaded to allow simple statements such as:

    ray2 = M1 * ray
    or
    M3 = M2 * M1

    The physical length is included in the matrix to allow simple management of
    the ray tracing. IF two matrices are multiplied, the resulting matrice
    will have a physical length that is the sum of both matrices.

    In addition finite apertures are considered: if the apertureDiameter
    is not infinite (default), then the object is assumed to limit the
    ray height to plus or minus apertureDiameter/2 from the front edge to the back
    edge of the element.
    """

    __epsilon__ = 1e-5  # Anything smaller is zero

    def __init__(
            self,
            A:float=1,
            B:float=0,
            C:float=0,
            D:float=1,
            physicalLength:float=0,
            frontVertex=None,
            backVertex=None,
            frontIndex=1.0,
            backIndex=1.0,
            apertureDiameter=float('+Inf'),
            label=''
            ):
        # Ray matrix formalism
        self.A = float(A)
        self.B = float(B)
        self.C = float(C)
        self.D = float(D)

        # Length of this element
        self.L = float(physicalLength)
        # Aperture
        self.apertureDiameter = apertureDiameter

        # First and last interfaces. Used for BFL and FFL
        self.frontVertex = frontVertex
        self.backVertex = backVertex

        # Index of refraction at entrance and exit.
        self.frontIndex = frontIndex
        self.backIndex = backIndex

        self.label = label
        self.isFlipped = False
        super(Matrix, self).__init__()

    @property
    def determinant(self):
        return self.A*self.D - self.B*self.C

    def __mul__(self, rightSide):
        """Operator overloading allowing easy to read matrix multiplication

        For instance, with M1 = Matrix() and M2 = Matrix(), one can write
        M3 = M1*M2. With r = Ray(), one can apply the M1 transform to a ray
        with r = M1*r

        """
        if isinstance(rightSide, Matrix):
            return self.mul_matrix(rightSide)
        elif isinstance(rightSide, Ray):
            return self.mul_ray(rightSide)
        elif isinstance(rightSide, GaussianBeam):
            return self.mul_beam(rightSide)
        else:
            raise TypeError(
                "Unrecognized right side element in multiply: '{0}'\
                 cannot be multiplied by a Matrix".format(rightSide))

    def mul_matrix(self, rightSideMatrix):
        """ Multiplication of two matrices.  Total length of the
        elements is calculated. Apertures are lost. We compute
        the first and last vertices.

        """

        a = self.A * rightSideMatrix.A + self.B * rightSideMatrix.C
        b = self.A * rightSideMatrix.B + self.B * rightSideMatrix.D
        c = self.C * rightSideMatrix.A + self.D * rightSideMatrix.C
        d = self.C * rightSideMatrix.B + self.D * rightSideMatrix.D
        L = self.L + rightSideMatrix.L

        # The front vertex of the combination is the front vertex
        # of the rightSideMatrix (occuring first) if the vertex exists.
        # If it does not, it will be the front vertex of the self element.
        # If neither element has a front vertex, then the combination has no
        # front vertex. This occurs when we have Space()*Space().

        # The back vertex of the combination is the back vertex of the self
        # element, occuring last, if it exists. If it does not, it is the
        # back vertex of the rightSideMatrix (which may or may not exist).
        # Vertices are measured with respect to the front edge of the
        # combined element.

        fv = rightSideMatrix.frontVertex
        if fv is None and self.frontVertex is not None:
            fv = rightSideMatrix.L + self.frontVertex

        if self.backVertex is not None:
            bv = rightSideMatrix.L + self.backVertex
        else:
            bv = rightSideMatrix.backVertex

        return Matrix(a, b, c, d, frontVertex=fv, backVertex=bv, physicalLength=L)

    def mul_ray(self, rightSideRay):
        """ Multiplication of a ray by a matrix.  New position of
        ray is updated by the physical length of the matrix.
        If the ray is beyond the aperture diameter it is labelled
        as "isBlocked = True" but can still propagate.

        """

        outputRay = Ray()
        outputRay.y = self.A * rightSideRay.y + self.B * rightSideRay.theta
        outputRay.theta = self.C * rightSideRay.y + self.D * rightSideRay.theta

        outputRay.z = self.L + rightSideRay.z
        outputRay.apertureDiameter = self.apertureDiameter

        if abs(outputRay.y) > abs(self.apertureDiameter / 2.0):
            outputRay.isBlocked = True
        else:
            outputRay.isBlocked = rightSideRay.isBlocked

        return outputRay

    def mul_beam(self, rightSideBeam):
        """ Multiplication of a coherent beam with complex radius
        of curvature q by a matrix.

        """
        q = rightSideBeam.q
        if rightSideBeam.n != self.frontIndex:
            print("Warning: the gaussian beam is not tracking the index of refraction properly")

        outputBeam = GaussianBeam(wavelength=rightSideBeam.wavelength)
        outputBeam.q = (self.A * q + self.B ) / (self.C*q + self.D)
        outputBeam.z = self.L + rightSideBeam.z
        outputBeam.n = self.backIndex

        if abs(outputBeam.w) > self.apertureDiameter / 2:
            outputBeam.isClipped = True
        else:
            outputBeam.isClipped = rightSideBeam.isClipped

        return outputBeam

    def largestDiameter(self):
        """ Largest diameter of the element or group of elements """
        return self.apertureDiameter

    def hasFiniteApertureDiameter(self):
        """ True if the element or group of elements have a finite aperture size """
        return self.apertureDiameter != float("+Inf")

    def transferMatrix(self, upTo=float('+Inf')):
        """ The Matrix() that corresponds to propagation from the edge
        of the element (z=0) up to distance "upTo" (z=upTo). If no parameter is 
        provided, the transfer matrix will be from the front edge to the back edge.
        If the element has a null thickness, the matrix representing the element
        is returned.
        """

        distance = upTo
        if self.L == 0:
            return self
        elif self.L <= distance:
            return self
        else:
            raise TypeError("Subclass of non-null physical length must override transferMatrix()")

    def transferMatrices(self):
        """ The list of Matrix() that corresponds to the propagation through 
        this element (or group). For a Matrix(), it simply returns a list 
        with a single element [self].
        For a MatrixGroup(), it returns the transferMatrices for 
        each individual element and appends each element to a list for this group."""

        return [self]

    def trace(self, ray):
        """Returns a list of rays (i.e. a ray trace) for the input ray through the matrix.
        
        Because we want to manage blockage by apertures, we need to perform a two-step process
        for elements that have a finite, non-null length: where is the ray blocked exactly?
        It can be blocked at the entrance, at the exit, or anywhere in between.
        The aperture diameter for a finite-length element is constant across the length
        of the element. We therefore check before entering the element and after having
        propagated through the element. For now, this will suffice.
        If the length is null, the ray is traced in a single step
        """

        rayTrace = []
        if isinstance(ray, Ray):
            if self.L > 0:
                if abs(ray.y) > self.apertureDiameter / 2:
                    ray.isBlocked = True
                rayTrace.append(ray)

        rayTrace.append(self*ray)

        return rayTrace

    def traceMany(self, inputRays):
        """ Trace each ray from a list from front edge of element to
        the back edge.

        Returns a list of ray traces for each input ray.
        See trace().
        """
        manyRayTraces = []
        for inputRay in inputRays:
            rayTrace = self.trace(inputRay)
            manyRayTraces.append(rayTrace)
        return manyRayTraces

    @property
    def isImaging(self):
        """If B=0, then the matrix is from a conjugate plane to another
        (i.e. object at the front edge and image at the back edge).

        In this case, A = transverse magnification, D = angular magnification
        As usual, C = -1/f (always).
        """

        return abs(self.B) < Matrix.__epsilon__

    @property
    def hasPower(self):
        return self.C != 0
    
    def pointsOfInterest(self, z):
        """ Any points of interest for this matrix (focal points,
        principal planes etc...)
        """

        # ptsOfInterest = []
        # if self.frontVertex is not None:
        #     ptsOfInterest.append({'z': self.frontVertex, 'label': '$V_f$'})
        # if self.backVertex is not None:
        #     ptsOfInterest.append({'z': self.backVertex, 'label': '$V_b$'})
        
        return []

    def focalDistances(self):
        """ Synonym of effectiveFocalLengths() """

        return self.effectiveFocalLengths()

    def effectiveFocalLengths(self):
        """ The effective focal lengths calculated from the power (C)
        of the matrix.

        Currently, it is assumed the index is n=1 on either side and
        both focal lengths are the same.
        """
        if self.hasPower:
            focalLength = -1.0 / self.C  # FIXME: Assumes n=1 on either side
        else:
            focalLength = float("+Inf")

        return (focalLength, focalLength)

    def backFocalLength(self):
        """ The focal lengths measured from the back vertex.
        This is the distance between the surface and the focal point.
        When the principal plane is not at the surface (which is usually
        the case in anything except a thin lens), the back and front focal
        lengths will be different from effective focal lengths. The effective
        focal lengths is always measured from the principal planes, but the
        BFL and FFL are measured from the vertex.

        If the matrix is the result of the product of several matrices,
        we may not know where the front and back vertices are. In that case,
        we return None (or undefined).

        Currently, it is assumed the index is n=1 on either side and
        both focal distances are the same.
        """

        if self.backVertex is not None and self.hasPower:
            (f1, f2) = self.effectiveFocalLengths()
            (p1, p2) = self.principalPlanePositions(z=0)

            return (p2 + f2 - self.backVertex)
        else:
            return None

    def frontFocalLength(self):
        """ The focal lengths measured from the front vertex.
        This is the distance between the surface and the focal point.
        When the principal plane is not at the surface (which is usually
        the case in anything except a thin lens), the back and front focal
        lengths will be different from effective focal lengths. The effective
        focal lengths is always measured from the principal planes, but the
        BFL and FFL are measured from the vertices.

        If the matrix is the result of the product of several matrices,
        we may not know where the front and back vertices are. In that case,
        we return None (or undefined).
        
        Currently, it is assumed the index is n=1 on either side and
        both focal distances are the same.
        """

        if self.frontVertex is not None and self.hasPower:
            (f1, f2) = self.effectiveFocalLengths()
            (p1, p2) = self.principalPlanePositions(z=0)

            return -(p1 - f1 - self.frontVertex)
        else:
            return None


    def focusPositions(self, z):
        """ Positions of both focal points on either side of the element.

        Currently, it is assumed the index is n=1 on either side and both focal
        distances are the same.
        """
        if self.hasPower:
            (f1, f2) = self.focalDistances()
            (p1, p2) = self.principalPlanePositions(z)
            return (p1 - f1, p2 + f2)
        else:
            return (None, None)

    def principalPlanePositions(self, z):
        """ Positions of the input and output principal planes.

        Currently, it is assumed the index is n=1 on either side.
        """
        if self.hasPower:
            p1 = z - (1 - self.D) / self.C  # FIXME: Assumes n=1 on either side
            # FIXME: Assumes n=1 on either side
            p2 = z + self.L + (1 - self.A) / self.C
        else:
            p1 = None
            p2 = None

        return (p1, p2)

    def forwardConjugate(self):
        """ With an object at the front edge of the element, where
        is the image? Distance after the element by which a ray
        must travel to reach the conjugate plane of the front of
        the element. A positive distance means the image is "distance"
        beyond the back of the element (or to the right, or after).

        M2 = Space(distance)*M1
        # M2.isImaging == True

        """

        if self.D == 0:
            distance = float("+inf")
            conjugateMatrix = None # Unable to compute with inf
        else:
            distance = -self.B / self.D
            conjugateMatrix = Space(d=distance) * self

        return (distance, conjugateMatrix)

    def backwardConjugate(self):
        """ With an image at the back edge of the element,
        where is the object ? Distance before the element by
        which a ray must travel to reach the conjugate plane at
        the back of the element. A positive distance means the
        object is "distance" in front of the element (or to the
        left, or before).

        M2 = M1*Space(distance)
        # M2.isImaging == True

        """
        if self.A == 0:
            return (None, None)
        distance = -self.B / self.A
        conjugateMatrix = self * Space(d=distance)
        return (distance, conjugateMatrix)

    def magnification(self):
        if self.isImaging:
            return (self.A, self.D)
        else:
            return (None, None)

    def flipOrientation(self):
        """ We flip the element around (as in, we turn a lens around front-back).
        This is useful for real elements and for groups. For individual objects,
        it does not do anything because they are the same either way. However,
        subclasses can override this function and act accordingly.
        """
        self.isFlipped = not self.isFlipped
        # First and last interfaces. Used for BFL and FFL
        tempVertex = self.frontVertex
        self.backVertex = tempVertex
        self.frontVertex = self.backVertex

        # Index of refraction at entrance and exit.
        tempIndex = self.frontIndex
        self.frontIndex = self.backIndex
        self.backIndex = self.frontIndex

        return self

    def display(self):
        """ Display this component, without any ray tracing but with 
        all of its cardinal points and planes. If the component has no
        power (i.e. C == 0) this will fail.
        """

        fig, axes = plt.subplots(figsize=(10, 7))
        displayRange = 2 * self.largestDiameter()
        if displayRange == float('+Inf'):
            displayRange = self.displayHalfHeight() * 4

        axes.set(xlabel='Distance', ylabel='Height', title="Properties of {0}".format(self.label))
        axes.set_ylim([-displayRange /2 * 1.2, displayRange / 2 * 1.2])

        self.drawAt(z=0, axes=axes)
        self.drawLabels(z=0, axes=axes)
        self.drawCardinalPoints(z=0, axes=axes)
        if self.L != 0:
            self.drawVertices(z=0, axes=axes)
        self.drawPointsOfInterest(z=0, axes=axes)
        self.drawPrincipalPlanes(z=0, axes=axes)

        plt.ioff()
        plt.show()

    def drawAt(self, z, axes, showLabels=False):
        """ Draw element on plot with starting edge at 'z'.

        Default is a black box of appropriate length.
        """
        halfHeight = self.largestDiameter()/2
        if halfHeight == float("+Inf"):
            halfHeight = self.displayHalfHeight()

        p = patches.Rectangle((z, -halfHeight), self.L,
                              2 * halfHeight, color='k', fill=False,
                              transform=axes.transData, clip_on=True)
        axes.add_patch(p)

    def drawVertices(self, z, axes):
        """ Draw vertices of the system """
        axes.plot([z+self.frontVertex, z+self.backVertex], [0, 0], 'ko', markersize=4, color="0.5", linewidth=0.2)
        halfHeight = self.displayHalfHeight()
        axes.text(z+self.frontVertex, 0, '$V_f$',ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)
        axes.text(z+self.backVertex, 0, '$V_b$',ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)

    def drawCardinalPoints(self, z, axes):
        """ Draw the focal points of a thin lens as black dots """
        (f1, f2) = self.focusPositions(z)
        axes.plot([f1, f2], [0, 0], 'ko', markersize=4, color='k', linewidth=0.4)

    def drawPrincipalPlanes(self, z, axes):
        """ Draw the principal planes """
        halfHeight = self.displayHalfHeight()
        (p1, p2) = self.principalPlanePositions(z=z)

        axes.plot([p1, p1], [-halfHeight, halfHeight], linestyle='--', color='k', linewidth=1)
        axes.plot([p2, p2], [-halfHeight, halfHeight], linestyle='--', color='k', linewidth=1)
        axes.text(p1, halfHeight*1.2, '$P_f$',ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)
        axes.text(p2, halfHeight*1.2, '$P_b$',ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)


        (f1, f2) = self.effectiveFocalLengths()
        FFL = self.frontFocalLength()
        BFL = self.backFocalLength()
        (F1, F2) = self.focusPositions(z=z)

        h = halfHeight * 0.4
        # Front principal plane to front focal spot (effective focal length)
        axes.annotate("", xy=(p1, h), xytext=(F1, h),
                     xycoords='data', arrowprops=dict(arrowstyle='<->'),
                     clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text(p1-f1/2, h, 'EFL = {0:0.1f}'.format(f1),
            ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)
        # Back principal plane to back focal spot (effective focal length)
        axes.annotate("", xy=(p2, -h), xytext=(F2, -h),
                     xycoords='data', arrowprops=dict(arrowstyle='<->'),
                     clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text(p2+f2/2, -h, 'EFL = {0:0.1f}'.format(f1),
            ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)

        # Front vertex to front focal spot (front focal length or FFL)
        h = 0.5

        axes.annotate("", xy=(self.frontVertex, h), xytext=(F1, h),
                     xycoords='data', arrowprops=dict(arrowstyle='<->'),
                     clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text((self.frontVertex+F1)/2, h, 'FFL = {0:0.1f}'.format(FFL),
            ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)

        # Back vertex to back focal spot (back focal length or BFL)
        axes.annotate("", xy=(self.backVertex, -h), xytext=(F2, -h),
                     xycoords='data', arrowprops=dict(arrowstyle='<->'),
                     clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text((self.backVertex+F2)/2, -h, 'BFL = {0:0.1f}'.format(BFL),
            ha='center', va='bottom',clip_box=axes.bbox, clip_on=True)

    def drawLabels(self, z, axes):
        """ Draw element labels on plot with starting edge at 'z'.

        Labels are drawn 50% above the display height
        """
        if self.hasFiniteApertureDiameter():
            halfHeight = self.largestDiameter()/2.0
        else:
            halfHeight = self.displayHalfHeight()
            
        center = z + self.L / 2.0
        axes.annotate(self.label, xy=(center, 0.0),
                     xytext=(center, halfHeight * 1.5),
                     fontsize=8, xycoords='data', ha='center',
                     va='bottom',clip_box=axes.bbox, clip_on=True)

    def drawPointsOfInterest(self, z, axes):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        """
        labels = {}  # Gather labels at same z
        for pointOfInterest in self.pointsOfInterest(z=z):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label

        halfHeight = self.displayHalfHeight()
        for zStr, label in labels.items():
            z = float(zStr)
            axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                         xycoords='data', fontsize=12,
                         ha='center', va='bottom')

    def drawAperture(self, z, axes):
        """ Draw the aperture size for this element.  Any element may 
        have a finite aperture size, so this function is general for all elements.
        """

        if self.apertureDiameter != float('+Inf'):
            halfHeight = self.apertureDiameter / 2.0

            center = z + self.L/2
            if self.L == 0:
                (xScaling,_) = self.axesToDataScaling(axes)
                width = xScaling*0.01/2
            else:
                width = self.L/2

            axes.add_patch(patches.Polygon(
                           [[center - width, halfHeight],
                            [center + width, halfHeight]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))
            axes.add_patch(patches.Polygon(
                           [[center - width, -halfHeight],
                            [center + width, -halfHeight]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))

    def displayHalfHeight(self):
        """ A reasonable height for display purposes for
        an element, whether it is infinite or not.

        If the element is infinite, currently the half-height
        will be '4'. If not, it is the apertureDiameter/2.

        """
        halfHeight = 4  # FIXME: reasonable half height when infinite
        if self.apertureDiameter != float('+Inf'):
            halfHeight = self.apertureDiameter / 2.0  # real half height
        return halfHeight

    def axesToDataScaling(self, axes):
        """ For drawing properly arrows and other things, sometimes 
        we need to draw along y in real space but in x in relative space 
        (i.e. relative to the width of the graph, not x coordinates).
        There are transforms in matplotlib, but only between axes-display, 
        and data-display, not between data-axes.  Here we obtain the scaling
        so we can set arrow properties intelligently """

        fromDispToData = axes.transData.inverted()
        fromAxesToDisp = axes.transAxes
        scalingFromAxesToData = fromDispToData.transform(fromAxesToDisp.transform([[1,1],[0,0]]))
        xScaling = abs(scalingFromAxesToData[1][0]-scalingFromAxesToData[0][0])
        yScaling = abs(scalingFromAxesToData[1][1]-scalingFromAxesToData[0][1])
        return (xScaling, yScaling)

    def __str__(self):
        """ String description that allows the use of print(Matrix())

        """
        description = "\n /             \\ \n"
        description += "| {0:6.3f}   {1:6.3f} |\n".format(self.A, self.B)
        description += "|               |\n"
        description += "| {0:6.3f}   {1:6.3f} |\n".format(self.C, self.D)
        description += " \\             /\n"
        if self.C != 0:
            description += "\nf={0:0.3f}\n".format(-1.0 / self.C)
        else:
            description += "\nf = +inf (afocal)\n"
        return description


class Lens(Matrix):
    """A thin lens of focal f, null thickness and infinite or finite diameter

    """

    def __init__(self, f, diameter=float('+Inf'), label=''):
        super(Lens, self).__init__(A=1, B=0, C=-1 / float(f), D=1,
                                   physicalLength=0,
                                   apertureDiameter=diameter,
                                   frontVertex=0,
                                   backVertex=0,
                                   label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Draw a thin lens at z """

        halfHeight = self.displayHalfHeight() # real units, i.e. data

        (xScaling, yScaling) = self.axesToDataScaling(axes)
        arrowWidth = xScaling * 0.01
        arrowHeight = yScaling * 0.03
        axes.arrow(z, 0, 0, halfHeight, width=arrowWidth/5, fc='k', ec='k',
                  head_length=arrowHeight, head_width=arrowWidth, length_includes_head=True)
        axes.arrow(z, 0, 0, -halfHeight, width=arrowWidth/5, fc='k', ec='k',
                  head_length=arrowHeight, head_width=arrowWidth, length_includes_head=True)
        self.drawCardinalPoints(z, axes)

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:
        'z':position
        'label':the label to be used.  Can include LaTeX math code.
        """
        (f1, f2) = self.focusPositions(z)

        pointsOfInterest = []
        if f1 is not None:
            pointsOfInterest.append({'z': f1, 'label': '$F_f$'})
        if f2 is not None:
            pointsOfInterest.append({'z': f2, 'label': '$F_b$'})

        return pointsOfInterest


class Space(Matrix):
    """Free space of length d

    """

    def __init__(self, d, n=1, diameter=float('+Inf'), label=''):
        super(Space, self).__init__(A=1,
                                    B=float(d),
                                    C=0,
                                    D=1,
                                    physicalLength=d,
                                    frontVertex=None,
                                    backVertex=None,
                                    frontIndex=n,
                                    backIndex=n, 
                                    apertureDiameter=diameter,
                                    label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Draw nothing because free space is nothing. """
        return

    def transferMatrix(self, upTo=float('+Inf')):
        """ Returns a Matrix() corresponding to a partial propagation
        if the requested distance is smaller than the length of this element"""
        distance = upTo
        if distance < self.L:
            return Space(distance)
        else:
            return self

class DielectricInterface(Matrix):
    """A dielectric interface of radius R, with an index n1 before and n2
    after the interface

    A convex interface from the perspective of the ray has R > 0
    """

    def __init__(self, n1, n2, R=float('+Inf'),
                 diameter=float('+Inf'), label=''):
        self.n1 = n1
        self.n2 = n2
        self.R = R
        a = 1.0
        b = 0.0
        c = - (n2-n1)/(n2*R)
        d = n1/n2

        super(DielectricInterface, self).__init__(A=a, B=b, C=c, D=d,
                                                  physicalLength=0,
                                                  apertureDiameter=diameter,
                                                  frontVertex=0,
                                                  backVertex=0,
                                                  frontIndex=n1,
                                                  backIndex=n2,
                                                  label=label)

    def flipOrientation(self):
        """ We flip the element around (as in, we turn a lens around front-back).
        This is useful for real elements and for groups. For individual objects,
        it does not do anything because they are the same either way. However,
        subclasses can override this function and act accordingly.
        """
        super(DielectricInterface, self).flipOrientation()

        temp = self.n1
        self.n1 = self.n2
        self.n2 = temp
        self.R = -self.R
        self.C = - (self.n2-self.n1)/(self.n2*self.R)
        self.D = self.n1/self.n2
        
        return self


class ThickLens(Matrix):
    """A thick lens of first radius R1 and then R2, with an index n
    and length d

    A biconvex lens has R1 > 0 and R2 < 0.
    """

    def __init__(self, n, R1, R2, thickness, diameter=float('+Inf'), label=''):
        self.R1 = R1
        self.R2 = R2
        self.n = n

        t = thickness

        a = t*(1.0-n)/(n*R1) + 1
        b = t/n
        c = - (n - 1.0)*(1.0/R1 - 1.0/R2 + t*(n-1.0)/(n*R1*R2))
        d = t*(n-1.0)/(n*R2) + 1
        super(ThickLens, self).__init__(A=a, B=b, C=c, D=d,
                                        physicalLength=thickness,
                                        apertureDiameter=diameter,
                                        frontVertex=0,
                                        backVertex=thickness,
                                        label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Draw a faint blue box with slightly curved interfaces
        of length 'thickness' starting at 'z'.

        An arc would be perfect, but matplotlib does not allow to fill
        an arc, hence we must use a patch and Bezier curve.
        We might as well draw it properly: it is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        """
        h = self.displayHalfHeight()
        
        # For simplicity, 1 is front, 2 is back.
        # For details, see https://pomax.github.io/bezierinfo/#circles_cubic
        v1 = z + self.frontVertex
        phi1 = math.asin(h/abs(self.R1))
        delta1 = self.R1*(1.0-math.cos(phi1))
        ctl1 = abs((1.0-math.cos(phi1))/math.sin(phi1)*self.R1)
        corner1 = v1 + delta1

        v2 = z + self.backVertex
        phi2 = math.asin(h/abs(self.R2))
        delta2 = self.R2*(1.0-math.cos(phi2))
        ctl2 = abs((1.0-math.cos(phi2))/math.sin(phi2)*self.R2)
        corner2 = v2 + delta2

        Path = mpath.Path
        p = patches.PathPatch(
            Path([(corner1, -h), (v1, -ctl1), (v1, 0), 
                  (v1, 0), (v1, ctl1), (corner1, h),
                  (corner2, h), (v2, ctl2), (v2, 0),
                  (v2, 0), (v2, -ctl2), (corner2, -h), 
                  (corner1, -h)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            color=[0.85, 0.95, 0.95],
            fill=True,
            transform=axes.transData)

        axes.add_patch(p)
        if showLabels:
            self.drawLabels(z,axes)

    def drawAperture(self, z, axes):
        """ Draw the aperture size for this element.
        The thick lens requires special care because the corners are not
        separated by self.L: the curvature makes the edges shorter.
        We are picky and draw it right.
        """

        if self.apertureDiameter != float('+Inf'):
            h = self.largestDiameter()/2.0
            phi1 = math.asin(h/abs(self.R1))
            corner1 = z + self.frontVertex + self.R1*(1.0-math.cos(phi1))

            phi2 = math.asin(h/abs(self.R2))
            corner2 = z + self.backVertex + self.R2*(1.0-math.cos(phi2))

            axes.add_patch(patches.Polygon(
                           [[corner1, h],[corner2, h]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))
            axes.add_patch(patches.Polygon(
                           [[corner1, -h],[corner2, -h]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:
        'z':position
        'label':the label to be used.  Can include LaTeX math code.
        """
        (f1, f2) = self.focusPositions(z)

        pointsOfInterest = []
        if f1 is not None:
            pointsOfInterest.append({'z': f1, 'label': '$F_f$'})
        if f2 is not None:
            pointsOfInterest.append({'z': f2, 'label': '$F_b$'})

        return pointsOfInterest

class DielectricSlab(ThickLens):
    """A slab of dielectric material of index n and length d, with flat faces

    """

    def __init__(self, n, thickness, diameter=float('+Inf'), label=''):
        super(DielectricSlab, self).__init__(n=n, R1=float("+Inf"),
                                             R2=float("+Inf"),
                                             thickness=thickness,
                                             diameter=diameter,
                                             label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Draw a faint blue box of length L starting at 'z'.

        """
        halfHeight = self.displayHalfHeight()
        p = patches.Rectangle((z, -halfHeight), self.L,
                              2 * halfHeight, color=[0.85, 0.95, 0.95],
                              fill=True, transform=axes.transData,
                              clip_on=True)
        axes.add_patch(p)


class Aperture(Matrix):
    """An aperture of finite diameter, null thickness.

    If the ray is beyond the finite diameter, the ray is blocked.
    """

    def __init__(self, diameter, label=''):
        super(
            Aperture,
            self).__init__(
            A=1,
            B=0,
            C=0,
            D=1,
            physicalLength=0,
            apertureDiameter=diameter,
            label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Currently nothing specific to draw because any
        aperture for any object is drawn with drawAperture()
        """


class MatrixGroup(Matrix):
    """MatrixGroup: A group of Matrix(), allowing
    the combination of several elements to be treated as a 
    whole, or treated explicitly as a sequence when needed.
    """

    def __init__(self, elements=[], label=""):
        super(MatrixGroup, self).__init__(1,0,0,1,label=label)
        self.elements = []

        for element in elements:
            self.append(element)

    def append(self, matrix):
        """ Add an element at the end of the path """
        self.elements.append(matrix)
        transferMatrix = self.transferMatrix()
        self.A = transferMatrix.A
        self.B = transferMatrix.B
        self.C = transferMatrix.C
        self.D = transferMatrix.D
        self.L = transferMatrix.L
        self.frontVertex = transferMatrix.frontVertex
        self.backVertex = transferMatrix.backVertex

    def ImagingPath(self):
        return ImagingPath(elements=self.elements, label=self.label)

    def LaserPath(self):
        return LaserPath(elements=self.elements, label=self.label)

    def transferMatrix(self, upTo=float('+Inf')):
        """ The transfer matrix between front edge and distance=upTo

        If "upTo" falls inside an element of finite length, then 
        it will request from that element a "partial" transfer matrix
        for a fraction of the length.  It is up to the Matrix() or 
        MatrixGroup() to define such partial transfer matrix when possible.
        Quite simply, Space() defines a partial matrix as Space(d=upTo).
        """
        transferMatrix = Matrix(A=1, B=0, C=0, D=1)
        distance = upTo
        for element in self.elements:
            if element.L <= distance:
                transferMatrix = element * transferMatrix
                distance -= element.L
            else:
                transferMatrix = element.transferMatrix(upTo=distance) * transferMatrix
                break

        return transferMatrix

    def transferMatrices(self):
        """ The list of Matrix() that corresponds to the propagation through 
        this element (or group). For a Matrix(), it simply returns a list 
        with a single element [self].
        For a MatrixGroup(), it returns the transferMatrices for 
        each individual element and appends them to a list for this group."""

        transferMatrices = []
        for element in self.elements:
            elementTransferMatrices = element.transferMatrices()
            transferMatrices.extend(elementTransferMatrices)
        return transferMatrices

    def propagate(self, inputRay):
        """ Deprecated function: use trace() """
        if not warningPrinted:
            print("propagate() was renamed trace().")
            warningPrinted = True

        return self.trace(inputRay)

    def propagateMany(self, inputRays):
        """ Deprecated function: use traceMany() """
        if not warningPrinted:
            print("propagateMany() was renamed traceMany().")
            warningPrinted = True

        return self.traceMany(inputRays)

    def trace(self, inputRay):
        """Trace the input ray from first element until after the last element

        Returns a ray trace (i.e. [Ray()]) starting with inputRay, followed by the ray after
        each element. If an element is composed of sub-elements, the ray will also be
        traced in several steps.
        """
        ray = inputRay
        rayTrace = [ray]
        for element in self.elements:
            rayTraceInElement = element.trace(ray)
            rayTrace.extend(rayTraceInElement)
            ray = rayTraceInElement[-1]  # last

        return rayTrace

    def hasFiniteApertureDiameter(self):
        """ True if ImagingPath has at least one element of finite diameter """
        for element in self.elements:
            if element.hasFiniteApertureDiameter():
                return True
        return False

    def largestDiameter(self):
        """ Largest finite diameter in all elements """

        maxDiameter = 0.0
        if self.hasFiniteApertureDiameter():
            for element in self.elements:
                diameter = element.largestDiameter()
                if diameter != float('+Inf') and diameter > maxDiameter:
                    maxDiameter = diameter
        else:
            maxDiameter = self.elements[0].displayHalfHeight() * 2

        return maxDiameter

    def flipOrientation(self):
        """ Flip the orientation (forward-backward) of this group of elements.
        Each element is also flipped individually. """

        allElements = self.elements
        allElements.reverse()
        self.elements = []

        for element in allElements:
            element.flipOrientation()
            self.append(element)

        return self

    def drawAt(self, z, axes, showLabels=True):
        """ Draw each element of this group """
        for element in self.elements:
            element.drawAt(z, axes)
            element.drawAperture(z, axes)

            if showLabels:
                element.drawLabels(z, axes)
            z += element.L

    def drawPointsOfInterest(self, z, axes):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        AS and FS are drawn at 110% of the largest diameter
        """
        labels = {}  # Gather labels at same z

        zElement = 0
        # For the group as a whole, then each element
        for pointOfInterest in self.pointsOfInterest(z=zElement):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label


        # Points of interest for each element
        for element in self.elements:
            pointsOfInterest = element.pointsOfInterest(zElement)

            for pointOfInterest in pointsOfInterest:
                zStr = "{0:3.3f}".format(pointOfInterest['z'])
                label = pointOfInterest['label']
                if zStr in labels:
                    labels[zStr] = labels[zStr] + ", " + label
                else:
                    labels[zStr] = label
            zElement += element.L

        halfHeight = self.largestDiameter()/2
        for zStr, label in labels.items():
            z = float(zStr)
            axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                         xycoords='data', fontsize=12,
                         ha='center', va='bottom')


class ImagingPath(MatrixGroup):
    """ImagingPath: the main class of the module, allowing
    the combination of Matrix() or MatrixGroup() to be used 
    as an imaging group with an object at the beginning.

    Usage is to create the ImagingPath(), then append() elements
    and display(). You may change objectHeight, fanAngle, fanNumber
    and rayNumber.
    """

    def __init__(self, elements=[], label=""):
        self.objectHeight = 1.0    # object height (full).
        self.objectPosition = 0.0  # always at z=0 for now.
        self.fanAngle = 0.5        # full fan angle for rays
        self.fanNumber = 9         # number of rays in fan
        self.rayNumber = 3         # number of points on object

        # Constants when calculating field stop
        self.precision = 0.001
        self.maxHeight = 10000.0

        # Display properties
        self.showObject = True
        self.showImages = True
        self.showEntrancePupil = True
        self.showElementLabels = True
        self.showPointsOfInterest = True
        self.showPointsOfInterestLabels = True
        self.showPlanesAcrossPointsOfInterest = True
        super(ImagingPath, self).__init__(elements=elements, label=label)

    def chiefRay(self, y):
        """ Chief ray for a height y (i.e., the ray that goes
        through the center of the aperture stop)

        The calculation is simple: obtain the transfer matrix
        to the aperture stop, then we know that the input ray
        (which we are looking for) will end at y=0 at the
        aperture stop.
        """
        (stopPosition, stopDiameter) = self.apertureStop()
        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        if B == 0:
            return None

        return Ray(y=y, theta=-A * y / B)

    def marginalRays(self, y=0):
        """ Marginal rays for a height y at object
        (i.e., the rays that hit the upper and lower
        edges of the aperture stop). In general, this could
        be any height, not just y=0. However, we usually
        only want y=0 which is implicitly called
        "the marginal ray (of the system)", and both rays
        will be symmetrically oriented on either side of the
        optical axis.

        The calculation is simple: obtain the transfer matrix
        to the aperture stop, then we know that the input ray
        (which we are looking for) will end at y= plus/minus diameter/2 at the
        aperture stop. We return the largest angle first, for
        convenience.
        """
        (stopPosition, stopDiameter) = self.apertureStop()
        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        thetaUp = (stopDiameter / 2.0 - A * y) / B
        thetaDown = (-stopDiameter / 2.0 - A * y) / B

        if thetaDown > thetaUp:
            (thetaUp, thetaDown) = (thetaDown, thetaUp)

        return (Ray(y=y, theta=thetaUp), Ray(y=y, theta=thetaDown))

    def axialRays(self, y):
        """ Synonym of marginal rays """
        return self.marginalRays(y)

    def apertureStop(self):
        """ The aperture in the system that limits the cone of angles
        originating from zero height at the object plane.

        Returns the position and diameter of the aperture stop

        Strategy: we take a ray height and divide by real aperture
        diameter at that position.  Some elements may have a finite length
        (e.g., Space() or ThickLens()), so we always calculate the ratio
        before propagating inside the element and after having propoagated
        through the element. The position where the absolute value of the
        ratio is maximum is the aperture stop.

        If there are no elements of finite diameter (i.e. all
        optical elements are infinite in diameters), then
        there is no aperture stop in the system and the size
        of the aperture stop is infinite.
        """
        if not self.hasFiniteApertureDiameter():
            return (None, float('+Inf'))
        else:
            ray = Ray(y=0, theta=0.1)  # Any ray angle will do
            rayTrace = self.trace(ray)

            maxRatio = 0.0
            apertureStopPosition = 0
            apertureStopDiameter = float("+Inf")

            for ray in rayTrace:
                ratio = abs(ray.y / ray.apertureDiameter)
                if ratio > maxRatio:
                    apertureStopPosition = ray.z
                    apertureStopDiameter = ray.apertureDiameter
                    maxRatio = ratio

            return (apertureStopPosition, apertureStopDiameter)

    def entrancePupil(self):
        """ The entrance pupil is the image of the aperture stop
        as seen from the object. To obtain this image, we simply
        need to know the tranfer matrix to the aperture stop,
        then find the "backward" conjugate, which means finding
        the position of the "image" (the entrance pupil) that would 
        lead to the "object" (aperture stop) at the end of the transfer
        matrix. All the terminology is such that it assumes
        the "object" is at the front and the "image" is at the back,
        so we need to invert the magnification.

        Returns the pupilPosition relative to input reference plane
        (positive means to the right) and its diameter.
        """

        if self.hasFiniteApertureDiameter():
            (stopPosition, stopDiameter) = self.apertureStop()
            transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
            (pupilPosition, matrixToPupil) = transferMatrixToApertureStop.backwardConjugate()
            (Mt, Ma) = matrixToPupil.magnification()
            return (-pupilPosition, stopDiameter/Mt)
        else:
            return (None, None)
        

    def fieldStop(self):
        """ The field stop is the aperture that limits the image
        size (or field of view)

        Returns the position and diameter of the field stop.

        Strategy: We want to find the exact height from the object
        where it is blocked by an aperture (which will become the
        field stop). We look for the point that separates the
        "unblocked" ray from the "blocked" ray.

        To do so, we take a ray at various heights starting at y=0
        from object with a finite increment "dy" and aim 
        at center of pupil (i.e. chief ray from that height) 
        until ray is blocked. If it is not blocked, increase
        dy and increase y by dy. When it is blocked, we turn
        around and increase by only half the dy, then we continue
        until it is unblocked, turn around, divide dy by 2, etc...
        This rapidly converges to the position at which the ray
        is blocked, which is the field stop half diameter. This
        strategy is better than linearly going through object heights
        because the precision can be very high without a long calculation
        time.

        It is possible to have finite diameter elements but
        still an infinite field of view and therefore no Field stop.
        In fact, if only a single element has a finite diameter,
        there is no field stop (only an aperture stop). The limit
        is arbitrarily set to maxHeight.

        If there are no elements of finite diameter (i.e. all
        optical elements are infinite in diameters), then there
        is no field stop and no aperture stop in the system
        and their sizes are infinite.
        """
        (apertureStopPosition, dummy) = self.apertureStop()

        fieldStopPosition = None
        fieldStopDiameter = float('+Inf')
        if self.hasFiniteApertureDiameter() and apertureStopPosition != 0:
            dy = self.precision * 100
            y = 0.0
            wasBlocked = False
            chiefRayTrace = []
            while abs(dy) > self.precision or not wasBlocked:
                chiefRay = self.chiefRay(y=y)
                chiefRayTrace = self.trace(chiefRay)
                outputChiefRay = chiefRayTrace[-1]

                if outputChiefRay.isBlocked != wasBlocked:
                    dy = -dy/2.0 # Go back, reduce increment
                else:
                    dy = dy*1.5 # Keep going, go faster (different factor)

                y += dy
                wasBlocked = outputChiefRay.isBlocked
                if abs(y) > self.maxHeight and not wasBlocked:
                    return (fieldStopPosition, fieldStopDiameter)
            
            for ray in chiefRayTrace:
                if ray.isBlocked:
                    fieldStopPosition = ray.z
                    fieldStopDiameter = ray.apertureDiameter
                    break

        return (fieldStopPosition, fieldStopDiameter)

    def fieldOfView(self):
        """ The field of view is the maximum object height
        visible until its chief ray is blocked by the field stop

        Strategy: take ray at various heights from object and
        aim at center of pupil (chief ray from that point)
        until ray is blocked. It is possible to have finite
        diameter elements but still an infinite field of view
        and therefore no Field stop.
        """

        (stopPosition, stopDiameter) = self.fieldStop()
        if stopPosition is None:
            return float('+Inf')

        transferMatrixToFieldStop = self.transferMatrix(upTo=stopPosition)

        dy = self.precision * 100
        y = 0.0
        chiefRay = Ray(y=0, theta=0)
        wasBlocked = False
        while abs(dy) > self.precision or not wasBlocked:
            chiefRay = self.chiefRay(y=y)
            chiefRayTrace = self.trace(chiefRay)
            outputChiefRay = chiefRayTrace[-1]

            if outputChiefRay.isBlocked != wasBlocked:
                dy = -dy/2.0
            else:
                dy = dy*1.5 # Don't use 2.0: could bounce forever

            y += dy
            wasBlocked = outputChiefRay.isBlocked
            if abs(y) > self.maxHeight and not wasBlocked:
                return float("+Inf")
        
        return chiefRay.y * 2.0

    def imageSize(self):
        """ The image size is the object field of view
        multiplied by magnification

        """
        fieldOfView = self.fieldOfView()
        (distance, conjugateMatrix) = self.forwardConjugate()
        print (distance, conjugateMatrix)
        magnification = conjugateMatrix.A
        return fieldOfView * magnification

    def createRayTracePlot(
            self, axes,
            limitObjectToFieldOfView=False,
            onlyChiefAndMarginalRays=False,
            removeBlockedRaysCompletely=False):
        """ Create a matplotlib plot to draw the rays and the elements.
            
        Three optional parameters:
            limitObjectToFieldOfView=False, to use the calculated field of view
            instead of the objectHeight

            onlyChiefAndMarginalRays=False, to only show principal rays

            removeBlockedRaysCompletely=False to remove rays that are blocked.

         """

        displayRange = 2 * self.largestDiameter()
        if displayRange == float('+Inf'):
            displayRange = self.objectHeight * 2

        axes.set(xlabel='Distance', ylabel='Height', title=self.label)
        axes.set_ylim([-displayRange /2 * 1.2, displayRange / 2 * 1.2])

        note1 = ""
        note2 = ""
        if limitObjectToFieldOfView:
            fieldOfView = self.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.objectHeight = fieldOfView
                note1 = "Field of view: {0:.2f}".format(self.objectHeight)
            else:
                raise ValueError(
                    "Infinite field of view: cannot use\
                    limitObjectToFieldOfView=True.")

        else:
            note1 = "Object height: {0:.2f}".format(self.objectHeight)

        if onlyChiefAndMarginalRays:
            (stopPosition, stopDiameter) = self.apertureStop()
            if stopPosition is None:
                raise ValueError(
                    "No aperture stop in system: cannot use\
                    onlyChiefAndMarginalRays=True since they\
                    are not defined.")
            note2 = "Only chief and marginal rays shown"

        axes.text(0.05, 0.15, note1 + "\n" + note2, transform=axes.transAxes,
                  fontsize=12, verticalalignment='top',clip_box=axes.bbox, clip_on=True)

        self.drawRayTraces(
            axes,
            onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
            removeBlockedRaysCompletely=removeBlockedRaysCompletely)
        if self.showObject:
            self.drawObject(axes)

        if self.showImages:
            self.drawImages(axes)

        if self.showEntrancePupil:
            self.drawEntrancePupil(z=0, axes=axes)

        self.drawAt(z=0, axes=axes)
        if self.showPointsOfInterest:
            self.drawPointsOfInterest(z=0, axes=axes)
            self.drawStops(z=0, axes=axes)

        return axes

    def display(self, limitObjectToFieldOfView=False,
                onlyChiefAndMarginalRays=False, removeBlockedRaysCompletely=False, comments=None):
        """ Display the optical system and trace the rays. If comments are included
        they will be displayed on a graph in the bottom half of the plot.

        """

        if comments is not None:
            fig, (axes, axesComments) = plt.subplots(2,1,figsize=(10, 7))
            axesComments.axis('off')
            axesComments.text(0., 1.0, comments, transform=axesComments.transAxes,
            fontsize=10, verticalalignment='top')
        else:
            fig, axes = plt.subplots(figsize=(10, 7))

        self.createRayTracePlot(axes=axes,
            limitObjectToFieldOfView=limitObjectToFieldOfView,
            onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
            removeBlockedRaysCompletely=removeBlockedRaysCompletely)

        plt.ioff()
        plt.show()

    def save(self, filepath,
            limitObjectToFieldOfView=False,
            onlyChiefAndMarginalRays=False, 
            removeBlockedRaysCompletely=False,
            comments=None):
        if comments is not None:
            fig, (axes, axesComments) = plt.subplots(2,1,figsize=(10, 7))
            axesComments.axis('off')
            axesComments.text(0., 1.0, comments, transform=axesComments.transAxes,
            fontsize=10, verticalalignment='top')
        else:
            fig, axes = plt.subplots(figsize=(10, 7))

        self.createRayTracePlot(axes=axes,
            limitObjectToFieldOfView=limitObjectToFieldOfView,
            onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
            removeBlockedRaysCompletely=removeBlockedRaysCompletely)

        fig.savefig(filepath, dpi=600)

    def drawObject(self, axes):
        """ Draw the object as defined by objectPosition, objectHeight """
        (xScaling, yScaling) = self.axesToDataScaling(axes)
        arrowWidth = xScaling * 0.01
        arrowHeight = yScaling * 0.03

        axes.arrow(
            self.objectPosition,
            -self.objectHeight / 2,
            0,
            self.objectHeight,
            width=arrowWidth/5,
            fc='b',
            ec='b',
            head_length=arrowHeight,
            head_width=arrowWidth,
            length_includes_head=True)

    def drawImages(self, axes):
        """ Draw all images (real and virtual) of the object defined by 
        objectPosition, objectHeight """

        (xScaling, yScaling) = self.axesToDataScaling(axes)
        arrowWidth = xScaling * 0.01
        arrowHeight = yScaling * 0.03

        transferMatrix = Matrix(A=1, B=0, C=0, D=1)
        matrices = self.transferMatrices()
        for element in matrices:
            transferMatrix = element * transferMatrix
            (distance, conjugate) = transferMatrix.forwardConjugate()
            if distance is not None:
                imagePosition = transferMatrix.L + distance
                if imagePosition != 0 and conjugate is not None:
                    magnification = conjugate.A
                    axes.arrow(
                        imagePosition,
                        -magnification * self.objectHeight / 2,
                        0,
                        (magnification) * self.objectHeight,
                        width=arrowWidth/5,
                        fc='r',
                        ec='r',
                        head_length=arrowHeight,
                        head_width=arrowWidth,
                        length_includes_head=True)

    def drawStops(self, z, axes):
        """
        AS and FS are drawn at 110% of the largest diameter
        """
        halfHeight = self.largestDiameter()/2

        (apertureStopPosition, apertureStopDiameter) = self.apertureStop()
        if apertureStopPosition is not None:
            axes.annotate('AS',
                         xy=(apertureStopPosition, 0.0),
                         xytext=(apertureStopPosition, halfHeight * 1.1),
                         fontsize=18,
                         xycoords='data',
                         ha='center',
                         va='bottom')

        (fieldStopPosition, fieldStopDiameter) = self.fieldStop()
        if fieldStopPosition is not None:
            axes.annotate('FS',
                         xy=(fieldStopPosition,
                             0.0),
                         xytext=(fieldStopPosition,
                                 halfHeight * 1.1),
                         fontsize=18,
                         xycoords='data',
                         ha='center',
                         va='bottom')

    def drawEntrancePupil(self, z, axes):
        (pupilPosition, pupilDiameter) = self.entrancePupil()
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0
            center = z + pupilPosition
            (xScaling,_) = self.axesToDataScaling(axes)
            width = xScaling*0.01/2

            axes.add_patch(patches.Polygon(
                           [[center - width, halfHeight],
                            [center + width, halfHeight]],
                           linewidth=3,
                           closed=False,
                           color='r'))
            axes.add_patch(patches.Polygon(
                           [[center - width, -halfHeight],
                            [center + width, -halfHeight]],
                           linewidth=3,
                           closed=False,
                           color='r'))


    def drawOpticalElements(self, z, axes):
        """ Deprecated. Use drawAt() """
        print("drawOpticalElements() was renamed drawAt()")
        self.drawAt(z,axes)

    def drawRayTraces(self, axes, onlyChiefAndMarginalRays,
                      removeBlockedRaysCompletely=True):
        """ Draw all ray traces corresponding to either 
        1. the group of rays defined by the user (fanAngle, fanNumber, rayNumber) 
        2. the principal rays (chief and marginal) """

        color = ['b', 'r', 'g']

        if onlyChiefAndMarginalRays:
            halfHeight = self.objectHeight / 2.0
            chiefRay = self.chiefRay(y=halfHeight - 0.01)
            (marginalUp, marginalDown) = self.marginalRays(y=0)
            rayGroup = (chiefRay, marginalUp)
            linewidth = 1.5
        else:
            halfAngle = self.fanAngle / 2.0
            halfHeight = self.objectHeight / 2.0
            rayGroup = Ray.fanGroup(
                yMin=-halfHeight,
                yMax=halfHeight,
                M=self.rayNumber,
                radianMin=-halfAngle,
                radianMax=halfAngle,
                N=self.fanNumber)
            linewidth = 0.5

        manyRayTraces = self.traceMany(rayGroup)

        for rayTrace in manyRayTraces:
            (x, y) = self.rearrangeRayTraceForPlotting(
                rayTrace, removeBlockedRaysCompletely)
            if len(y) == 0:
                continue  # nothing to plot, ray was fully blocked

            rayInitialHeight = y[0]
            binSize = 2.0 * halfHeight / (len(color) - 1)
            colorIndex = int(
                (rayInitialHeight - (-halfHeight - binSize / 2)) / binSize)
            axes.plot(x, y, color[colorIndex], linewidth=linewidth)

    def rearrangeRayTraceForPlotting(
            self,
            rayList,
            removeBlockedRaysCompletely=True):
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
        return (x, y)


class LaserPath(MatrixGroup):
    """LaserPath: the main class of the module for coherent
    laser beams: it is the combination of Matrix() or MatrixGroup()
    to be used as a laser path with a laser beam (GaussianBeam)
    at the entrance.

    Usage is to create the LaserPath(), then append() elements
    and display(). You may change the inputBeam to any GaussianBeam(),
    or provide one to display(beam=GaussianBeam())

    Gaussian laser beams are not "blocked" by aperture. The formalism
    does not explicitly allow that.  However, if it appears that a 
    GaussianBeam() would be clipped by  finite aperture, a property 
    is set to indicate it, but it will propagate nevertheless
    and without diffraction due to that aperture.
    """
    def __init__(self, elements=[], label=""):
        self.inputBeam = None
        self.showElementLabels = True
        self.showPointsOfInterest = True
        self.showPointsOfInterestLabels = True
        self.showPlanesAcrossPointsOfInterest = True
        super(LaserPath, self).__init__(elements=elements, label=label)

    def display(self, inputBeam=None, comments=None):
        """ Display the optical system and trace the laser beam. 
        If comments are included they will be displayed on a
        graph in the bottom half of the plot.

        """

        if comments is not None:
            fig, (axes, axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            axesComments.axis('off')
            axesComments.text(0., 1.0, comments, transform=axesComments.transAxes,
                              fontsize=10, verticalalignment='top')
        else:
            fig, axes = plt.subplots(figsize=(10, 7))

        if inputBeam is None:
            inputBeam = self.inputBeam

        self.createBeamTracePlot(axes=axes, inputBeam=inputBeam)

        plt.ioff()
        plt.show()

    def createBeamTracePlot(self, axes, inputBeam):
        """ Create a matplotlib plot to draw the laser beam and the elements.
        """

        displayRange = 2 * self.largestDiameter()
        if displayRange == float('+Inf'):
            displayRange = self.inputBeam.w * 6

        axes.set(xlabel='Distance', ylabel='Height', title=self.label)
        axes.set_ylim([-displayRange / 2 * 1.2, displayRange / 2 * 1.2])

        self.drawBeamTrace(axes, inputBeam)
        self.drawWaists(axes, inputBeam)
        self.drawAt(z=0, axes=axes)

        return axes

    def rearrangeBeamTraceForPlotting(self, rayList):
        x = []
        y = []
        for ray in rayList:
            x.append(ray.z)
            y.append(ray.w)
        return (x, y)

    def drawBeamTrace(self, axes, beam):
        """ Draw beam trace corresponding to input beam 
        Because the laser beam diffracts through space, we cannot
        simply propagate the beam over large distances and trace it
        (as opposed to rays, where we can). We must split Space() 
        elements into sub elements to watch the beam size expand.
        
        We arbitrarily split Space() elements into 100 sub elements
        before plotting.
        """

        highResolution = ImagingPath()
        for element in self.elements:
            if isinstance(element, Space):
                for i in range(100):
                    highResolution.append(Space(d=element.L/100, 
                                                n=element.frontIndex))
            else:
                highResolution.append(element)


        beamTrace = highResolution.trace(beam)
        (x, y) = self.rearrangeBeamTraceForPlotting(beamTrace)
        axes.plot(x, y, 'r', linewidth=1)
        axes.plot(x, [-v for v in y], 'r', linewidth=1)

    def drawWaists(self, axes, beam):
        """ Draws the expected waist (i.e. the focal spot or the spot where the
        size is minimum) for all positions of the beam. This will show "waists" that
        are virtual if there is an additional lens between the beam and the expceted
        waist.

        It is easy to obtain the waist position from the complex radius of curvature
        because it is the position where the complex radius is imaginary. The position
        returned is relative to the position of the beam, which is why we add the actual
        position of the beam to the relative position. """

        beamTrace = self.trace(beam)
        for beam in beamTrace:
            relativePosition = beam.waistPosition
            position = beam.z + relativePosition
            size = beam.waist

            arrowSize = 1
            axes.arrow(position, size+arrowSize, 0, -arrowSize,
                width=0.1, fc='g', ec='g',
                head_length=0.5, head_width=2,
                length_includes_head=True)
            axes.arrow(position, -size-arrowSize, 0, arrowSize,
                width=0.1, fc='g', ec='g',
                head_length=0.5, head_width=2,
                length_includes_head=True)


""" Synonym of Matrix: Element 

We can use a mathematical language (Matrix) or optics terms (Element)
"""
Element = Matrix
Group = MatrixGroup
OpticalPath = ImagingPath
