from typing import List, Union
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import path as mpath
from .matrix import *
from .matrixgroup import *
from .specialtylenses import *
import warnings


class Figure:
    def __init__(self, opticalPath):
        self.path = opticalPath
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)
        self.elementGraphics = []

        self.styles = dict()
        self.styles['default'] = {'rayColors': ['b', 'r', 'g'], 'onlyAxialRay': False,
                                  'imageColor': 'r', 'objectColor': 'b', 'onlyPrincipalAndAxialRays': True,
                                  'limitObjectToFieldOfView': True}
        self.styles['publication'] = self.styles['default'].copy()
        self.styles['presentation'] = self.styles['default'].copy()  # same as default for now

        self.styles['publication'].update({'rayColors': ['0.4', '0.2', '0.6'],
                                           'imageColor': '0.3', 'objectColor': '0.1'})

        self.designParams = self.styles['default']

    def createFigure(self, comments=None, title=None):
        if comments is not None:
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def initializeDisplay(self):
        """ Configure the imaging path and the figure according to the display conditions. """

        note1 = ""
        note2 = ""
        if self.designParams['limitObjectToFieldOfView']:
            fieldOfView = self.path.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.path.objectHeight = fieldOfView
                note1 = "FOV: {0:.2f}".format(self.path.objectHeight)
            else:
                warnings.warn("Infinite field of view: cannot use limitObjectToFieldOfView=True.")
                self.designParams['limitObjectToFieldOfView'] = False

            imageSize = self.path.imageSize()
            if imageSize != float('+Inf'):
                note1 += " Image size: {0:.2f}".format(imageSize)
            else:
                warnings.warn("Infinite image size: cannot use limitObjectToFieldOfView=True.")
                self.designParams['limitObjectToFieldOfView'] = False

        if not self.designParams['limitObjectToFieldOfView']:
            note1 = "Object height: {0:.2f}".format(self.path.objectHeight)

        if self.designParams['onlyPrincipalAndAxialRays']:
            (stopPosition, stopDiameter) = self.path.apertureStop()
            if stopPosition is None or self.path.principalRay() is None:
                warnings.warn("No aperture stop in system: cannot use onlyPrincipalAndAxialRays=True since they are "
                              "not defined.")
                self.designParams['onlyPrincipalAndAxialRays'] = False
            else:
                note2 = "Only chief and marginal rays shown"

        self.addFigureInfo(text=note1 + "\n" + note2)

    def addFigureInfo(self, text):
        """Text note in the bottom left of the figure. This note is fixed and cannot be moved."""
        # fixme: might be better to put it out of the axes since it only shows object height and display conditions
        self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
                       fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def design(self, style: str = None,
               rayColors: List[Union[str, tuple]] = None, onlyAxialRay: bool = None,
               imageColor: Union[str, tuple] = None, objectColor: Union[str, tuple] = None):
        # todo: maybe move all display() arguments here instead
        """ Update the design parameters of the figure.

        All parameters are None by default to allow for the update of one parameter at a time.

        Parameters
        ----------
        style: str, optional
            Set all design parameters following a supported design style : 'default', 'presentation', 'publication'.
        rayColors : List[Union[str, tuple]], optional
            List of the colors to use for the three different ray type. Default is ['b', 'r', 'g'].
        onlyAxialRay : bool, optional
            Only draw the ray fan coming from the center of the object (axial ray).
            Works with fanAngle and fanNumber. Default to False.
        imageColor : Union[str, tuple], optional
            Color of image arrows. Default to 'r'.
        objectColor : Union[str, tuple], optional
            Color of object arrow. Default to 'b'.
        """
        if style is not None:
            if style in self.styles.keys():
                self.designParams = self.styles[style]
            else:
                raise ValueError("Available styles are : {}".format(self.styles.keys()))

        newDesignParams = {'rayColors': rayColors, 'onlyAxialRay': onlyAxialRay,
                           'imageColor': imageColor, 'objectColor': objectColor}
        for key, value in newDesignParams.items():
            if value is not None:
                if key is 'rayColors':
                    assert len(value) is 3, \
                        "rayColors has to be a list with 3 elements."
                self.designParams[key] = value

    def display(self, onlyPrincipalAndAxialRays=True,
                removeBlockedRaysCompletely=False, filepath=None):
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        onlyPrincipalAndAxialRays : bool (Optional)
            If True, only the principal ray and the axial ray will appear on the plot (default=True)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)

        """

        self.designParams['onlyPrincipalAndAxialRays'] = onlyPrincipalAndAxialRays
        self.initializeDisplay()

        self.drawLines(self.rayTraceLines(removeBlockedRaysCompletely=removeBlockedRaysCompletely))
        self.drawDisplayObjects()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        self.axes.set_xlim(0 - self.path.L * 0.05, self.path.L + self.path.L * 0.05)
        self.axes.set_ylim([-self.displayRange() / 2 * 1.6, self.displayRange() / 2 * 1.6])

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def displayGaussianBeam(self, beams=None, filepath=None):
        """ Display the optical system and trace the laser beam.
        If comments are included they will be displayed on a
        graph in the bottom half of the plot.

        Parameters
        ----------
        inputBeams : list of object of GaussianBeam class
            A list of Gaussian beams
        """

        if len(beams) != 0:
            self.drawBeamTraces(beams=beams)

        self.drawDisplayObjects()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        self.axes.set_xlim(0 - self.path.L * 0.05, self.path.L + self.path.L * 0.05)
        self.axes.set_ylim([-self.displayRange() / 2 * 1.6, self.displayRange() / 2 * 1.6])

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def drawBeamTraces(self, beams):
        for beam in beams:
            self.drawBeamTrace(beam)
            self.drawWaists(beam)

    def rearrangeBeamTraceForPlotting(self, rayList):
        x = []
        y = []
        for ray in rayList:
            x.append(ray.z)
            y.append(ray.w)
        return (x, y)

    def drawBeamTrace(self, beam):
        """ Draw beam trace corresponding to input beam 
        Because the laser beam diffracts through space, we cannot
        simply propagate the beam over large distances and trace it
        (as opposed to rays, where we can). We must split Space() 
        elements into sub elements to watch the beam size expand.
        
        We arbitrarily split Space() elements into N sub elements
        before plotting.
        """
        from .imagingpath import ImagingPath  # Fixme: circular import fix

        N = 100
        highResolution = ImagingPath()
        for element in self.path.elements:
            if isinstance(element, Space):
                for i in range(N):
                    highResolution.append(Space(d=element.L / N,
                                                n=element.frontIndex))
            else:
                highResolution.append(element)

        beamTrace = highResolution.trace(beam)
        (x, y) = self.rearrangeBeamTraceForPlotting(beamTrace)
        self.axes.plot(x, y, 'r', linewidth=1)
        self.axes.plot(x, [-v for v in y], 'r', linewidth=1)

    def drawWaists(self, beam):
        """ Draws the expected waist (i.e. the focal spot or the spot where the
        size is minimum) for all positions of the beam. This will show "waists" that
        are virtual if there is an additional lens between the beam and the expceted
        waist.

        It is easy to obtain the waist position from the complex radius of curvature
        because it is the position where the complex radius is imaginary. The position
        returned is relative to the position of the beam, which is why we add the actual
        position of the beam to the relative position. """

        (xScaling, yScaling) = self.axesToDataScale()
        arrowWidth = xScaling * 0.01
        arrowHeight = yScaling * 0.03
        arrowSize = arrowHeight * 3

        beamTrace = self.path.trace(beam)
        for beam in beamTrace:
            relativePosition = beam.waistPosition
            position = beam.z + relativePosition
            size = beam.waist

            self.axes.arrow(position, size + arrowSize, 0, -arrowSize,
                       width=0.1, fc='g', ec='g',
                       head_length=arrowHeight, head_width=arrowWidth,
                       length_includes_head=True)
            self.axes.arrow(position, -size - arrowSize, 0, arrowSize,
                       width=0.1, fc='g', ec='g',
                       head_length=arrowHeight, head_width=arrowWidth,
                       length_includes_head=True)

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
        from .laserpath import LaserPath   # Fixme: circular import fix

        if isinstance(self.path, LaserPath):
            return self.laserDisplayRange()
        else:
            return self.imagingDisplayRange()

    def imagingDisplayRange(self):
        displayRange = 0
        for graphic in self.elementGraphics:
            if graphic.halfHeight * 2 > displayRange:
                displayRange = graphic.halfHeight * 2

        if displayRange == float('+Inf') or displayRange <= self.path._objectHeight:
            displayRange = self.path._objectHeight

        conjugates = self.path.intermediateConjugates()
        if len(conjugates) != 0:
            for (planePosition, magnification) in conjugates:
                if not 0 <= planePosition <= self.path.L:
                    continue
                magnification = abs(magnification)
                if displayRange < self.path._objectHeight * magnification:
                    displayRange = self.path._objectHeight * magnification

        return displayRange

    def laserDisplayRange(self):
        displayRange = 0
        for graphic in self.elementGraphics:
            if graphic.halfHeight * 2 > displayRange:
                displayRange = graphic.halfHeight * 2

        if displayRange == float('+Inf') or displayRange == 0:
            if self.path.inputBeam is not None:
                displayRange = self.path.inputBeam.w * 3
            else:
                displayRange = 100

        return displayRange

    def drawLines(self, lines):
        for line in lines:
            self.axes.add_line(line)

    def drawDisplayObjects(self):
        """ Draw the object, images and all elements to the figure. """
        from .laserpath import LaserPath  # Fixme: circular import fix
        if isinstance(self.path, LaserPath):
            return self.drawElements(self.path.elements)

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
            fc=self.designParams['objectColor'],
            ec=self.designParams['objectColor'],
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
                fc=self.designParams['imageColor'],
                ec=self.designParams['imageColor'],
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

    def drawElements(self, elements):
        self.elementGraphics = []
        z = 0
        for element in elements:
            graphic = Graphic(element)
            graphic.drawAt(z, self.axes)
            graphic.drawAperture(z, self.axes)

            if self.path.showElementLabels:
                graphic.drawLabels(z, self.axes)
            z += graphic.L
            self.elementGraphics.append(graphic)

    def rayTraceLines(self, removeBlockedRaysCompletely=True):
        """ A list of all ray trace line objects corresponding to either
        1. the group of rays defined by the user (fanAngle, fanNumber, rayNumber).
        2. the principal and axial rays.
        """

        color = self.designParams['rayColors']

        if self.designParams['onlyPrincipalAndAxialRays']:
            halfHeight = self.path.objectHeight / 2.0
            principalRay = self.path.principalRay()
            axialRay = self.path.axialRay()
            rayGroup = (principalRay, axialRay)
            linewidth = 1.5
        else:
            halfAngle = self.path.fanAngle / 2.0
            halfHeight = self.path.objectHeight / 2.0
            rayGroup = Ray.fanGroup(
                yMin=-halfHeight,
                yMax=halfHeight,
                M=self.path.rayNumber,
                radianMin=-halfAngle,
                radianMax=halfAngle,
                N=self.path.fanNumber)
            linewidth = 0.5

        manyRayTraces = self.path.traceMany(rayGroup)

        lines = []
        for rayTrace in manyRayTraces:
            (x, y) = self.rearrangeRayTraceForPlotting(
                rayTrace, removeBlockedRaysCompletely)
            if len(y) == 0:
                continue  # nothing to plot, ray was fully blocked

            rayInitialHeight = y[0]
            # FIXME: We must take the maximum y in the starting point of manyRayTraces,
            # not halfHeight
            maxStartingHeight = halfHeight # FIXME
            binSize = 2.0 * maxStartingHeight / (len(color) - 1)
            colorIndex = int(
                (rayInitialHeight - (-maxStartingHeight - binSize / 2)) / binSize)
            if colorIndex < 0:
                colorIndex = 0
            elif colorIndex >= len(color):
                colorIndex = len(color) - 1

            line = plt.Line2D(x, y, color=color[colorIndex], linewidth=linewidth, label='ray')
            lines.append(line)

        return lines

    def rearrangeRayTraceForPlotting(self, rayList: List[Ray],
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
                return [], []
            # else: # ray will simply stop drawing from here
        return x, y

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
        xScale = self.path.L * 1.1
        yScale = self.displayRange() * 1.6

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
        self._halfHeight = None

    @property
    def L(self):
        return self.matrix.L

    @property
    def halfHeight(self):
        if self._halfHeight is None:
            self._halfHeight = self.displayHalfHeight()
        return self._halfHeight

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

        self._halfHeight = self.displayHalfHeight(minSize=maxRayHeight)  # real units, i.e. data

        (xScaling, yScaling) = self.axesToDataScale(axes)
        arrowHeadHeight = 2 * self._halfHeight * 0.08

        heightFactor = self._halfHeight * 2 / yScaling
        arrowHeadWidth = xScaling * 0.008 * (heightFactor / 0.2) ** (3 / 4)

        axes.arrow(z, 0, 0, self._halfHeight, width=arrowHeadWidth / 10, fc='k', ec='k',
                   head_length=arrowHeadHeight, head_width=arrowHeadWidth, length_includes_head=True)
        axes.arrow(z, 0, 0, -self._halfHeight, width=arrowHeadWidth / 10, fc='k', ec='k',
                   head_length=arrowHeadHeight, head_width=arrowHeadWidth, length_includes_head=True)
        self.drawCardinalPoints(z, axes)


class SpaceGraphic(MatrixGraphic):
    def __init__(self, matrix):
        super(SpaceGraphic, self).__init__(matrix)
        self._halfHeight = 0

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


class MatrixGroupGraphic(MatrixGraphic):
    def __init__(self, matrixGroup: MatrixGroup):
        self.matrixGroup = matrixGroup
        self._halfHeight = None
        super().__init__(matrixGroup)

    @property
    def L(self):
        L = 0
        for element in self.matrixGroup.elements:
            L += element.L
        return L

    @property
    def halfHeight(self):
        if self._halfHeight is None:
            self._halfHeight = self.displayHalfHeight()
        return self._halfHeight

    def drawAt(self, z, axes, showLabels=True):
        """ Draw each element of this group """
        for element in self.matrixGroup:
            graphic = Graphic(element)
            graphic.drawAt(z, axes)
            graphic.drawAperture(z, axes)

            if showLabels:
                graphic.drawLabels(z, axes)
            z += graphic.L

    def drawPointsOfInterest(self, z, axes):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        AS and FS are drawn at 110% of the largest diameter
        """
        labels = {}  # Gather labels at same z

        zElement = 0
        # For the group as a whole, then each element
        for pointOfInterest in self.matrixGroup.pointsOfInterest(z=zElement):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label

        # Points of interest for each element
        for element in self.matrixGroup.elements:
            pointsOfInterest = element.pointsOfInterest(zElement)

            for pointOfInterest in pointsOfInterest:
                zStr = "{0:3.3f}".format(pointOfInterest['z'])
                label = pointOfInterest['label']
                if zStr in labels:
                    labels[zStr] = labels[zStr] + ", " + label
                else:
                    labels[zStr] = label
            zElement += element.L

        halfHeight = self.matrixGroup.largestDiameter / 2
        for zStr, label in labels.items():
            z = float(zStr)
            axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                          xycoords='data', fontsize=12,
                          ha='center', va='bottom')

    def display(self):
        fig, axes = plt.subplots(figsize=(10, 7))
        self.drawAt(0, axes, showLabels=True)
        self.drawAperture(0, axes)
        self.drawPointsOfInterest(0, axes)
        self.drawVertices(0, axes)
        self.drawCardinalPoints(0, axes)
        self.drawPrincipalPlanes(0, axes)
        axes.set_ylim(-self.halfHeight * 1.6, self.halfHeight * 1.6)
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


