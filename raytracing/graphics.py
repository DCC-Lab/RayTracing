import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib import text as mplText
import matplotlib.path as mpath
from typing import List
import numpy as np
import math


class Graphic:
    """ The base class that defines the graphic of any element.

    A Graphic can be a composition of different graphic components (ex.: A lens graphic is two arrows).
    Do not use directly. Use a child class with the desired backend.

    Args:
        *components: The required graphic components that define the Graphic.

            These graphic patches should be instantiated at x = 0 to allow for proper positioning and scaling.

    """

    def __init__(self, components, label: str = None,
                 x=0, y=0, fixedWidth=False):
        self.components = components
        self.label = None

        self.axes = None
        self.x = x
        self.y = y
        self.useAutoScale = not fixedWidth

        if label is not None:
            self.label = Label(text=label, x=self.centroid[0], y=self.halfHeight() * 1.2)
        # fixme: label is still a matplotlib patch

    @property
    def hasLabel(self) -> bool:
        if self.label is None:
            return False
        return True

    def applyTo(self, renderer, x: float = None, y: float = None):
        """ Apply the Graphic on a figure at a given position (x, y) with auto-scale.

        Overwritten for specific backend.

        Args:
            x, y (:obj:`float`, optional): The x and y position in data units where to apply the graphic.
                Defaults to (0, 0).

        """

        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def update(self, x: float = None, y: float = None):
        """ Update the graphic's position and scaling.

        Overwritten for specific backend.

        Args:
            x, y (:obj:`float`, optional): The x and y position where to apply the graphic.
                Defaults to the originally applied position.

        """

        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def halfHeight(self) -> float:
        """ Maximum absolute Y-value of the graphic (not affected by the transforms).
        Used internally to auto-scale. """
        halfHeight = 0
        for component in self.components:
            componentMaxY = np.max(np.abs(component.get_xy()), axis=0)[1]
            if componentMaxY > halfHeight:
                halfHeight = componentMaxY
        return halfHeight

    @property
    def centroid(self):
        xy = []
        for component in self.components:
            xy.extend(component.get_xy())

        return np.mean(xy, axis=0)


class MatplotlibGraphic(Graphic):
    """ The graphic of any element using a Matplotlib backend.

    A Graphic can be a composition of different graphic components (ex.: A lens graphic is two arrows).

    Args:
        *components: The required graphic components (of type `matplotlib.patches.Patch`) that define the Graphic.

            These graphic patches should be instantiated at x = 0 to allow for proper positioning and scaling.

    Examples:
        Create a Graphic from multiple patches

        >>> arrowUp = ArrowPatch(dy=5)
        >>> arrowDown = ArrowPatch(dy=-5)
        >>> lensGraphic = Graphic([arrowUp, arrowDown])

        Apply the Graphic on a figure at x=10

        >>> fig, axes = plt.subplots()
        >>> lensGraphic.applyTo(axes, x=10)

        Take advantage of the auto-scaling feature by updating the Graphic after the figure's limits have changed
        (on a zoom callback)

        >>> lensGraphic.update()

        Update the Graphic's position

        >>> lensGraphic.update(x=5)

    """

    def __init__(self, components: List[patches.Patch], label: str = None,
                 x=0, y=0, fixedWidth=False):

        super(MatplotlibGraphic, self).__init__(components, label, x, y, fixedWidth)

    def applyTo(self, axes: plt.Axes, x: float = None, y: float = None):
        """ Apply the Graphic on a figure at a given position (x, y) with auto-scale.

        Args:
            axes (matplotlib.pyplot.Axes): The figure's Axes on which to apply the graphic.
            x, y (:obj:`float`, optional): The x and y position in data units where to apply the graphic.
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
        """ Update the graphic's position and scaling.

        Args:
            x, y (:obj:`float`, optional): The x and y position where to apply the graphic.
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


class Component:

    @property
    def bezierCurves(self):
        """ A list of bezier curves that defines the graphic of this component.
        To overwrite.
        """
        return []

    @property
    def xy(self):
        # compile A and B of all bezier curves
        return None

    @property
    def patch(self):
        """ Create a Matplotlib Patch from a list of bezier curves """
        return patches.PathPatch()


class BezierCurve:
    def __init__(self, A, B, cp):
        pass


class SurfacePair(Component):
    def __init__(self, surfaceA, surfaceB, halfHeight, x=0.0):
        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.halfHeight = halfHeight
        self.x = x
        self.corners = None
        
    @property
    def bezierCurves(self):
        # coordsA, actionsA = self.pathSurfaceA()
        # coordsB, actionsB = self.pathSurfaceB()
        #
        # self.coords = coordsA + coordsB
        # self.codes = actionsA + actionsB
        # todo
        return []


