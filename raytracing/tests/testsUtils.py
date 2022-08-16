import envtest # modifies path  # fixme: requires path to raytracing/tests
from raytracing.utils import checkLatestVersion


class TestUtils(envtest.RaytracingTestCase):
    def testCheckOldVersion(self):
        self.assertTrue(checkLatestVersion(currentVersion="1.3.0"))

    def testCheckNewVersion(self):
        self.assertFalse(checkLatestVersion(currentVersion="1.4.0"))

if __name__ == '__main__':
    envtest.main()