class AchromatDoubletLensGraphic(MatrixGroupGraphic):
    def drawAt(self, z, axes, showLabels=False):
        """ Draw the doublet as two dielectric of different colours.

        An arc would be perfect, but matplotlib does not allow to fill
        an arc, hence we must use a patch and Bezier curve.
        We might as well draw it properly: it is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        Because the element can be flipped with flipOrientation()
        we collect information from the list of elements.
        """
        R1 = self.matrixGroup.elements[0].R
        tc1 = self.matrixGroup.elements[1].L
        R2 = self.matrixGroup.elements[2].R
        tc2 = self.matrixGroup.elements[3].L
        R3 = self.matrixGroup.elements[4].R

        h = self.matrixGroup.largestDiameter / 2.0
        v1 = z
        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        v2 = v1 + tc1
        phi2 = math.asin(h / abs(R2))
        delta2 = R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * R2)
        corner2 = v2 + delta2

        v3 = z + tc1 + tc2
        phi3 = math.asin(h / abs(R3))
        delta3 = R3 * (1.0 - math.cos(phi3))
        ctl3 = abs((1.0 - math.cos(phi3)) / math.sin(phi3) * R3)
        corner3 = v3 + delta3

        Path = mpath.Path
        p1 = patches.PathPatch(
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

        p2 = patches.PathPatch(
            Path([(corner2, -h), (v2, -ctl2), (v2, 0),
                  (v2, 0), (v2, ctl2), (corner2, h),
                  (corner3, h), (v3, ctl3), (v3, 0),
                  (v3, 0), (v3, -ctl3), (corner3, -h),
                  (corner2, -h)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            color=[0.80, 0.90, 0.95],
            fill=True,
            transform=axes.transData)

        axes.add_patch(p1)
        axes.add_patch(p2)
        if showLabels:
            self.drawLabels(z, axes)

        self.drawAperture(z, axes)

    def drawAperture(self, z, axes):
        """ Draw the aperture size for this element.
        The lens requires special care because the corners are not
        separated by self.L: the curvature makes the edges shorter.
        We are picky and draw it right.
        """

        if self.matrixGroup.apertureDiameter != float('+Inf'):
            R1 = self.matrixGroup.elements[0].R
            tc1 = self.matrixGroup.elements[1].L
            R2 = self.matrixGroup.elements[2].R
            tc2 = self.matrixGroup.elements[3].L
            R3 = self.matrixGroup.elements[4].R

            h = self.matrixGroup.largestDiameter / 2.0
            phi1 = math.asin(h / abs(R1))
            corner1 = z + R1 * (1.0 - math.cos(phi1))

            phi3 = math.asin(h / abs(R3))
            corner3 = z + tc1 + tc2 + R3 * (1.0 - math.cos(phi3))

            axes.add_patch(patches.Polygon(
                [[corner1, h], [corner3, h]],
                linewidth=3,
                closed=False,
                color='0.7'))
            axes.add_patch(patches.Polygon(
                [[corner1, -h], [corner3, -h]],
                linewidth=3,
                closed=False,
                color='0.7'))


class SingletLensGraphic(MatrixGroupGraphic):
    def drawAt(self, z, axes, showLabels=False):
        """ Draw the doublet as two dielectric of different colours.

        An arc would be perfect, but matplotlib does not allow to fill
        an arc, hence we must use a patch and Bezier curve.
        We might as well draw it properly: it is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        Because the element can be flipped with flipOrientation()
        we collect information from the list of elements.
        """
        R1 = self.matrixGroup.elements[0].R
        tc = self.matrixGroup.elements[1].L
        R2 = self.matrixGroup.elements[2].R

        h = self.matrixGroup.largestDiameter / 2.0
        v1 = z
        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        v2 = v1 + tc
        phi2 = math.asin(h / abs(R2))
        delta2 = R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * R2)
        corner2 = v2 + delta2

        Path = mpath.Path
        p1 = patches.PathPatch(
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

        axes.add_patch(p1)
        if showLabels:
            self.drawLabels(z, axes)

        self.drawAperture(z, axes)

    def drawAperture(self, z, axes):
        """ Draw the aperture size for this element.
        The lens requires special care because the corners are not
        separated by self.L: the curvature makes the edges shorter.
        We are picky and draw it right.
        """

        if self.matrixGroup.apertureDiameter != float('+Inf'):
            R1 = self.matrixGroup.elements[0].R
            tc = self.matrixGroup.elements[1].L
            R2 = self.matrixGroup.elements[2].R

            h = self.matrixGroup.largestDiameter / 2.0
            phi1 = math.asin(h / abs(R1))
            corner1 = z + R1 * (1.0 - math.cos(phi1))

            phi2 = math.asin(h / abs(R2))
            corner2 = z + tc + R2 * (1.0 - math.cos(phi2))

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


class ObjectiveGraphic(MatrixGroupGraphic):
    def __init__(self, objective: Objective):
        super().__init__(objective)
        self.matrixGroup = objective

    def drawAperture(self, z, axes):
        # This MatrixGroup is special: we want to use apertureDiameter as the back aperture
        # but we don't want to draw it becuase it looks like garbage.  Each element will
        # draw its own aperture, so that is ok.
        return

    def drawAt(self, z, axes, showLabels=False):
        L = self.matrixGroup.focusToFocusLength
        f = self.matrixGroup.f
        wd = self.matrixGroup.workingDistance
        halfHeight = self.matrixGroup.backAperture / 2
        shoulder = halfHeight / self.matrixGroup.NA

        points = [[0, halfHeight],
                  [(L - shoulder), halfHeight],
                  [(L - wd), self.matrixGroup.frontAperture / 2],
                  [(L - wd), -self.matrixGroup.frontAperture / 2],
                  [(L - shoulder), -halfHeight],
                  [0, -halfHeight]]

        if self.matrixGroup.isFlipped:
            trans = transforms.Affine2D().scale(-1).translate(tx=z + L, ty=0) + axes.transData
        else:
            trans = transforms.Affine2D().translate(tx=z, ty=0) + axes.transData

        axes.add_patch(patches.Polygon(
            points,
            linewidth=1, linestyle='--', closed=True,
            color='k', fill=False, transform=trans))

        self.drawCardinalPoints(z, axes)

        for element in self.matrixGroup.elements:
            graphic = Graphic(element)
            graphic.drawAperture(z, axes)
            z += graphic.L


class Graphic:
    def __new__(cls, element):
        if type(element) is AchromatDoubletLens or issubclass(type(element), AchromatDoubletLens):
            return AchromatDoubletLensGraphic(element)
        if type(element) is SingletLens or issubclass(type(element), SingletLens):
            return SingletLensGraphic(element)
        if issubclass(type(element), Objective) or issubclass(type(element), Objective):
            return ObjectiveGraphic(element)
        if issubclass(type(element), MatrixGroup):
            return MatrixGroupGraphic(element)

        if type(element) is Lens:
            return LensGraphic(element)
        if type(element) is ThickLens:
            return ThickLensGraphic(element)
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
