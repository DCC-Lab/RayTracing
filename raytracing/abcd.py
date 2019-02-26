import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
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

        # First and last interfaces. Used for BFL and FFL
        self.frontVertex = frontVertex
        self.backVertex = backVertex

        # Aperture
        self.apertureDiameter = apertureDiameter

        self.label = label
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

        if abs(outputRay.y) > self.apertureDiameter / 2:
            outputRay.isBlocked = True
        else:
            outputRay.isBlocked = rightSideRay.isBlocked

        return outputRay

    def largestDiameter(self):
        return self.apertureDiameter

    def hasFiniteApertureDiameter(self):
        return self.apertureDiameter != float("+Inf")

    def transferMatrix(self, upTo=float('+Inf')):
        distance = upTo
        if self.L == 0:
            return self
        elif self.L <= distance:
            return self
        else:
            raise TypeError("Subclass of non-null physical length must override transferMatrix()")

    def transferMatrices(self):
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
        if self.L > 0:
            if ray.y > self.apertureDiameter/2:
                ray.isBlocked = True
            rayTrace.append(ray)                            

        rayTrace.append(self.mul_ray(ray))

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
        return self.effectiveFocalLengths()

    def effectiveFocalLengths(self):
        """ The effective focal lengths calculated from the power (C)
        of the matrix.

        Currently, it is assumed the index is n=1 on either side and
        both focal lengths are the same.
        """

        focalLength = -1.0 / self.C  # FIXME: Assumes n=1 on either side
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

        if self.backVertex is not None:
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

        if self.frontVertex is not None:
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
        (f1, f2) = self.focalDistances()
        (p1, p2) = self.principalPlanePositions(z)
        return (p1 - f1, p2 + f2)

    def principalPlanePositions(self, z):
        """ Positions of the input and output principal planes.

        Currently, it is assumed the index is n=1 on either side.
        """
        p1 = z - (1 - self.D) / self.C  # FIXME: Assumes n=1 on either side
        # FIXME: Assumes n=1 on either side
        p2 = z + self.L + (1 - self.A) / self.C
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

    def drawAt(self, z, axes, showLabels=False):
        """ Draw element on plot with starting edge at 'z'.

        Default is a black box of appropriate length.
        """
        halfHeight = self.largestDiameter()
        p = patches.Rectangle((z, -halfHeight), self.L,
                              2 * halfHeight, color='k', fill=False,
                              transform=axes.transData, clip_on=True)
        axes.add_patch(p)

    def drawCardinalPoints(self, z, axes):
        """ Draw the focal points of a thin lens as black dots """
        (f1, f2) = self.focusPositions(z)
        axes.plot([f1, f2], [0, 0], 'ko', color='k', linewidth=0.4)

    def drawLabels(self, z, axes):
        """ Draw element labels on plot with starting edge at 'z'.

        Labels are drawn 50% above the display height
        """
        halfHeight = self.displayHalfHeight()
        center = z + self.L / 2.0
        axes.annotate(self.label, xy=(center, 0.0),
                     xytext=(center, halfHeight * 1.5),
                     fontsize=8, xycoords='data', ha='center',
                     va='bottom')

    def drawAperture(self, z, axes):
        if self.apertureDiameter != float('+Inf'):
            halfHeight = self.apertureDiameter / 2.0

            center = z + self.L/2
            if self.L == 0:
                width = 3
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
        halfHeight = self.displayHalfHeight()
        axes.arrow(z, 0, 0, halfHeight, width=0.1, fc='k', ec='k',
                  head_length=0.25, head_width=0.25, length_includes_head=True)
        axes.arrow(z, 0, 0, -halfHeight, width=0.1, fc='k', ec='k',
                  head_length=0.25, head_width=0.25, length_includes_head=True)
        self.drawCardinalPoints(z, axes)

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:
        'z':position
        'label':the label to be used.  Can include LaTeX math code.
        """
        (f1, f2) = self.focusPositions(z)
        return [{'z': f1, 'label': '$F_f$'}, {'z': f2, 'label': '$F_b$'}]


class Space(Matrix):
    """Free space of length d

    """

    def __init__(self, d, diameter=float('+Inf'), label=''):
        super(Space, self).__init__(A=1,
                                    B=float(d),
                                    C=0,
                                    D=1,
                                    physicalLength=d,
                                    frontVertex=None,
                                    backVertex=None,
                                    apertureDiameter=diameter,
                                    label=label)

    def drawAt(self, z, axes, showLabels=False):
        """ Draw nothing because free space is nothing. """
        return

    def transferMatrix(self, upTo=float('+Inf')):
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
        a = 1.0
        b = 0.0
        c = - (n2-n1)/(n2*R)
        d = n1/n2

        super(DielectricInterface, self).__init__(A=a, B=b, C=c, D=d,
                                                  physicalLength=0,
                                                  apertureDiameter=diameter,
                                                  frontVertex=0,
                                                  backVertex=0,
                                                  label=label)


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

        """
        halfHeight = self.displayHalfHeight()
        apexHeight = self.L * 0.2
        frontVertex = z + apexHeight * (-self.R1/abs(self.R1))
        backVertex = z + self.L + apexHeight * (-self.R2/abs(self.R2))

        Path = mpath.Path
        p = patches.PathPatch(
            Path([(z, -halfHeight), (frontVertex, 0), (z, halfHeight),
                  (z+self.L, halfHeight), (backVertex, 0),
                  (z+self.L, -halfHeight), (z, -halfHeight)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            color=[0.85, 0.95, 0.95],
            fill=True,
            transform=axes.transData)

        axes.add_patch(p)
        if showLabels:
            self.drawLabels(z,axes)


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
        transferMatrices = []
        for element in self.elements:
            elementTransferMatrices = element.transferMatrices()
            transferMatrices.extend(elementTransferMatrices)
        return transferMatrices

    def propagate(self, inputRay):
        if not warningPrinted:
            print("propagate() was renamed trace().")
            warningPrinted = True

        return self.trace(inputRay)

    def propagateMany(self, inputRays):
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
        """ True if OpticalPath has at least one element of finite diameter """
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

    def drawAt(self, z, axes, showLabels=True):
        for element in self.elements:
            element.drawAt(z, axes)
            element.drawAperture(z, axes)

            if showLabels:
                element.drawLabels(z, axes)
            z += element.L


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

        fieldStopPosition = None
        fieldStopDiameter = float('+Inf')
        if self.hasFiniteApertureDiameter():            
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
                  fontsize=12, verticalalignment='top')

        self.drawRayTraces(
            axes,
            onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
            removeBlockedRaysCompletely=removeBlockedRaysCompletely)
        if self.showObject:
            self.drawObject(axes)

        if self.showImages:
            self.drawImages(axes)

        self.drawAt(z=0, axes=axes)
        if self.showPointsOfInterest:
            self.drawPointsOfInterest(axes)

        return axes

    def display(self, limitObjectToFieldOfView=False,
                onlyChiefAndMarginalRays=False, removeBlockedRaysCompletely=False, comments=None):
        
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
        axes.arrow(
            self.objectPosition,
            -self.objectHeight / 2,
            0,
            self.objectHeight,
            width=0.1,
            fc='b',
            ec='b',
            head_length=0.25,
            head_width=0.25,
            length_includes_head=True)

    def drawImages(self, axes):
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
                        width=0.1,
                        fc='r',
                        ec='r',
                        head_length=0.25,
                        head_width=0.25,
                        length_includes_head=True)

    def drawPointsOfInterest(self, axes):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        AS and FS are drawn at 110% of the largest diameter
        """
        labels = {}  # Regroup labels at same z
        zElement = 0
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

    def drawOpticalElements(self, z, axes):
        print("drawOpticalElements() was renamed drawAt()")
        self.drawAt(z,axes)

    def drawRayTraces(self, axes, onlyChiefAndMarginalRays,
                      removeBlockedRaysCompletely=True):
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

""" Synonym of Matrix: Element 

