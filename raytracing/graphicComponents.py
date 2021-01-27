from typing import Union, List, Tuple
from matplotlib import text as mplText
from matplotlib import path as mpath
from matplotlib import transforms
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import math


class BezierCurve:
    """ A bezier curve defined by a set of control points from P0 to Pn
    where n is the order (1=linear, 2=quadratic, etc.).

    Arguments
    ---------
    controlPoints: List
        A list of (x, y) coordinates for the control points.

    """

    def __init__(self, controlPoints: List[Tuple[float, float]]):
        self.controlPoints = controlPoints

    @property
    def xy(self):
        """The (x, y) coordinates of the end points of the curve. """
        return self.controlPoints[0], self.controlPoints[-1]

    @property
    def isLinear(self):
        return len(self.controlPoints) == 2

    @property
    def isQuadratic(self):
        return len(self.controlPoints) == 3


class Component:
    """ The base class for all graphic components. Defined from bezier curves. """

    def __init__(self, color=(0.85, 0.95, 0.95), fill=True, lineWidth=1.0, lineStyle='-', hasFixedWidth=True):

        self.color = color
        self.fill = fill
        self.lineWidth = lineWidth
        self.lineStyle = lineStyle
        self.hasFixedWidth = hasFixedWidth

        self._patch = None
        self._isVisible = True

    @property
    def bezierCurves(self) -> List[BezierCurve]:
        """ A list of bezier curves that defines the graphic of this component.
        To overwrite.
        """
        return []

    @property
    def xy(self) -> List[Tuple]:
        """ The (x, y) coordinates of the component. """
        xy = []
        for bezierCurve in self.bezierCurves:
            xy.extend(bezierCurve.xy)
        xy = list(set(xy))  # remove duplicates
        return xy

    @property
    def length(self):
        minX = np.min(self.xy, axis=0)
        maxX = np.max(self.xy, axis=0)
        return maxX - minX

    @property
    def patch(self):
        """ A Matplotlib Patch of the component. Used to draw on a matplotlib figure. """
        if self._patch is None:
            coords = []
            codes = []
            for bezierCurve in self.bezierCurves:
                newCoords = bezierCurve.controlPoints
                if bezierCurve.isLinear:
                    newCodes = [mpath.Path.MOVETO, mpath.Path.LINETO]
                elif bezierCurve.isQuadratic:
                    newCodes = [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]
                else:
                    raise NotImplemented("BezierCurves of order > 2 not supported. ")

                if coords:
                    # Join lines if point in common
                    if newCoords[0] == coords[-1]:
                        newCodes[0] = mpath.Path.LINETO

                codes.extend(newCodes)
                coords.extend(newCoords)
            self._patch = patches.PathPatch(mpath.Path(coords, codes), color=self.color, fill=self.fill,
                                            linewidth=self.lineWidth, linestyle=self.lineStyle, visible=self.isVisible)
        return self._patch

    @property
    def isVisible(self):
        return self._isVisible

    @isVisible.setter
    def isVisible(self, value):
        self._isVisible = value
        if self._patch is not None:
            self._patch.set_visible(self._isVisible)

    @staticmethod
    def linearBezierCurvesFrom(controlPoints: List[Tuple]) -> List[BezierCurve]:
        """ A list of linear bezier curves that go through all points.

        Arguments
        ---------
        controlPoints: List
            The coordinates in (x, y) tuples that define all required linear bezier curves.
        """

        bezierCurves = []
        for i, cpA in enumerate(controlPoints[:-1]):
            cpB = controlPoints[i + 1]
            bezierCurves.append(BezierCurve([cpA, cpB]))
        return bezierCurves


