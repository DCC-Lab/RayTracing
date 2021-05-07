import envtest
import unittest
import os
from collections import Counter
import numpy as np

class TestUnittestSkipMethodsWrapper(envtest.RaytracingTestCase):

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


class TestEnvtestClass(envtest.RaytracingTestCase):
    tempDir = envtest.RaytracingTestCase.tempDir
    randomNumbersFromSeed0 = [0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777]
    def clearTempDir(self):
        if os.path.exists(self.tempDir):
            for file in os.listdir(self.tempDir):
                os.remove(os.path.join(self.tempDir, file))
            os.rmdir(self.tempDir)

    def setUp(self) -> None:
        self.clearTempDir()
        super().setUp()

    def tearDown(self) -> None:  # Just in case the directory doesn't get properly deleted at the end of a test.
        self.clearTempDir()
        super().tearDown()

    def assertEmptyDirectory(self, path, delete: bool = True):
        self.assertTrue(os.path.exists(path))
        self.assertListEqual(os.listdir(path), [])
        if delete:
            os.rmdir(path)

    def testRandomNumbersSeed(self):
        a = []
        for i in range(10):
            a.append(np.random.random())

        np.random.seed(0)
        b = []
        for i in range(10):
            b.append(np.random.random())

        self.assertEqual(a,b)
        self.assertEqual(a,self.randomNumbersFromSeed0)

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


    def testClearMatplotlibPlots(self):
        import matplotlib.pyplot as plt
        fig, _ = plt.subplots(2, 1, figsize=(10, 7))
        figNum = fig.number
        envtest.RaytracingTestCase.clearMatplotlibPlots()
        self.assertFalse(plt.fignum_exists(figNum))

    def testRedirectStdOutDecoratorNoFileSpecifiedReturnOnlyValue(self):
        @envtest.redirectStdOutToFile
        def printHelloWorld():
            print("Hello world")

        value = printHelloWorld()
        self.assertEqual(value.strip(), "Hello world")

    def testRedirectStdOutDecoratorNoFileSpecifiedReturnFile(self):
        @envtest.redirectStdOutToFile(returnOnlyValue=False)
        def printHelloWorld():
            print("Hello world")

        value = printHelloWorld()
        value = value.getvalue()
        self.assertEqual(value.strip(), "Hello world")

    def testRedirectStdOutDecoratorFileSpecified(self):
        import io

        file = io.StringIO()

        @envtest.redirectStdOutToFile(file=file)
        def printHelloWorld():
            print("Hello world")

        printHelloWorld()
        self.assertEqual(file.getvalue().strip(), "Hello world")


class TestEnvtestClassSelfMethod(envtest.RaytracingTestCase):

    def testAssertDoesNotRaiseSpecificException(self):
        val = self.assertDoesNotRaise(lambda x: 2 / x, ZeroDivisionError, x=1e-7)
        self.assertEqual(val, 20e6)

    def testAssertDoesNotRaiseGeneralException(self):
        val = self.assertDoesNotRaise(lambda x: f"x = {x}", None, x=1e-7)
        self.assertEqual(val, f"x = {1e-7}")

    def testAssertDoesNotRaiseReturnNone(self):
        def toto(x1, x2):
            x1 + x2

        val = self.assertDoesNotRaise(toto, x1=1, x2=1)
        self.assertIsNone(val)

    def testAssertDoesNotRaiseFails(self):
        with self.assertRaises(AssertionError) as assertError:
            self.assertDoesNotRaise(lambda x: x / 0, x=2)
        otherValue = f"An exception was raised:\ndivision by zero"
        self.assertEqual(str(assertError.exception), otherValue)

    def testAssertDoesNotRaiseLetExceptionPass(self):
        with self.assertRaises(ZeroDivisionError):
            with self.assertRaises(AssertionError):
                self.assertDoesNotRaise(lambda x: x / 0, IOError, x=2)

    def testAssertPrintsStripOutput(self):
        def toto():
            print("Hello world")

        self.assertPrints(toto, "Hello world")

    def testAssertPrintsNoStrip(self):
        def toto():
            print("Hello world")

        self.assertPrints(toto, "Hello world\n", False)

    def testAssertPrintsFails(self):
        def toto():
            return "Nothing is printed"

        with self.assertRaises(AssertionError):
            self.assertPrints(toto, "Nothing is printed")



if __name__ == '__main__':
    unittest.main()
