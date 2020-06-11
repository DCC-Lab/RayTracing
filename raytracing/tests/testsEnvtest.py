import envtest
import unittest
import os
from collections import Counter


class TestUnittestSkipMethodsWrapper(unittest.TestCase):

    @envtest.skip("Skipped")
    def testSkip(self):
        self.fail()

    @envtest.skipIf(True, "Skipped")
    def testSkipIfWithTrueCondition(self):
        self.fail()

    @envtest.skipIf(False, "Not skipped")
    def testSkipIfWithFalseCondition(self):
        pass

    @envtest.skipUnless(True, "Not skipped")
    def testSkipUnlessTrueCondition(self):
        pass

    @envtest.skipUnless(False, "Skipped")
    def testSkipUnlessFalseCondition(self):
        self.fail()

    @envtest.expectedFailure
    def testShouldFail(self):
        self.fail()


class TestEnvtestClass(unittest.TestCase):
    tempDir = envtest.RaytracingTestCase.tempDir

    def clearTempDir(self):
        if os.path.exists(self.tempDir):
            for file in os.listdir(self.tempDir):
                os.remove(os.path.join(self.tempDir, file))
            os.rmdir(self.tempDir)

    def setUp(self) -> None:
        self.clearTempDir()

    def tearDown(self) -> None:  # Just in case the directory doesn't get properly deleted at the end of a test.
        self.clearTempDir()

    def assertEmptyDirectory(self, path, delete: bool = True):
        self.assertTrue(os.path.exists(path))
        self.assertListEqual(os.listdir(path), [])
        if delete:
            os.rmdir(path)

    def testTemptempDir(self):
        self.assertTrue(self.tempDir.endswith("tempDir"))

    def testCreateTempDirectoryAlreadyExistsAndDelete(self):
        tempDir = envtest.RaytracingTestCase.tempDir
        os.mkdir(tempDir)
        try:
            envtest.RaytracingTestCase.createTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(tempDir)

    def testCreateTempDirectoryNotAlreadyPresent(self):
        try:
            envtest.RaytracingTestCase.createTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.tempDir)

    def testDeleteTempDirectoryNotAlreadyPresent(self):
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.tempDir))

    def testDeleteTempDirectoryAlreadyExists(self):
        os.mkdir(self.tempDir)
        self.assertTrue(os.path.exists(self.tempDir))  # make sure it exists
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.tempDir))

    def testDeleteTempDirectoryFilesInDirectory(self):
        os.mkdir(self.tempDir)
        fname = lambda x: f"test_{x}.txt"
        fnames = []
        for x in range(100):
            tempName = fname(x)
            name = os.path.join(self.tempDir, tempName)
            fnames.append(tempName)
            with open(name, "w") as file:
                file.write(f"This is the {x}th file. This file is only for tests. If you read this, have a nice day")
        self.assertTrue(os.path.exists(self.tempDir))
        self.assertEqual(Counter(os.listdir(self.tempDir)), Counter(fnames))
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.tempDir))

    def testSetupClass(self):
        try:
            envtest.RaytracingTestCase.setUpClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.tempDir)

    def testTearDownClass(self):
        os.mkdir(self.tempDir)
        self.assertTrue(os.path.exists(self.tempDir))  # make sure it exists
        try:
            envtest.RaytracingTestCase.tearDownClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.tempDir))

    def testSetUpThenTearDownClass(self):
        try:
            envtest.RaytracingTestCase.setUpClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.tempDir)
        try:
            envtest.RaytracingTestCase.tearDownClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.tempDir))


if __name__ == '__main__':
    unittest.main()
