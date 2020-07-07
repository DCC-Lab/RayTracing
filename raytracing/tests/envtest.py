import sys
import os
import io
from contextlib import redirect_stdout
import unittest
import tempfile


class RaytracingTestCase(unittest.TestCase):
    tempDir = os.path.join(tempfile.gettempdir(), "tempDir")

    def __init__(self, tests=()):
        super(RaytracingTestCase, self).__init__(tests)

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
