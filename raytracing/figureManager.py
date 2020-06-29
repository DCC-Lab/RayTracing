from .graphics import *
from .ray import Ray
import matplotlib.pyplot as plt
import itertools
import warnings
import sys


class Figure:
    """Base class to contain the required objects of a figure.
    Promote to a backend-derived Figure class to enable display features.
    """
    def __init__(self, opticalPath):
        self.path = opticalPath

        self.graphics = []
        self.lines = []
        self.labels = []

        self.styles = dict()
        self.styles['default'] = {'rayColors': ['b', 'r', 'g'], 'onlyAxialRay': False,
                                  'imageColor': 'r', 'objectColor': 'b', 'onlyPrincipalAndAxialRays': True,
                                  'limitObjectToFieldOfView': True, 'removeBlockedRaysCompletely': False}
        self.styles['publication'] = self.styles['default'].copy()
        self.styles['presentation'] = self.styles['default'].copy()  # same as default for now
        self.styles['publication'].update({'rayColors': ['0.4', '0.2', '0.6'],
                                           'imageColor': '0.3', 'objectColor': '0.1'})

        self.designParams = self.styles['default']

    def design(self, style: str = None,
               rayColors: List[Union[str, tuple]] = None, onlyAxialRay: bool = None,
               imageColor: Union[str, tuple] = None, objectColor: Union[str, tuple] = None):
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
                if key == 'rayColors':
                    assert len(value) == 3, \
                        "rayColors has to be a list with 3 elements."
                self.designParams[key] = value

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

        # TODO, fixme, everything, toaster: implement Label and Label.patch with MPL figure
        label = MplLabel(x=0.05, y=0.15, text=note1 + "\n" + note2, fontsize=12)  # todo: , useDataUnits=False)
        self.labels.append(label)

        # self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
        #                fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def setGraphicsFromPath(self):
        self.lines = self.rayTraceLines()

        self.graphics = self.graphicsOfElements
        self.graphics.append(self.graphicOfObject)
        self.graphics.extend(self.graphicsOfImages)

        (pupilPosition, pupilDiameter) = self.path.entrancePupil()
        if pupilPosition is not None:
            self.graphics.append(self.graphicOfEntrancePupil)

    @property
    def graphicsOfElements(self) -> List[Graphic]:
        graphics = []
        z = 0
        for element in self.path.elements:
            graphic = GraphicOf(element, x=z)
            if graphic is not None:
                graphics.append(graphic)
            z += element.L
        return graphics

    @property
    def graphicOfObject(self) -> Graphic:
        objectArrow = Arrow(dy=self.path.objectHeight, y=-self.path.objectHeight / 2, color='b')
        objectGraphic = Graphic([objectArrow], x=self.path.objectPosition)
        return objectGraphic

    @property
    def graphicsOfImages(self) -> List[Graphic]:
        imageGraphics = []

        images = self.path.intermediateConjugates()

        for (imagePosition, magnification) in images:
            imageHeight = magnification * self.path.objectHeight

            arrow = Arrow(dy=imageHeight, y=-imageHeight / 2, color='r')
            graphic = Graphic([arrow], x=imagePosition)

            imageGraphics.append(graphic)

        return imageGraphics

    @property
    def graphicOfEntrancePupil(self) -> Graphic:
        (pupilPosition, pupilDiameter) = self.path.entrancePupil()
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0

            c1 = Aperture(y=halfHeight)
            c2 = Aperture(y=-halfHeight)

            apertureGraphic = Graphic([c1, c2], x=pupilPosition)
            return apertureGraphic

    @property
    def displayRange(self):
        """ The maximum height of the objects in the optical path. """
        from .laserpath import LaserPath   # Fixme: circular import fix

        if isinstance(self.path, LaserPath):
            return self.laserDisplayRange
        else:
            return self.imagingDisplayRange

    @property
    def imagingDisplayRange(self):
        displayRange = 0
        for graphic in self.graphicsOfElements:
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

    @property
    def laserDisplayRange(self):
        displayRange = 0
        for graphic in self.graphicsOfElements:
            if graphic.halfHeight * 2 > displayRange:
                displayRange = graphic.halfHeight * 2

        if displayRange == float('+Inf') or displayRange == 0:
            if self.path.inputBeam is not None:
                displayRange = self.path.inputBeam.w * 3
            else:
                displayRange = 100

        return displayRange

    def rayTraceLines(self) -> List[Line]:
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
            lineWidth = 1.5
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
            lineWidth = 0.5

        manyRayTraces = self.path.traceMany(rayGroup)

        lines = []
        for rayTrace in manyRayTraces:
            (x, y) = self.rearrangeRayTraceForPlotting(
                rayTrace)
            if len(y) == 0:
                continue  # nothing to plot, ray was fully blocked

            rayInitialHeight = y[0]
            # FIXME: We must take the maximum y in the starting point of manyRayTraces,
            #  not halfHeight
            maxStartingHeight = halfHeight
            binSize = 2.0 * maxStartingHeight / (len(color) - 1)
            colorIndex = int(
                (rayInitialHeight - (-maxStartingHeight - binSize / 2)) / binSize)
            if colorIndex < 0:
                colorIndex = 0
            elif colorIndex >= len(color):
                colorIndex = len(color) - 1

            line = Line(x, y, color=color[colorIndex], lineWidth=lineWidth, label='ray')
            lines.append(line)

        return lines

    def rearrangeRayTraceForPlotting(self, rayList: List[Ray]):
        """
        This function removes the rays that are blocked in the imaging path.
        Parameters
        ----------
        rayList : List of Rays
            an object from rays class or a list of rays
        """
        x = []
        y = []
        for ray in rayList:
            if not ray.isBlocked:
                x.append(ray.z)
                y.append(ray.y)
            elif self.designParams['removeBlockedRaysCompletely']:
                return [], []
            # else: # ray will simply stop drawing from here
        return x, y

    @property
    def mplFigure(self) -> 'MplFigure':
        figure = MplFigure(opticalPath=self.path)
        figure.graphics = self.graphics
        figure.lines = self.lines
        figure.labels = self.labels
        figure.designParams = self.designParams
        return figure

    def display(self, comments=None, title=None, backend='matplotlib', display3D=False, filepath=None):
        self.setGraphicsFromPath()

        if backend is 'matplotlib':
            mplFigure = self.mplFigure
            mplFigure.create(comments, title)
            if display3D:
                mplFigure.display3D(filepath=filepath)
            else:
                mplFigure.display2D(filepath=filepath)
        else:
            raise NotImplementedError("The only supported backend is matplotlib.")


