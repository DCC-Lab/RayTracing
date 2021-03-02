from typing import Any, Union, List
from .figure import Figure
from .matrixgroup import *
from .ray import *
import numpy as np

""" We start with general, useful namedtuples to simplify management of values """
from typing import NamedTuple

class MarginalRays(NamedTuple):
    up: Ray = None
    down: Ray = None

class Stop(NamedTuple):
    z: float = 0
    diameter: float = None


class ImagingPath(MatrixGroup):
    """ImagingPath: the main class of the module, allowing
    the combination of Matrix() or MatrixGroup() to be used 
    as an imaging group with an object at the beginning.

    Usage is to create the ImagingPath(), then append() elements
    and display(). You may change objectHeight, fanAngle, fanNumber
    and rayNumber.

    Parameters
    ----------
    elements : (Matrix)
        definitiion (default=None).
    label : string
        The label for the imaging path

    Attributes
    ----------
    objectHeight : float
        The full height of object can be defined using this attribute (default=10.0)
    objectPosition : float
        This attribute defines the position of the object which must be defined zero for now. (default=0)
    fanAngle : float
        This value indicates full fan angle in radians for rays (default=0.1)
    fanNumber : int
        This value indicates the number of fans from the object (default=3)
    precision : float
        The accuracy to be considered when calculating the field stop (default=0.001)
    maxHeight : float
        The maximum height to be considered when calculating the field stop (default=10000.0)
    showObject : bool
        If True, the object will be shown on display (default=True)
    showImage : bool
        If True, the image will be shown on display (default=True)
    showEntrancePupil : bool
        If True, the entrance pupil will be shown on display (default=False)
    showElementLabels : bool
        If True, the labels of the elements will be shown on display (default=True)
    showPointsOfInterest : bool
        If True, the points of interests will be shown on display (default=True)
    showPointsOfInterestLabels : bool
        If True, the labels of the points of interests will be shown on display (default=True)
    showPlanesAcrossPointsOfInterest : bool
        If True, the planes across the points of interests will be shown (default=True)

    Examples
    --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> #set the desire properties
        >>> path.objectHeight=4
        >>> path.fanAngle=0.1
        >>> path.fanNumber=5
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> #display the imeging path
        >>> path.display()

        And the following figure will be plotted:

        .. image:: ../images/ImagingPath.png
                    :width: 70%
                    :align: center
    """

    def __init__(self, elements: list = None, label=""):

        self._objectHeight = 10.0  # object height (full).
        self.objectPosition = 0.0  # always at z=0 for now.
        self.fanAngle = 0.1  # full fan angle for rays
        self.fanNumber = 3  # number of points on object
        self.rayNumber = 3  # number of rays in fan

        # Constants when calculating field stop
        self.precision = 0.000001
        self.maxHeight = 10000.0

        # Display properties
        self.figure = Figure(opticalPath=self)
        self.design = self.figure.design
        self.showObject = True
        self.showImages = True
        self.showEntrancePupil = False
        self.showElementLabels = True
        self.showPointsOfInterest = True
        self.showPointsOfInterestLabels = True
        self.showPlanesAcrossPointsOfInterest = True
        super(ImagingPath, self).__init__(elements=elements, label=label)

    @property
    def objectHeight(self):
        """Get or set the object height, at the starting edge of the ImagingPath.
        """
        return self._objectHeight

    @objectHeight.setter
    def objectHeight(self, objectHeight: float):
        """Set the object height, raises an error if negative.
        """
        if objectHeight < 0:
            raise ValueError("The object height can't be negative.")
        self._objectHeight = objectHeight
        self.figure.designParams['limitObjectToFieldOfView'] = False

    def chiefRay(self, y=None):
        r"""This function returns the chief ray for a height y at object.
        The chief ray for height y is the ray that goes
        through the center of the aperture stop.

        Parameters
        ----------
        y : float
            The starting height of the chief ray at the object (default=None)
            If no height is provided, then the function uses the limit of the field of view.

        Returns
        -------
        chiefRay : object of Ray class
            The properties (i.e. height and the angle of the chief ray.)

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=2,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print(path.chiefRay())
        y =  3.333
        theta = -0.167
        z = 0.000

        See Also
        --------
        raytracing.ImagingPath.marginalRays
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.principalRay

        Notes
        -----
        The calculation is simple: obtain the transfer matrix
        to the aperture stop, then we know that the input ray
        (which we are looking for) will end at y=0 at the
        aperture stop.
        If the element B in the transfer matrix for the imaging path
        is zero, there is no value for the height and angle that makes
        a proper chief ray. So the function will return None.
        If there is no aperture stop, there is no chief ray either. None is also returned.
        """
        (stopPosition, stopDiameter) = self.apertureStop()
        if stopPosition is None:
            return None

        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        if transferMatrixToApertureStop.isImaging:
            return None

        if y is None:
            y = self.halfFieldOfView()
            if abs(y) == float("+inf"):
                raise ValueError("Must provide y when the field of view is infinite")

        return Ray(y=y, theta=-A * y / B)

    def principalRay(self):
        """This function returns the principal ray, which is the chief ray 
        for the height y at the edge of the field of view. The chief ray
        is the ray that goes through the center of the aperture stop.

        Returns
        -------
        principalRay : object of Ray class
            The properties (i.e. height and the angle of the principal ray).

        Notes
        -----
        Because of round off errors, we need to double check that the ray 
        really goes through. We lower the height until it does if it 
        initially does not.

        See Also
        --------
        raytracing.ImagingPath.marginalRays
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.chiefRay

        """

        objectEdge = self.halfFieldOfView()
        if objectEdge == float("+inf"):
            return None
        
        return self.chiefRay(y=objectEdge)

    def marginalRays(self, y=0):
        r"""This function calculates the marginal rays for a height y at object.
        The marginal rays for height y are the rays that hit the upper and lower
        edges of the aperture stop. There are always two marginal rays for any
        point on the object.  They are symmetric on either side of the optic axis
        only when y=0, in which case they are called the axial rays (or just axial
        ray).

        Parameters
        ----------
        y : float
            The starting height of the marginal rays at the object (default=0)
            In general, this could be any height, not just y=0. However, we usually
            want y=0 which is implicitly called "the axial ray (of the system)",


        Returns
        -------
        marginalRays : list of object of Ray class
            The properties (i.e. heights and the angles of the marginal rays.).
            If the default value is used at the input (y=0), both rays will be
            symmetrically oriented on either side of the optical axis.

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=2,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print( 'the first marginal ray is:\n', path.marginalRays()[0])
        the first marginal ray is:
         y =  0.000
        theta =  0.050
        z = 0.000
        >>> print( 'the second marginal ray is:\n', path.marginalRays()[1])
        the second marginal ray is:
         y =  0.000
        theta = -0.050
        z = 0.000

        As it can be seen in the example, the marginal rays at y=0 
        are symmetrically oriented on either side of the optical axis.

        See Also
        --------
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.chiefRay
        raytracing.ImagingPath.principalRay

        Notes
        -----
        The calculation is simple: obtain the transfer matrix
        to the aperture stop, then we know that the input ray
        (which we are looking for) will end at y= +/-(diameter/2) at the
        aperture stop. We return the largest (positive) angle first, for
        convenience.

        """
        (stopPosition, stopDiameter) = self.apertureStop()
        if stopPosition is None:
            return MarginalRays(None, None)  # No aperture stop -> no marginal rays

        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        if transferMatrixToApertureStop.isImaging:
            return MarginalRays(None, None)

        thetaUp = (stopDiameter / 2.0 - A * y) / B
        thetaDown = (-stopDiameter / 2.0 - A * y) / B

        if thetaDown > thetaUp:
            (thetaUp, thetaDown) = (thetaDown, thetaUp)

        return MarginalRays(up=Ray(y=y, theta=thetaUp), down=Ray(y=y, theta=thetaDown))

    def axialRay(self):
        """This function returns the axial ray of the system, also known as
        the marginal ray for a point on axis (y=0) at the object.

        Returns
        -------
        axialRay : object of Ray class
            The properties (i.e. height and the angle of the marginal ray).
            Another axial can be obtained with the opposite of the angle.

        See Also
        --------
        raytracing.ImagingPath.marginalRays
        raytracing.ImagingPath.chiefRay
        raytracing.ImagingPath.principalRay
        """
        rayUp, rayDown = self.marginalRays()
        return rayUp

    def fNumber(self):
        """This function returns the f-number of the component or system
        by dividing the diameter of the entrance pupil by the effective
        focal length of the system.

        It is not always appreciated that the f-number of *an optical system*
        is meaningful mostly in "infinite conjugate" situations, that is, 
        when either the object or the image is at infinity. In practice, this means
        with photography and telescopes for example. On the other hand, 
        finite conjugate systems are better described by their NA.
        For elements, we calculate the f-number of lenses by assuming they
        are used with an object at infinity. A system is designed as either a finite-conjugate 
        system or an infinite-conjugate: this is a design decision.
        See Smith "Modern Optical Engineering" Section 6.7 Apertures 
        and Image Illumination.

        Returns
        -------
        fNumber : float
            

        See Also
        --------
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.NA
        """
        (position, pupilDiameter) = self.entrancePupil()
        (focalFront, focalBack) = self.effectiveFocalLengths()
        if pupilDiameter is None:
            return None

        return focalFront/pupilDiameter

    def NA(self):
        """This function returns the numerical aperture of the component
        or imaging system, which is the sin of the axial ray angle, times 
        the index of refraction.

        It is not always appreciated that the NA of an *optical system*
        is meaningful mostly in "finite conjugate" situations, that is, 
        when either the object and the image are at small, finite distances.
        In practice, this means microscope objectives and 4f relays for example.
        On the other hand, infinite conjugate systems are better described
        by their f-number. A system is designed as either a finite-conjugate 
        system or an infinite-conjugate: this is a design decision.
        See Smith "Modern Optical Engineering" Section 6.7 Apertures 
        and Image Illumination.


        Returns
        -------
        NA : float
            

        See Also
        --------
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.fNumber
        """
        axialRay = self.axialRay()
        return self.frontIndex * np.sin(axialRay.theta)

    def apertureStop(self):
        """The "aperture stop" is an aperture in the system that limits
        the cone of angles originating from zero height at the object plane.

        Returns
        -------
        apertureStop : (float,float)
            Returns an array including the position (index [0] of the output)
            and diameter (index [1] of the output) of the aperture stop.
            If there are no elements of finite diameter (i.e. all optical elements
            are infinite in diameters), then there is no aperture stop in the system
            and the size of the aperture stop is infinite (+Inf).

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> path.objectHeight=6
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=5,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print('The position of aperture stop is:', path.apertureStop()[0])
        The position of aperture stop is: 20.0

        >>> print('The diameter of aperture stop is:',path.apertureStop()[1])
        The diameter of aperture stop is: 5

        Also, as the following, you can use display() to follow the rays in the imaging path and view the
        aperture stop and field stop. Since the diameter of the first lens (f=20) is limited,
        this is the aperture stop in the imaging path.

        >>> path.display()

        .. image:: ../../../images/apertureStop.png
            :width: 70%
            :align: center


        See Also
        --------
        raytracing.ImagingPath.apertureStopPosition
        raytracing.ImagingPath.apertureStopDiameter
        raytracing.ImagingPath.fieldStop

        Notes
        -----
        Strategy: we take a ray height and divide by real aperture
        diameter at that position.  Some elements may have a finite length
        (e.g., Space() or ThickLens()), so we always calculate the ratio
        before propagating inside the element and after having propagated
        through the element. The position where the absolute value of the
        ratio is maximum is the aperture stop.
        """
        if not self.hasFiniteApertureDiameter():
            return Stop(z=None, diameter=float('+Inf'))
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

            return Stop(z=apertureStopPosition, diameter=apertureStopDiameter)

    def entrancePupil(self):
        """The entrance pupil is the image of the aperture stop
        as seen from the object. To obtain this image, we simply
        need to know the transfer matrix to the aperture stop,
        then find the "backward" conjugate, which means finding
        the position of the "image" (the entrance pupil) that would 
        lead to the "object" (aperture stop) at the end of the transfer
        matrix. All the terminology is such that it assumes
        the "object" is at the front and the "image" is at the back,
        so we need to invert the magnification.

        Returns
        -------
         entrancePupil : (float,float)
            the position of the pupil relative to input reference plane
            (positive means to the right) and its diameter.

        Examples
        --------
        >>> path = ImagingPath() # define an imaging path
        >>> path.objectHeight=6
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=5,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print('The (position,diameter) of entrance pupil:', path.entrancePupil())
        The (position,diameter) of entrance pupil: (20.0, 5.0)

        """

        if self.hasFiniteApertureDiameter():
            (stopPosition, stopDiameter) = self.apertureStop()
            transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
            (pupilPosition, matrixToPupil) = transferMatrixToApertureStop.backwardConjugate()
            if matrixToPupil is None:
                return Stop(None, None)
            else:
                (Mt, Ma) = matrixToPupil.magnification()
                if Mt != 0:
                    return Stop(-pupilPosition, stopDiameter / abs(Mt))
                else:
                    return Stop(-pupilPosition, float("+inf"))
        else:
            return Stop(None, None)

    def fieldStop(self):
        """ The field stop is the aperture that limits the image size (or field of view)
        It is possible to have finite diameter elements but
        still an infinite field of view and therefore no Field stop.
        In fact, if only a single element has a finite diameter,
        there is no field stop (only an aperture stop). The limit
        is arbitrarily set to maxHeight.

        Returns
        -------
        fieldStop : (float,float)
            the output is the (position, diameter) of the field stop.
            If there are no elements of finite diameter (i.e. all
            optical elements are infinite in diameters), then there
            is no field stop and no aperture stop in the system
            and their sizes are infinite.

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> path.objectHeight=6
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=5,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print('The position of field stop is:', path.apertureStop()[0])
        The position of field stop is: 20.0

        >>> print('The diameter of field stop is:',path.apertureStop()[1])
        The diameter of field stop is: 5

        Also, as the following, you can use display() to follow the rays in the imaging path and view the
        aperture stop and field stop. The second lens in the imaging path (f=10) is the field stop.

        >>> path.display()

        .. image:: ../../../images/apertureStop.png
            :width: 70%
            :align: center


        Notes
        -----
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
                    dy = -dy / 2.0  # Go back, reduce increment
                else:
                    dy = dy * 1.5  # Keep going, go faster (different factor)

                y += dy
                wasBlocked = outputChiefRay.isBlocked
                if abs(y) > self.maxHeight and not wasBlocked:
                    return Stop(z=fieldStopPosition, diameter=fieldStopDiameter)

            for ray in chiefRayTrace:
                if ray.isBlocked:
                    fieldStopPosition = ray.z
                    fieldStopDiameter = ray.apertureDiameter
                    break

        return Stop(z=fieldStopPosition, diameter=fieldStopDiameter)

    def fieldOfView(self):
        """The field of view is the length visible before the chief
        rays on either side are blocked by the field stop.

        Returns
        -------
        fieldOfView : float
            length of object that can be visible at the image plane.
            It can be infinity if there is no field stop.

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> path.objectHeight=6
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=5,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print('field of view :', path.fieldOfView())
        field of view : 6.666665124862807

        Notes
        -----
        Strategy: take ray at various heights from object and
        aim at center of pupil (chief ray from that point)
        until ray is blocked. It is possible to have finite
        diameter elements but still an infinite field of view
        and therefore no Field stop.

        """

        return 2*self.halfFieldOfView() 

    def halfFieldOfView(self):
        """The half field of view is the maximum height
        visible before its chief ray is blocked by the field stop.
        A ray at that height is the principal ray, of "highest chief ray".

        Returns
        -------
        halfFieldOfView : float
            maximum ray height that can still be visible at the image plane.
            It can be infinity if there is no field stop.

        Examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> path.objectHeight=6
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=20))
        >>> path.append(Lens(f=20,diameter=5,label="f=20"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=10))
        >>> print('field of view :', path.fieldOfView())
        field of view : 6.666665124862807

        Notes
        -----
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
        while abs(dy) > self.precision or wasBlocked:
            chiefRay = self.chiefRay(y=y)
            chiefRayTrace = self.trace(chiefRay)
            outputChiefRay = chiefRayTrace[-1]

            if outputChiefRay.isBlocked != wasBlocked:
                dy = -dy / 2.0
            else:
                dy = dy * 1.5  # Don't use 2.0: could bounce forever

            y += dy
            wasBlocked = outputChiefRay.isBlocked
            if abs(y) > self.maxHeight and not wasBlocked:
                return float("+Inf")

        return chiefRay.y

    def imageSize(self):
        """The image size is the object field of view multiplied by magnification.
        This value is independent from the height of the object.

        Returns
        -------
        imageSize : float
            the size of the image

        examples
        --------
        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=10))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=20,diameter=15,label="f=20"))
        >>> path.append(Space(d=20))
        >>> print('size of the image :', path.imageSize())
        size of the image : 9.999998574656525

        """
        fieldOfView = self.fieldOfView()
        (distance, conjugateMatrix) = self.forwardConjugate()
        if conjugateMatrix is None:
            return float("+inf")

        magnification = conjugateMatrix.A
        return abs(fieldOfView * magnification)

    def lagrangeInvariant(self):
        """
        The lagrange invariant is the optical invariant calculated
        with the principal and axial rays. It represents the maximum
        optical invariant for which both rays can propagate unimpeded.

        Returns
        -------
        lagrangeInvariant : float
            The value of the lagrange invariant for the system

        """

        ray1 = self.axialRay()
        ray2 = self.principalRay()

        if ray1 is None or ray2 is None:
            return float("+inf")

        return self.opticalInvariant(ray1, ray2)

    def reportEfficiency(self, objectDiameter=None, emissionHalfAngle=None, nRays=10000): #pragma: no cover
        """
        The collection efficiency of the optical system is computed and a report is printed.
        By default, it is computed across the field of view, but a specific object diameter 
        can be provided as welll as an emission half angle.
        The analysis is based on representing each ray as a linear combination
        of the principal and axial rays. If the coefficients are more than 1.0, the rays will
        be blocked.  If they are both less than 1.0, they should propagated unblocked to the 
        image unless there is vignetting.

        Parameters
        ----------
        objectDiameter : float
            The size of the object for the efficiency reference. Default: field of view
        nRays : int
            Number of rays simulated to calculate efficiency.  Default: 10000
        """
        import matplotlib.patches as p

        principal = self.principalRay()
        axial = self.axialRay()
        Iap = abs(self.lagrangeInvariant()) # corresponds to Zhe in the article

        if emissionHalfAngle is not None:
            maxAngle = emissionHalfAngle
        else:
            maxAngle = np.pi/2

        if objectDiameter is not None:
            maxHeight = objectDiameter/2
        else:
            maxHeight = principal.y

        sourceRays = RandomUniformRays(yMax=maxHeight, 
                                 yMin=-maxHeight,
                                 thetaMax=maxAngle,
                                 thetaMin=-maxAngle,
                                 maxCount=nRays)
        Is = maxHeight * maxAngle

        expectedBlocked = []
        notBlocked = []
        vignettedBlocked = []
        vignettePositions = []
        for ray in sourceRays:
            Irp = self.opticalInvariant(ray, principal)
            Iar = self.opticalInvariant(axial, ray)
            outputRay = self.traceThrough(ray)

            if abs(Irp) > Iap or abs(Iar) > Iap:
                expectedBlocked.append((Irp/Iap, Iar/Iap))
                continue

            if outputRay.isBlocked:
                vignettedBlocked.append((Irp/Iap, Iar/Iap))
                vignettePositions.append(outputRay.z)
            else:
                notBlocked.append((Irp/Iap, Iar/Iap))

        print("Optical System Properties for {0}".format(self.label))
        print("---------------------------------------------------")
        print(" Lagrange invariant: {0:.2f} mm = {1:.2f} mm ⨉ {2:.2f} ≈ 1/2 FOV ⨉ NA".format(Iap, principal.y, axial.theta))
        print(" Object-side NA is {0:.2f}, and f/# is {1:.2f} ".format(self.NA(), self.fNumber()))
        print(" Field of view is {0:.2f} mm".format(self.fieldOfView()))        
        print("\nSource Properties")
        print("-------------------")
        print(" Object/source equivalent invariant: {0:.2f} mm = {1:.2f} mm ⨉ {2:.2f} ≈ height ⨉ half-angle".format(Is, maxHeight, maxAngle))
        print("\nEfficiency")
        print("----------")
        print(" Collection efficiency from Monte Carlo: {0:.1f}% of ±{2:.2f} radian, over field diameter of {1:.1f} mm".format(100*len(notBlocked)/sourceRays.maxCount, 2*maxHeight, maxAngle))
        print(" Collection efficiency from ratio of system to source invariants: {0:.1f}%".format(Iap/Is*100))
        stopPosition, stopDiameter = self.apertureStop()
        print(" Efficiency limited by {0:.1f} mm diameter of AS at z={1:.1f}".format(stopDiameter, stopPosition))
        print(" For 100% efficiency, the system would require an increase of {0:.2f}⨉ in detection NA with same FOV".format(Is/Iap))
        print("\nVignetting")
        print("----------")
        print("Relative efficiency: {0:.1f}% of maximum for this system".format(100*len(notBlocked)/(len(vignettedBlocked)+len(notBlocked))))
        if len(vignettedBlocked) >= 2:
            print("  Loss to vignetting: {0:.1f}%".format(100*len(vignettedBlocked)/(len(vignettedBlocked)+len(notBlocked))))
            print("  Vignetting is due to blockers at positions: {0}".format(set(vignettePositions)))
        else:
            print("  No losses to vignetting")

        fontScale = 1.5
        fig, axis1 = plt.subplots(1, figsize=(10, 7))
        fig.tight_layout(pad=4.0)
        axis1.add_patch(p.Rectangle((-1,-1),2, 2, color=(0, 1.0, 0, 0.5), lw=3, fill=False,
                              transform=axis1.transData, clip_on=True))

        (x,y) = list(zip(*notBlocked))
        plt.scatter(x,y, color=(0,1,0), marker='.',label="Transmitted")
        if len(vignettedBlocked) >= 2:
            (x,y) = list(zip(*vignettedBlocked))
            plt.scatter(x,y, color=(1,0,0), marker='.',label="Vignetted")
        if len(expectedBlocked) >= 2:
            (x,y) = list(zip(*expectedBlocked))
            plt.scatter(x,y, color=(0.5,0.5,0.5), marker='.',label="Blocked")
        axis1.set_xlabel("$B$\n\nFigure: Each point is a ray emitted from the source.", fontsize=13*fontScale)
        axis1.set_ylabel("$A$", fontsize=13*fontScale)
        axis1.set_xlim(-2, 2)
        axis1.set_ylim(-2, 2)
        axis1.set_aspect('equal')
        axis1.legend(loc="upper right", fontsize=13*fontScale)
        axis1.tick_params(labelsize=13*fontScale)
        plt.show()

    def subPath(self, zStart: float, backwards=False):
        """ Secondary ImagingPath defined from a desired zStart to the end of current path
        or to the start of current path if 'backwards' is True. Used internally to trace rays
        from different positions. """

        z = 0
        for i, element in enumerate(self.elements):
            if z < zStart < z + element.L:
                assert type(element).__name__ is 'Space', 'The position of the rays cannot be in the same ' \
                                                          'position of another element.'
                if backwards:
                    newElements = [Space(zStart - z)]
                    if i != 0:
                        newElements.extend(self.elements[i-1::-1])
                    return ImagingPath(elements=newElements)
                else:
                    newElements = [Space(z + element.L - zStart)]
                    newElements.extend(self.elements[i+1:])
                    return ImagingPath(elements=newElements)

            z += element.L

        raise ValueError('The position of the rays does not fit in any spaces.')

    def display(self, rays=None, raysList=None, removeBlocked=True, comments=None,
                onlyPrincipalAndAxialRays=None, limitObjectToFieldOfView=None, interactive=True, filePath=None):
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        rays : `Rays` instance

        raysList : list of `Rays` or list of list of `Ray`
        onlyPrincipalAndAxialRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=True)
        removeBlocked : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)
        """

        if limitObjectToFieldOfView is not None:
            self.figure.designParams['limitObjectToFieldOfView'] = limitObjectToFieldOfView
        if onlyPrincipalAndAxialRays is not None:
            self.figure.designParams['onlyPrincipalAndAxialRays'] = onlyPrincipalAndAxialRays
        self.figure.designParams['removeBlockedRaysCompletely'] = removeBlocked

        if raysList is None:
            raysList = []
        if rays is not None:
            raysList.append(rays)

        self.figure.initializeDisplay()

        if len(raysList) == 0:
            self.figure.designParams['showFOV'] = True
            if not self.figure.designParams['onlyPrincipalAndAxialRays']:
                self.figure.designParams['showFOV'] = False
            else:
                warnings.warn('No rays were provided for the display. Using principal and axial rays.')
                if self.principalRay() is None and self.axialRay() is None:
                    warnings.warn('Principal and axial rays are not defined for this system. '
                                  'Using default ObjectRays.')

        if 'ObjectRays' not in [type(rays).__name__ for rays in raysList]:
            defaultObject = ObjectRays(self.objectHeight, z=self.objectPosition,
                                       halfAngle=self.fanAngle, T=self.rayNumber, H=self.fanNumber)
            raysList.append(defaultObject)
        else:
            self.figure.designParams['showObjectImage'] = True

        self.figure.display(raysList=raysList, comments=comments, title=self.label,
                            backend='matplotlib', display3D=False, interactive=interactive, filepath=filePath)

    def saveFigure(self, filePath, rays=None, raysList=None, removeBlocked=True, comments=None,
                   onlyPrincipalAndAxialRays=None, limitObjectToFieldOfView=None):
        """
        The figure of the imaging path can be saved using this function.

        Parameters
        ----------
        filePath : str or PathLike or file-like object
            A path, or a Python file-like object, or possibly some backend-dependent object.
            If filepath is not a path or has no extension, remember to specify format to
            ensure that the correct backend is used.
        rays : `Rays` instance
        raysList : list of `Rays` or list of list of `Ray`
        onlyPrincipalAndAxialRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=True)
        removeBlocked : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)
        """

        self.display(rays=rays, raysList=raysList, removeBlocked=removeBlocked, comments=comments,
                     onlyPrincipalAndAxialRays=onlyPrincipalAndAxialRays,
                     limitObjectToFieldOfView=limitObjectToFieldOfView,
                     interactive=False, filePath=filePath)

    def displayWithObject(self, diameter, z=0, fanAngle=0.1, fanNumber=3, rayNumber=3, removeBlocked=True, comments=None):
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        diameter : float
            Diameter of the object.
        removeBlocked : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)
        """

        self._objectHeight = diameter
        rays = ObjectRays(diameter, halfAngle=fanAngle, H=fanNumber, T=rayNumber, z=z)

        self.display(rays=rays, raysList=None, removeBlocked=removeBlocked, comments=comments,
                     onlyPrincipalAndAxialRays=False,
                     limitObjectToFieldOfView=False)
