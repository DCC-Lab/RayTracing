import envtest # modifies path
from raytracing import *
from raytracing.preferences import Preferences

class TestRaytracingPrefs(envtest.RaytracingTestCase):
    def setUp(self):
        super().setUp()
        self.savedPrefs = Preferences()
        self.savedPrefs.readFromDisk()

    def tearDown(self):
        self.savedPrefs.writeToDisk()
        super().tearDown()

    def testVersionCheckPrefs(self):
        p = Preferences()
        self.assertIsNotNone(p)
        self.assertTrue("lastVersionCheck" in p.keys())

    def testSaveBeginnerMode(self):
        beginnerMode(saveToPrefs=True)
        p = Preferences()
        self.assertIsNotNone(p)
        self.assertTrue("mode" in p.keys())
        self.assertEqual(p["mode"], "beginner")
        expertMode(saveToPrefs=False)
        silentMode(saveToPrefs=False)
        self.assertEqual(p["mode"], "beginner")

    def testSaveSilentMode(self):
        silentMode(saveToPrefs=True)
        p = Preferences()
        self.assertIsNotNone(p)
        self.assertTrue("mode" in p.keys())
        self.assertEqual(p["mode"], "silent")
        expertMode(saveToPrefs=False)
        beginnerMode(saveToPrefs=False)
        self.assertEqual(p["mode"], "silent")

    def testSaveExpertMode(self):
        expertMode(saveToPrefs=True)
        p = Preferences()
        self.assertIsNotNone(p)
        self.assertTrue("mode" in p.keys())
        self.assertEqual(p["mode"], "expert")
        silentMode(saveToPrefs=False)
        beginnerMode(saveToPrefs=False)
        self.assertEqual(p["mode"], "expert")

    def testWarningsFormat(self):
        beginnerMode()
        message = "This is a test."
        filename = "test.py"
        lineno = 10
        category = UserWarning
        warningsMessage = warningLineFormat(message, category, filename, lineno)
        self.assertEqual(warningsMessage, "UserWarning [in test.py]: This is a test.\n")

if __name__ == '__main__':
    envtest.main()
