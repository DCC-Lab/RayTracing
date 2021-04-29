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
        path.display(rays=ObjectRays(diameter=20))

    def testMatrixGroup(self):
        design = self.zmx.matrixGroup()
        self.assertIsNotNone(design)
        lens = thorlabs.AC254_100_A()

        self.assertAlmostEqual(design.effectiveFocalLengths().f1, lens.effectiveFocalLengths().f1, 3)
        self.assertAlmostEqual(design.effectiveFocalLengths().f2, lens.effectiveFocalLengths().f1, 3)
        self.assertAlmostEqual(design.backFocalLength(), lens.backFocalLength(), 3)
        self.assertAlmostEqual(design.frontFocalLength(), lens.frontFocalLength(), 3)

    def testAllMaterials(self): 
        mat = self.zmx.identifyMaterial('NBK-7')       
        self.assertIsNotNone(mat)
        self.assertTrue(isinstance(mat, N_BK7))

    def testPrescription(self): 
        print(self.zmx.prescription())

    def testWAVM(self): 
        self.assertTrue(self.zmx.designWavelengths() == [4.861E-1, 5.876E-1, 6.563E-1])
        self.assertAlmostEqual(self.zmx.designWavelength, 0.5876)

    def testEdmundFile(self):
        zmx = ZMXReader("../specifications/zmax_49270.zmx")
        self.assertIsNotNone(zmx)
        print(zmx.prescription())

if __name__ == '__main__':
    envtest.main()
