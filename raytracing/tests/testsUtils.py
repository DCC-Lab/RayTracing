import envtest # modifies path  # fixme: requires path to raytracing/tests
from raytracing.utils import checkLatestVersion

import io
import json
import contextlib
from unittest.mock import patch, MagicMock

class TestUtils(envtest.RaytracingTestCase):
    def fakePyPIResponse(self, versions):
        """Mimics the object returned by urllib.request.urlopen used as a
        context manager, holding a PyPi-style JSON payload of releases."""
        payload = json.dumps({"releases": {v: [] for v in versions}}).encode()
        response = MagicMock()
        response.read.return_value = payload
        response.__enter__.return_value = response
        return response

    def testCheckOldVersion(self):
        f = io.StringIO()
        with patch("urllib.request.urlopen", return_value=self.fakePyPIResponse(["1.3.0", "1.4.0"])):
            with contextlib.redirect_stdout(f):
                self.assertTrue(checkLatestVersion(currentVersion="1.3.0"))
        self.assertTrue(len(f.getvalue()) != 0)

    def testCheckNewVersion(self):
        f = io.StringIO()
        with patch("urllib.request.urlopen", return_value=self.fakePyPIResponse(["1.3.0", "1.4.0"])):
            with contextlib.redirect_stdout(f):
                self.assertFalse(checkLatestVersion(currentVersion="1.4.0"))
        self.assertTrue(len(f.getvalue()) == 0)

if __name__ == '__main__':
    envtest.main()
