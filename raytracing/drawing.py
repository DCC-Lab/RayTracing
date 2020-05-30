import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib import text as mplText
import matplotlib.path as mpath
from typing import List
import numpy as np
import math


class Drawing:
    """ The drawing of any element.

    A Drawing can be a composition of different drawing components (ex.: A lens drawing is two arrows).

    Args:
        *components: The required drawing components (of type `matplotlib.patches.Patch`) that define the Drawing.

            These drawing patches should be instantiated at x = 0 to allow for proper positioning and scaling.

    Examples:
        Create a Drawing from multiple patches

        >>> arrowUp = ArrowPatch(dy=5)
        >>> arrowDown = ArrowPatch(dy=-5)
        >>> lensDrawing = Drawing(arrowUp, arrowDown)

        Apply the Drawing on a figure at x=10

        >>> fig, axes = plt.subplots()
        >>> lensDrawing.applyTo(axes, x=10)

        Take advantage of the auto-scaling feature by updating the Drawing after the figure's limits have changed
        (on a zoom callback)

        >>> lensDrawing.update()

        Update the Drawing's position

        >>> lensDrawing.update(x=5)

    """

    def __init__(self, *components: patches.Patch, label: str = None,
                 x=0, y=0, fixedWidth=False):
        self.components: List[patches.Patch] = [*components]  # could be renamed to drawings, parts, patches, artists...
        self.label = None

        self.axes = None
        self.x = x
        self.y = y
        self.useAutoScale = not fixedWidth

        if label is not None:
            self.label = Label(text=label, y=self.halfHeight() * 1.2)

    @property
    def hasLabel(self) -> bool:
        if self.label is None:
            return False
        return True

    def applyTo(self, axes: plt.Axes, x: float = None, y: float = None):
        """ Apply the Drawing on a figure at a given position (x, y) with auto-scale.

        Args:
            axes (matplotlib.pyplot.Axes): The figure's Axes on which to apply the drawing.
            x, y (:obj:`float`, optional): The x and y position in data units where to apply the drawing.
                Defaults to (0, 0).

        """

        self.axes = axes
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        self.update()

        for component in self.components:
            self.axes.add_patch(component)

        if self.label is not None:
            self.axes.add_artist(self.label)

    def update(self, x: float = None, y: float = None):
        """ Update the drawing's position and scaling.

        Args:
            x, y (:obj:`float`, optional): The x and y position where to apply the drawing.
                Defaults to the originally applied position.

        """

        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        xScaling, yScaling = self.scaling()

        translation = transforms.Affine2D().translate(self.x, self.y)
        scaling = transforms.Affine2D().scale(xScaling, yScaling)

        for component in self.components:
            component.set_transform(scaling + translation + self.axes.transData)

        if self.label is not None:
            self.label.set_transform(translation + self.axes.transData)

    def scaling(self):
        """ Used internally to compute the required scale transform so that the width of the objects stay the same
        respective to the Axes. """
        if not self.useAutoScale:
            return 1, 1

        xScale, yScale = self.axesToDataScale()

        heightFactor = self.halfHeight() * 2 / yScale
        xScaling = xScale * (heightFactor / 0.2) ** (3 / 4)

        return xScaling, 1

    def axesToDataScale(self):
        """ Dimensions of the figure in data units. """
        xScale, yScale = self.axes.viewLim.bounds[2:]

        return xScale, yScale

    def halfHeight(self) -> float:
        """ Maximum absolute Y-value of the drawing (not affected by the transforms).
        Used internally to auto-scale. """
        halfHeight = 0
        for component in self.components:
            componentMaxY = np.max(np.abs(component.get_xy()), axis=0)[1]
            if componentMaxY > halfHeight:
                halfHeight = componentMaxY
        return halfHeight


class ArrowPatch(patches.FancyArrow):
    """Define a FancyArrow patch with default RayTracing style created at (0,0).
    Use with Drawing class to set position and scaling.

    Examples
    --------
        Create a black arrow of height +5
        >>> arrow = ArrowPatch(dy=5)

        Set position and label by creating a Drawing object
        >>> drawing = Drawing(arrow, x=10, label='Image')
    """

    def __init__(self, dy: float, y=0.0, color='k', width=0.002, headLengthRatio=0.1):
        super(ArrowPatch, self).__init__(x=0, y=y, dx=0, dy=dy,
                                         fc=color, ec=color,
                                         width=width, length_includes_head=True,
                                         head_width=width * 5, head_length=abs(dy) * headLengthRatio)


