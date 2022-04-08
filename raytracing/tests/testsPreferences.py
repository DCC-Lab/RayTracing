import envtest # modifies path
from raytracing import *
from raytracing.preferences import Preferences


class TestPrefs(envtest.RaytracingTestCase):
    def testInitPrefs(self):
        p = Preferences()
        self.assertIsNotNone(p)

    def testReset(self):
        p = Preferences()
        p.resetPreferences()
        self.assertTrue(os.path.exists(p.path))
        v = p.readPreferences()
        self.assertFalse(v) # empty

    def testPathExists(self):
        p = Preferences()
        self.assertIsNotNone(p.path)
        self.assertTrue(os.path.exists(p.path))

    def testReadPrefs(self):
        p = Preferences()
        d = p.readPreferences()
        self.assertIsNotNone(d)
        self.assertTrue(isinstance(d, dict))

    def testWritePrefs(self):
        p = Preferences()
        d = p.readPreferences()
        d["test"] = 123
        p.writePreferences(d)
        d2 = p.readPreferences()
        self.assertTrue(d2["test"] == 123)

if __name__ == '__main__':
    envtest.main()
