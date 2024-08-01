import envtest # modifies path  # fixme: requires path to raytracing/tests
from raytracing.utils import checkLatestVersion

import io
import contextlib

class TestUtils(envtest.RaytracingTestCase):
    def testCheckOldVersion(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.assertTrue(checkLatestVersion(currentVersion="1.3.0"))
        self.assertTrue(len(f.getvalue()) != 0)

    def testCheckNewVersion(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.assertFalse(checkLatestVersion(currentVersion="1.4.0"))
        self.assertTrue(len(f.getvalue()) == 0)

if __name__ == '__main__':
    envtest.main()