class Arrow(Component):
    """ A standard arrow graphic component.

    Arguments
    ---------
    dy: float
        Total height of the arrow from 'y'.

    Other parameters
    ----------------
    y: float
        Starting point in y-axis where the base of the arrow sits. Defaults to 0.
    """

    def __init__(self, dy: float, y=0.0, color='k', width=0.002, headLengthRatio=0.1, fill=True, lineStyle='-'):
        super(Arrow, self).__init__(color=color, hasFixedWidth=False, fill=fill, lineStyle=lineStyle, lineWidth=0.5)
        self.dy = dy
        self.y = y
        self.width = width

        self.headWidth = width * 5
        self.headLength = dy * headLengthRatio

    @property
    def bezierCurves(self):
        """ The standard thick arrow is defined by a list of straight lines that surround the arrow. """
        dx0 = self.width / 2
        dx1 = self.headWidth / 2
        dy = self.y + self.dy
        dy1 = dy - self.headLength

        p0 = (-dx0, self.y)
        p1 = (-dx0, dy1)
        p2 = (-dx1, dy1)
        p3 = (0, dy)
        p4 = (dx1, dy1)
        p5 = (dx0, dy1)
        p6 = (dx0, self.y)

        return self.linearBezierCurvesFrom([p0, p1, p2, p3, p4, p5, p6, p0])

    @property
    def length(self):
        return 0


class Rectangle(Component):
    def __init__(self, xy: tuple, width: float, height: float, color='k', fill=False, lineWidth=1, lineStyle='-'):
        super(Rectangle, self).__init__(color=color, fill=fill, lineWidth=lineWidth, lineStyle=lineStyle)

        self.x, self.y = xy
        self.width = width
        self.height = height

    @property
    def bezierCurves(self):
        p0 = (self.x, self.y)
        p1 = (self.x, self.y + self.height)
        p2 = (self.x + self.width, self.y + self.height)
        p3 = (self.x + self.width, self.y)

        return self.linearBezierCurvesFrom([p0, p1, p2, p3, p0])


class Surface(Component):
    def __init__(self, surface, halfHeight, x=0.0, color='k'):
        super(Surface, self).__init__(color=color, fill=False)
        self.surface = surface
        self.halfHeight = halfHeight
        self.x = x

    @property
    def bezierCurves(self) -> List[BezierCurve]:
        h = self.halfHeight
        v1 = self.x

        if self.surface.R == float("+inf"):
            return [BezierCurve([(v1, -h), (v1, h)])]

        R1 = self.surface.R
        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        return [BezierCurve([(corner1, -h), (v1, -ctl1), (v1, 0)]),
                BezierCurve([(v1, 0), (v1, ctl1), (corner1, h)])]


class SurfacePair(Component):
    def __init__(self, surfaceA, surfaceB, halfHeight, x=0.0):
        colorValue = 1.0 - np.min([(surfaceA.n - 1) ** 2 / 2, 0.5])
        color = (colorValue - 0.1, colorValue, 0.95)
        super(SurfacePair, self).__init__(color=color)

        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.halfHeight = halfHeight
        self.x = x
        self.corners = None

        self.pathSurfaceA = self.getPathA()
        self.pathSurfaceB = self.getPathB()

    @property
    def bezierCurves(self) -> List[BezierCurve]:
        bezierCurves = []
        bezierCurves.extend(self.pathSurfaceA)
        bezierCurves.extend(self.pathSurfaceB)
        return bezierCurves

    def getPathA(self) -> List[BezierCurve]:
        h = self.halfHeight
        v1 = self.x

        if type(self.surfaceA).__name__ == 'ConicalInterface':
            a = self.surfaceA.alpha
            corner = v1 - np.tan(a) * h
            self.corners = [corner]
            return [BezierCurve([(corner, -h), (v1, 0)]), BezierCurve([(v1, 0), (corner, h)])]

        if self.surfaceA.R == float("+inf"):
            self.corners = [v1]
            return [BezierCurve([(v1, -h), (v1, h)])]

        R1 = self.surfaceA.R
        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        self.corners = [corner1]
        if self.surfaceA.L == 0:  # realistic thin lens exception
            self.surfaceA.L = delta1 * 2

        return [BezierCurve([(corner1, -h), (v1, -ctl1), (v1, 0)]),
                BezierCurve([(v1, 0), (v1, ctl1), (corner1, h)])]

    def getPathB(self) -> List[BezierCurve]:
        h = self.halfHeight
        v2 = self.x + self.surfaceA.L

        if type(self.surfaceB).__name__ == 'ConicalInterface':
            a = self.surfaceB.alpha
            delta = np.tan(a) * h
            corner2 = v2 + delta
            self.corners.append(corner2)
            return [BezierCurve([(self.corners[0], h), (corner2, h)]),
                    BezierCurve([(corner2, h), (v2, 0)]),
                    BezierCurve([(v2, 0), (corner2, -h)]),
                    BezierCurve([(corner2, -h), (self.corners[0], -h)])]

        if self.surfaceB.R == float("+inf"):
            self.corners.append(v2)
            return [BezierCurve([(self.corners[0], h), (v2, h)]),
                    BezierCurve([(v2, h), (v2, -h)]),
                    BezierCurve([(v2, -h), (self.corners[0], -h)])]

        R2 = self.surfaceB.R
        phi2 = math.asin(h / abs(R2))
        delta2 = R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * R2)
        corner2 = v2 + delta2
        self.corners.append(corner2)

        return [BezierCurve([(self.corners[0], h), (corner2, h)]),
                BezierCurve([(corner2, h), (v2, ctl2), (v2, 0)]),
                BezierCurve([(v2, 0), (v2, -ctl2), (corner2, -h)]),
                BezierCurve([(corner2, -h), (self.corners[0], -h)])]


