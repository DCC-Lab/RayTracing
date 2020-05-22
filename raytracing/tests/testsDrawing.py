import unittest
import envtest  # modifies path  # fixme: requires path to /tests
from raytracing.drawing import Drawing, ArrowPatch, StopPatch
import matplotlib.pyplot as plt

# FIXME: Temporary display tests


class TestDrawing(unittest.TestCase):
    def testLensDrawing(self):
        arrowUp = ArrowPatch(dy=5)
        arrowDown = ArrowPatch(dy=-5)
        drawings = [Drawing(arrowUp, arrowDown, x=8), Drawing(ArrowPatch(dy=5), x=0)]

        fig, axes = plt.subplots(figsize=(10, 7))

        for d in drawings:
            d.applyTo(axes)

        plt.ylim(-7.5, 7.5)
        plt.xlim(-0.5, 8.5)

        for d in drawings:
            d.update()

        plt.show()

    def testLensAndApertureDrawing(self):
        apertureDiameter = 10

        halfHeight = apertureDiameter / 2.0

        components = [ArrowPatch(dy=halfHeight, headLengthRatio=0.2),
                      ArrowPatch(dy=-halfHeight, headLengthRatio=0.2),
                      StopPatch(y=halfHeight),
                      StopPatch(y=-halfHeight)]

        drawing = Drawing(*components, x=8, label="Nada")

        fig, axes = plt.subplots(figsize=(10, 7))
        plt.ylim(-10, 10)
        plt.xlim(-10, 10)

        drawing.applyTo(axes)
        plt.show()

    def testThickApertureDrawingWithFixedWidth(self):
        apertureDiameter = 10

        halfHeight = apertureDiameter / 2.0

        components = [StopPatch(y=halfHeight, width=1),
                      StopPatch(y=-halfHeight, width=1)]

        drawing = Drawing(*components, x=8, label="Nada", fixedWidth=True)

        fig, axes = plt.subplots(figsize=(10, 7))
        plt.ylim(-10, 10)
        plt.xlim(-10, 10)

        drawing.applyTo(axes)

        plt.xlim(6, 10)

        drawing.update()

        plt.show()
