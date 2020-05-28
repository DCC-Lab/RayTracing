import matplotlib.pyplot as plt
import sys
import itertools
from raytracing.drawing import *


class FigureManager:
    # # Singleton setup
    # # Not sure we want a singleton since that probably means we can't work on two imagingPaths at the same time
    #
    # __instance = None
    # def __new__(cls):
    #     """ Singleton """
    #     if LayoutHelper.__instance is None:
    #         LayoutHelper.__instance = object.__new__(cls)
    #     # LayoutHelper.__instance.val = val
    #     return LayoutHelper.__instance

    def __init__(self):
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)
        self.styles = ['publication', 'presentation', 'teaching']
        self.outputFormats = ['pdf', 'png', 'screen']

        self.drawings = []

        # ok. A Drawing should contain its own Aperture and labels set at a specific position.
        # FigureManager can display them, request their position to check they do not overlap.
        # If they overlap he can ask to update their position
        # * Labels do not need size rescaling but position update (delta Y is -5% of displayRange ish)
        # But there's also some Labels that are not necessarily tied to a drawing. like A/F stops

    def createFigure(self, style='presentation', comments=None):
        if style == 'teaching':
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))


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

    def display(self):
        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)

        self._showPlot()

    def _showPlot(self):  # internal, do not use
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