class SurfacePairPatch(patches.PathPatch):
    def __init__(self, surfaceA, surfaceB, halfHeight, x=0.0):
        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.halfHeight = halfHeight
        self.x = x
        self.corners = None

        super(SurfacePairPatch, self).__init__(self.path(),
                                               color=[0.85, 0.95, 0.95],
                                               fill=True)  # transform=axes.transData

    def pathSurfaceA(self) -> tuple:
        # todo: cleanup
        Path = mpath.Path
        h = self.halfHeight
        R1 = self.surfaceA.R
        v1 = self.x

        if self.surfaceA.R == float("+inf"):
            return [(v1, -h), (v1, h)], [Path.MOVETO, Path.LINETO]

        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        coords = [(corner1, -h), (v1, -ctl1), (v1, 0),
                  (v1, 0), (v1, ctl1), (corner1, h)]
        actions = [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                   Path.LINETO, Path.CURVE3, Path.CURVE3]

        self.corners = [corner1]

        if self.surfaceA.L == 0:  # thin lens exception
            self.surfaceA.L = delta1 * 2

        return coords, actions

    def pathSurfaceB(self) -> tuple:
        Path = mpath.Path
        R2 = self.surfaceB.R
        h = self.halfHeight
        v2 = self.x + self.surfaceA.L

        if self.surfaceB.R == float("+inf"):
            return [(v2, h), (v2, -h), (self.corners[0], -h)], [Path.LINETO, Path.LINETO, Path.LINETO]

        phi2 = math.asin(h / abs(R2))
        delta2 = R2 * (1.0 - math.cos(phi2))
        ctl2 = abs((1.0 - math.cos(phi2)) / math.sin(phi2) * R2)
        corner2 = v2 + delta2

        # append from (corner1, h), stop at (corner1, -h)
        coords = [(corner2, h), (v2, ctl2), (v2, 0),
                  (v2, 0), (v2, -ctl2), (corner2, -h), (self.corners[0], -h)]
        actions = [Path.LINETO, Path.CURVE3, Path.CURVE3,
                   Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO]

        self.corners.append(corner2)

        return coords, actions

    def path(self):
        coordsA, actionsA = self.pathSurfaceA()
        coordsB, actionsB = self.pathSurfaceB()

        path = mpath.Path(coordsA + coordsB,
                          actionsA + actionsB)

        return path

    def get_xy(self):
        return self.get_path().vertices


class ArrowPatch(patches.FancyArrow):
    """Define a FancyArrow patch with default RayTracing style created at (0,0).
    Use with Graphic class to set position and scaling.

    Examples
    --------
        Create a black arrow of height +5
        >>> arrow = ArrowPatch(dy=5)

        Set position and label by creating a Graphic object
        >>> graphic = Graphic([arrow], x=10, label='Image')
    """

    def __init__(self, dy: float, y=0.0, color='k', width=0.002, headLengthRatio=0.1):
        super(ArrowPatch, self).__init__(x=0, y=y, dx=0, dy=dy,
                                         fc=color, ec=color,
                                         width=width, length_includes_head=True,
                                         head_width=width * 5, head_length=abs(dy) * headLengthRatio)


class DoubleArrowPatch(patches.PathPatch):
    """Define a thin double arrow patch with default RayTracing style created at (0,0).
    Use with Graphic class to set position and scaling.

    Examples
    --------
        Create a black double arrow with a total height of 10
        >>> arrow = DoubleArrowPatch(height=10)

        Set position and label by creating a Graphic object
        >>> graphic = Graphic([arrow], x=5, label='Lens')

    """

    def __init__(self, height: float, color='k'):
        self.y = height / 2

        super(DoubleArrowPatch, self).__init__(self.path(), color=color, fill=False, linewidth=1.5)

    def path(self):
        h = self.y
        dy = h * 0.2
        dx = 0.008
        Path = mpath.Path

        coords = [(0, -h), (0, h),
                  (-dx, h-dy), (0, h), (dx, h-dy),
                  (-dx, -h+dy), (0, -h), (dx, -h+dy)]
        actions = [Path.MOVETO, Path.LINETO,
                   Path.MOVETO, Path.LINETO, Path.LINETO,
                   Path.MOVETO, Path.LINETO, Path.LINETO]

        return Path(coords, actions)

    def get_xy(self):
        return self.get_path().vertices


class AperturePatch(patches.Polygon):
    """Define a Polygon patch with default RayTracing style used to draw the aperture.
    Use with Graphic class to set position and scaling.

    Examples
    --------
        Create aperture patches for a lens
        >>> apertureAbove = AperturePatch(y=halfHeight)
        >>> apertureBelow = AperturePatch(y=-halfHeight)

        Create aperture patches for a thick lens
        >>> apertureAbove = AperturePatch(y=halfHeight, width=0.1)
        >>> apertureBelow = AperturePatch(y=-halfHeight, width=0.1)

        Create thick lens Graphic with a fixed width (autoScale Off)
        >>> graphic = Graphic([thickLens, apertureAbove, apertureBelow], fixedWidth=True)
    """

    def __init__(self, y: float, x=0.0, width=0.01, color='0.7'):
        if width <= 0.01:
            coords = [[x - 0.01 / 2, y], [x + 0.01 / 2, y]]
        else:
            coords = [[x, y], [x + width, y]]
        super(AperturePatch, self).__init__(coords,
                                            linewidth=3,
                                            closed=False,
                                            color=color)


class Label(mplText.Text):
    def __init__(self, text: str, x=0.0, y=0.0, fontsize=8):
        super(Label, self).__init__(x=x, y=y, text=text, fontsize=fontsize, horizontalalignment='center')

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
