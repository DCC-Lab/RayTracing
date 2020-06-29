from raytracing.graphicComponents import *
import numpy as np


class Graphic:
    """ The base class that defines the graphic of any element.

    A Graphic can be a composition of different graphic components (ex.: A lens graphic is two arrows).

    Args:
        *components: The required graphic components that define the Graphic.

            These graphic components should be instantiated at x = 0 to allow for proper positioning and scaling.

    """

    def __init__(self, components=None, label: str = None,
                 x=0, y=0, fixedWidth=False):
        self._components = components
        self.label = None
        self.points = []

        self.x = x
        self.y = y
        self.useAutoScale = not fixedWidth

        if label is not None:
            self.label = Label(text=label, x=self.centroid[0], y=self.halfHeight * 1.2)

    @property
    def hasLabel(self):
        if self.label is None:
            return False
        return True

    @property
    def components(self):
        """ Can be overwritten by other graphics """
        return self._components

    @property
    def halfHeight(self) -> float:
        """ Maximum absolute Y-value of the graphic (not affected by the transforms).
        Used internally to auto-scale. """
        halfHeight = 0
        for component in self.components:
            componentMaxY = np.max(np.abs(component.xy), axis=0)[1]
            if componentMaxY > halfHeight:
                halfHeight = componentMaxY
        return halfHeight

    @property
    def centroid(self):
        xy = []
        for component in self.components:
            xy.extend(component.get_xy())

        return np.mean(xy, axis=0)

    @property
    def patches2D(self):
        return [c.patch for c in self.components]

    @property
    def length(self):
        return np.sum([c.length for c in self.components])


class GraphicOf:
    def __new__(cls, element) -> Union[Graphic, None]:
        instance = type(element).__name__
        if instance is 'Lens':
            return LensGraphic(element)
        if instance is 'Space':
            return None
        if instance is 'Aperture':
            return ApertureGraphic(element)
        else:
            return cls.matrixGraphic(element)

    @classmethod
    def matrixGraphic(cls, element):
        components = []  # todo: black box (rectangle component)
        components.extend(cls.apertureComponents(element))
        return Graphic(components)

    @classmethod
    def apertureComponents(cls, element):
        components = []
        if element.apertureDiameter != float('+Inf'):
            halfHeight = element.apertureDiameter / 2.0
            components.append(Aperture(y=halfHeight, width=element.L))
            components.append(Aperture(y=-halfHeight, width=element.L))
        return components


class MatrixGraphic(Graphic):
    def __init__(self, matrix, fixedWidth=False):
        super(MatrixGraphic, self).__init__(fixedWidth=fixedWidth)
        self.matrix = matrix

    @property
    def components(self):
        if self._components is None:
            self._components = self.mainComponents
            self._components.extend(self.apertureComponents)

            (f1, f2) = self.matrix.focusPositions(self.x)
            if f1 is not None:
                self.points.append(Label(x=f1, hasPoint=True))
            if f2 is not None:
                self.points.append(Label(x=f2, hasPoint=True))

            # self.drawLabels(z=0, axes=axes)
            # self.drawCardinalPoints(z=0, axes=axes)
            # if self.matrix.L != 0:
            #     self.drawVertices(z=0, axes=axes)
            # self.drawPointsOfInterest(z=0, axes=axes)
            # self.drawPrincipalPlanes(z=0, axes=axes)
        return self._components

    @property
    def mainComponents(self):
        return []

    @property
    def apertureComponents(self):
        # todo: make Aperture a single component with +- y
        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0
            return [Aperture(y=halfHeight, width=self.matrix.L),
                    Aperture(y=-halfHeight, width=self.matrix.L)]


class LensGraphic(MatrixGraphic):
    @property
    def mainComponents(self):
        return [DoubleThinArrow(self.matrix.displayHalfHeight()*2)]


class ApertureGraphic(MatrixGraphic):
    def __init__(self, matrix):
        super().__init__(matrix, fixedWidth=True)
