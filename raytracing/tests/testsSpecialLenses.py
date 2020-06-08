import envtest  # modifies path

from raytracing import *

inf = float("+inf")


class TestSpecialLenses(envtest.RaytracingTestCase):

    def testOlympusLens(self):
        self.assertIsNotNone(olympus.LUMPlanFL40X())
        self.assertIsNotNone(olympus.XLUMPlanFLN20X())
        self.assertIsNotNone(olympus.MVPlapo2XC())
        self.assertIsNotNone(olympus.UMPLFN20XW())

    def testThorlabsLenses(self):
        l = thorlabs.ACN254_100_A()
        l = thorlabs.ACN254_075_A()
        l = thorlabs.ACN254_050_A()
        l = thorlabs.ACN254_040_A()
        l = thorlabs.AC254_030_A()
        l = thorlabs.AC254_035_A()
        l = thorlabs.AC254_045_A()
        l = thorlabs.AC254_050_A()
        l = thorlabs.AC254_060_A()
        l = thorlabs.AC254_075_A()
        l = thorlabs.AC254_080_A()
        l = thorlabs.AC254_100_A()
        l = thorlabs.AC254_125_A()
        l = thorlabs.AC254_200_A()
        l = thorlabs.AC254_250_A()
        l = thorlabs.AC254_300_A()
        l = thorlabs.AC254_400_A()
        l = thorlabs.AC254_500_A()

        l = thorlabs.AC508_075_B()
        l = thorlabs.AC508_080_B()
        l = thorlabs.AC508_100_B()
        l = thorlabs.AC508_150_B()
        l = thorlabs.AC508_200_B()
        l = thorlabs.AC508_250_B()
        l = thorlabs.AC508_300_B()
        l = thorlabs.AC508_400_B()
        l = thorlabs.AC508_500_B()
        l = thorlabs.AC508_750_B()
        l = thorlabs.AC508_1000_B()

    def testEdmundLens(self):
        l = eo.PN_33_921()


if __name__ == '__main__':
    envtest.main()
