import unittest
import numpy as np
import envtest # modifies path  # fixme: requires path to raytracing/tests
import matplotlib.pyplot as plt
from matplotlib import patches, transforms


class TestTransforms(unittest.TestCase):
    SHOWPLOT = False

    def tearDown(self) -> None:
        """ Deletes the Figure in memory between each test. """
        plt.close()

    def testApplyDrawing(self):
        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        self.assertEqual(len(axes.patches), 1)
        self.assertIsInstance(axes.patches[0], patches.FancyArrow)

    def xMean(self, drawing):
        """ Return the average x position of a drawing's array.
            It is equal to the centroid if the drawing is symmetric.
        """
        return np.mean(drawing.get_xy(), axis=0)[0]

    def testCenterOfDrawing(self):
        drawing = patches.FancyArrow(
            x=5, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        xCenter = self.xMean(drawing)

        self.assertEqual(xCenter, 5)

    def testTranslate(self):
        """ The translate works, but I have not found a way to assert it other than by looking at the plot. """
        drawing = patches.FancyArrow(
            x=5, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)

        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        if self.SHOWPLOT:
            plt.title("Drawing at x=5 + Translate x=+10")
            plt.show()

    def testTranslateOverwrite(self):
        """ The translate overwrites previous translate. """
        drawing = patches.FancyArrow(
            x=5, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)

        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        transform = transforms.Affine2D().translate(15, 0)
        drawing.set_transform(transform + axes.transData)

        if self.SHOWPLOT:
            plt.title("Drawing at x=5 + Translate x=+15 (Overwrites previous +10)")
            plt.show()

    def testCenterOfDrawingNotUpdatedAfterTranslate(self):
        """ This is fine. I thought I could read the new position, but the xy array of a drawing is not affected by
        the transforms even though the drawing gets translated. """

        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        xCenter = self.xMean(drawing)

        self.assertEqual(xCenter, 0)
