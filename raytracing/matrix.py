from .ray import *
from .gaussianbeam import *
from .rays import *

import multiprocessing
import sys
import math
import warnings


def warningLineFormat(message, category, filename, lineno, line=None):
    return '\n%s:%s\n%s:%s\n' % (filename, lineno, category.__name__, message)


warnings.formatwarning = warningLineFormat


# todo: fix docstrings since draw-related methods were removed


class Matrix(object):
    r"""A matrix and an optical element that can transform a ray or another
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

    Parameters
    ----------
    A : float
        Value of the index (1,1) in the ABCD matrix of the element. (default =1)
    B : float
        Value of the index (2,1) in the ABCD matrix of the element. (default =0)
    C : float
        Value of the index (1,2) in the ABCD matrix of the element. (default =0)
    D : float
        Value of the index (2,2) in the ABCD matrix of the element. (default =1)
    physicalLength: float (Optional)
        Length of the object. (default =0)
    frontVertex : float (Optional)
        Position of the front interface, from which FFL is calculated (default = None)
    backVertex : float (Optional)
        Position of the back interface, from which BFL is calculated (default = None)
    frontIndex : float (Optional)
        Index of refraction at the entrance (front). (default = 1.0)
        This value cannot be less than 1.0.
    backIndex : float (Optional)
        Index of refraction at exit (back). (default = 1.0)
        This value cannot be less than 1.0.
    apertureDiameter : float (Optional)
        Aperture of the element. (default = +Inf)
        The diameter of the aperture must be a positive value.
    label : string (Optional)
        The label of the element.

    Returns
    -------
    Matrix : object
        an element with a defined ABCD matrix and properties.

    Examples
    --------
    An ABCD matrix of a free space of length 3 can be defined as follows

    >>> from raytracing import *
    >>> M= Matrix(A=1,B=3,C=0,D=1)
    >>> print(M)
    /                \
    |  1.000    3.000 |
    |                 |
    |  0.000    1.000 |
     \               /
    f = +inf (afocal)


    Notes
    -----
    The vertices are not mandatory: they represent the first (front) and second
    (back) physical interfaces.  It is possible to have None (e.g., freespace)
    1 (dielectric interface) or 2 (any lens).

    The front and back indices are important in the calculation of the determinant
    and the effective focal lengths.

    """

    __epsilon__ = 1e-5  # Anything smaller is zero

    def __init__(
            self,
            A: float = 1,
            B: float = 0,
            C: float = 0,
            D: float = 1,
            physicalLength: float = 0,
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
        if apertureDiameter <= 0:
            raise ValueError("The aperture diameter must be strictly positive.")
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

        if areAbsolutelyNotEqual(self.determinant, frontIndex / backIndex, self.__epsilon__):
            raise ValueError("The matrix has inconsistent values: \
                determinant is incorrect considering front and back indices.")

    @property
    def isIdentity(self):
        return self.A == 1 and self.D == 1 and self.B == 0 and self.C == 0

    @property
    def determinant(self):
        """The determinant of the ABCD matrix is always frontIndex/backIndex,
        which is often 1.0. 
        We make a calculation exception when C == 0 and B is infinity: since
        B is never really infinity, but C can be precisely zero (especially
        in free space), then B*C is zero in that particular case.

        Examples
        --------
        >>> from raytracing import *

        >>> # M is an ABCD matrix of a lens (f=3)
        >>> M= Matrix(A=1,B=0,C=-1/3,D=1,label='Lens')
        >>> print('the determinant of matrix is equal to :' , M.determinant())
        the determinant of matrix is equal to : 1.0

        """

        if self.C == 0:
            return self.A * self.D

        return self.A * self.D - self.B * self.C

    def __mul__(self, rightSide):
        """Operator overloading allowing easy-to-read matrix multiplication
        with other `Matrix`, with a `Ray` or a `GaussianBeam`.

        For instance, with M1 = Matrix() and M2 = Matrix(), one can write
        M3 = M1*M2. With r = Ray(), one can apply the M1 transform to a ray
        with rOut = M1*r

        Examples
        --------
        >>> from raytracing import *

        >>> M1= Matrix(A=1,B=0,C=-1/3,D=1,label='Lens')
        >>> M2= Matrix(A=1,B=0,C=-1/3,D=1,label='Lens')
        >>> print('product M2*M1 :' , M2*M1)

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

    def mul_matrix(self, rightSideMatrix: 'Matrix'):
        r""" This function is used to combine two elements into a single matrix.
        The multiplication of two ABCD matrices calculates the total ABCD matrix of the system.
        Total length of the elements is calculated (z) but apertures are lost. We compute
        the first and last vertices.

        Parameters
        ----------
        rightSideMatrix : object from Matrix class
            including the ABCD matrix and other properties of an element.

        Returns
        -------
        A matrix with:

        a : float
            Value of the index (1,1) in the ABCD matrix of the combination of the two elements.
        b : float
            Value of the index (2,1) in the ABCD matrix of the combination of the two elements.
        c : float
            Value of the index (1,2) in the ABCD matrix of the combination of the two elements.
        d : float
            Value of the index (2,2) in the ABCD matrix of the combination of the two elements.
        frontVertex : float
            First interface used for FFL
        backVertex : float
            Last interface used for BFL
        physicalLength: float
            Length of the combination of the two elements.

        Examples
        --------
        Consider a Lens (f=3) and a free space (d=2). The equal ABCD matrix
        of this system can be calculated as the following

        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=3)
        >>> M1= Matrix(A=1,B=0,C=-1/3,D=1,label='Lens')
        >>> # M2 is an ABCD matrix of free space (d=2)
        >>> M2= Matrix(A=1,B=2,C=0,D=1,label='freeSpace')
        >>> print('Total ABCD matrix :' , M1.mul_matrix(M2))
        Total ABCD matrix :
         /             \
        |  1.000    2.000 |
        |               |
        | -0.333    0.333 |
         \             /
        f=3.000

        See Also
        --------
        raytracing.Matrix.mul_ray
        raytracing.Matrix.mul_beam

        Notes
        -----
        If there is more than two elements, the multplication can be repeated
        to calculate the total ABCD matrix of the system. When combining matrices,
        any apertures are lost.
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

        if self.isIdentity:  # If LHS is identity, take the other's indices
            fIndex = rightSideMatrix.frontIndex
            bIndex = rightSideMatrix.backIndex
        elif rightSideMatrix.isIdentity:  # If RHS is identity, take other's indices
            fIndex = self.frontIndex
            bIndex = self.backIndex
        else:  # Else, take the "first one" front index and the "last one" back index (physical first and last)
            fIndex = rightSideMatrix.frontIndex
            bIndex = self.backIndex

        return Matrix(a, b, c, d, frontVertex=fv, backVertex=bv, physicalLength=L, frontIndex=fIndex, backIndex=bIndex)

    def mul_ray(self, rightSideRay):
        r"""This function does the multiplication of a ray by a matrix.
        The output shows the propagated ray through the system.
        New position of ray is updated by the physical length of the matrix.

        Parameters
        ----------
        rightSideRay : object from Ray class
            including the Ray properties

        Returns
        -------
        outputRay : an object from Ray class
            New position of the input ray after passing through the element.

        Examples
        --------
        A propagation of a ray at height 10 with angle 10 can be written as the following:

        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=10)
        >>> M1= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=5,label='Lens')
        >>> # R is a ray
        >>> R= Ray(y=10,theta=10)
        >>> print('The output ray of Lens M1 :' , M1.mul_ray(R))
        The output ray of Lens M1 :
         /       \
        | 10.000  |
        |         |
        |  9.000  |
         \       /
        z = 5.000

        And after a free space (d=2)

        >>> # M2 is an ABCD matrix of free space (d=2)
        >>> M2= Matrix(A=1,B=2,C=0,D=1,physicalLength=2,label='freeSpace')
        >>> M=M1.mul_matrix(M2)
        >>> print('The output ray of Lens M1 and free space M2 :' , M.mul_ray(R))
        The output ray of Lens M1 and free space M2 :
         /       \
        | 30.000  |
        |         |
        |  7.000  |
         \       /
        z = 7.000


        See Also
        --------
        raytracing.Matrix.mul_matrix
        raytracing.Matrix.mul_beam
        raytracing.ray

        Notes
        -----
        If the ray is beyond the aperture diameter it is labelled
        as "isBlocked = True" but the propagation can still be calculated.
        """

        outputRay = Ray()

        if rightSideRay.isNotBlocked:
            outputRay.y = self.A * rightSideRay.y + self.B * rightSideRay.theta
            outputRay.theta = self.C * rightSideRay.y + self.D * rightSideRay.theta
            outputRay.z = self.L + rightSideRay.z
            outputRay.apertureDiameter = self.apertureDiameter

            if abs(rightSideRay.y) > abs(self.apertureDiameter / 2.0):
                outputRay.isBlocked = True
            else:
                outputRay.isBlocked = rightSideRay.isBlocked
        else:
            outputRay = rightSideRay

        return outputRay

    def mul_beam(self, rightSideBeam):
        """This function calculates the multiplication of a coherent beam with complex radius
        of curvature q by an ABCD matrix.

        Parameters
        ----------
        rightSideBeam : object from GaussianBeam class
            including the beam properties


        Returns
        -------
        outputBeam : object from GaussianBeam class
            The properties of the beam at the output of the system with the defined ABCD matrix

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=10)
        >>> M1= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=5,label='Lens')
        >>> # B is a Gaussian Beam
        >>> B=GaussianBeam(q=complex(1,1),w=1,R=5,n=1)
        >>> print('The output properties of are:' , M1.mul_beam(B))
        The output ray of Lens M1 : Complex radius: (0.976+1.22j)
        w(z): 0.020, R(z): 2.500, z: 5.000, λ: 632.8 nm
        zo: 1.220, wo: 0.016, wo position: -0.976

        See Also
        --------
        raytracing.Matrix.mul_matrix
        raytracing.Matrix.mul_ray
        raytracing.GaussianBeam
        """
        q = rightSideBeam.q
        if rightSideBeam.n != self.frontIndex:
            msg = "The gaussian beam is not tracking the index of refraction properly {0} {1}".format(
                rightSideBeam.n, self.frontIndex)
            warnings.warn(msg, UserWarning)

        qprime = (complex(self.A) * q + complex(self.B)) / (complex(self.C) * q + complex(self.D))

        outputBeam = GaussianBeam(q=qprime, wavelength=rightSideBeam.wavelength)
        outputBeam.z = self.L + rightSideBeam.z
        outputBeam.n = self.backIndex

        if abs(outputBeam.w) > self.apertureDiameter / 2:
            outputBeam.isClipped = True
        else:
            outputBeam.isClipped = rightSideBeam.isClipped

        return outputBeam

    @property
    def largestDiameter(self):
        """ Largest diameter for a group of elements

        Returns
        -------
        LargestDiameter : float
            Largest diameter of the element or group of elements. For a `Matrix`
            this will simply be the aperture diameter of this element.
        """
        return self.apertureDiameter

    def hasFiniteApertureDiameter(self):
        """If the system has a finite aperture size

        Returns
        -------
        apertureDiameter : bool
            If True, the element or group of elements have a finite aperture size
        """
        return self.apertureDiameter != float("+Inf")

    def transferMatrix(self, upTo=float('+Inf')):
        r""" The Matrix() that corresponds to propagation from the edge
        of the element (z=0) up to distance "upTo" (z=upTo). If no parameter is
        provided, the transfer matrix will be from the front edge to the back edge.
        If the element has a null thickness, the matrix representing the element
        is returned.

        Parameters
        ----------
        upTo : float
            A distance that shows the propagation length (default=Inf)

        Returns
        -------
        tramsferMatrix : object from Matrix class
            The matrix for the propagation length through the system

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=2)
        >>> M1= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> transferM=M1.transferMatrix(upTo=5)
        >>> print('The transfer matrix is:', transferM)
        The transfer matrix is:
         /             \
        |  1.000    0.000 |
        |               |
        | -0.100    1.000 |
         \             /
        f=10.000

        See Also
        --------
        raytracing.Matrix.transferMatrices

        Notes
        -----
        The upTo parameter should have a value greater than the physical distance of the system.
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

    def lagrangeInvariant(self, ray1, ray2, z=0):
        """ The Lagrange invariant is a quantity that is conserved
        for any two rays in the system. It is often seen with the
        chief ray and marginal ray in an imaging system, but it is
        actually very general and any two rays can be used.
        In ImagingPath(), if no rays are provided, the chief and
        marginal rays are used.

        Parameters
        ----------
        ray1 : object of Ray class
            A ray at height y1 and angle theta1
        ray2 : object of Ray class
            A ray at height y2 and angle theta2
        z : float
            A distance that shows propagation length

        Returns
        -------
        lagrangeInvariant : float
            The value of the lagrange invariant constant for ray1 and ray2

        Examples
        --------
        >>> from raytracing import *
        >>> # M is an ABCD matrix of a lens (f=10)
        >>> M= Matrix(A=1,B=0,C=-1/10,D=1,label='Lens')
        >>> # R1 and R2 are two rays
        >>> R1=Ray(y=5,theta=20)
        >>> R2=Ray(y=2,theta=10)
        >>> LagrangeInv=M.lagrangeInvariant(R1,R2)
        >>> print('The lagrange invariant value for R1 and R2 is:', LagrangeInv)
        The lagrange invariant value for R1 and R2 is: -10.0

        See Also
        --------
        raytracing.Matrix.transferMatrices
        raytracing.ImagingPath.lagrangeInvariant

        Notes
        -----
        To use this function, the physicalLength of the system should be zero.
        """

        matrix = self.transferMatrix(upTo=z)

        outputRay1 = matrix.traceThrough(ray1)
        outputRay2 = matrix.traceThrough(ray2)

        return matrix.backIndex * (outputRay1.theta * outputRay2.y - outputRay1.y * outputRay2.theta)

    def trace(self, ray):
        """The ray matrix formalism, through multiplication of a ray by 
        a matrix, will give the correct ray but will never consider apertures.
        By "tracing" a ray, we explicitly consider all apertures in the system.
        If a ray is blocked, its property isBlocked will be true, and
        isNotBlocked will be false.

        Because we want to manage blockage by apertures, we need to perform a two-step process
        for elements that have a finite, non-null length: where is the ray blocked exactly?
        It can be blocked at the entrance, at the exit, or anywhere in between.
        The aperture diameter for a finite-length element is constant across the length
        of the element. We therefore check before entering the element and after having
        propagated through the element. For now, this will suffice.

        Parameters
        ----------
        ray : object of Ray class
            A ray at height y and angle theta

        Returns
        -------
        rayTrace : List of ray(s)
            A list of rays (i.e. a ray trace) for the input ray through the matrix. 

        Examples
        --------
        >>> from raytracing import *
        >>> # M is an ABCD matrix of a lens (f=10)
        >>> M= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=0,label='Lens')
        >>> # R1 is a ray
        >>> R1=Ray(y=5,theta=20)
        >>> Tr=M.trace(R1)
        >>> print('the height of traced ray is' , Tr[0].y,  'and the angle is', Tr[0].theta)
        the height of traced ray is 5.0 and the angle is 19.5

        See Also
        --------
        raytracing.Matrix.traceThrough
        raytracing.Matrix.mul_ray

        Notes
        -----
        Currently, the output of the function is returned as a list. It is
        sufficient to trace (i.e. display) the ray to draw lines between the points.
        For some elements, (zero physical length), there will be a single element. For
        other elements there may be more.  For groups of elements, there can be any 
        number of rays in the list.

        If you only care about the final ray that has propagated through, use 
        `traceThrough()`
        """

        rayTrace = []
        if isinstance(ray, Ray):
            if self.L > 0:
                if abs(ray.y) > self.apertureDiameter / 2:
                    ray.isBlocked = True
                rayTrace.append(ray)

        rayTrace.append(self * ray)

        return rayTrace

    def traceThrough(self, inputRay):
        """Contrary to trace(), this only returns the last ray.
        Mutiplying the ray by the transfer matrix will give the correct ray
        but will not consider apertures.  By "tracing" a ray, we do consider
        all apertures in the system.

        Parameters
        ----------
        inputRay : object of Ray class
            A ray at height y and angle theta

        Returns
        -------
        rayTrace : object of Ray class
            The height and angle of the last ray after propagating through the system,
            including apertures.

        Examples
        --------
        >>> from raytracing import *
        >>> # M is an ABCD matrix of a lens (f=10)
        >>> M= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> # R1 is a ray
        >>> R1=Ray(y=5,theta=20)
        >>> Tr=M.traceThrough(R1)
        >>> print('the height of traced ray is' , Tr.y,  'and the angle is', Tr.theta)
        the height of traced ray is 5.0 and the angle is 19.5

        See Also
        --------
        raytracing.Matrix.trace
        raytracing.Matrix.traceMany

        Notes
        -----
        If a ray is blocked, its property isBlocked will be true, and isNotBlocked will be false.
        """

        rayTrace = self.trace(inputRay)
        return rayTrace[-1]

    def traceMany(self, inputRays):
        r"""This function trace each ray from a group of rays from front edge of element to
        the back edge. It can be either a list of Ray(), or a Rays() object:
        the Rays() object is an iterator and can be used like a list.

        Parameters
        ----------
        inputRays : object of Ray class
            A List of rays, each object includes two ray. The fisr is the properties
            of the input ray and the second is the properties of the output ray.

        Returns
        -------
        rayTrace : object of Ray class
            List of Ray() (i,e. a raytrace), one for each input ray.

        Examples
        --------
        First, a list of 10 uniformly distributed random ray is generated
        and then the output of the system for the rays are calculated.

        >>> from raytracing import *
        >>> # M is an ABCD matrix of a lens (f=10)
        >>> M= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> # inputRays is a group of random rays with uniform distribution at center
        >>> nRays = 10
        >>> inputRays = RandomUniformRays(yMax=0, maxCount=nRays)
        >>> Tr=M.traceMany(inputRays)
        >>> #index[0] of the first object in the list is the first input
        >>> print('The properties of the first input ray:', Tr[0][0])
        The properties of the first input ray:
         /       \
        |  0.000  |
        |         |
        |  1.113  |
         \       /
        z = 0.000

        >>> #index[1] of the first object in the list is the first output
        >>> print('The properties of the first output ray:', Tr[0][1])
        The properties of the first output ray:
         /       \
        |  0.000  |
        |         |
        |  1.113  |
         \       /
        z = 2.000

        See Also
        --------
        raytracing.Matrix.trace
        raytracing.Matrix.traceThrough
        raytracing.Matrix.traceManyThrough
        """
        manyRayTraces = []
        for inputRay in inputRays:
            rayTrace = self.trace(inputRay)
            manyRayTraces.append(rayTrace)

        return manyRayTraces

    def traceManyThrough(self, inputRays, progress=True):
        """This function trace each ray from a list or a Rays() distribution from
        front edge of element to the back edge.
        Input can be either a list of Ray(), or a Rays() object:
        the Rays() object is an iterator and can be used like a list of rays.
        UniformRays, LambertianRays() etc... can be used.

        Parameters
        ----------
        inputRays : object of Ray class
            A group of rays
        progress : bool
            if True, the progress of the raceTrough is shown (default=Trye)


        Returns
        -------
        outputRays : object of Ray class
            List of Ray() (i,e. a raytrace), one for each input ray.

        Examples
        --------
        >>> from raytracing import *
        >>> # M is an ABCD matrix of a lens (f=10)
        >>> M= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> # inputRays is a group of random rays with uniform distribution at center
        >>> nRays = 3
        >>> inputRays = RandomUniformRays(yMax=5, yMin=0, maxCount=nRays)
        >>> Tr=M.traceManyThrough(inputRays)
        >>> print('heights of the output rays:', Tr.yValues)
        heights of the output rays: [4.323870378874155, 2.794064779525441, 0.7087442942835853]

        >>>> print('angles of the output rays:', Tr.thetaValues)
        angles of the output rays: [-1.499826089814585, 0.7506850963379516, -0.44348989046728904]

        See Also
        --------
        raytracing.Matrix.traceThrough
        raytracing.Matrix.traceMany

        Notes
        -----
        We assume that if the user will be happy to receive
        Rays() as an output even if they passed a list of rays as inputs.
        """

        try:
            iter(inputRays)
        except TypeError:
            raise TypeError("'inputRays' argument is not iterable.")

        if not isinstance(inputRays, Rays):
            inputRays = Rays(inputRays)

        outputRays = Rays()

        for ray in inputRays:
            lastRay = self.traceThrough(ray)
            if lastRay.isNotBlocked:
                outputRays.append(lastRay)

            if progress:
                inputRays.displayProgress()

        return outputRays

    def traceManyThroughInParallel(self, inputRays, progress=True, processes=None):
        """ This is an advanced technique to gain from parallel computation:
        it is the same as traceManyThrough(), but splits this call in
        several other parallel processes using the `multiprocessing` module,
        which is os-independent.

        Everything hinges on a simple pool.map() command that will apply 
        the provided function to every element of the array, but across several
        processors. It is trivial to implement and the benefits are simple:
        if you create 8 processes on 8 CPU cores, you gain a factor of 
        approximately 8 in speed. We are not talking GPU acceleration, but
        still: 1 minute is shorter than 8 minutes.

        Parameters
        ----------
        inputRays : object of Ray class
            A group of rays
        progress : bool
            If True, the progress in percentage of the traceTrough is shown (default=True)

        Returns
        -------
        outputRays : object of Ray class
            List of Ray() (i,e. a raytrace), one for each input ray.

        See Also
        --------
        raytracing.Matrix.traceManyThrough
        raytracing.Matrix.traceMany

        Notes
        -----
        One important technical issue: Pool accesses the array in multiple processes
        and cannot be dynamically generated (because it is not thread-safe).
        We explicitly generate the list before the computation, then we split
        the array in #processes different lists.
        """

        if processes is None:
            processes = multiprocessing.cpu_count()

        theExplicitList = list(inputRays)
        manyInputRays = [(theExplicitList[i::processes], progress) for i in range(processes)]

        with multiprocessing.Pool(processes=processes) as pool:
            outputRays = pool.starmap(self.traceManyThrough, manyInputRays)

        outputRaysList = []
        for rays in outputRays:
            outputRaysList += rays.rays

        return Rays(rays=outputRaysList)

    @property
    def isImaging(self):
        """If B=0, then the matrix represents that transfer from a conjugate
        plane to another (i.e. object at the front edge and image at the
        back edge).

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=10)
        >>> M1= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> print('isImaging:' , M1.isImaging)
        isImaging: True

        >>> # M2 is an ABCD matrix of free space (d=2)
        >>> M2= Matrix(A=1,B=2,C=0,D=1,physicalLength=2,label='Lens')
        >>> print('isImaging:' , M2.isImaging)
        isImaging: False

        Notes
        -----
        In this case:
        A = transverse magnification
        D = angular magnification
        And as usual, C = -1/f (always).
        """

        return isAlmostZero(self.B, self.__epsilon__)

    @property
    def hasPower(self):
        """ If True, then there is a non-null focal length because C!=0. We compare to an epsilon value, because
        computational errors can occur and lead to C being very small, but not 0.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=10)
        >>> M1= Matrix(A=1,B=0,C=-1/10,D=1,physicalLength=2,label='Lens')
        >>> print('hasPower:' , M1.hasPower)
        hasPower: True

        >>> # M2 is an ABCD matrix of free space (d=2)
        >>> M2= Matrix(A=1,B=2,C=0,D=1,physicalLength=2,label='Lens')
        >>> print('hasPower:' , M2.hasPower)
        hasPower: False
        """
        return isNotZero(self.C, self.__epsilon__)

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
        """ This is the synonym of effectiveFocalLengths()

        Returns
        -------
        focalDistances : array
            Returns the effective focal lengths on either side.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=0,label='Lens')
        >>> f1=M1.focalDistances()
        >>> print('focal distances:' , f1)
        focal distances: (5.0, 5.0)

        This function has the same out put as effectiveFocalLengths()

        >>> f2=M1.effectiveFocalLengths()
        >>> print('focal distances:' , f2)
        focal distances: (5.0, 5.0)
        """

        return self.effectiveFocalLengths()

    def effectiveFocalLengths(self):
        """ The effective focal lengths calculated from the power (C)
        of the matrix.

        There are in general two effective focal lengths: front effective
        and back effective focal lengths (not to be confused with back focal
        and front focal lengths which are measured from the physical interface).
        The easiest way to calculate this is to use
        f = -1/C for current matrix, then flipOrientation and f = -1/C


        Returns
        -------
        effectiveFocalLengths : array
            Returns the effective focal lengths in the forward and backward
            directions. When in air, both are equal.

        See Also
        --------
        raytracing.Matrix.focalDistances

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=0,label='Lens')
        >>> f2=M1.effectiveFocalLengths()
        >>> print('focal distances:' , f2)
        focal distances: (5.0, 5.0)

        This function has the same out put as effectiveFocalLengths()
        >>> f1=M1.focalDistances()
        >>> print('focal distances:' , f1)
        focal distances: (5.0, 5.0)

        """
        if self.hasPower:
            focalLength2 = -1.0 / self.C  # left (n1) to right (n2)
            focalLength1 = -(self.frontIndex / self.backIndex) / self.C  # right (n2) to left (n2)
        else:
            focalLength1 = float("+Inf")
            focalLength2 = float("+Inf")

        return (focalLength1, focalLength2)

    def backFocalLength(self):
        """ The focal lengths measured from the back vertex.
        This is the distance between the surface and the focal point.
        When the principal plane is not at the surface (which is usually
        the case in anything except a thin lens), the back and front focal
        lengths will be different from effective focal lengths. The effective
        focal lengths is always measured from the principal planes, but the
        BFL and FFL are measured from the vertex.

        Returns
        -------
        backFocalLength : float
            Returns the BFL

        Examples
        --------
        Since this function returns the BFL, if the focal distance of an object is 5
        and the back vertex is 2, we expect to have back focal length of 3, as the following example:

        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=0,backVertex=2,label='Lens')
        >>> BFL=M1.backFocalLength()
        >>> print('the back focal distance:' , BFL)
        the back focal distance: 3.0

        See Also
        --------
        raytracing.Matrix.focalDistances
        raytracing.Matrix.effectiveFocalLengths
        raytracing.Matrix.frontFocalLength


        Notes
        -----
        If the matrix is the result of the product of several matrices,
        we may not know where the front and back vertices are. In that case,
        we return None (or undefined).

        The front and back focal lengths will be different if the index
        of refraction is different on both sides.
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

        Returns
        -------
        frontFocalLength : float
            Returns the FFL

        Examples
        --------
        In the following example, we have defined an object(f=5) with physical length of 4.
        And the front vertex is placed one unit before the front principal plane.
        There for the front focal length will be 4.

        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=4,frontVertex=-1,label='Lens')
        >>> FFL=M1.frontFocalLength()
        >>> print('the front focal distance:' , FFL)
        the front focal distance: 4.0

        See Also
        --------
        raytracing.Matrix.focalDistances
        raytracing.Matrix.effectiveFocalLengths
        raytracing.Matrix.backFocalLength


        Notes
        -----
        If the matrix is the result of the product of several matrices,
        we may not know where the front and back vertices are. In that case,
        we return None (or undefined).

        The front and back focal lengths will be different if the index
        of refraction is different on both sides.
        """

        if self.frontVertex is not None and self.hasPower:
            (f1, f2) = self.effectiveFocalLengths()
            (p1, p2) = self.principalPlanePositions(z=0)

            return -(p1 - f1 - self.frontVertex)
        else:
            return None

    def focusPositions(self, z):
        """ Positions of both focal points on either side of the element.

        The front and back focal spots will be different if the index
        of refraction is different on both sides.

        Parameters
        ----------
        z : float
            Position from where the positions are calculated

        Returns
        -------
        focusPositions : array
            An array of front focal position and the back focal position.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=4,frontVertex=-1,backVertex=5,label='Lens')
        >>> Position0=M1.focusPositions(z=0)
        >>> print('focal positions (F,B):' , Position0)
        focal positions (F,B): (-5.0, 9.0)

        And if we move object 2 units:

        >>> Position2=M1.focusPositions(z=2)
        >>> print('focal positions (F,B):' , Position2)
        focal positions (F,B): (-3.0, 11.0)

        See Also
        --------
        raytracing.Matrix.effectiveFocalLengths
        raytracing.Matrix.principalPlanePositions
        """

        if self.hasPower:
            (f1, f2) = self.focalDistances()
            (p1, p2) = self.principalPlanePositions(z)
            return (p1 - f1, p2 + f2)
        else:
            return (None, None)

    def principalPlanePositions(self, z):
        """ Positions of the input and output principal planes.

        Parameters
        ----------
        z : float
            Position from where the positions are calculated

        Returns
        -------
        principalPlanePositions : array
            An array of front principal plane position and the back principal plane position.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of a lens (f=5)
        >>> M1= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=3,frontVertex=-1,backVertex=5,label='Lens')
        >>> Position0=M1.principalPlanePositions(z=0)
        >>> print('PP positions (F,B):' , Position0)
        PP positions (F,B): (0.0, 3.0)

        See Also
        --------
        raytracing.Matrix.effectiveFocalLengths
        raytracing.Matrix.focusPositions
        """
        if self.hasPower:
            p1 = z - (self.frontIndex / self.backIndex - self.D) / self.C
            p2 = z + self.L + (1 - self.A) / self.C
        else:
            p1 = None
            p2 = None

        return (p1, p2)

    def forwardConjugate(self):
        r""" With an object at the front edge of the element, where
        is the image? Distance after the element by which a ray
        must travel to reach the conjugate plane of the front of
        the element. A positive distance means the image is "distance"
        beyond the back of the element (or to the right, or after).

        Returns
        -------
        forwardConjugate : object
            index [0] output object is the distance of the image at the back of the element
             and index [1] is the conjugate matrix.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of an object
        >>> M1= Matrix(A=1,B=-2,C=3,D=1,physicalLength=0,label='Lens')
        >>> Image=M1.forwardConjugate()
        >>> print('The position of the image:' , Image[0])
        The position of the image: 2.0

        And to see the conjugate matrix you can call index 1 of the output.

        >>> print('conjugate matrix:' , Image[1])
        conjugate matrix:
         /               \
        |  7.000    0.000 |
        |                 |
        |  3.000    1.000 |
         \               /
        f=-0.333

        See Also
        --------
        raytracing.Matrix.backwardConjugate

        Notes
        -----
        M2 = Space(distance)*M1
        M2.isImaging == True

        """

        if self.D == 0:
            distance = float("+inf")
            conjugateMatrix = None  # Unable to compute with inf
        else:
            distance = -self.B / self.D
            conjugateMatrix = Space(d=distance, n=self.backIndex) * self

        return (distance, conjugateMatrix)

    def backwardConjugate(self):
        r""" With an image at the back edge of the element,
        where is the object ? Distance before the element by
        which a ray must travel to reach the conjugate plane at
        the back of the element. A positive distance means the
        object is "distance" in front of the element (or to the
        left, or before).

        Returns
        -------
        backwardConjugate : object
            index [0] output object is the distance of the image in front of the element
             and index [1] is the conjugate matrix.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of an object
        >>> M1= Matrix(A=1,B=-3,C=1,D=1,physicalLength=0,label='Lens')
        >>> Image=M1.backwardConjugate()
        >>> print('The position of the image:' , Image[0])
        The position of the image: 3.0

        And to see the conjugate matrix you can call index 1 of the output.

        >>> print('conjugate matrix:' , Image[1])
        conjugate matrix:
         /               \
        |  1.000    0.000 |
        |                 |
        |  1.000    4.000 |
         \               /
        f=-1.000


        See Also
        --------
        raytracing.Matrix.forwardConjugate

        Notes
        -----
        M2 = M1*Space(distance)
        M2.isImaging == True
        """
        if self.A == 0:
            return (float("+inf"), None)
        distance = -self.B / self.A
        conjugateMatrix = self * Space(d=distance)
        return (distance, conjugateMatrix)

    def magnification(self):
        """The magnification of the element

        Returns
        -------
        magnification : array
            index [0] output object is A in the matrix and
            index [1] is D in the matrix.

        Examples
        --------
        >>> from raytracing import *
        >>> # M1 is an ABCD matrix of an object
        >>> Mat= Matrix(A=2,B=0,C=1,D=3,physicalLength=0,label='Lens')
        >>> M=Mat.magnification()
        >>> print('(A , D): (',M[0],',',M[1],')')
        (A , D): ( 2.0 , 3.0 )


        See Also
        --------
        raytracing.Matrix

        Notes
        -----
        The magnification can be calculated having both A and D.
        """

        if self.isImaging:
            return (self.A, self.D)
        else:
            return (None, None)

    def flipOrientation(self):
        """We flip the element around (as in, we turn a lens around front-back).
        This is useful for real elements and for groups.

        Returns
        -------
        Matrix : object of Matrix class
            An element with the properties of the flipped original element

        Examples
        --------
        >>> # Mat is an ABCD matrix of an object
        >>> Mat= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=2,frontVertex=-1,backVertex=2,label='Lens')
        >>> Mat.display()
        >>> flippedMat=Mat.flipOrientation()
        >>> flippedMat.display()

        The original object:

        .. image:: flipOrientation_before.png
            :width: 70%
            :align: center

        The flipped object:

        .. image:: flipOrientation_after.png
            :width: 70%
            :align: center


        See Also
        --------
        raytracing.Matrix

        Notes
        -----
        For individual objects, it does not do anything because they are the same either way.
        However, subclasses can override this function and act accordingly.
        """
        self.isFlipped = not self.isFlipped
        # First and last interfaces. Used for BFL and FFL
        tempVertex = self.backVertex
        self.backVertex = self.frontVertex
        self.frontVertex = tempVertex

        # Index of refraction at entrance and exit.
        tempIndex = self.frontIndex
        self.frontIndex = self.backIndex
        self.backIndex = tempIndex

        return self

    def displayHalfHeight(self, minSize=0):
        """ A reasonable height for display purposes for
        an element, whether it is infinite or not.
        If the element is infinite, the half-height is currently
        set to '4' or to the specified minimum half height.
        If not, it is the apertureDiameter/2.
        Parameters
        ----------
        minSize : float
            The minimum size to be considered as the aperture half height
        Returns
        -------
        halfHeight : float
            The half height of the optical element
        """
        halfHeight = 4  # FIXME: keep a minimum half height when infinite ?
        if minSize > halfHeight:
            halfHeight = minSize
        if self.apertureDiameter != float('+Inf'):
            halfHeight = self.apertureDiameter / 2.0  # real half height
        return halfHeight

    def display(self):
        from .figure import Graphic
        return Graphic(self).display()

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

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.__dict__ == other.__dict__
        return False


class Lens(Matrix):
    r"""A thin lens of focal f, null thickness and infinite or finite diameter

    Parameters
    ----------
    f : float
        The focal length of the lens
    diameter : float
        The diameter (default=Inf)
    label : string
        The label of the lens

    Examples
    --------
    >>> from raytracing import *
    >>> #define a lens with f=5 and diameter 20
    >>> L=Lens(f=5,diameter=20,label='Lens')
    >>> print('The transfer matrix of Lens :', L)
    The transfer matrix of Lens :
     /             \
    |  1.000    0.000 |
    |               |
    | -0.200    1.000 |
     \             /
    f=5.000
    """

    def __init__(self, f, diameter=float('+Inf'), label=''):
        super(Lens, self).__init__(A=1, B=0, C=-1 / float(f), D=1,
                                   physicalLength=0,
                                   apertureDiameter=diameter,
                                   frontVertex=0,
                                   backVertex=0,
                                   label=label)

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:

        Parameters
        ----------
        z : float
            Position of the lens

        Returns
        -------
        pointsOfInterest : List
            List of points of interest for the input element

        """
        (f1, f2) = self.focusPositions(z)

        pointsOfInterest = []
        if f1 is not None:
            pointsOfInterest.append({'z': f1, 'label': '$F_f$'})
        if f2 is not None:
            pointsOfInterest.append({'z': f2, 'label': '$F_b$'})

        return pointsOfInterest


