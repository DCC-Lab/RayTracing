import unittest
import envtest # modifies path
from raytracing import *

inf = float("+inf")

class TestBeam(unittest.TestCase):
    def testBeam(self):
        beam = GaussianBeam()
        beam = GaussianBeam(w=1)
        self.assertEqual(beam.w, 1)
        self.assertEqual(beam.R, float("+Inf"))
        self.assertEqual(beam.wavelength, 0.0006328)

    def testWo(self):
        beam = GaussianBeam(w=1)
        self.assertAlmostEqual(beam.w, beam.wo, 3)
        self.assertAlmostEqual(beam.w, beam.waist, 3)

    def testInvalidParameters(self):
        with self.assertRaises(Exception) as context:
	        beam = GaussianBeam(w=1,R=0)

    def testMultiplicationBeam(self):
    	# No default parameters
        beamIn = GaussianBeam(w=0.01, R=1, n=1.5, wavelength=0.400e-3)
        beamOut = Space(d=0,n=1.5)*beamIn
        self.assertEqual(beamOut.q, beamIn.q)
        self.assertEqual(beamOut.w, beamIn.w)
        self.assertEqual(beamOut.R, beamIn.R)
        self.assertEqual(beamOut.n, beamIn.n)
        self.assertEqual(beamOut.wavelength, beamIn.wavelength)

    def testDielectricInterfaceBeam(self):
        # No default parameters
        beamIn = GaussianBeam(w=10, R=inf, n=1.5, wavelength=0.400e-3)
        beamOut = DielectricInterface(R=-20,n1=1.5, n2=1.0)*beamIn
        self.assertEqual(beamOut.w, beamIn.w)
        self.assertEqual(beamOut.n, 1.0)
        self.assertEqual(beamOut.wavelength, beamIn.wavelength)

    def testPointBeam(self):
        beamIn = GaussianBeam(w=0.0000001)
        beamOut = Space(d=100)*beamIn
        self.assertEqual(beamOut.R, 100)
        self.assertEqual(beamOut.zo, beamIn.zo)
        self.assertEqual(beamOut.confocalParameter, beamIn.confocalParameter)
        self.assertEqual(beamOut.rayleighRange, beamIn.rayleighRange)

    def testFocalSpot(self):
        beamIn = GaussianBeam(w=0.1)
        beamOut = Space(d=100)*beamIn
        self.assertEqual(beamOut.waistPosition, -100)

    def testPrint(self):
        self.assertIsNotNone(GaussianBeam(w=0.1).__str__)
        self.assertTrue(len(GaussianBeam(w=0.1).__str__()) != 0)


if __name__ == '__main__':
    unittest.main()