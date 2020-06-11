import sys
import os
import unittest
import tempfile

class RaytracingTestCase(unittest.TestCase):
    tempDir = os.path.join(tempfile.gettempdir(), "tempDir")

    def __init__(self, tests=()):
        super(RaytracingTestCase, self).__init__(tests)

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
