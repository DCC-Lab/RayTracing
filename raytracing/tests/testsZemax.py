import envtest  # modifies path
from raytracing.zemax import ZMXReader
from numpy import linspace, pi

inf = float("+inf")

class TestZemax(envtest.RaytracingTestCase):
    zmx = ZMXReader(r"../specifications/AC254-100-A-Zemax(ZMX).zmx")

    def testCreation(self):
        self.assertIsNotNone(self.zmx)

    def testSurface0Raw(self):
        self.assertIsNotNone(self.zmx)
        surface = self.zmx.rawSurfaceInfo(index=0)
        self.assertTrue( surface["SURF"] == 0)
        self.assertAlmostEqual( float(surface["CURV"][0]), 0.0)
        self.assertAlmostEqual( float(surface["DISZ"][0]), float("+inf")) 

    def testSurface1Raw(self):
        self.assertIsNotNone(self.zmx)
        surface = self.zmx.rawSurfaceInfo(index=1)
        self.assertTrue( surface["SURF"] == 1)
        self.assertAlmostEqual( float(surface["CURV"][0]), 1.593625498007969800E-002)
        self.assertAlmostEqual( float(surface["DISZ"][0]), 4.0) 

    def testSurface1Info(self):
        self.assertIsNotNone(self.zmx)
        surface = self.zmx.surfaceInfo(index=1)
        self.assertTrue( surface.number == 1)
        self.assertAlmostEqual( surface.R, 1.593625498007969800E-002)
        self.assertAlmostEqual( surface.spacing, 4.0) 

    def testSurfaces(self):
        self.assertIsNotNone(self.zmx)
        self.assertTrue(len(self.zmx.surfaces()) == 5)

if __name__ == '__main__':
    envtest.main()
