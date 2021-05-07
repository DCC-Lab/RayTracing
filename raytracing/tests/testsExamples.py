import envtest  # modifies path
import subprocess
from matplotlib import patches, transforms
from unittest.mock import Mock, patch

from raytracing import *

class TestExamples(envtest.RaytracingTestCase):
    @patch("matplotlib.pyplot.show", new=Mock())
    def testExamplesRun(self):
        import raytracing.examples as ex
        for ex in ex.all:
            ex["code"]()
            self.assertTrue(len(ex["title"])!=0)
            self.assertTrue(len(ex["sourceCode"])!=0)

    def testExamplesHaveSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.all:
            self.assertTrue(len(ex["sourceCode"])!=0)

    def testExamplesHaveBmpSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.all:
            self.assertIsNotNone(ex["bmpSourceCode"])

if __name__ == '__main__':
    envtest.main()
