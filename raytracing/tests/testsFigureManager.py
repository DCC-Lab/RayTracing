import unittest
import envtest  # modifies path  # fixme: requires path to /tests
from raytracing import *
from raytracing.figureManager import FigureManager  # todo: append init
from raytracing.drawing import *

# FIXME: Temporary display tests


class TestFigureManager(unittest.TestCase):
    def testHandleDrawings(self):
        figure = FigureManager()
        figure.createFigure()

        components = [ArrowPatch(dy=5),
                      ArrowPatch(dy=-5),
                      StopPatch(y=5),
                      StopPatch(y=-5)]

        figure.add(Drawing(ArrowPatch(dy=5, color='b'), x=0, label="Object"))
        figure.add(Drawing(ArrowPatch(dy=-5, color='r'), x=7.6, label="Label 1"))
        figure.add(Drawing(ArrowPatch(dy=-5, color='r'), x=7.8, label="Label 2"))
        figure.add(Drawing(*components, x=8, label="Label 3"))

        figure.draw()

        figure.display()

    def testFigureFromPath(self):
        # path = ImagingPath()
        # path.append(Space(d=40))
        # path.append(Lens(f=5))
        # path.append(Space(d=10))
        # path.newDisplay()

        path = ImagingPath()
        path.label = "Thick diverging lens"
        path.objectHeight = 20
        path.append(Space(d=25))
        path.append(Lens(f=8, label='Lens'))
        path.append(Space(d=25))
        path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='ThickLens'))
        path.append(Space(d=5))
        path.newDisplay(onlyChiefAndMarginalRays=True)
