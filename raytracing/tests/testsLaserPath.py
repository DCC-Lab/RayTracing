import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestLaserPath(unittest.TestCase):

    def testLaserPathNoElements(self):
        lasPath = LaserPath()
        self.assertIsNone(lasPath.inputBeam)
        self.assertFalse(lasPath.isResonator)
        self.assertTrue(lasPath.showElementLabels)
        self.assertTrue(lasPath.showPointsOfInterest)
        self.assertTrue(lasPath.showPointsOfInterestLabels)
        self.assertTrue(lasPath.showPlanesAcrossPointsOfInterest)
        self.assertListEqual(lasPath.elements, [])

    def testLaserPath(self):
        elements = [Space(5), Lens(5), Space(20), Lens(15), Space(15)]
        lp = LaserPath(elements, "Laser Path")
        self.assertListEqual(lp.elements, elements)
        self.assertEqual(lp.label, "Laser Path")

    def testLaserPathIncorrectElements(self):
        elements = [Ray(), Lens(10)]
        with self.assertRaises(TypeError):
            LaserPath(elements)

    def testEigenModesNoPower(self):
        lp = LaserPath([Space(10)])
        self.assertTupleEqual(lp.eigenModes(), (None, None))

    def testEigenModes(self):
        lp = LaserPath([Space(10), Lens(10)])
        beam1, beam2 = lp.eigenModes()
        self.assertEqual(beam1.q.real, -5)
        self.assertEqual(beam2.q.real, -5)
        self.assertAlmostEqual(beam1.q.imag, -5 * 3 ** 0.5)
        self.assertAlmostEqual(beam2.q.imag, 5 * 3 ** 0.5)

        lp = LaserPath([Lens(10)])
        beam1, beam2 = lp.eigenModes()
        self.assertEqual(beam1.q, beam2.q)
        self.assertEqual(beam1.q, 0)

    def testLaserModesNoPower(self):
        lp = LaserPath([Space(10)])
        self.assertListEqual(lp.laserModes(), [])

    def testLaserModes(self):
        lp = LaserPath([Space(10), Lens(10)])
        laserModes = lp.laserModes()
        self.assertEqual(len(laserModes), 1)
        beam = laserModes[0]
        self.assertEqual(beam.q.real, -5)
        self.assertAlmostEqual(beam.q.imag, 5 * 3 ** 0.5)

        elements = [Space(1, 1.33), DielectricInterface(1.33, 1, 1), ThickLens(1.33, -10, -5, -20)]
        lp = LaserPath(elements)
        laserModes = lp.laserModes()
        self.assertEqual(len(laserModes), 1)
        beam = laserModes[0]
        self.assertAlmostEqual(beam.q.real, -5.90770102)
        self.assertAlmostEqual(beam.q.imag, 1.52036515)

        lp = LaserPath([Space(10), CurvedMirror(5)])
        self.assertListEqual(lp.laserModes(), [])
        lp = LaserPath()
        self.assertListEqual(lp.laserModes(), [])

    def testRearrangeBeamTraceForPlotting(self):
        x = [x for x in range(1, 6)]
        y = [y for y in range(1, 6)]
        rayList = [GaussianBeam(w=x_, z=y_) for (x_, y_) in zip(x, y)]
        lp = LaserPath()
        self.assertTupleEqual(lp.rearrangeBeamTraceForPlotting(rayList), (x, y))

if __name__ == '__main__':
    unittest.main()