class MplFigure(Figure):
    """Matplotlib Figure"""
    def __init__(self, opticalPath):
        super().__init__(opticalPath)

        self.figure = None
        self.axes = None
        self.axesComments = None

    def create(self, comments=None, title=None):
        if comments is not None:
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def display2D(self, filepath=None):
        self.draw()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def display3D(self, filepath=None):
        raise NotImplementedError()

    def draw(self):
        self.drawGraphics()
        self.drawLabels()

        for line in self.lines:
            self.axes.add_line(line.patch)

        self.updateDisplayRange()
        self.updateGraphics()
        self.updateLabels()

    def drawGraphics(self):
        for graphic in self.graphics:
            components = graphic.patches2D

            for component in components:
                self.axes.add_patch(component)

            if graphic.hasLabel:
                graphic.label = graphic.label.mplLabel
                self.axes.add_artist(graphic.label.patch)

            for point in graphic.points:
                self.axes.plot([point.x], [0], 'ko', markersize=4, color='k', linewidth=0.4)
                if point.text is not None:
                    self.labels.append(point)

    def drawLabels(self):
        self.labels = [label.mplLabel for label in self.labels]

        for label in self.labels:
            self.axes.add_artist(label.patch)

    def updateGraphics(self):
        for graphic in self.graphics:
            xScaling, yScaling = self.scalingOfGraphic(graphic)

            translation = transforms.Affine2D().translate(graphic.x, graphic.y)
            scaling = transforms.Affine2D().scale(xScaling, yScaling)

            for patch in graphic.patches2D:
                patch.set_transform(scaling + translation + self.axes.transData)

            if graphic.hasLabel:
                graphic.label.patch.set_transform(translation + self.axes.transData)

    def updateLabels(self):
        self.resetLabelOffsets()
        self.fixLabelOverlaps()

    def resetLabelOffsets(self):
        """Reset previous offsets applied to the labels.

        Used with a zoom callback to properly replace the labels.
        """
        for graphic in self.graphics:
            if graphic.hasLabel:
                graphic.label.resetPosition()

        for label in self.labels:
            label.resetPosition()

    def getRenderedLabels(self) -> List[MplLabel]:
        """List of labels rendered inside the current display."""
        labels = []
        for graphic in self.graphics:
            if graphic.hasLabel:
                if graphic.label.isRenderedOn(self.figure):
                    labels.append(graphic.label)

        for label in self.labels:
            if label.isRenderedOn(self.figure):
                labels.append(label)

        return labels

    def fixLabelOverlaps(self, maxIteration: int = 5):
        """Iteratively identify overlapping label pairs and move them apart in x-axis."""
        labels = self.getRenderedLabels()
        if len(labels) < 2:
            return

        i = 0
        while i < maxIteration:
            noOverlap = True
            boxes = [label.boundingBox(self.axes, self.figure) for label in labels]
            for (a, b) in itertools.combinations(range(len(labels)), 2):
                boxA, boxB = boxes[a], boxes[b]

                if boxA.overlaps(boxB):
                    noOverlap = False
                    if boxB.x1 > boxA.x1:
                        requiredSpacing = boxA.x1 - boxB.x0
                    else:
                        requiredSpacing = boxA.x0 - boxB.x1

                    self.translateLabel(labels[a], boxA, dx=-requiredSpacing/2)
                    self.translateLabel(labels[b], boxB, dx=requiredSpacing/2)

            i += 1
            if noOverlap:
                break

    def translateLabel(self, label, bbox, dx):
        """Internal method to translate a label and make sure it stays inside the display."""
        label.translate(dx)

        xMin, xMax = self.axes.get_xlim()
        if bbox.x0 + dx < xMin:
            label.translate(xMin - (bbox.x0 + dx))
        elif bbox.x1 + dx > xMax:
            label.translate(xMax - (bbox.x1 + dx))

    def updateDisplayRange(self):
        """Set a symmetric Y-axis display range defined as 1.5 times the maximum halfHeight of all graphics."""
        halfDisplayHeight = self.displayRange/2 * 1.5
        self.axes.autoscale()
        self.axes.set_ylim(-halfDisplayHeight, halfDisplayHeight)

    def onZoomCallback(self, axes):
        self.updateGraphics()
        self.updateLabels()

    def scalingOfGraphic(self, graphic):
        if not graphic.useAutoScale:
            return 1, 1

        xScale, yScale = self.axesToDataScale()

        heightFactor = graphic.halfHeight * 2 / yScale
        xScaling = xScale * (heightFactor / 0.2) ** (3 / 4)

        return xScaling, 1

    def axesToDataScale(self):
        """ Dimensions of the figure in data units. """
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
