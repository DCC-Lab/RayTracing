from raytracing.graphicComponents import *
import numpy as np


class Graphic:
    """ The base class that defines the graphic of any element.

    A Graphic can be a composition of different graphic components (ex.: A lens graphic is two arrows).

    Args:
        *components: The required graphic components that define the Graphic.

            These graphic components should be instantiated at x = 0 to allow for proper positioning and scaling.

    """

    def __init__(self, components, label: str = None,
                 x=0, y=0, fixedWidth=False):
        self.components = components
        self.label = None

        self.x = x
        self.y = y
        self.useAutoScale = not fixedWidth

        if label is not None:
            self.label = MplLabel(text=label, x=self.centroid[0], y=self.halfHeight * 1.2)
        # fixme: label is still a matplotlib patch

    @property
    def hasLabel(self) -> bool:
        if self.label is None:
            return False
        return True

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
    # fixme: not sure this logistic is ideal...
    #  maybe change components to _components property with default to None...
    #  and move aperture component to MatrixGraphic or something...
    def __init__(self, matrix):
        self.matrix = matrix
        super(MatrixGraphic, self).__init__(components=self.getComponents())

    def getComponents(self):
        components = []  # todo: black box (rectangle component)
        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0
            components.append(Aperture(y=halfHeight, width=self.matrix.L))
            components.append(Aperture(y=-halfHeight, width=self.matrix.L))
        return components


class LensGraphic(MatrixGraphic):
    def getComponents(self):
        components = [DoubleThinArrow(self.matrix.displayHalfHeight()*2)]
        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0
            components.append(Aperture(y=halfHeight, width=self.matrix.L))
            components.append(Aperture(y=-halfHeight, width=self.matrix.L))
        return components


class ApertureGraphic(MatrixGraphic):
    def __init__(self, matrix):
        super(ApertureGraphic, self).__init__(matrix=matrix)
        super(MatrixGraphic, self).__init__(components=self.getComponents(), fixedWidth=True)

    def getComponents(self):
        components = []
        if self.matrix.apertureDiameter != float('+Inf'):
            halfHeight = self.matrix.apertureDiameter / 2.0
            components.append(Aperture(y=halfHeight, width=self.matrix.L))
            components.append(Aperture(y=-halfHeight, width=self.matrix.L))
        return components