class DoubleThinArrow(Component):
    """ A thin arrow centered on y-axis with an arrow head on both ends. """

    def __init__(self, height: float, color='k', headWidth=0.01, headLengthRatio=0.12):
        super(DoubleThinArrow, self).__init__(color=color, lineWidth=1.5, fill=False, hasFixedWidth=False)

        self.dy = height / 2
        self.headWidth = headWidth
        self.headLength = self.dy * headLengthRatio

    @property
    def bezierCurves(self):
        """ The thin arrow is defined by a list of straight lines without the notion of contours. """
        dx1 = self.headWidth / 2
        dy1 = self.dy - self.headLength

        topHead = self.linearBezierCurvesFrom([(-dx1, dy1), (0, self.dy), (dx1, dy1)])
        bottomHead = self.linearBezierCurvesFrom([(-dx1, -dy1), (0, -self.dy), (dx1, -dy1)])

        bezierCurves = [BezierCurve([(0, -self.dy), (0, self.dy)])]
        bezierCurves.extend(topHead)
        bezierCurves.extend(bottomHead)

        return bezierCurves


class ApertureBars(Component):
    """Define an aperture graphic component with default RayTracing style used to draw the apertures. """

    def __init__(self, y: float, x=0.0, width=0.0, color='0.7'):
        super().__init__(color=color, fill=False, lineWidth=3)
        if width == 0.0:
            width = 0.01
            self.hasFixedWidth = False

        self.width = width
        self.y = y
        self.x = x

    @property
    def bezierCurves(self) -> List[BezierCurve]:
        """ An aperture component is defined as a straight line at 'y' and '-y'. """
        if self.width <= 0.01:
            coordsTop = [(self.x - 0.005, self.y), (self.x + 0.005, self.y)]
            coordsBottom = [(self.x - 0.005, -self.y), (self.x + 0.005, -self.y)]
        else:
            coordsTop = [(self.x, self.y), (self.x + self.width, self.y)]
            coordsBottom = [(self.x, -self.y), (self.x + self.width, -self.y)]

        return [BezierCurve(coordsTop), BezierCurve(coordsBottom)]


class Polygon(Component):
    def __init__(self, points: List[tuple], lineWidth=1.0, color='k', fill=False, lineStyle='-'):
        super(Polygon, self).__init__(color=color, fill=fill, lineWidth=lineWidth, lineStyle=lineStyle)
        self.points = points

    @property
    def bezierCurves(self) -> List[BezierCurve]:
        return self.linearBezierCurvesFrom(self.points)


