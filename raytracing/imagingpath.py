from typing import Any, Union

from .matrixgroup import *

from .ray import *
from .figure import Figure
import sys
import warnings


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
    _objectHeight : float
        The full height of object can be defined using this attribute (default=10.0)
    objectPosition : float
        This attribute defines the position of the object which must be defined zero for now. (default=0)
    fanAngle : float
        This value indicates full fan angle in radians for rays (default=0.1)
    fanNumber : int
        This value indicates the number of ray(s) in fan (default=9)
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

        .. image:: ImagingPath.png
                    :width: 70%
                    :align: center
    """

    def __init__(self, elements=None, label=""):

        self._objectHeight = 10.0  # object height (full).
        self.objectPosition = 0.0  # always at z=0 for now.
        self.fanAngle = 0.1  # full fan angle for rays
        self.fanNumber = 9  # number of rays in fan
        self.rayNumber = 3  # number of points on object

        # Constants when calculating field stop
        self.precision = 0.001
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
        /       \
        |  6.668  |
        |         |
        | -0.333  |
         \       /
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
            y = self.fieldOfView()/2
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

        See Also
        --------
        raytracing.ImagingPath.marginalRays
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.chiefRay

        """

        objectEdge = self.fieldOfView()/2
        if objectEdge == float("+inf"):
            return None

        principalRay = self.chiefRay(y=objectEdge)
        principalRay.y -= 0.001 #FIXME: be more intelligent than this.
        return principalRay

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
        >>> print( 'the first and the second marginal rays are :', path.marginalRays()[0],path.marginalRays()[1])
        the first and the second marginal rays are :
         /       \
        |  0.000  |
        |         |
        |  0.050  |
         \       /
        z = 0.000
         /       \
        |  0.000  |
        |         |
        | -0.050  |
         \       /
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
            return None  # No aperture stop -> no marginal rays

        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        if transferMatrixToApertureStop.isImaging:
            return None

        thetaUp = (stopDiameter / 2.0 - A * y) / B
        thetaDown = (-stopDiameter / 2.0 - A * y) / B

        if thetaDown > thetaUp:
            (thetaUp, thetaDown) = (thetaDown, thetaUp)

        return [Ray(y=y, theta=thetaUp), Ray(y=y, theta=thetaDown)]

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
        >>> print('The diameter of aperture stop is:',path.apertureStop()[1])
        The position of aperture stop is: 20.0
        The diameter of aperture stop is: 5

        Also, as the following, you can use display() to follow the rays in the imaging path and view the
        aperture stop and field stop. Since the diameter of the first lens (f=20) is limited,
        this is the aperture stop in the imaging path.

        >>> path.display()

        .. image:: apertureStop.png
            :width: 70%
            :align: center


        See Also
        --------
        rayreacing.ImagingPath.apertureStopPosition
        raytracing.ImagingPath.apertureStopDiameter
        rayreacing.ImagingPath.fieldStop

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
                return None, None
            else:
                (Mt, Ma) = matrixToPupil.magnification()
                return (-pupilPosition, stopDiameter / abs(Mt))
        else:
            return (None, None)

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
            the outpu is the (position, diameter) of the field stop.
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
        >>> print('The diameter of field stop is:',path.apertureStop()[1])
        The position of field stop is: 20.0
        The diameter of field stop is: 5

        Also, as the following, you can use display() to follow the rays in the imaging path and view the
        aperture stop and field stop. The second lens in the imaging path (f=10) is the field stop.

        >>> path.display()

        .. image:: apertureStop.png
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
                    return (fieldStopPosition, fieldStopDiameter)

            for ray in chiefRayTrace:
                if ray.isBlocked:
                    fieldStopPosition = ray.z
                    fieldStopDiameter = ray.apertureDiameter
                    break

        return (fieldStopPosition, fieldStopDiameter)

    def fieldOfView(self):
        """The field of view is the maximum object height
        visible until its chief ray is blocked by the field stop.

        Returns
        -------
        fieldOfView : float
            maximum object height that can be visible at the image plane

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
        field of view : 6.668181337416174

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
        while abs(dy) > self.precision or not wasBlocked:
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

        return chiefRay.y * 2.0

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
        size of the image : 10.001885411934927

        """
        fieldOfView = self.fieldOfView()
        (distance, conjugateMatrix) = self.forwardConjugate()
        if conjugateMatrix is None:
            return float("+inf")

        magnification = conjugateMatrix.A
        return abs(fieldOfView * magnification)

    def lagrangeInvariant(self, ray1=None, ray2=None, z=0):
        """
        The Lagrange invariant is a quantity that is conserved
        for any two rays in the system. It is often seen with the
        chief ray and marginal ray in an imaging system, but it is
        actually very general and any two rays can be used.
        In ImagingPath(), if no rays are provided, the chief and
        marginal rays are used.

        Parameters
        ----------
        ray1 : object of Ray class
            A ray at height y1 and angle theta1 (default=None)
        ray2 : object of Ray class
            A ray at height y2 and angle theta2 (default=None)
        z : float
            A distance that shows propagation length (default=0)

        Returns
        -------
        lagrangeInvariant : float
            The value of the lagrange invariant constant for ray1 and ray2

        Examples
        --------
        Since there is no input for the function, the lagrange invariant value is
        calculated for chief and marginal rays.

        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.append(Space(d=10))
        >>> path.append(Lens(f=10,diameter=10,label="f=10"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=20,diameter=15,label="f=20"))
        >>> path.append(Space(d=20))
        >>> print('lagrange invariant :', path.lagrangeInvariant())
        lagrange invariant : 2.5004713529837317

        See Also
        --------
        raytracing.Matrix.lagrangeInvariant

        Notes
        -----
        This quantity is L = n (y1 theta2 - y2 theta1)

        """

        if ray1 is None:
            (apertureStopPosition, apertureStopDiameter) = self.apertureStop()
            if apertureStopPosition is None:
                raise ValueError("There is no aperture stop in this ImagingPath and therefore no marginal ray")

            (ray1, dummy) = self.marginalRays()

        if ray2 is None:
            (fieldStopPosition, fieldStopDiameter) = self.fieldStop()
            if fieldStopPosition is None:
                raise ValueError("There is no field stop in this ImagingPath and therefore no chief ray")

            ray2 = self.chiefRay()

        return super(ImagingPath, self).lagrangeInvariant(z=z, ray1=ray1, ray2=ray2)

    def display(self, onlyPrincipalAndAxialRays=True,
                removeBlockedRaysCompletely=False, comments=None,
                limitObjectToFieldOfView=None, onlyChiefAndMarginalRays=None):
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        limitObjectToFieldOfView : bool (Optional)
            If True, the object will be limited to the field of view and
            the calculated field of view will be used instead of the objectHeight (default=True)
        onlyPrincipalAndAxialRays : bool (Optional)
            If True, only the principal and axial rays will appear on the plot (default=True)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)

        """
        if onlyChiefAndMarginalRays is not None:
            warnings.warn(" Usage of onlyChiefAndMarginalRays is deprecated, "
                          "use onlyPrincipalAndAxialRays instead.")
            onlyPrincipalAndAxialRays = onlyChiefAndMarginalRays
        if limitObjectToFieldOfView is not None:
            self.figure.designParams['limitObjectToFieldOfView'] = limitObjectToFieldOfView

        self.figure.createFigure(title=self.label, comments=comments)

        self.figure.display(onlyPrincipalAndAxialRays=onlyPrincipalAndAxialRays,
                            removeBlockedRaysCompletely=removeBlockedRaysCompletely)

    def saveFigure(self, filepath,
                   onlyPrincipalAndAxialRays=True,
                   removeBlockedRaysCompletely=False, comments=None,
                   limitObjectToFieldOfView=None, onlyChiefAndMarginalRays=None):
        """
        The figure of the imaging path can be saved using this function.

        Parameters
        ----------
        filepath : str or PathLike or file-like object
            A path, or a Python file-like object, or possibly some backend-dependent object.
            If filepath is not a path or has no extension, remember to specify format to
            ensure that the correct backend is used.
        limitObjectToFieldOfView : bool (Optional)
            If True, the object will be limited to the field of view and
            the calculated field of view will be used instead of the objectHeight(default=True)
        onlyPrincipalAndAxialRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=True)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)

        """
        if onlyChiefAndMarginalRays is not None:
            warnings.warn(" Usage of onlyChiefAndMarginalRays is deprecated, "
                          "use onlyPrincipalAndAxialRays instead.")
            onlyPrincipalAndAxialRays = onlyChiefAndMarginalRays
        if limitObjectToFieldOfView is not None:
            self.figure.designParams['limitObjectToFieldOfView'] = limitObjectToFieldOfView

        self.figure.createFigure(title=self.label, comments=comments)

        self.figure.display(onlyPrincipalAndAxialRays=onlyPrincipalAndAxialRays,
                            removeBlockedRaysCompletely=removeBlockedRaysCompletely,
                            filepath=filepath)
