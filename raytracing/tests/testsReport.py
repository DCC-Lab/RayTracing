import envtest  # modifies path
from raytracing import *
from raytracing.zemax import ZMXReader
from numpy import linspace, pi
from raytracing.materials import *

inf = float("+inf")

class TestReport(envtest.RaytracingTestCase):
    def testCreation(self):
        f = 50
        path = ImagingPath()
        path.append(Space(d=f))
        path.append(Lens(f=f))
        path.append(Space(d=f))
        self.assertDoesNotRaise(path.reportEfficiency)


if __name__ == '__main__':
    envtest.main()