We can use a mathematical language (Matrix) or optics terms (Element)
"""
Element = Matrix
Group = MatrixGroup
OpticalPath = ImagingPath

def installModule():
    directory = subprocess.check_output(
        'python -m site --user-site', shell=True)
    os.system('mkdir -p "`python -m site --user-site`"')
    os.system('cp ABCD.py "`python -m site --user-site`/"')
    os.system('cp Axicon.py "`python -m site --user-site`/"')
    os.system('cp Objectives.py "`python -m site --user-site`/"')
    print('Module ABCD.py, Axicon.py and Objectives.py copied to ', directory)

# This is an example for the module.
# Don't modify this: create a new script that imports ABCD
# See test.py or examples/*.py

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'install':
            installModule()
            exit()

    path = ImagingPath()
    path.label = "Simple demo: one infinite lens f = 5cm"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.display()
    # or
    # path.save("Figure 1.png")

    path = ImagingPath()
    path.label = "Simple demo: two infinite lenses with f = 5cm"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=20))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.display()
    # or
    # path.save("Figure 2.png")

    path = ImagingPath()
    path.label = "Simple demo: Aperture behind lens"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=3))
    path.append(Aperture(diameter=3))
    path.append(Space(d=17))
    path.display()
    # or
    # path.save("Figure 3.png")

    path = ImagingPath()
    path.label = "Microscope system"
#   path.objectHeight = 0.1
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=0.8, label='Obj'))
    path.append(Space(d=4 + 18))
    path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
    path.append(Space(d=18))
    path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
    path.save("MicroscopeSystem.png", onlyChiefAndMarginalRays=True,
              limitObjectToFieldOfView=True)
    # or
    # path.save("Figure 4.png")

    path = ImagingPath()
    path.label = "Focussing through a dielectric slab"
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=3))
    path.append(DielectricSlab(n=1.5, thickness=4))
    path.append(Space(d=10))
    path.display()
