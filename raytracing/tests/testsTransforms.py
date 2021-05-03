import unittest
import numpy as np
import envtest # modifies path  # fixme: requires path to raytracing/tests
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from unittest.mock import Mock, patch

""" N.B.: Most of these tests do not assert anything. The transforms work, but I have not found a way to assert it other 
than by looking at the plot. Set SHOWPLOT to True to see the effect (acts like a HOWTO-Transforms). """


class TestTransforms(unittest.TestCase):
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

    def xMeanOf(self, drawing):
        """ Return the average x position of a drawing's array.
            It is equal to the centroid if the drawing is symmetric.
            * Turns out this value is not affected by the transforms *
                see: testCenterOfDrawingNotUpdatedAfterTranslate
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

        xCenter = self.xMeanOf(drawing)

        self.assertEqual(xCenter, 5)

    @patch("matplotlib.pyplot.show", new=Mock())
    def testTranslate(self):
        """ The translate works, but I have not found a way to assert it other than by looking at the plot. """
        drawing = patches.FancyArrow(
            x=5, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Graphic at x=5 + Translate x=+10")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testTranslateOverwrite(self):
        """ The translate overwrites previous translate. """
        drawing = patches.FancyArrow(
            x=5, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        transform = transforms.Affine2D().translate(15, 0)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Graphic at x=5 + Translate x=+15 (Overwrites previous +10)")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testCenterOfDrawingNotUpdatedAfterTranslate(self):
        """ I thought I could read the new position, but the xy array of a drawing is not affected by
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

        xCenter = self.xMeanOf(drawing)

        self.assertEqual(xCenter, 0)

    @patch("matplotlib.pyplot.show", new=Mock())
    def testScaleTransform(self):
        """ Successfully applying a (2x2) scaling on a centered drawing (at x=0). """
        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().scale(2, 2)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(-10, 10)
        plt.title("Scale Transform\nGraphic is (0.1 x 10) + Scale (2 x 2)")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testScaleTransformAlsoScalesPosition(self):
        """ This (2x2) scaling also affects the position since the drawing is instantiated at x=10 """
        drawing = patches.FancyArrow(
            x=10, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().scale(2, 2)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Scale Transform\nGraphic is (0.1 x 10) + Scale (2 x 2)")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testScaleTransformAlsoScalesPositionAfterTranslate(self):
        """ This (2x2) scaling affects the position of the drawing after translation even if it was instantiated
        at x=0 """
        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0) + transforms.Affine2D().scale(2, 2)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Scale Transform\nGraphic is (0.1 x 10) at x=0 + Translate x=10 + Scale (2 x 2)")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testScaleTransformDoesNotScalePositionBeforeTranslate(self):
        """ This (2x2) scaling does not affect the position of the drawing if the translation is done after the
        scaling and the drawing is instantiated at x=0 """
        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().scale(2, 2) + transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Scale Transform\nGraphic is (0.1 x 10) at x=0 + Scale (2 x 2) + Translate x=10")
        plt.show()

    @patch("matplotlib.pyplot.show", new=Mock())
    def testScaleTransformOnTranslatedDrawing(self):
        """ In order to correctly scale a drawing previously translated, we have to reset its transforms
        (automatically done with set_transform) and re-apply the required translation after. """

        drawing = patches.FancyArrow(
            x=0, y=-5, dx=0, dy=10,
            width=0.1, fc='k', ec='k',
            head_length=1, head_width=1,
            length_includes_head=True)

        fig, axes = plt.subplots()
        axes.add_patch(drawing)

        transform = transforms.Affine2D().translate(10, 0)  # initial positioning of the drawing
        drawing.set_transform(transform + axes.transData)

        # some code...

        # later if a rescaling is required we need to reapply the translation (in 2nd place)
        transform = transforms.Affine2D().scale(2, 2) + transforms.Affine2D().translate(10, 0)
        drawing.set_transform(transform + axes.transData)

        axes.set_ylim(-10, 10)
        axes.set_xlim(0, 20)
        plt.title("Scale Transform after translation requires a reset\nGraphic is (0.1 x 10) at x=0 + Scale (2 x "
                  "2) + Translate x=10")
        plt.show()

if __name__ == '__main__':
    unittest.main()
