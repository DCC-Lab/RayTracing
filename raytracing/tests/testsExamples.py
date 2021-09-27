import envtest  # modifies path
import subprocess
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import patches, transforms
from unittest.mock import Mock, patch

from raytracing import *

class TestExamples(envtest.RaytracingTestCase):

    def testRegex(self):
        pattern = r'^(ex\d+|fig.+)\.py$'
        matchObj = re.match(pattern, "fig8-bla.py")
        self.assertIsNotNone(matchObj)
        self.assertIsNotNone(matchObj.group(1) == 'fig8-bla')
        matchObj = re.match(pattern, "ex08.py")
        self.assertIsNotNone(matchObj)
        self.assertIsNotNone(matchObj.group(1) == 'ex08')

    def testExamplesArePresent(self):
        import raytracing.examples as ex
        self.assertTrue(len(ex.short) > 0)

    @envtest.skipUnless(envtest.performanceTests, "Skipping long performance tests")
    @patch('matplotlib.pyplot.show', new=Mock())
    def testExamplesRun(self):
        import raytracing.examples as ex
        for ex in ex.short:
            self.assertTrue(len(ex["title"])!=0)
            self.assertTrue(len(ex["sourceCode"])!=0)
            print(".", end='', file=sys.stderr)
            print(ex["name"], end='', file=sys.stderr)
            with envtest.redirect_stdout(self.stdout):
                ex["code"]()

    def testExamplesHaveSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.short:
            self.assertTrue(len(ex["sourceCode"])!=0)

    def testExamplesHaveBmpSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.short:
            self.assertIsNotNone(ex["bmpSourceCode"])

    @envtest.skipUnless(envtest.performanceTests, "Skipping long performance tests")
    def testScriptsRun(self):
        import raytracing.examples as ex
        for scripts in ex.long:
            err = subprocess.run([sys.executable,  scripts["path"]], capture_output=True)
            self.assertTrue(err == 0)
    


if __name__ == '__main__':
    envtest.main()