class CurvedMirror(Matrix):
    r"""A curved mirror of radius R and infinite or finite diameter.

    Parameters
    ----------
    R : float
        the radius of curvature of the mirror
    diameter : float
        The diameter of the element (default=Inf)
    label : string
        The label of the curved mirror

    Examples
    --------
    >>> from raytracing import *
    >>> #define a curved mirror with R=5 and diameter 20
    >>> M=CurvedMirror(R=5,diameter=20,label='curved mirror')
    >>> print('The transfer matrix of curved mirror :' ,M)
    The transfer matrix of curved mirror :
     /             \
    |  1.000    0.000 |
    |               |
    | -0.400    1.000 |
     \             /
    f=2.500


    Notes
    -----
    A concave mirror (i.e. converging mirror) has a negative
    radius of curvature if we want to keep the same sign convention.
    (there was a mistake up to version 1.2.7 of the module)
    """

    def __init__(self, R, diameter=float('+Inf'), label=''):
        warnings.warn("The sign of the radius of curvature in CurvedMirror was changed \
in version 1.2.8 to maintain the sign convention", UserWarning)
        super(CurvedMirror, self).__init__(A=1, B=0, C=2 / float(R), D=1,
                                           physicalLength=0,
                                           apertureDiameter=diameter,
                                           frontVertex=0,
                                           backVertex=0,
                                           label=label)

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:

        Parameters
        ----------
        z : float
            Position of the lens

        Returns
        -------
        pointsOfInterest : List
            List of points of interest for the input element

        """
        (f1, f2) = self.focusPositions(z)

        pointsOfInterest = []
        if f1 is not None:
            pointsOfInterest.append({'z': f1, 'label': '$F_f$'})
        if f2 is not None:
            pointsOfInterest.append({'z': f2, 'label': '$F_b$'})

        return pointsOfInterest

    def flipOrientation(self):
        """ This function flips the element around (as in, we turn a lens around front-back).

        Notes
        -----
        In this case, R -> -R.  It is important to call the
        super implementation because other things must be flipped (vertices for instance)
        """
        super(CurvedMirror, self).flipOrientation()

        self.C = - self.C
        return self


class Space(Matrix):
    r"""Free space of length d

    Parameters
    ----------
    d : float
        the length of the free space
    n : float
        The refraction index of the space. This value cannot be negative. (default=1)
    diameter : float
        The diameter of the free space (default=Inf)
    label : string
        The label of the free space

    Examples
    --------
    >>> from raytracing import *
    >>> #define a free space of length 3, refraction index 1 and diameter 20
    >>> S=Space(d=3,n=1,diameter=20,label='free space')
    >>> print('The transfer matrix of free space :' ,S)
    The transfer matrix of free space :
     /             \
    |  1.000    3.000 |
    |               |
    |  0.000    1.000 |
     \             /
    f = +inf (afocal)
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

    def transferMatrix(self, upTo=float('+Inf')):
        """ Returns a Matrix() corresponding to a partial propagation
        if the requested distance is smaller than the length of this element

        Parameters
        ----------
        upTo : float
            The length of the propagation (default=Inf)

        Returns
        -------
        transferMatrix : object of class Matrix
            the corresponding matrix to the propagation

        """
        distance = upTo
        if distance < self.L:
            return Space(distance, self.frontIndex)
        else:
            return self


