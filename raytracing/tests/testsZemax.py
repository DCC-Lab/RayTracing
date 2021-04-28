import envtest  # modifies path
from raytracing.zemax import ZMXReader
from numpy import linspace, pi

inf = float("+inf")

class TestZemax(envtest.RaytracingTestCase):
    zmx = ZMXReader(r"../specifications/AC254-100-A-Zemax(ZMX).zmx")

    def testCreation(self):
        self.assertIsNotNone(self.zmx)

    def testSurface0(self):
        self.assertIsNotNone(self.zmx)
        surface = self.zmx.surfaceInfo(index=0)
        self.assertTrue( surface["SURF"] == 0)
        self.assertAlmostEqual( float(surface["CURV"][0]), 0.0)
        self.assertAlmostEqual( float(surface["DISZ"][0]), float("+inf")) 

    def testSurfaces(self):
        self.assertIsNotNone(self.zmx)
        self.assertTrue(len(self.zmx.surfaces()) == 5)

if __name__ == '__main__':
    envtest.main()
