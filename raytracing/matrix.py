from .ray import *
from .gaussianbeam import *

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms

import math


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

        qprime = (complex(self.A) * q + complex(self.B) ) / (complex(self.C)*q + complex(self.D))
        
        outputBeam = GaussianBeam(q=qprime, wavelength=rightSideBeam.wavelength)
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

class CurvedMirror(Matrix):
    """A curved mirror of radius R and infinite or finite diameter

    """

    def __init__(self, R, diameter=float('+Inf'), label=''):
        super(CurvedMirror, self).__init__(A=1, B=0, C=-2 / float(R), D=1,
                                   physicalLength=0,
                                   apertureDiameter=diameter,
                                   frontVertex=0,
                                   backVertex=0,
                                   label=label)


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

