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

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)

    def draw(self):
        for drawing in self.drawings:
            drawing.applyTo(self.axes)

        self.updateDisplayRange()
        self.update()

    def add(self, drawing: Drawing):
        self.drawings.append(drawing)

    def updateDisplayRange(self):
        """Set a symmetric Y-axis display range defined as 1.5 times the maximum halfHeight of all drawings."""
        halfHeight = 0

        for drawing in self.drawings:
            if drawing.halfHeight() > halfHeight:
                halfHeight = drawing.halfHeight()

        self.axes.autoscale()
        self.axes.set_ylim(-halfHeight * 1.5, halfHeight * 1.5)

    def update(self):
        """Update all figure drawings to properly rescale their dimensions with the display range."""
        for drawing in self.drawings:
            drawing.update()

        self.checkLabels()

    def onZoomCallback(self, axes):
        self.update()

    def checkLabels(self):
        labels, bboxes = [], []
        for drawing in self.drawings:
            if drawing.label is not None:
                drawing.label.resetPosition()
                bbox = drawing.label.get_tightbbox(self.figure.canvas.get_renderer())
                if bbox is not None:  # (i.e. not out of view)
                    dataBox = bbox.inverse_transformed(self.axes.transData)
                    labels.append(drawing.label)
                    bboxes.append(dataBox)

        self.checkBBoxOverlap(labels, bboxes)

    def checkBBoxOverlap(self, labels, bboxes):
        for (a, b) in itertools.combinations(range(len(bboxes)), 2):
            if bboxes[a].overlaps(bboxes[b]):
                if bboxes[b].x1 > bboxes[a].x1:
                    requiredSpacing = bboxes[a].x1 - bboxes[b].x0
                else:
                    requiredSpacing = bboxes[a].x0 - bboxes[b].x1
                requiredSpacing *= 1.2

                labels[a].offset(dx=- requiredSpacing/2)
                labels[b].offset(dx=requiredSpacing/2)

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
