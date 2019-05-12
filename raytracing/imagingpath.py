from .matrixgroup import *

from .ray import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms

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
