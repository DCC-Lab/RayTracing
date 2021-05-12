import envtest  # modifies path
from raytracing import *
from raytracing.zemax import ZMXReader
from numpy import linspace, pi
from raytracing.materials import *
import io
from contextlib import redirect_stdout

inf = float("+inf")

class TestReport(envtest.RaytracingTestCase):
    stdout = io.StringIO()
    
    def setUp(self):
        self.stdout = io.StringIO()
        super().setUp()
        
    def testCreationNoASNoFS(self):
        f = 50
        path = ImagingPath()
        path.append(Space(d=f))
        path.append(Lens(f=f))
        path.append(Space(d=f))
        with redirect_stdout(self.stdout):
            path.reportEfficiency()

        self.assertTrue(len(self.stdout.getvalue()) < 100)
        position, diameter = path.fieldStop()
        self.assertIsNone(position)
        self.assertTrue(diameter == float("+inf"))

    @envtest.patchMatplotLib()
    def testCreationASNoFS(self):
        f = 50
        path = ImagingPath()
        path.append(Space(d=f))
        path.append(Lens(f=f,diameter=10))
        path.append(Space(d=f))
        with redirect_stdout(self.stdout):
            path.reportEfficiency()

        self.assertTrue(len(self.stdout.getvalue()) < 100)
        position, diameter = path.fieldStop()
        self.assertIsNone(position)
        self.assertTrue(diameter == float("+inf"))

    @envtest.patchMatplotLib()
    def testCreationASFS(self):
        f = 50
        path = ImagingPath()
        path.append(Space(d=f))
        path.append(Lens(f=f, diameter=6))
        path.append(Space(d=f))
        path.append(Lens(f=f, diameter=6))
        with redirect_stdout(self.stdout):
            path.reportEfficiency()

        self.assertTrue(len(self.stdout.getvalue()) > 100)
        position, diameter = path.fieldStop()
        self.assertIsNotNone(position)
        self.assertTrue(diameter != float("+inf"))


if __name__ == '__main__':
    envtest.main()
