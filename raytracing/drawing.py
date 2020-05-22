import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from typing import List
import numpy as np


class Drawing:
    """ The drawing of any element.

    A Drawing can be a composition of different drawing components (ex.: A lens drawing is two arrows).

    Args:
        *components: The required drawing components (of type `matplotlib.patches.Patch`) that define the Drawing.

            These drawing patches should be instantiated at x = 0 to allow for proper positioning and scaling.

    Examples:
        Create a Drawing from multiple patches

        >>> arrowUp = ArrowPatch(dy=5, headLengthRatio=0.2)
        >>> arrowDown = ArrowPatch(dy=-5, headLengthRatio=0.2)
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
            self.createLabel(label)

    def createLabel(self, label: str):
        self.label = Label(text=label, y=self.halfHeight() * 1.2)

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

    def append(self, component: patches.Patch):
        self.components.append(component)

    def remove(self):
        """ Remove the Drawing from the figure. """

        for component in self.components:
            component.remove()


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

    def __init__(self, dy: float, color='k', width=0.002, headLengthRatio=0.1):
        super(ArrowPatch, self).__init__(x=0, y=0, dx=0, dy=dy,
                                         fc=color, ec=color,
                                         width=width, length_includes_head=True,
                                         head_width=width * 5, head_length=abs(dy) * headLengthRatio)


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
        super(StopPatch, self).__init__([[- width/2, y],
                                         [+ width/2, y]],
                                        linewidth=3,
                                        closed=False,
                                        color='0.7')

