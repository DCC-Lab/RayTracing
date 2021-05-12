import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr
import unittest
import tempfile
import matplotlib.pyplot as plt
from unittest.mock import Mock, patch
import numpy as np
import warnings

import io
import contextlib

#Use with patch('matplotlib.pyplot.show', new=Mock()):
# or @patch('matplotlib.pyplot.show', new=Mock())

perfTestKey = "RAYTRACING_PERF_TESTS"
performanceTests = False
if perfTestKey in os.environ:
    performanceTests = os.environ[perfTestKey]
else:
    performanceTests = False

class RaytracingTestCase(unittest.TestCase):
    tempDir = os.path.join(tempfile.gettempdir(), "tempDir")
    setupCalled = False
    stdout = None
    stderr = None
    def __init__(self, tests=()):
        super(RaytracingTestCase, self).__init__(tests)
        warnings.simplefilter("ignore")

    def setUp(self):
        super().setUp()
        warnings.simplefilter("ignore")

        # Seed with same seed every time
        np.random.seed(0)

        self.setupCalled = True

    def tearDown(self) -> None:
        self.clearMatplotlibPlots()

    def testProperlySetup(self):
        self.assertTrue(self.setupCalled, msg="You must call super().setUp() in your own setUp()")

    @classmethod
    def clearMatplotlibPlots(cls):
        plt.clf()
        plt.cla()
        plt.close()

    def assertDoesNotRaise(self, func, exceptionType=None, *funcArgs, **funcKwargs):
        returnValue = None
        if exceptionType is None:
            exceptionType = Exception
        try:
            returnValue = func(*funcArgs, **funcKwargs)
        except exceptionType as e:
            self.fail(f"An exception was raised:\n{e}")
        # Don't handle exceptions not in exceptionType
        return returnValue

    def assertPrints(self, func, out, stripOutput: bool = True, *funcArgs, **funcKwargs):
        @redirectStdOutToFile
        def getOutput():
            func(*funcArgs, **funcKwargs)

        value = getOutput()
        if stripOutput:
            value = value.strip()
        self.assertEqual(value, out)


    @classmethod
    def createTempDirectory(cls):
        if os.path.exists(cls.tempDir):
            cls.deleteTempDirectory()
        os.mkdir(cls.tempDir)

    @classmethod
    def deleteTempDirectory(cls):
        if os.path.exists(cls.tempDir):
            for file in os.listdir(cls.tempDir):
                os.remove(os.path.join(cls.tempDir, file))
            os.rmdir(cls.tempDir)

    @classmethod
    def setUpClass(cls) -> None:
        cls.createTempDirectory()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.deleteTempDirectory()

    def tempFilePath(self, filename="temp.dat") -> str:
        return os.path.join(RaytracingTestCase.tempDir, filename)


def redirectStdOutToFile(_func=None, file=None, returnOnlyValue: bool = True):
    if file is None:
        file = io.StringIO()

    def redirectStdOut(func):
        def wrapperRedirectStdOut(*args, **kwargs):
            with redirect_stdout(file):
                func(*args, **kwargs)

            return file.getvalue() if returnOnlyValue else file

        return wrapperRedirectStdOut

    if _func is None:
        return redirectStdOut
    return redirectStdOut(_func)


def main():
    unittest.main()


def skip(reason: str):
    return unittest.skip(reason)


def skipIf(condition: object, reason: str):
    return unittest.skipIf(condition, reason)


def skipUnless(condition: object, reason: str):
    return unittest.skipUnless(condition, reason)


def expectedFailure(func):
    return unittest.expectedFailure(func)

def patchMatplotLib():
    return patch('matplotlib.pyplot.show', new=Mock())
     
# append module root directory to sys.path
sys.path.insert(0,
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__)
                        )
                    )
                )
                )