class DielectricInterface(Matrix):
    """A dielectric interface of radius R, with an index n1 before and n2
    after the interface

    Parameters
    ----------
    n1 : float
        The refraction index before the surface
    n2 : float
        The refraction index after the interface
    R : float (Optional)
        The radius of the dielectric interface

    Notes
    -----
    A convex interface from the perspective of the ray has R > 0
    """

    def __init__(self, n1, n2, R=float('+Inf'),
                 diameter=float('+Inf'), label=''):
        self.n1 = n1
        self.n2 = n2
        self.R = R
        a = 1.0
        b = 0.0
        c = - (n2 - n1) / (n2 * R)
        d = n1 / n2

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

        Notes
        -----
        This is useful for real elements and for groups. For individual objects,
        it does not do anything because they are the same either way. However,
        subclasses can override this function and act accordingly.
        """
        super(DielectricInterface, self).flipOrientation()

        temp = self.n1
        self.n1 = self.n2
        self.n2 = temp
        self.R = -self.R
        self.C = - (self.n2 - self.n1) / (self.n2 * self.R)
        self.D = self.n1 / self.n2

        return self


class ThickLens(Matrix):
    r"""A thick lens of first radius R1 and then R2, with an index n
    and length d

    Parameters
    ----------
    n : float
        The refraction index of the thick lens. This value cannot be negative.
    R1 : float
        The first radius of thick lens
    R2 : float
        The second radius of the thick lens
    thickness : float
        The length of the thick lens. This value cannot be negative.
    diameter : float (Optional)
        The diameter of the thick lens. (default=Inf)
    label : string (Optional)
        The label of the thick lens

    Examples
    --------
    >>> from raytracing import *
    >>> #define a thick lens with desired parameters
    >>> TLens=ThickLens(n=1.5,R1=4,R2=6,thickness=3,diameter=20,label='thick lens')
    >>> print('The transfer matrix of thick lens :' ,TLens)
    The transfer matrix of thick lens :
     /             \
    |  0.750    2.000 |
    |               |
    | -0.062    1.167 |
     \             /
    f=16.000


    Notes
    -----
    A biconvex lens has R1 > 0 and R2 < 0.
    """

    def __init__(self, n, R1, R2, thickness, diameter=float('+Inf'), label=''):
        self.R1 = R1
        self.R2 = R2
        self.n = n

        t = thickness

        a = t * (1.0 - n) / (n * R1) + 1
        b = t / n
        c = - (n - 1.0) * (1.0 / R1 - 1.0 / R2 + t * (n - 1.0) / (n * R1 * R2))
        d = t * (n - 1.0) / (n * R2) + 1
        super(ThickLens, self).__init__(A=a, B=b, C=c, D=d,
                                        physicalLength=thickness,
                                        apertureDiameter=diameter,
                                        frontVertex=0,
                                        backVertex=thickness,
                                        label=label)

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:

        Parameters
        ----------
        z : float
            Position of the element

        Returns
        -------
        pointsOfInterest : List
            List of points of interest for the input element
        """
        (f1, f2) = self.focusPositions(z)

        pointsOfInterest = []
        if f1 is not None:
            pointsOfInterest.append({'z': f1, 'label': '$F_f$'})
        if f2 is not None:
            pointsOfInterest.append({'z': f2, 'label': '$F_b$'})

        return pointsOfInterest

    def transferMatrix(self, upTo=float('+Inf')):
        """ Returns a ThickLens() or a Matrix() corresponding to a partial propagation
        if the requested distance is smaller than the length of this element

        Parameters
        ----------
        upTo : float
            The length of the propagation (default=Inf)

        Returns
        -------
        transferMatrix : object of class Matrix
            the corresponding matrix to the propagation

        """
        if self.L <= upTo:
            return self
        else:
            return Space(upTo, self.n, self.apertureDiameter) * DielectricInterface(1.0, self.n, self.R1,
                                                                                    self.apertureDiameter)

    def flipOrientation(self):
        """ We flip the element around (as in, we turn a lens around front-back).

        Notes
        -----
        In this case, R1 = -R2, and R2 = -R1.  It is important to call the
        super implementation because other things must be flipped (vertices for instance)
        """
        super(ThickLens, self).flipOrientation()

        temp = self.R1
        self.R1 = -self.R2
        self.R2 = -temp

        R1 = self.R1
        R2 = self.R2
        t = self.L
        n = self.n

        self.A = t * (1.0 - n) / (n * R1) + 1
        self.B = t / n
        self.C = - (n - 1.0) * (1.0 / R1 - 1.0 / R2 + t * (n - 1.0) / (n * R1 * R2))
        self.D = t * (n - 1.0) / (n * R2) + 1
        return self


