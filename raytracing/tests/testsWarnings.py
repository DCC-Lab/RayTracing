import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestMatrix(envtest.RaytracingTestCase):
    def testMatrix(self):
        m = Matrix()
        self.assertIsNotNone(m)

    def testThorlabsLensesWarning(self):
        l = thorlabs.AC254_030_A()


if __name__ == '__main__':
    envtest.main()
