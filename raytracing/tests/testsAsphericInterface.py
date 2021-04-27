import envtest  # modifies path
from raytracing import *
from numpy import linspace

inf = float("+inf")

class TestAsphericInterface(envtest.RaytracingTestCase):

    def testCreation(self):
        asphere = AsphericInterface(R=10, kappa=-1.0, n1=1, n2=1.5)
        self.assertIsNotNone(asphere)

    def testProperties(self):
        asphere = AsphericInterface(R=10, kappa=-1.0, n1=1, n2=1.5)
        self.assertIsNotNone(asphere)
        self.assertAlmostEqual(asphere.R, 10)
        self.assertAlmostEqual(asphere.kappa, 1)
        self.assertAlmostEqual(asphere.n1, 1)
        self.assertAlmostEqual(asphere.n2, 1.5)

    def testProperties(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        self.assertIsNotNone(asphere)
        for r in linspace(0,10,100):
            print(r, asphere.z(r), asphere.dzdr(r))

if __name__ == '__main__':
    envtest.main()
