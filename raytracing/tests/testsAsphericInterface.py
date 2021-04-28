import envtest  # modifies path
from raytracing import *
from numpy import linspace, pi

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
        self.assertAlmostEqual(asphere.surfaceNormal(y=0), 0)
        # self.assertAlmostEqual(asphere.angle(r=9.9), 1.57)

        # for r in linspace(-10,10,100):
        #     print(r, asphere.z(r), asphere.angle(r))

    def testdzdrWithKappaZero(self):

        R = 10
        for kappa in [0, -0.5, -1, -1.5, -100]:
            asphere = AsphericInterface(R=R, kappa=kappa, n1=1, n2=1.5)

            dz, dr = asphere.dzdr(y=0)
            self.assertAlmostEqual(dz, 0)

            for y in [-2*R, -R, -R/2, 0, R/2, R, 2*R]:
                if asphere.z(y) is not None:
                    # Then derivative must be defined
                    dz1, dr1 = asphere.dzdr(y=y)
                    self.assertIsNotNone(dz1)

                    dz2, dr2 = asphere.dzdr(y=-y)
                    self.assertIsNotNone(dz2)

                    self.assertAlmostEqual(dz1, -dz2)
                else:
                    # Then derivative must be None
                    dz1, dr1 = asphere.dzdr(y=y)
                    self.assertIsNone(dz1)

    def testSurfaceNormalValues(self):
        # We defined the normal to be negative on a convex
        # sphere above axis
        R = 10
        kappa = 0
        asphere = AsphericInterface(R=R, kappa=kappa, n1=1, n2=1.5)

        n1 = asphere.surfaceNormal(y=0)
        self.assertAlmostEqual(n1, 0)

        n1 = asphere.surfaceNormal(y=R)
        self.assertAlmostEqual(n1, -pi/2, 3)

        n1 = asphere.surfaceNormal(y=-R)
        self.assertAlmostEqual(n1, pi/2, 3)

        n1 = asphere.surfaceNormal(y=R/2)
        self.assertTrue(n1 < 0)
        self.assertAlmostEqual(n1, -pi/6)

        n2 = asphere.surfaceNormal(y=-R/2)
        self.assertTrue(n2 > 0)
        self.assertAlmostEqual(n2, pi/6)

        # We defined the normal to be negative on a convex
        # sphere above axis, so let;s try concave
        R = -10
        kappa = 0
        asphere = AsphericInterface(R=R, kappa=kappa, n1=1, n2=1.5)

        n1 = asphere.surfaceNormal(y=abs(R/2))
        self.assertTrue(n1 > 0)

        n2 = asphere.surfaceNormal(y=-abs(R/2))
        self.assertTrue(n2 < 0)

    def testSurfaceNormalWithKappa(self):

        R = 10
        for kappa in [0, -0.5, -1, -1.5, -100]:
            asphere = AsphericInterface(R=R, kappa=kappa, n1=1, n2=1.5)

            self.assertAlmostEqual(asphere.surfaceNormal(y=0), 0)

            for y in [-2*R, -R, -R/2, 0, R/2, R, 2*R]:
                if asphere.z(y) is not None:
                    # Then angle must be defined
                    n1 = asphere.surfaceNormal(y=y)
                    self.assertIsNotNone(n1)

                    n2 = asphere.surfaceNormal(y=-y)
                    self.assertIsNotNone(n2)

                    self.assertAlmostEqual(n1, -n2)
                else:
                    self.assertIsNone(asphere.surfaceNormal(y=y))


    def testNormalIncidenceRefraction(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        paraxialRay = Ray(y=0, theta=0)
        self.assertAlmostEqual(asphere.surfaceNormal(y=paraxialRay.y),0)

        paraxialOut = asphere.mul_ray_paraxial(paraxialRay)
        nonparaxialOut = asphere.mul_ray_nonparaxial(paraxialRay)
        self.assertAlmostEqual(paraxialRay.y, nonparaxialOut.y)
        self.assertAlmostEqual(paraxialRay.theta, nonparaxialOut.theta)

    def testOnAxisUpwardIncidenceRefraction(self):
        asphere = AsphericInterface(R=10, kappa=0, n1=1, n2=1.5)
        paraxialRay = Ray(y=0, theta=0.1)
        self.assertAlmostEqual(asphere.surfaceNormal(y=paraxialRay.y),0)

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

    @envtest.skip
    def testOpticalPath(self):
        Matrix.useNonParaxialCalculations = True
        path = ImagingPath()

        path.append(Space(d=10))
        path.append(AsphericInterface(R=10, kappa=-1, n1=1, n2=1.5))
        path.append(Space(d=2))
        path.append(AsphericInterface(R=-10, kappa=-1, n1=1.5, n2=1.0))
        path.append(Space(d=20))
        path.display(ObjectRays(diameter=8, halfAngle=0,H=21, T=1))

    @envtest.skip
    def testAnAxicon(self):
        Matrix.useNonParaxialCalculations = True
        path = ImagingPath()

        path.append(Space(d=10))
        path.append(AsphericInterface(R=0.01, kappa=-131, n1=1.0, n2=1.5))
        path.append(Space(d=5))
        path.append(DielectricInterface(n1=1.5, n2=1.0))
        path.append(Space(d=20))
        path.display(ObjectRays(diameter=0.1, halfAngle=0,H=21, T=1))

if __name__ == '__main__':
    envtest.main()
