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
        self.assertAlmostEqual(asphere.angle(r=0), 0)
        # self.assertAlmostEqual(asphere.angle(r=9.9), 1.57)

        # for r in linspace(-10,10,100):
        #     print(r, asphere.z(r), asphere.angle(r))

    def testNormalIncidenceRefraction(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        paraxialRay = Ray(y=0, theta=0)
        self.assertAlmostEqual(asphere.angle(r=paraxialRay.y),0)

        paraxialOut = asphere.mul_ray_paraxial(paraxialRay)
        nonparaxialOut = asphere.mul_ray_nonparaxial(paraxialRay)
        self.assertAlmostEqual(paraxialRay.y, nonparaxialOut.y)
        self.assertAlmostEqual(paraxialRay.theta, nonparaxialOut.theta)

    def testOnAxisUpwardIncidenceRefraction(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        paraxialRay = Ray(y=0, theta=0.1)
        self.assertAlmostEqual(asphere.angle(r=paraxialRay.y),0)

        paraxialOut = asphere.mul_ray_paraxial(paraxialRay)
        nonparaxialOut = asphere.mul_ray_nonparaxial(paraxialRay)
        self.assertAlmostEqual(paraxialOut.y, nonparaxialOut.y, 3)
        self.assertAlmostEqual(paraxialOut.theta, nonparaxialOut.theta, 3)

    def testOffAxisUpwardIncidenceRefraction(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        paraxialRay = Ray(y=0.1, theta=0.1)

        paraxialOut = asphere.mul_ray_paraxial(paraxialRay)
        nonparaxialOut = asphere.mul_ray_nonparaxial(paraxialRay)
        self.assertAlmostEqual(paraxialOut.y, nonparaxialOut.y, 3)
        self.assertAlmostEqual(paraxialOut.theta, nonparaxialOut.theta, 3)

    def testCollection(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        rays =[Ray(0, 0),Ray(0, 0.1),Ray(0.1, 0),Ray(0.1, 0.1),
        Ray(0.1, -0.1), Ray(-0.1, 0.1),Ray(0, -0.1),Ray(-0.1, 0),
        Ray(-0.1, -0.1)] 

        for paraxialRay in rays:
            paraxialOut = asphere.mul_ray_paraxial(paraxialRay)
            nonparaxialOut = asphere.mul_ray_nonparaxial(paraxialRay)
            self.assertAlmostEqual(paraxialOut.y, nonparaxialOut.y, 3)
            self.assertAlmostEqual(paraxialOut.theta, nonparaxialOut.theta, 3)


if __name__ == '__main__':
    envtest.main()
