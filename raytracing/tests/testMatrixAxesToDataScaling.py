import unittest
from raytracing import *


class TestMatrixAxesToDataScaling(unittest.TestCase):
    def testWithEmptyAxes(self):
        fig, axes = plt.subplots(figsize=(10, 7))

        m = Matrix()

        xScaling, yScaling = m.axesToDataScaling(axes)

        self.assertEqual(xScaling, 1)
        self.assertEqual(yScaling, 1)

    def testWithForcedScale(self):
        fig, axes = plt.subplots(figsize=(10, 7))
        axes.set_xlim(-10, 10)
        axes.set_ylim(-5, 5)

        m = Matrix()
        xScaling, yScaling = m.axesToDataScaling(axes)

        self.assertEqual(xScaling, 20)
        self.assertEqual(yScaling, 10)

    def testWithEmptyImagingPath(self):
        """ Does not pass. The xScaling is wrong. """
        path = ImagingPath()

        fig, axes = plt.subplots(figsize=(10, 7))
        path.createRayTracePlot(axes=axes)

        (xScaling, yScaling) = path.axesToDataScaling(axes)

        self.assertEqual(yScaling, path.displayRange * 1.5)
        self.assertEqual(xScaling, (2*0.05) * 1.1)  # There's a text for objectHeight displayed at 0.05

    def testWithImagingPath(self):
        """ Does not pass. The xScaling is wrong. Next test isolates the bug. """
        path = ImagingPath()
        path.append(Space(d=10))
        path.append(Lens(f=5))
        path.append(Space(d=10))

        fig, axes = plt.subplots(figsize=(10, 7))
        path.createRayTracePlot(axes=axes)

        (xScaling, yScaling) = path.axesToDataScaling(axes)

        self.assertEqual(yScaling, path.displayRange * 1.5)
        self.assertEqual(xScaling, 20 * 1.1)

    def testBugWherePropertyChanges(self):
        """ Calling an Axis getter somehow debugs the xScaling value"""
        path = ImagingPath()
        path.append(Space(d=10))
        path.append(Lens(f=5))
        path.append(Space(d=10))

        fig, axes = plt.subplots(figsize=(10, 7))
        path.createRayTracePlot(axes=axes)

        (xScaling1, yScaling1) = path.axesToDataScaling(axes)
        # xScaling1 is wrong
        axes.get_xlim()

        (xScaling2, yScaling2) = path.axesToDataScaling(axes)
        # xScaling2 is good

        self.assertEqual(xScaling1, 1)
        self.assertEqual(xScaling2, 20 * 1.1)


if __name__ == '__main__':
    unittest.main()
