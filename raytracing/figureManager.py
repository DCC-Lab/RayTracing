import matplotlib.pyplot as plt
import sys
import itertools
from raytracing.graphics import *
from raytracing.interface import *
from raytracing import *


class FigureManager:
    def __init__(self, opticPath, style='presentation', comments=None, title=None):
        self.path = opticPath
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)
        self.style = style  # ['publication', 'presentation', 'teaching']
        self.outputFormats = ['pdf', 'png', 'screen']

        self.labels = []
        self.graphics = []
        self.createFigure(comments=comments, title=title)

    def createFigure(self, comments=None, title=None):
        if self.style == 'teaching':
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def add(self, *dataObjects):
        """Add a supported object to the display.

        Parameters
        ----------
            dataObjects: Variable number of Graphic or plt.Line2D objects
        """
        dataType = type([*dataObjects][0])
        if dataType is plt.Line2D:
            self.addLine(*dataObjects)
        elif dataType is MatplotlibGraphic:
            self.addGraphic(*dataObjects)
        elif dataType is Label:
            self.addLabel(*dataObjects)
        elif dataObjects[0] is None:
            pass
        else:
            raise ValueError("Data type not supported.")

    def addGraphic(self, *graphics: Graphic):
        for graphic in [*graphics]:
            self.graphics.append(graphic)

    def addLine(self, *lines: plt.Line2D):
        for line in [*lines]:
            self.axes.add_line(line)

    def addLabel(self, *labels: Label):
        for label in [*labels]:
            self.labels.append(label)

    def addFigureInfo(self, text):
        """Text note in the bottom left of the figure. This note is fixed and cannot be moved."""
        # fixme: might be better to put it out of the axes since it only shows object height and display conditions
        self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
                       fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def draw(self):
        for graphic in self.graphics:
            graphic.applyTo(self.axes)

        for label in self.labels:
            self.axes.add_artist(label)

        self.updateDisplayRange()
        self.update()

    def onZoomCallback(self, axes):
        self.update()

    def updateDisplayRange(self):
        """Set a symmetric Y-axis display range defined as 1.5 times the maximum halfHeight of all graphics."""
        halfHeight = 0

        for graphic in self.graphics:
            if graphic.halfHeight() > halfHeight:
                halfHeight = graphic.halfHeight()

        self.axes.autoscale()
        self.axes.set_ylim(-halfHeight * 1.5, halfHeight * 1.5)

    def update(self):
        """Update all figure graphics to properly rescale their dimensions with the display range.
        Fix overlapping labels if any. """
        for graphic in self.graphics:
            graphic.update()

        self.resetLabelOffsets()
        self.fixLabelOverlaps()

    def resetLabelOffsets(self):
        """Reset previous offsets applied to the labels.

        Used with a zoom callback to properly replace the labels.
        """
        for graphic in self.graphics:
            if graphic.hasLabel:
                graphic.label.resetPosition()

    def getRenderedLabels(self) -> List[Label]:
        """List of labels rendered inside the current display."""
        labels = []
        for graphic in self.graphics:
            if graphic.hasLabel:
                if graphic.label.isRenderedOn(self.figure):
                    labels.append(graphic.label)
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

    def drawPoint(self, x, y, label=None):
        """ Primitive to draw a point with or without labels """
        raise (NotImplemented)

    def drawMeasurement(self, zi, zf, label=None):
        """ Primitive to draw a line with double arrows indicating length with or without labels """

        # axes.annotate("", xy=(self.backVertex, -h), xytext=(F2, -h),
        #               xycoords='data', arrowprops=dict(arrowstyle='<->'),
        #               clip_box=axes.bbox, clip_on=True).arrow_patch.set_clip_box(axes.bbox)
        # axes.text((self.backVertex + F2) / 2, -h, 'BFL = {0:0.1f}'.format(BFL),
        #           ha='center', va='bottom', clip_box=axes.bbox, clip_on=True)
        raise (NotImplemented)

    def drawPlane(self, z, label=None):
        """ Primitive to draw a plane with or without labels """
        raise (NotImplemented)

    def display(self, limitObjectToFieldOfView=False, onlyChiefAndMarginalRays=False,
                removeBlockedRaysCompletely=False):

        self.initializeDisplay(limitObjectToFieldOfView=limitObjectToFieldOfView,
                               onlyChiefAndMarginalRays=onlyChiefAndMarginalRays)

        self.add(*self.path.rayTraceLines(onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
                                          removeBlockedRaysCompletely=removeBlockedRaysCompletely))

        self.createGraphics()

        self.draw()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        self._showPlot()

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

    def createGraphics(self):
        if self.path.showObject:
            self.add(self.graphicOfObject())

        if self.path.showImages:
            self.add(*self.graphicsOfImages())

        if self.path.showEntrancePupil:
            self.add(self.graphicOfEntrancePupil())

        if self.path.showPointsOfInterest:
            self.add(*self.labelsOfStops())
            # self.add(*self.labelsOfPointsOfInterest())

        z = 0
        for element in self.path.elements:
            if element.surfaces:
                graphic = self.graphicOfElement(element)
                graphic.x = z
                self.add(graphic)
            z += element.L

        # TODO: entrancePupil, POI, stops labels

    def graphicOfObject(self) -> MatplotlibGraphic:
        """ The graphic of the object.

        Returns:
            Graphic: The created Graphic object.
        """
        arrow = ArrowPatch(dy=self.path.objectHeight, y=-self.path.objectHeight / 2, color='b')
        graphic = MatplotlibGraphic([arrow], x=self.path.objectPosition)

        return graphic

    def graphicsOfImages(self) -> List[MatplotlibGraphic]:
        """ The graphic of all the images (real and virtual).

        Returns:
            List[Graphic]: A list of the created Graphic object for each image.
        """

        images = self.path.intermediateConjugates()

        graphics = []
        for (imagePosition, magnification) in images:
            imageHeight = magnification * self.path.objectHeight

            arrow = ArrowPatch(dy=imageHeight, y=-imageHeight/2, color='r')
            graphic = MatplotlibGraphic([arrow], x=imagePosition)

            graphics.append(graphic)

        return graphics

    def graphicOfEntrancePupil(self) -> MatplotlibGraphic:
        """
        Graphic of the entrance pupil on an optical system using the position and diameter of the
        entrance pupil.

        See Also
        --------
        raytracing.ImagingPath.entrancePupil

        """
        (pupilPosition, pupilDiameter) = self.path.entrancePupil()
        pupilPosition = None
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0

            p1 = AperturePatch(y=halfHeight, color='r')
            p2 = AperturePatch(y=-halfHeight, color='r')

            return MatplotlibGraphic([p1, p2], x=pupilPosition)

    def graphicOfElement(self, element: Lens, showLabel=True) -> MatplotlibGraphic:
        if not element.surfaces:
            return MatplotlibGraphic([])

        if type(element) is Lens:
            return self.graphicOfThinLens(element, showLabel=showLabel)

        else:
            return self.graphicOfSurfaces(element, showLabel=showLabel)

    def graphicOfThinLens(self, element, showLabel=True) -> MatplotlibGraphic:
        components = []
        halfHeight = element.displayHalfHeight(minSize=self.maxRayHeight())

        components.append(DoubleArrowPatch(height=halfHeight*2))

        if element.hasFiniteApertureDiameter():
            components.append(AperturePatch(y=halfHeight, width=element.L))
            components.append(AperturePatch(y=-halfHeight, width=element.L))

        label = element.label if showLabel else None
        return MatplotlibGraphic(components, label=label)

    def graphicOfSurfaces(self, element, showLabel=True) -> MatplotlibGraphic:
        components = []
        halfHeight = element.displayHalfHeight()

        z = 0
        for i, surfaceA in enumerate(element.surfaces[:-1]):
            surfaceB = element.surfaces[i+1]
            p = SurfacePairPatch(surfaceA, surfaceB, x=z,
                                 halfHeight=halfHeight)
            z += surfaceA.L
            components.append(p)

            outerWidth = p.corners[1] - p.corners[0]
            components.append(AperturePatch(y=halfHeight, x=p.corners[0], width=outerWidth))
            components.append(AperturePatch(y=-halfHeight, x=p.corners[0], width=outerWidth))

        label = element.label if showLabel else None
        return MatplotlibGraphic(components, label=label, fixedWidth=True)

    def labelsOfStops(self) -> List[Label]:
        """ AS and FS labels are drawn at 110% of the largest diameter. """

        labels = []
        halfHeight = self.path.largestDiameter / 2
        (apertureStopPosition, apertureStopDiameter) = self.path.apertureStop()

        if apertureStopPosition is not None:
            labels.append(Label('AS', x=apertureStopPosition, y=halfHeight*1.1, fontsize=18))

        (fieldStopPosition, fieldStopDiameter) = self.path.fieldStop()
        if fieldStopPosition is not None:
            labels.append(Label('FS', x=fieldStopPosition, y=halfHeight * 1.1, fontsize=18))

        return labels

    def labelsOfPointsOfInterest(self) -> List[Label]:
        labels = []
        return labels

    def maxRayHeight(self):
        # FIXME: need a more robust reference to rayTraces... and maybe maxRayHeightAt(y) instead?
        maxRayHeight = 0
        for line in self.axes.lines:
            if line.get_label() == 'ray':
                if max(abs(line._y)) > maxRayHeight:
                    maxRayHeight = max(abs(line._y))

        return maxRayHeight

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

    def reset(self):
        pass
