import envtest # modifies path
import os
from raytracing.preferences import Preferences


class TestPrefs(envtest.RaytracingTestCase):
    def setUp(self):
        super().setUp()
        self.savedPrefs = Preferences()
        self.savedPrefs.readFromDisk()

    def tearDown(self):
        self.savedPrefs.writeToDisk()
        super().tearDown()

    def testInitPrefs(self):
        p = Preferences()
        self.assertIsNotNone(p)

    def testReset(self):
        p = Preferences()
        p.resetPreferences()
        self.assertTrue(os.path.exists(p.path))
        self.assertFalse(p.keys()) # empty

    def testPathExists(self):
        p = Preferences()
        self.assertIsNotNone(p.path)
        self.assertTrue(os.path.exists(p.path))

    def testReadPrefs(self):
        p = Preferences()
        p.readFromDisk()
        self.assertIsNotNone(p)

    def testWritePrefs(self):
        p = Preferences()
        p["test"] = 123
        p.writeToDisk()
        p.readFromDisk()
        self.assertTrue(p["test"] == 123)

    def testPrefsAsDict(self):
        p = Preferences()
        p["test"] = 345
        self.assertEqual(p["test"], 345)        

    # def testPrefsAsIter(self):
    #     p = Preferences()
    #     p["test"] = 1
    #     for key in p:
    #         self.assertEqual(key, "test")

    def testZZPrefsIncludesKey(self):
        p = Preferences()
        p["test"] = "ouch"
        self.assertTrue('test' in p)

    def testZZZPrefsLargeDict(self):
        p = Preferences()
        p["test"] = "ouch"
        p["test1"] = "ouch"
        p["test2"] = "ouch"
        p["test3"] = "ouch"
        self.assertTrue(len(p.keys()) >= 4)

if __name__ == '__main__':
    envtest.main()
