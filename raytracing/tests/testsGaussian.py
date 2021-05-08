import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestBeam(envtest.RaytracingTestCase):
    def testBeam(self):
        beam = GaussianBeam(w=1)
        self.assertEqual(beam.w, 1)
        self.assertEqual(beam.R, float("+Inf"))
        self.assertEqual(beam.wavelength, 0.0006328)

    def testBeamWAndQGiven(self):
        w = 1
        q = 4.96459e3 * 1j
        self.assertDoesNotRaise(GaussianBeam, ValueError, q=q, w=w)

    def testBeamWAndQGivenMismatch(self):
        w = 1
        q = 4.96459e3 * 1j
        q += q * 0.007
        with self.assertRaises(ValueError):
            GaussianBeam(q, w)

    def testIsInFinite(self):
        beam = GaussianBeam(w=inf, R=2)
        self.assertFalse(beam.isFinite)

    def testIsFinite(self):
        beam = GaussianBeam(w=0.1, R=20)
        self.assertTrue(beam.isFinite)

    def testFiniteW(self):
        beam = GaussianBeam(w=0.1)
        self.assertAlmostEqual(beam.w, 0.1)

    def testInfiniteW(self):
        beam = GaussianBeam(w=inf, R=10)
        self.assertEqual(beam.w, inf)

    def testNull(self):
        beam = GaussianBeam(0)
        self.assertFalse(beam.isFinite)
        self.assertEqual(beam.w, float("+Inf"))
        self.assertEqual(beam.R, float("+Inf"))
        self.assertEqual(beam.wavelength, 0.0006328)

    def testZ0is0(self):
        beam = GaussianBeam(w=inf, R=1)
        self.assertEqual(beam.zo, 0)

    def testZ0isNot0(self):
        wavelength = 632.8e-6
        beam = GaussianBeam(w=1, R=1, wavelength=wavelength)
        a = wavelength / pi
        imag = a / (1 + a ** 2)
        self.assertAlmostEqual(beam.zo, imag)

    def testWo(self):
        beam = GaussianBeam(w=1)
        self.assertAlmostEqual(beam.w, beam.wo, 3)
        self.assertAlmostEqual(beam.w, beam.waist, 3)

    def testWoIsNone(self):
        beam = GaussianBeam(w=inf, R=1)
        self.assertIsNone(beam.wo)

    def testInvalidParameters(self):
        with self.assertRaises(ValueError) as context:
            beam = GaussianBeam()
        self.assertEqual(str(context.exception), "Please specify 'q' or 'w'.")

        with self.assertRaises(Exception) as context:
            beam = GaussianBeam(w=1, R=0)

    def testMultiplicationBeam(self):
        # No default parameters
        beamIn = GaussianBeam(w=0.01, R=1, n=1.5, wavelength=0.400e-3)
        beamOut = Space(d=0, n=1.5) * beamIn
        self.assertEqual(beamOut.q, beamIn.q)
        self.assertEqual(beamOut.w, beamIn.w)
        self.assertEqual(beamOut.R, beamIn.R)
        self.assertEqual(beamOut.n, beamIn.n)
        self.assertEqual(beamOut.wavelength, beamIn.wavelength)

    def testDielectricInterfaceBeam(self):
        # No default parameters
        beamIn = GaussianBeam(w=10, R=inf, n=1.5, wavelength=0.400e-3)
        beamOut = DielectricInterface(R=-20, n1=1.5, n2=1.0) * beamIn
        self.assertEqual(beamOut.w, beamIn.w)
        self.assertEqual(beamOut.n, 1.0)
        self.assertEqual(beamOut.wavelength, beamIn.wavelength)

    def testPointBeam(self):
        beamIn = GaussianBeam(w=0.0000001)
        beamOut = Space(d=100) * beamIn
        self.assertEqual(beamOut.R, 100)
        self.assertEqual(beamOut.zo, beamIn.zo)
        self.assertEqual(beamOut.confocalParameter, beamIn.confocalParameter)
        self.assertEqual(beamOut.rayleighRange, beamIn.rayleighRange)

    def testFocalSpot(self):
        beamIn = GaussianBeam(w=0.1)
        beamOut = Space(d=100) * beamIn
        self.assertEqual(beamOut.waistPosition, -100)

    def testStr(self):
        self.assertIsNotNone(GaussianBeam(w=0.1).__str__)
        self.assertTrue(len(GaussianBeam(w=0.1).__str__()) != 0)

    def testStrInvalidRadiusOfCurvature(self):
        beam = GaussianBeam(w=inf, R=1)
        self.assertFalse(beam.isFinite)
        self.assertEqual(str(beam), "Beam is not finite: q=(1+0j)")

    def testPerformance(self):
        path = LaserPath()
        path.append(Space(d=100))
        beamIn = GaussianBeam(w=0.01, R=1, wavelength=0.400e-3)

        path.trace(beamIn)


if __name__ == '__main__':
    envtest.main()
