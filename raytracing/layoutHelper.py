import matplotlib.pyplot as plt
import sys


class LayoutHelper:
    __instance = None

    def __new__(cls):
        """ Singleton """
        if LayoutHelper.__instance is None:
            LayoutHelper.__instance = object.__new__(cls)
        # LayoutHelper.__instance.val = val
        return LayoutHelper.__instance

    def __init__(self):
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)
        self.styles = ['publication', 'presentation', 'teaching']
        self.outputFormats = ['pdf', 'png', 'screen']

    def createFigure(self, style='presentation'):
        if style == 'teaching':
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

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
