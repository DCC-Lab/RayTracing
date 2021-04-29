import envtest  # modifies path
from raytracing import *
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
        self.assertAlmostEqual( surface.R, 62.75, 1)
        self.assertAlmostEqual( surface.spacing, 4.0) 

    def testSurfaces(self):
        self.assertIsNotNone(self.zmx)
        self.assertTrue(len(self.zmx.surfaces()) == 5)

    def testMatrixGroup(self):
        group = self.zmx.matrixGroup()
        self.assertIsNotNone(group)
        f1, f2 = group.effectiveFocalLengths()
        self.assertAlmostEqual(f1, 100, 0)
        self.assertAlmostEqual(f2, 100, 0)
        self.assertTrue(len(group.elements)==5)

        path = OpticalPath()
        path.append(Space(d=300))
        path.append(group)
        path.append(Space(d=100))
        path.display(ObjectRays(diameter=20))

    def testAllMaterials(self): 
        mat = self.zmx.identifyMaterial('NBK-7')       
        self.assertIsNotNone(mat)
        self.assertTrue(isinstance(mat, N_BK7))

    def testPrescription(self): 
        print(self.zmx.prescription())

    def testOtherFile(self):
        zmx = ZMXReader("../specifications/zmax_49270.zmx")
        self.assertIsNotNone(zmx)

if __name__ == '__main__':
    envtest.main()