class DielectricSlab(ThickLens):
    r"""A slab of dielectric material of index n and length d, with flat faces

    Parameters
    ----------
    n : float
        The refraction index of the dielectric. This value cannot be negative
    thickness : float
        The thickness of the dielectric
    diameter : float
        The diameter of the dielectric. (default=Inf)
    label : string
        the label of the element

    Examples
    --------
    >>> from raytracing import *
    >>> #define a dielectric with refraction index of 1.5
    >>> D=DielectricSlab(n=1.5,thickness=5,diameter=20,label='Dielectric')
    >>> print('The transfer matrix of dielectric slab :' ,D)
    The transfer matrix of dielectric slab :
     /                \
    |  1.000    3.333 |
    |                 |
    | -0.000    1.000 |
     \               /
    f = +inf (afocal)
    """

    def __init__(self, n, thickness, diameter=float('+Inf'), label=''):
        super(DielectricSlab, self).__init__(n=n, R1=float("+Inf"),
                                             R2=float("+Inf"),
                                             thickness=thickness,
                                             diameter=diameter,
                                             label=label)

    def transferMatrix(self, upTo=float('+Inf')):
        """ Returns a either DielectricSlab() or a Matrix() corresponding to a partial propagation
                if the requested distance is smaller than the length of this element

        Parameters
        ----------
        upTo : float
            The length of the propagation (default=Inf)

        Returns
        -------
        transferMatrix : object of class Matrix
            the corresponding matrix to the propagation

        """
        if self.L <= upTo:
            return self
        else:
            return Space(upTo, self.n, self.apertureDiameter) * DielectricInterface(1.0, self.n, float("+inf"),
                                                                                    self.apertureDiameter)


class Aperture(Matrix):
    r"""An aperture of finite diameter, null thickness.

    Parameters
    ----------
    diameter : float
        The diameter of the aperture to be considered
    label : string
        The label of the aperture

    Examples
    --------
    >>> from raytracing import *
    >>> #define an aperture of diameter 10
    >>> A=Aperture(diameter=10,label='aperture')
    >>> print('The transfer matrix of aperture :' ,A)
    The transfer matrix of aperture :
     /                \
    |  1.000    0.000 |
    |                 |
    |  0.000    1.000 |
     \               /
    f = +inf (afocal)

    Notes
    -----
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
