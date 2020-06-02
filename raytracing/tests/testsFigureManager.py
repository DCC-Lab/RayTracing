import unittest
import envtest  # modifies path  # fixme: requires path to /tests
from raytracing import *
from raytracing.figureManager import FigureManager  # todo: append init
from raytracing.drawing import *

# FIXME: Temporary display tests


class TestFigureManager(unittest.TestCase):
    def testFigureFromPath(self):
        # path = ImagingPath()
        # path.append(Space(d=40))
        # path.append(Lens(f=5))
        # path.append(Space(d=10))
        # path.display(onlyChiefAndMarginalRays=True)
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