class SurfacePairPatch(patches.PathPatch):
    # TODO
    def __init__(self, surfaceA, surfaceB, halfHeight, x=0.0):
        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.halfHeight = halfHeight
        self.x = x
        self.xy = None
        self.centerWidth = None
        self.xLink = None

        super(SurfacePairPatch, self).__init__(self.path(),
                                               color=[0.85, 0.95, 0.95],
                                               fill=True)  # transform=axes.transData

    def pathSurfaceA(self) -> tuple:
        # todo: cleanup
        # todo: R=+inf exception
        h = self.halfHeight
        R1 = self.surfaceA.R
        v1 = self.x

        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1
        corner2 = corner1 + self.surfaceA.L

        Path = mpath.Path
        coords = [(corner2, -h),
                  (corner1, -h), (v1, -ctl1), (v1, 0),
                  (v1, 0), (v1, ctl1), (corner1, h),
                  (corner2, h)]
        actions = [Path.MOVETO,
                   Path.LINETO, Path.CURVE3, Path.CURVE3,
                   Path.LINETO, Path.CURVE3, Path.CURVE3,
                   Path.LINETO]

        self.xy = [(corner2, -h), (corner1, -h), (v1, 0), (corner1, h), (corner2, h)]
        self.centerWidth = self.surfaceA.L + delta1
        self.xLink = corner2

        return coords, actions

    def pathSurfaceB(self) -> tuple:
        # use self.xLink as corner2

        v2 = v1 + self.L
        phi2 = math.asin(h / abs(R2))
        delta2 = R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * R2)
        corner2 = v2 + delta2

        # path commands for simple arc from (corner2, h) to (corner2, -h)
        # + R=inf exception

        self.xy.append((v2, 0))
        self.centerWidth -= delta2
        return coords, actions

    def path(self):
        coordsA, actionsA = self.pathSurfaceA()
        coordsB, actionsB = self.pathSurfaceB()

        path = mpath.Path(coordsA.extend(coordsB),
                          actionsA.extend(actionsB))

        return path

    def get_xy(self):
        return self.xy


class StopPatch(patches.Polygon):
    """Define a Polygon patch with default RayTracing style used for aperture stops.
    Use with Drawing class to set position and scaling.

    Examples
    --------
        Create aperture stops for a lens
        >>> stopAbove = StopPatch(y=halfHeight)
        >>> stopBelow = StopPatch(y=-halfHeight)

        Create aperture stops for a thick lens
        >>> stopAbove = StopPatch(y=halfHeight, width=0.1)
        >>> stopBelow = StopPatch(y=-halfHeight, width=0.1)

        Create thick lens Drawing with a fixed width (autoScale Off)
        >>> drawing = Drawing(thickLens, stopAbove, stopBelow, fixedWidth=True)
    """

    def __init__(self, y: float, width=0.01):
        super(StopPatch, self).__init__([[- width / 2, y],
                                         [+ width / 2, y]],
                                        linewidth=3,
                                        closed=False,
                                        color='0.7')


class Label(mplText.Text):
    def __init__(self, text: str, x=0.0, y=0.0):
        super(Label, self).__init__(x=x, y=y, text=text, fontsize=8, horizontalalignment='center')

        self.offset = 0.0

    @property
    def position(self):
        return self.get_position()

    @position.setter
    def position(self, xy: tuple):
        self.set_position(xy)

    def isRenderedOn(self, figure: plt.Figure):
        """Whether the label is rendered on the given figure (i.e. visible when displayed)."""
        if self.get_tightbbox(figure.canvas.get_renderer()) is None:
            return False
        return True

    def boundingBox(self, axes: plt.Axes, figure: plt.Figure, stretch=1.2) -> transforms.BboxBase:
        """Bounding box of the label drawn on a figure.
        Stretched in the x-axis to give more free space to the labels."""

        displayBox = self.get_tightbbox(figure.canvas.get_renderer())
        dataBox = displayBox.inverse_transformed(axes.transData)
        dataBox = dataBox.expanded(sw=stretch, sh=1)
        return dataBox

    def translate(self, dx: float):
        """Translate the label in the x-axis by a small amount 'dx'.

        The offset is stackable and can be removed with the method resetPosition().
        Used by the FigureManager to solve overlapping issues with the labels.
        """
        self.offset += dx

        x, y = self.get_position()
        self.set_position((x + dx, y))

    def resetPosition(self):
        """Remove the effect of previous translations."""
        x, y = self.get_position()
        self.set_position((x - self.offset, y))

        self.offset = 0.0
