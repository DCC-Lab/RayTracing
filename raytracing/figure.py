from .matrixgroup import MatrixGroup
import matplotlib.pyplot as plt
from matplotlib import path as mpath
import matplotlib.patches as patches
from .matrix import *


class Figure:
    def __init__(self, opticPath, comments=None, title=None):
        self.path = opticPath
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)

        self.createFigure(comments=comments, title=title)

    def createFigure(self, comments=None, title=None):
        if comments is not None:
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def initializeDisplay(self, limitObjectToFieldOfView=False,
                          onlyChiefAndMarginalRays=False):
        """ *Renamed and refactored version of createRayTracePlot*
        Configure the imaging path and the figure according to the display conditions.

            Three optional parameters:
            limitObjectToFieldOfView=False, to use the calculated field of view
            instead of the objectHeight
            onlyChiefAndMarginalRays=False, to only show principal rays
            removeBlockedRaysCompletely=False to remove rays that are blocked.
         """

        note1 = ""
        note2 = ""
        if limitObjectToFieldOfView:
            fieldOfView = self.path.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.path.objectHeight = fieldOfView
                note1 = "FOV: {0:.2f}".format(self.path.objectHeight)
            else:
                raise ValueError(
                    "Infinite field of view: cannot use\
                    limitObjectToFieldOfView=True.")

            imageSize = self.path.imageSize()
            if imageSize != float('+Inf'):
                note1 += " Image size: {0:.2f}".format(imageSize)
            else:
                raise ValueError(
                    "Infinite image size: cannot use\
                    limitObjectToFieldOfView=True.")

        else:
            note1 = "Object height: {0:.2f}".format(self.path.objectHeight)

        if onlyChiefAndMarginalRays:
            (stopPosition, stopDiameter) = self.path.apertureStop()
            if stopPosition is None:
                raise ValueError(
                    "No aperture stop in system: cannot use\
                    onlyChiefAndMarginalRays=True since they\
                    are not defined.")
            note2 = "Only chief and marginal rays shown"

        self.addFigureInfo(text=note1 + "\n" + note2)

    def addFigureInfo(self, text):
        """Text note in the bottom left of the figure. This note is fixed and cannot be moved."""
        # fixme: might be better to put it out of the axes since it only shows object height and display conditions
        self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
                       fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def display(self, limitObjectToFieldOfView=False, onlyChiefAndMarginalRays=False,
                removeBlockedRaysCompletely=False, filepath=None):
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

        """
        self.initializeDisplay(limitObjectToFieldOfView=limitObjectToFieldOfView,
                               onlyChiefAndMarginalRays=onlyChiefAndMarginalRays)

        self.drawLines(self.path.rayTraceLines(onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
                                               removeBlockedRaysCompletely=removeBlockedRaysCompletely))

        self.drawDisplayObjects()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        self.axes.set_ylim([-self.displayRange() / 2 * 1.5, self.displayRange() / 2 * 1.5])

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def displayRange(self):
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

        displayRange = self.path.largestDiameter

        if displayRange == float('+Inf') or displayRange <= 2 * self.path._objectHeight:
            displayRange = 2 * self.path._objectHeight

        conjugates = self.path.intermediateConjugates()
        if len(conjugates) != 0:
            for (planePosition, magnification) in conjugates:
                magnification = abs(magnification)
                if displayRange < self.path._objectHeight * magnification:
                    displayRange = self.path._objectHeight * magnification

        return displayRange

    def drawLines(self, lines):
        for line in lines:
            self.axes.add_line(line)

    def drawDisplayObjects(self):
        """ Draw the object, images and all elements to the figure. """
        if self.path.showObject:
            self.drawObject()

        if self.path.showImages:
            self.drawImages()

        if self.path.showEntrancePupil:
            self.drawEntrancePupil(z=0)

        self.drawElements(self.path.elements)
        if self.path.showPointsOfInterest:
            self.drawPointsOfInterest(z=0)
            self.drawStops(z=0)

    def onZoomCallback(self, axes):
        """ Callback function used to redraw the objects when zooming.

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Automatically passed on a callback.

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

        self.drawDisplayObjects()

    def drawObject(self):
        """Draw the object as defined by objectPosition, objectHeight

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        (xScaling, yScaling) = self.axesToDataScale()

        arrowHeadHeight = self.path._objectHeight * 0.1

        heightFactor = self.path._objectHeight / yScaling
        arrowHeadWidth = xScaling * 0.01 * (heightFactor / 0.2) ** (3 / 4)

        self.axes.arrow(
            self.path.objectPosition,
            -self.path._objectHeight / 2,
            0,
            self.path._objectHeight,
            width=arrowHeadWidth / 5,
            fc='b',
            ec='b',
            head_length=arrowHeadHeight,
            head_width=arrowHeadWidth,
            length_includes_head=True)

    def drawImages(self):
        """ Draw all images (real and virtual) of the object defined by
        objectPosition, objectHeight

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        (xScaling, yScaling) = self.axesToDataScale()
        images = self.path.intermediateConjugates()

        for (imagePosition, magnification) in images:
            arrowHeight = abs(magnification * self.path._objectHeight)
            arrowHeadHeight = arrowHeight * 0.1

            heightFactor = arrowHeight / yScaling
            arrowHeadWidth = xScaling * 0.01 * (heightFactor / 0.2) ** (3 / 4)

            self.axes.arrow(
                imagePosition,
                -magnification * self.path._objectHeight / 2,
                0,
                magnification * self.path._objectHeight,
                width=arrowHeadWidth / 5,
                fc='r',
                ec='r',
                head_length=arrowHeadHeight,
                head_width=arrowHeadWidth,
                length_includes_head=True)

    def drawPointsOfInterest(self, z):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        AS and FS are drawn at 110% of the largest diameter
        """
        labels = {}  # Gather labels at same z

        zElement = 0
        # For the group as a whole, then each element
        for pointOfInterest in self.path.pointsOfInterest(z=zElement):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label

        # Points of interest for each element
        for element in self.path.elements:
            pointsOfInterest = element.pointsOfInterest(zElement)

            for pointOfInterest in pointsOfInterest:
                zStr = "{0:3.3f}".format(pointOfInterest['z'])
                label = pointOfInterest['label']
                if zStr in labels:
                    labels[zStr] = labels[zStr] + ", " + label
                else:
                    labels[zStr] = label
            zElement += element.L

        halfHeight = self.path.largestDiameter / 2
        for zStr, label in labels.items():
            z = float(zStr)
            self.axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                               xycoords='data', fontsize=12,
                               ha='center', va='bottom')

    def drawStops(self, z):  # pragma: no cover
        """ AS and FS are drawn at 110% of the largest diameter

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """
        halfHeight = self.path.largestDiameter / 2

        (apertureStopPosition, apertureStopDiameter) = self.path.apertureStop()
        if apertureStopPosition is not None:
            self.axes.annotate('AS',
                          xy=(apertureStopPosition, 0.0),
                          xytext=(apertureStopPosition, halfHeight * 1.1),
                          fontsize=18,
                          xycoords='data',
                          ha='center',
                          va='bottom')

        (fieldStopPosition, fieldStopDiameter) = self.path.fieldStop()
        if fieldStopPosition is not None:
            self.axes.annotate('FS',
                          xy=(fieldStopPosition,
                              0.0),
                          xytext=(fieldStopPosition,
                                  halfHeight * 1.1),
                          fontsize=18,
                          xycoords='data',
                          ha='center',
                          va='bottom')

    def drawEntrancePupil(self, z):
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

        (pupilPosition, pupilDiameter) = self.path.entrancePupil()
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0
            center = z + pupilPosition
            (xScaling, yScaling) = self.axesToDataScale()
            heightFactor = halfHeight * 2 / yScaling
            width = xScaling * 0.01 / 2 * (heightFactor / 0.2) ** (3 / 4)

            self.axes.add_patch(patches.Polygon(
                [[center - width, halfHeight],
                 [center + width, halfHeight]],
                linewidth=3,
                closed=False,
                color='r'))
            self.axes.add_patch(patches.Polygon(
                [[center - width, -halfHeight],
                 [center + width, -halfHeight]],
                linewidth=3,
                closed=False,
                color='r'))

    def drawElements(self, elements, z=0):
        z = z
        for element in elements:
            if issubclass(type(element), MatrixGroup):  # recursive for systems and objectives
                z = self.drawElements(element.elements, z=z)
                continue
            graphic = self.graphicOf(element)
            graphic.drawAt(z, self.axes)
            graphic.drawAperture(z, self.axes)

            if self.path.showElementLabels:
                graphic.drawLabels(z, self.axes)
            z += element.L
        return z

    def graphicOf(self, element):
        if type(element) is Lens:
            return LensGraphic(element)
        if type(element) is Space:
            return SpaceGraphic(element)
        if type(element) is DielectricInterface:
            return DielectricInterfaceGraphic(element)
        if type(element) is DielectricSlab:
            return DielectricSlabGraphic(element)
        if type(element) is Aperture:
            return ApertureGraphic(element)
        else:
            return MatrixGraphic(element)

    def axesToDataScale(self):
        """ Display dimensions in data units.
        Used to properly draw elements on the display
        with appropriate data coordinates.

        Returns
        -------
        xScale: float
            The scale of x axes
        yScale : float
            The scale of y axes
        """

        xScale, yScale = self.axes.viewLim.bounds[2:]

        return xScale, yScale

    def _showPlot(self):
        try:
            plt.plot()
            if sys.platform.startswith('win'):
                plt.show()
            else:
                plt.draw()
                while True:
                    if plt.get_fignums():
                        plt.pause(0.001)
                    else:
                        break

        except KeyboardInterrupt:
            plt.close()


class MatrixGraphic:
    def __init__(self, matrix: Matrix):
        self.matrix = matrix

    def drawAt(self, z, axes, showLabels=False):  # pragma: no cover
        """ Draw element on plot with starting edge at 'z'.

        Parameters
        ----------
        z : float
            the starting position of the element on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        showLabels : bool
            If True, the label of the element will be shown (default=False)

        Notes
        -----
        Default is a black box of appropriate length.
        """
        halfHeight = self.matrix.largestDiameter / 2
        if halfHeight == float("+Inf"):
            halfHeight = self.displayHalfHeight()

        p = patches.Rectangle((z, -halfHeight), self.matrix.L,
                              2 * halfHeight, color='k', fill=False,
                              transform=axes.transData, clip_on=True)
        axes.add_patch(p)

    def drawVertices(self, z, axes):  # pragma: no cover
        """ Draw vertices of the system

        Parameters
        ----------
        z : float
            the starting position of the element on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        """

        axes.plot([z + self.matrix.frontVertex, z + self.matrix.backVertex], [0, 0], 'ko',
                  markersize=4, color="0.5", linewidth=0.2)
        halfHeight = self.displayHalfHeight()
        axes.text(z + self.matrix.frontVertex, 0, '$V_f$', ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)
        axes.text(z + self.matrix.backVertex, 0, '$V_b$', ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)

    def drawCardinalPoints(self, z, axes):  # pragma: no cover
        """Draw the focal points of a thin lens as black dots

        Parameters
        ----------
        z : float
            the starting position of the element on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        """
        (f1, f2) = self.matrix.focusPositions(z)
        axes.plot([f1, f2], [0, 0], 'ko', markersize=4, color='k', linewidth=0.4)

    def drawPrincipalPlanes(self, z, axes):  # pragma: no cover
        """Draw the principal planes

        Parameters
        ----------
        z : float
            the starting position of the element on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        """
        halfHeight = self.displayHalfHeight()
        (p1, p2) = self.matrix.principalPlanePositions(z=z)

        if p1 is None or p2 is None:
            return

        axes.plot([p1, p1], [-halfHeight, halfHeight], linestyle='--', color='k', linewidth=1)
        axes.plot([p2, p2], [-halfHeight, halfHeight], linestyle='--', color='k', linewidth=1)
        axes.text(p1, halfHeight * 1.2, '$P_f$', ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)
        axes.text(p2, halfHeight * 1.2, '$P_b$', ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)

        (f1, f2) = self.matrix.effectiveFocalLengths()
        FFL = self.matrix.frontFocalLength()
        BFL = self.matrix.backFocalLength()
        (F1, F2) = self.matrix.focusPositions(z=z)

        h = halfHeight * 0.4
        # Front principal plane to front focal spot (effective focal length)
        axes.annotate("", xy=(p1, h), xytext=(F1, h),
                      xycoords='data', arrowprops=dict(arrowstyle='<->'),
                      clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text(p1 - f1 / 2, h, 'EFL = {0:0.1f}'.format(f1),
                  ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)
        # Back principal plane to back focal spot (effective focal length)
        axes.annotate("", xy=(p2, -h), xytext=(F2, -h),
                      xycoords='data', arrowprops=dict(arrowstyle='<->'),
                      clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text(p2 + f2 / 2, -h, 'EFL = {0:0.1f}'.format(f1),
                  ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)

        # Front vertex to front focal spot (front focal length or FFL)
        h = 0.5

        axes.annotate("", xy=(self.matrix.frontVertex, h), xytext=(F1, h),
                      xycoords='data', arrowprops=dict(arrowstyle='<->'),
                      clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text((self.matrix.frontVertex + F1) / 2, h, 'FFL = {0:0.1f}'.format(FFL),
                  ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)

        # Back vertex to back focal spot (back focal length or BFL)
        axes.annotate("", xy=(self.matrix.backVertex, -h), xytext=(F2, -h),
                      xycoords='data', arrowprops=dict(arrowstyle='<->'),
                      clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        axes.text((self.matrix.backVertex + F2) / 2, -h, 'BFL = {0:0.1f}'.format(BFL),
                  ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)

    def drawLabels(self, z, axes):  # pragma: no cover
        """ Draw element labels on plot with starting edge at 'z'.

        Parameters
        ----------
        z : float
            the starting position of the labels on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        Notes
        -----
        Labels are drawn 50% above the display height
        """
        if self.matrix.hasFiniteApertureDiameter():
            halfHeight = self.matrix.largestDiameter / 2.0
        else:
            halfHeight = self.displayHalfHeight()

        center = z + self.matrix.L / 2.0
        axes.annotate(self.matrix.label, xy=(center, 0.0),
                      xytext=(center, halfHeight * 1.4),
                      fontsize=8, xycoords='data', ha='center',
                      va='bottom', clip_box=axes.bbox, clip_on=True)

    def drawPointsOfInterest(self, z, axes):  # pragma: no cover
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        Parameters
        ----------
        z : float
            the starting position of the label on display
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """
        labels = {}  # Gather labels at same z
        for pointOfInterest in self.matrix.pointsOfInterest(z=z):
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

    def drawAperture(self, z, axes):  # pragma: no cover
        """ Draw the aperture size for this element.  Any element may
        have a finite aperture size, so this function is general for all elements.

        Parameters
        ----------
        z : float
            the starting position of the apreture
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0

            center = z + self.matrix.L / 2
            if self.matrix.L == 0:
                (xScaling, yScaling) = self.axesToDataScale(axes)
                heightFactor = halfHeight * 2 / yScaling
                width = xScaling * 0.01 / 2 * (heightFactor / 0.2) ** (3 / 4)
            else:
                width = self.matrix.L / 2

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

    def axesToDataScale(self, axes):
        """ Display dimensions in data units.
        Used to properly draw elements on the display
        with appropriate data coordinates.

        Parameters
        ----------
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        Returns
        -------
        xScale: float
            The scale of x axes
        yScale : float
            The scale of y axes
        """

        xScale, yScale = axes.viewLim.bounds[2:]

        return xScale, yScale

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
        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0  # real half height
        return halfHeight

    def display(self):  # pragma: no cover
        """ Display this component, without any ray tracing but with
        all of its cardinal points and planes.

        Examples
        --------
        >>> from raytracing import *
        >>> # Mat is an ABCD matrix of an object
        >>> Mat= Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=2,frontVertex=-1,backVertex=2,
        >>>            frontIndex=1.5,backIndex=1,label='Lens')
        >>> Mat.display()

        And the result is shown in the following figure:

        .. image:: display.png
            :width: 70%
            :align: center


        Notes
        -----
        If the component has no power (i.e. C == 0) this will fail.
        """

        fig, axes = plt.subplots(figsize=(10, 7))
        displayRange = 2 * self.matrix.largestDiameter
        if displayRange == float('+Inf'):
            displayRange = self.displayHalfHeight() * 4

        axes.set(xlabel='Distance', ylabel='Height', title="Properties of {0}".format(self.matrix.label))
        axes.set_ylim([-displayRange / 2 * 1.2, displayRange / 2 * 1.2])

        self.drawAt(z=0, axes=axes)
        self.drawLabels(z=0, axes=axes)
        self.drawCardinalPoints(z=0, axes=axes)
        if self.matrix.L != 0:
            self.drawVertices(z=0, axes=axes)
        self.drawPointsOfInterest(z=0, axes=axes)
        self.drawPrincipalPlanes(z=0, axes=axes)

        self._showPlot()

    def _showPlot(self):  # pragma: no cover
        # internal, do not use
        try:
            plt.plot()
            if sys.platform.startswith('win'):
                plt.show()
            else:
                plt.draw()
                while True:
                    if plt.get_fignums():
                        plt.pause(0.001)
                    else:
                        break

        except KeyboardInterrupt:
            plt.close()


class LensGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):
        """ Draw a thin lens at z

        Parameters
        ----------
        z : float
            The position of the lens
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        showLabels : bool
            If True, the label for the lens is shown (default=False)
        """
        maxRayHeight = 0
        for line in axes.lines:
            if line.get_label() == 'ray':  # FIXME: need a more robust reference to rayTraces
                if max(line._y) > maxRayHeight:
                    maxRayHeight = max(line._y)

        halfHeight = self.displayHalfHeight(minSize=maxRayHeight)  # real units, i.e. data

        (xScaling, yScaling) = self.axesToDataScale(axes)
        arrowHeadHeight = 2 * halfHeight * 0.1

        heightFactor = halfHeight * 2 / yScaling
        arrowHeadWidth = xScaling * 0.01 * (heightFactor / 0.2) ** (3 / 4)

        axes.arrow(z, 0, 0, halfHeight, width=arrowHeadWidth / 5, fc='k', ec='k',
                   head_length=arrowHeadHeight, head_width=arrowHeadWidth, length_includes_head=True)
        axes.arrow(z, 0, 0, -halfHeight, width=arrowHeadWidth / 5, fc='k', ec='k',
                   head_length=arrowHeadHeight, head_width=arrowHeadWidth, length_includes_head=True)
        self.drawCardinalPoints(z, axes)


class SpaceGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):
        """This function draws nothing because free space is not visible. """
        return


class DielectricInterfaceGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):  # pragma: no cover
        """ Draw a curved surface starting at 'z'.
        We are not able yet to determine the color to fill with.

        Parameters
        ----------
        z : float
            The starting position of the curved surface
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        showLabels : bool (Optional)
            If True, the label of the curved surface is shown. (default=False)

        Notes
        -----
        It is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        """
        h = self.displayHalfHeight()

        # For simplicity, 1 is front, 2 is back.
        # For details, see https://pomax.github.io/bezierinfo/#circles_cubic
        v1 = z + self.matrix.frontVertex
        phi1 = math.asin(h / abs(self.matrix.R))
        delta1 = self.matrix.R * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * self.matrix.R)
        corner1 = v1 + delta1

        Path = mpath.Path
        p = patches.PathPatch(
            Path([(corner1, -h), (v1, -ctl1), (v1, 0),
                  (v1, 0), (v1, ctl1), (corner1, h)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3]),
            fill=False,
            transform=axes.transData)

        axes.add_patch(p)
        if showLabels:
            self.drawLabels(z, axes)


class ThickLensGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):  # pragma: no cover
        """ Draw a faint blue box with slightly curved interfaces
        of length 'thickness' starting at 'z'.

        Parameters
        ----------
        z : float
            The starting position of the curved surface
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        showLabels : bool (Optional)
            If True, the label of the curved surface is shown. (default=False)

        Notes
        -----
        An arc would be perfect, but matplotlib does not allow to fill
        an arc, hence we must use a patch and Bezier curve.
        We might as well draw it properly: it is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        """
        h = self.displayHalfHeight()

        # For simplicity, 1 is front, 2 is back.
        # For details, see https://pomax.github.io/bezierinfo/#circles_cubic
        v1 = z + self.matrix.frontVertex
        phi1 = math.asin(h / abs(self.matrix.R1))
        delta1 = self.matrix.R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * self.matrix.R1)
        corner1 = v1 + delta1

        v2 = z + self.matrix.backVertex
        phi2 = math.asin(h / abs(self.matrix.R2))
        delta2 = self.matrix.R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * self.matrix.R2)
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
            self.drawLabels(z, axes)

        self.drawCardinalPoints(z=z, axes=axes)

    def drawAperture(self, z, axes):  # pragma: no cover
        """ Draw the aperture size for this element.
        The thick lens requires special care because the corners are not
        separated by self.L: the curvature makes the edges shorter.
        We are picky and draw it right.

        Parameters
        ----------
        z : float
            The starting position of the curved surface
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.

        """

        if self.matrix.apertureDiameter != float('+Inf'):
            h = self.matrix.largestDiameter / 2.0
            phi1 = math.asin(h / abs(self.matrix.R1))
            corner1 = z + self.matrix.frontVertex + self.matrix.R1 * (1.0 - math.cos(phi1))

            phi2 = math.asin(h / abs(self.matrix.R2))
            corner2 = z + self.matrix.backVertex + self.matrix.R2 * (1.0 - math.cos(phi2))

            axes.add_patch(patches.Polygon(
                [[corner1, h], [corner2, h]],
                linewidth=3,
                closed=False,
                color='0.7'))
            axes.add_patch(patches.Polygon(
                [[corner1, -h], [corner2, -h]],
                linewidth=3,
                closed=False,
                color='0.7'))


class DielectricSlabGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):  # pragma: no cover
        """ Draw a faint blue box of length L starting at 'z'.

        Parameters
        ----------
        z : float
            The starting position of the curved surface
        axes : object from matplotlib.pyplot.axes class
            Add an axes to the current figure and make it the current axes.
        showLabels : bool (Optional)
            If True, the label of the curved surface is shown. (default=False)


        """
        halfHeight = self.displayHalfHeight()
        p = patches.Rectangle((z, -halfHeight), self.matrix.L,
                              2 * halfHeight, color=[0.85, 0.95, 0.95],
                              fill=True, transform=axes.transData,
                              clip_on=True)
        axes.add_patch(p)


class ApertureGraphic(MatrixGraphic):
    def drawAt(self, z, axes, showLabels=False):
        """ Currently nothing specific to draw because any
        aperture for any object is drawn with drawAperture()
        """
        return