class Label:
    """ Label base class. Promoted to MplLabel by the Figure Manager if using a matplotlib backend.
    A label can have a text and a point, independently, but the point will always sit on the optical axis at y=0.
    """

    def __init__(self, text: str = None, x=0.0, y=0.0, fontsize=10, hasPointMarker=False, color='k',
                 useDataUnits=True, alignment='center'):
        self.text = text
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.useDataUnits = useDataUnits
        self.alignment = alignment

        self.offset = 0.0
        self.hasPointMarker = hasPointMarker
        self.color = color

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, xy: tuple):
        self.x, self.y = xy

    def translate(self, dx: float):
        """Translate the label in the x-axis by a small amount 'dx'.

        The offset is stackable and can be removed with the method resetPosition().
        Used by the FigureManager to solve overlapping issues with the labels.
        """
        self.offset += dx

        x, y = self.position
        self.position = (x + dx, y)

    def resetPosition(self):
        """Remove the effect of previous translations."""
        x, y = self.position
        self.position = (x - self.offset, y)

        self.offset = 0.0

    @property
    def mplLabel(self) -> 'MplLabel':
        # fixme? promoting to mplLabel to help the figure manager
        return MplLabel(self.text, self.x, self.y, self.fontsize, self.hasPointMarker, self.color, self.useDataUnits,
                        self.alignment)


class MplLabel(Label):
    def __init__(self, text: str = None, x=0.0, y=0.0, fontsize=10, hasPointMarker=False, color='k',
                 useDataUnits=True, alignment='center'):
        super(MplLabel, self).__init__(text, x=x, y=y, fontsize=fontsize, hasPointMarker=hasPointMarker,
                                       color=color, useDataUnits=useDataUnits, alignment=alignment)

        self.patch = None
        if text is not None:
            self.patch = mplText.Text(x=x, y=y, text=text, fontsize=fontsize, horizontalalignment=self.alignment)

    @Label.position.setter
    def position(self, xy: tuple):
        self.x, self.y = xy
        self.patch.set_position(xy)

    def isRenderedOn(self, figure: plt.Figure):
        """Whether the label is rendered on the given figure (i.e. visible when displayed)."""
        if self.patch.get_tightbbox(figure.canvas.get_renderer()) is None:
            return False
        return True

    def boundingBox(self, axes: plt.Axes, figure: plt.Figure, stretch=1.2) -> transforms.BboxBase:
        """Bounding box of the label drawn on a figure.
        Stretched in the x-axis to give more free space to the labels."""

        displayBox = self.patch.get_tightbbox(figure.canvas.get_renderer())
        dataBox = displayBox.transformed(axes.transData.inverted())

        dataBox = dataBox.expanded(sw=stretch, sh=1)
        return dataBox


class Point(Label):
    def __init__(self, x=0.0, y=0.0, text=None, fontsize=12, color='k', hasMarker=True):
        super().__init__(text=text, x=x, y=y, fontsize=fontsize, hasPointMarker=hasMarker, color=color)


class Line:
    """ A 2D data line object """

    def __init__(self, xData, yData, color: Union[tuple, str] = 'k', lineWidth=1, lineStyle='-', label=None):
        super().__init__()
        self.xData = xData
        self.yData = yData
        self.color = color
        self.lineWidth = lineWidth
        self.lineStyle = lineStyle
        self.label = label

        self._isVisible = True
        self._patch = None

    @property
    def patch(self):
        if self._patch is None:
            self._patch = plt.Line2D(self.xData, self.yData, color=self.color, label=self.label,
                                     linewidth=self.lineWidth, linestyle=self.lineStyle, visible=self.isVisible)
        return self._patch

    @property
    def isVisible(self):
        return self._isVisible

    @isVisible.setter
    def isVisible(self, value):
        self._isVisible = value
        if self._patch is not None:
            self._patch.set_visible(self._isVisible)


class ArrowAnnotation:
    def __init__(self, A: tuple, B: tuple, arrowStyle='<->', color='k'):
        self.A = A
        self.B = B
        self.arrowStyle = arrowStyle
        self.color = color

    @property
    def patch(self):
        return patches.FancyArrowPatch(posA=self.A, posB=self.B,
                                       arrowstyle=self.arrowStyle, color=self.color, mutation_scale=10)
