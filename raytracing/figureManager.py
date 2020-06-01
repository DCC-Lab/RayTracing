import matplotlib.pyplot as plt
import sys
import itertools
from raytracing.drawing import *
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

        self.drawings = []
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
            dataObjects:
        """
        dataType = type([*dataObjects][0])
        if dataType is plt.Line2D:
            self.addLine(*dataObjects)
        elif dataType is Drawing:
            self.addDrawing(*dataObjects)
        else:
            raise ValueError("Data type not supported.")

    def addDrawing(self, *drawings: Drawing):
        for drawing in [*drawings]:
            self.drawings.append(drawing)

    def addLine(self, *lines: plt.Line2D):
        for line in [*lines]:
            self.axes.add_line(line)

    def addFigureInfo(self, text):
        """Text note in the bottom left of the figure. This note is fixed and cannot be moved."""
        # fixme: might be better to put it out of the axes since it only shows object height and display conditions
        self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
                       fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def draw(self):
        for drawing in self.drawings:
            drawing.applyTo(self.axes)

        self.updateDisplayRange()
        self.update()

    def onZoomCallback(self, axes):
        self.update()

    def updateDisplayRange(self):
        """Set a symmetric Y-axis display range defined as 1.5 times the maximum halfHeight of all drawings."""
        halfHeight = 0

        for drawing in self.drawings:
            if drawing.halfHeight() > halfHeight:
                halfHeight = drawing.halfHeight()

        self.axes.autoscale()
        self.axes.set_ylim(-halfHeight * 1.5, halfHeight * 1.5)

    def update(self):
        """Update all figure drawings to properly rescale their dimensions with the display range.
        Fix overlapping labels if any. """
        for drawing in self.drawings:
            drawing.update()

        self.resetLabelOffsets()
        self.fixLabelOverlaps()

    def resetLabelOffsets(self):
        """Reset previous offsets applied to the labels.

        Used with a zoom callback to properly replace the labels.
        """
        for drawing in self.drawings:
            if drawing.hasLabel:
                drawing.label.resetPosition()

    def getRenderedLabels(self) -> List[Label]:
        """List of labels rendered inside the current display."""
        labels = []
        for drawing in self.drawings:
            if drawing.hasLabel:
                if drawing.label.isRenderedOn(self.figure):
                    labels.append(drawing.label)
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

        self.createDrawings()

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

    def createDrawings(self):
        if self.path.showObject:
            self.add(self.drawingOfObject())

        if self.path.showImages:
            self.add(*self.drawingsOfImages())

        z = 0
        for element in self.path.elements:
            if element.surfaces:
                drawing = self.drawingOfElement(element)
                drawing.x = z
                self.add(drawing)
            z += element.L

        # TODO: entrancePupil, POI, stop labels

    def drawingOfObject(self) -> Drawing:
        """ The drawing of the object.

        Returns:
            Drawing: The created Drawing object.
        """
        arrow = ArrowPatch(dy=self.path.objectHeight, y=-self.path.objectHeight / 2, color='b')
        drawing = Drawing([arrow], x=self.path.objectPosition)

        return drawing

    def drawingsOfImages(self) -> List[Drawing]:
        """ The drawing of all the images (real and virtual).

        Returns:
            List[Drawing]: A list of the created Drawing object for each image.
        """

        images = self.path.intermediateConjugates()

        drawings = []
        for (imagePosition, magnification) in images:
            imageHeight = magnification * self.path.objectHeight

            arrow = ArrowPatch(dy=imageHeight, y=-imageHeight/2, color='r')
            drawing = Drawing([arrow], x=imagePosition)

            drawings.append(drawing)

        return drawings

    def drawingOfElement(self, element: Lens, showLabel=True) -> Drawing:
        if not element.surfaces:
            return Drawing([])

        if type(element) is Lens:
            return self.drawingOfThinLens(element, showLabel=showLabel)

        else:
            return self.drawingOfSurfaces(element, showLabel=showLabel)

    def drawingOfThinLens(self, element, showLabel=True):
        components = []
        halfHeight = element.displayHalfHeight(minSize=self.maxRayHeight())

        components.append(ArrowPatch(dy=halfHeight, headLengthRatio=0.2))
        components.append(ArrowPatch(dy=-halfHeight, headLengthRatio=0.2))

        if element.hasFiniteApertureDiameter():
            components.append(AperturePatch(y=halfHeight, width=element.L))
            components.append(AperturePatch(y=-halfHeight, width=element.L))

        label = element.label if showLabel else None
        return Drawing(components, label=label)

    def drawingOfSurfaces(self, element, showLabel=True):
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
        return Drawing(components, label=label, fixedWidth=True)

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
