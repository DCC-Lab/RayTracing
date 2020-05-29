from typing import Any, Union

from .matrixgroup import *

from .ray import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms
import sys


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
        this value indicates full fan angle in radians for rays (max? min?) (default=0.1)
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

        self.objectHeight = 10.0  # object height (full).
        self.objectPosition = 0.0  # always at z=0 for now.
        self.fanAngle = 0.1  # full fan angle for rays
        self.fanNumber = 9  # number of rays in fan
        self.rayNumber = 3  # number of points on object

        # Constants when calculating field stop
        self.precision = 0.001
        self.maxHeight = 10000.0

        # Display properties
        self.showObject = True
        self.showImages = True
        self.showEntrancePupil = False
        self.showElementLabels = True
        self.showPointsOfInterest = True
        self.showPointsOfInterestLabels = True
        self.showPlanesAcrossPointsOfInterest = True
        super(ImagingPath, self).__init__(elements=elements, label=label)

    def chiefRay(self, y=None):
        """This function returns the chief ray for a height y at object.
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

        if B == 0:
            return None

        if y is None:
            y = self.fieldOfView()

        return Ray(y=y, theta=-A * y / B)

    def principalRay(self):
        """This function returns the chief ray for the height y at the edge 
        of the field of view. The chief ray for height y is the ray that goes
        through the center of the aperture stop.

        Returns
        -------
        principalRay : object of Ray class
            The properties (i.e. height and the angle of the marginal ray).

        See Also
        --------
        raytracing.ImagingPath.marginalRays
        raytracing.ImagingPath.axialRay
        raytracing.ImagingPath.chiefRay

        """
        return self.chiefRay(y=None)


    def marginalRays(self, y=0):
        """This function calculates the marginal rays for a height y at object.
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
        transferMatrixToApertureStop = self.transferMatrix(upTo=stopPosition)
        A = transferMatrixToApertureStop.A
        B = transferMatrixToApertureStop.B

        thetaUp  = (stopDiameter / 2.0 - A * y) / B
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
        return self.marginalRays()

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
                return (-pupilPosition, stopDiameter / Mt)
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
        The position of field stop is: 50.0
        The diameter of field stop is: 10

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
        >>> ath.objectHeight=6
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

    def displayRange(self, axes=None):
        """ We return the largest object in the ImagingPath for display purposes.
        The object is considered only "half" because it starts on axis and goes up.

        Returns
        -------
        displayRange : float
            The maximum height of the objects in an imaging path

        Examples
        --------
        In the following example, we have defined three elements in an imaging path:
        An object (height=3), a first lens (height=5) and a second lens (height=7).
        The height of the second lens is returned as the display range.

        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.objectHeight=3
        >>> path.append(Space(d=10))
        >>> path.append(Lens(f=10,diameter=5,label="f=10"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=20,diameter=7,label="f=20"))
        >>> path.append(Space(d=20))
        >>> print('display range :', path.displayRange())
        display range : 7

        """
        
        displayRange = self.largestDiameter
        if displayRange == float('+Inf') or displayRange <= 2*self.objectHeight:
            displayRange = 2*self.objectHeight

        conjugates = self.intermediateConjugates()
        if len(conjugates) != 0:
            for (planePosition, magnification) in conjugates:
                if displayRange < self.objectHeight * magnification:
                    displayRange = self.objectHeight * magnification
        return displayRange

    def createRayTracePlot(
            self, axes,
            limitObjectToFieldOfView=False,
            onlyChiefAndMarginalRays=False,
            removeBlockedRaysCompletely=False):  # pragma: no cover
        """ This function creates a matplotlib plot to draw the rays and the elements.

            Parameters
            ----------
            axes : object from matplotlib.pyplot.axes class
                Add an axes to the current figure and make it the current axes.
            limitObjectToFieldOfView : bool (Optional)
                If True, the object will be limited to the field of view and
                the calculated field of view will be used instead of the objectHeight(default=False)
            onlyChiefAndMarginalRays : bool (Optional)
                If True, only the principal rays will appear on the plot (default=False)
            removeBlockedRaysCompletely : bool (Optional)
                If True, the blocked rays are removed (default=False)

         """

        axes.set(xlabel='Distance', ylabel='Height', title=self.label)
        axes.set_ylim([-self.displayRange(axes) / 2 * 1.5, self.displayRange(axes) / 2 * 1.5])

        note1 = ""
        note2 = ""
        if limitObjectToFieldOfView:
            fieldOfView = self.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.objectHeight = fieldOfView
                note1 = "FOV: {0:.2f}".format(self.objectHeight)
            else:
                raise ValueError(
                    "Infinite field of view: cannot use\
                    limitObjectToFieldOfView=True.")

            imageSize = self.imageSize()
            if imageSize != float('+Inf'):
                note1 += " Image size: {0:.2f}".format(imageSize)
            else:
                raise ValueError(
                    "Infinite image size: cannot use\
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
                  fontsize=12, verticalalignment='top', clip_box=axes.bbox, clip_on=True)

        self.drawRayTraces(
            axes,
            onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
            removeBlockedRaysCompletely=removeBlockedRaysCompletely)

        self.drawDisplayObjects(axes)

        return axes

    def updateDisplay(self, axes):
        """ Callback function used to redraw the objects when zooming.

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """
        for artist in axes.artists:
            artist.remove()
        axes.artists = []
        for patch in axes.patches:
            patch.remove()
        axes.patches = []
        for text in axes.texts:
            text.remove()
        axes.texts = []

        self.drawDisplayObjects(axes)

    def display(self, limitObjectToFieldOfView=False,
                onlyChiefAndMarginalRays=False, removeBlockedRaysCompletely=False, comments=None):  # pragma: no cover
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        limitObjectToFieldOfView : bool (Optional)
            If True, the object will be limited to the field of view and
            the calculated field of view will be used instead of the objectHeight(default=False)
        onlyChiefAndMarginalRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=False)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)

        """
        if comments is not None:
            fig, (axes, axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            axesComments.axis('off')
            axesComments.text(0., 1.0, comments, transform=axesComments.transAxes,
                              fontsize=10, verticalalignment='top')
        else:
            fig, axes = plt.subplots(figsize=(10, 7))

        self.createRayTracePlot(axes=axes,
                                limitObjectToFieldOfView=limitObjectToFieldOfView,
                                onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
                                removeBlockedRaysCompletely=removeBlockedRaysCompletely)

        axes.callbacks.connect('ylim_changed', self.updateDisplay)
        axes.set_ylim([-self.displayRange(axes) / 2 * 1.5, self.displayRange(axes) / 2 * 1.5])

        self._showPlot()

    def save(self, filepath,
             limitObjectToFieldOfView=False,
             onlyChiefAndMarginalRays=False,
             removeBlockedRaysCompletely=False,
             comments=None):
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
            the calculated field of view will be used instead of the objectHeight(default=False)
        onlyChiefAndMarginalRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=False)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)


        """

        if comments is not None:
            fig, (axes, axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            axesComments.axis('off')
            axesComments.text(0., 1.0, comments, transform=axesComments.transAxes,
                              fontsize=10, verticalalignment='top')
        else:
            fig, axes = plt.subplots(figsize=(10, 7))

        self.createRayTracePlot(axes=axes,
                                limitObjectToFieldOfView=limitObjectToFieldOfView,
                                onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
                                removeBlockedRaysCompletely=removeBlockedRaysCompletely)

        axes.callbacks.connect('ylim_changed', self.updateDisplay)
        axes.set_ylim([-self.displayRange(axes) / 2 * 1.5, self.displayRange(axes) / 2 * 1.5])

        fig.savefig(filepath, dpi=600)

    def drawRayTraces(self, axes, onlyChiefAndMarginalRays,
                      removeBlockedRaysCompletely=True):  # pragma: no cover
        """ Draw all ray traces corresponding to either
        1. the group of rays defined by the user (fanAngle, fanNumber, rayNumber)
        2. the principal rays (chief and marginal)

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        onlyChiefAndMarginalRays : bool
            If True, only the principal rays will appear on the plot
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False).

        """

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
            axes.plot(x, y, color[colorIndex], linewidth=linewidth, label='ray')

    def rearrangeRayTraceForPlotting(self, rayList,
                                     removeBlockedRaysCompletely=True):
        """
        This function removes the rays that are blocked in the imaging path.

        Parameters
        ----------
        rayList : List of Rays
            an object from rays class or a list of rays
        removeBlockedRaysCompletely : bool
            If True, the blocked rays will be removed of the list (default=True)

        """
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

    def drawDisplayObjects(self, axes):
        """ Draw the object, images and all elements to the figure

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """
        if self.showObject:
            self.drawObject(axes)

        if self.showImages:
            self.drawImages(axes)

        if self.showEntrancePupil:
            self.drawEntrancePupil(z=0, axes=axes)

        self.drawAt(z=0, axes=axes, showLabels=self.showElementLabels)
        if self.showPointsOfInterest:
            self.drawPointsOfInterest(z=0, axes=axes)
            self.drawStops(z=0, axes=axes)

    def drawObject(self, axes):  # pragma: no cover
        """Draw the object as defined by objectPosition, objectHeight

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        (xScaling, yScaling) = self.axesToDataScale(axes)

        arrowHeadHeight = self.objectHeight * 0.1

        heightFactor = self.objectHeight / yScaling
        arrowHeadWidth = xScaling * 0.01 * (heightFactor/0.2) ** (3/4)

        axes.arrow(
            self.objectPosition,
            -self.objectHeight / 2,
            0,
            self.objectHeight,
            width=arrowHeadWidth / 5,
            fc='b',
            ec='b',
            head_length=arrowHeadHeight,
            head_width=arrowHeadWidth,
            length_includes_head=True)

    def drawImages(self, axes):  # pragma: no cover
        """ Draw all images (real and virtual) of the object defined by 
        objectPosition, objectHeight

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        (xScaling, yScaling) = self.axesToDataScale(axes)
        images = self.intermediateConjugates()

        for (imagePosition, magnification) in images:
            arrowHeight = abs(magnification * self.objectHeight)
            arrowHeadHeight = arrowHeight * 0.1

            heightFactor = arrowHeight / yScaling
            arrowHeadWidth = xScaling * 0.01 * (heightFactor/0.2) ** (3/4)

            axes.arrow(
                imagePosition,
                -magnification * self.objectHeight / 2,
                0,
                magnification * self.objectHeight,
                width=arrowHeadWidth / 5,
                fc='r',
                ec='r',
                head_length=arrowHeadHeight,
                head_width=arrowHeadWidth,
                length_includes_head=True)

    def drawStops(self, z, axes):  # pragma: no cover
        """ AS and FS are drawn at 110% of the largest diameter

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """
        halfHeight = self.largestDiameter / 2

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

    def drawEntrancePupil(self, z, axes):  # pragma: no cover
        """
        Draw the entrance pupil on an optical system using the position and diameter of the
        entrance pupil.

        Parameters
        ----------
        z : float
            The position of the centre of the entrance pupil will shift by this number.
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        See Also
        --------
        raytracing.ImagingPath.entrancePupil

        """

        (pupilPosition, pupilDiameter) = self.entrancePupil()
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0
            center = z + pupilPosition
            (xScaling, yScaling) = self.axesToDataScale(axes)
            heightFactor = halfHeight * 2 / yScaling
            width = xScaling * 0.01 / 2 * (heightFactor/0.2) ** (3/4)

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

    def drawOpticalElements(self, z, axes):  # pragma: no cover
        """ Deprecated. Use drawAt()

        Parameters
        ----------
        z : float
            The position of the optical element.
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        See Also
        --------
        raytracing.ImagingPath.drawAt

        """
        msg = "drawOpticalElements() was renamed drawAt()"
        warnings.warn(msg, DeprecationWarning)
        self.drawAt(z, axes, showLabels=self.showElementLabels)
