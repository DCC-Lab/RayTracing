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


class TestEnvtestClass(unittest.TestCase):
    dirname = envtest.RaytracingTestCase.dirName

    def clearTempDir(self):
        if os.path.exists(self.dirname):
            for file in os.listdir(self.dirname):
                os.remove(os.path.join(self.dirname, file))
            os.rmdir(self.dirname)

    def setUp(self) -> None:
        self.clearTempDir()

    def tearDown(self) -> None:  # Just in case the directory doesn't get properly deleted at the end of a test.
        self.clearTempDir()

    def assertEmptyDirectory(self, path, delete: bool = True):
        self.assertTrue(os.path.exists(path))
        self.assertListEqual(os.listdir(path), [])
        if delete:
            os.rmdir(path)

    def testTempDirName(self):
        self.assertTrue(self.dirname.endswith("tempDir"))

    def testRemoveAlreadyExistsFalse(self):
        envtest.RaytracingTestCase.removeAlreadyExists = False
        self.assertFalse(envtest.RaytracingTestCase.removeAlreadyExists)

    def testRemoveAlreadyExistsTrue(self):
        envtest.RaytracingTestCase.removeAlreadyExists = True
        self.assertTrue(envtest.RaytracingTestCase.removeAlreadyExists)

    def testCreateTempDirectoryAlreadyExistsDoNotDelete(self):
        msg = f"'{self.dirname}' directory already exists. Please set RaytracingTestCase.removeAlreadyExists to True if"
        msg += f" you want to delete this directory."
        envtest.RaytracingTestCase.removeAlreadyExists = False
        os.mkdir(self.dirname)
        with self.assertRaises(FileExistsError) as context:
            envtest.RaytracingTestCase.createTempDirectory()
        self.assertEqual(str(context.exception), msg)
        os.rmdir(self.dirname)  # Delete the directory!

    def testCreateTempDirectoryAlreadyExistsAndDelete(self):
        dirname = envtest.RaytracingTestCase.dirName
        envtest.RaytracingTestCase.removeAlreadyExists = True
        os.mkdir(dirname)
        try:
            envtest.RaytracingTestCase.createTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(dirname)

    def testCreateTempDirectoryNotAlreadyPresent(self):
        try:
            envtest.RaytracingTestCase.createTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.dirname)

    def testDeleteTempDirectoryNotAlreadyPresent(self):
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.dirname))

    def testDeleteTempDirectoryAlreadyExists(self):
        os.mkdir(self.dirname)
        self.assertTrue(os.path.exists(self.dirname))  # make sure it exists
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.dirname))

    def testDeleteTempDirectoryFilesInDirectory(self):
        os.mkdir(self.dirname)
        fname = lambda x: f"test_{x}.txt"
        fnames = []
        for x in range(100):
            tempName = fname(x)
            name = os.path.join(self.dirname, tempName)
            fnames.append(tempName)
            with open(name, "w") as file:
                file.write(f"This is the {x}th file. This file is only for tests. If you read this, have a nice day")
        self.assertTrue(os.path.exists(self.dirname))
        self.assertEqual(Counter(os.listdir(self.dirname)), Counter(fnames))
        try:
            envtest.RaytracingTestCase.deleteTempDirectory()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.dirname))

    def testSetupClass(self):
        try:
            envtest.RaytracingTestCase.setUpClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.dirname)

    def testTearDownClass(self):
        os.mkdir(self.dirname)
        self.assertTrue(os.path.exists(self.dirname))  # make sure it exists
        try:
            envtest.RaytracingTestCase.tearDownClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.dirname))

    def testSetUpThenTearDownClass(self):
        try:
            envtest.RaytracingTestCase.setUpClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertEmptyDirectory(self.dirname)
        try:
            envtest.RaytracingTestCase.tearDownClass()
        except Exception as exception:
            self.fail(f"An exception was raised!\n{exception}")
        self.assertFalse(os.path.exists(self.dirname))


if __name__ == '__main__':
    unittest.main()
