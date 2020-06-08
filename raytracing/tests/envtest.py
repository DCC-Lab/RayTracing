import sys
import os
import unittest
import tempfile

class RaytracingTestCase(unittest.TestCase):
    dirName = os.path.join(tempfile.gettempdir(), "tempDir")
    removeAlreadyExists = False

    def __init__(self, tests=()):
        super(RaytracingTestCase, self).__init__(tests)

    @classmethod
    def createTempDirectory(cls):
        if os.path.exists(cls.dirName):
            if cls.removeAlreadyExists:
                cls.deleteTempDirectory()
            else:
                fullDirName = os.path.join(os.getcwd(), cls.dirName)
                msg = f"'{fullDirName}' directory already exists. " \
                    f"Please set RaytracingTestCase.removeAlreadyExists to True if you want to delete this directory."
                raise FileExistsError(msg)
        os.mkdir(cls.dirName)

    @classmethod
    def deleteTempDirectory(cls):
        if os.path.exists(cls.dirName):
            for file in os.listdir(cls.dirName):
                os.remove(os.path.join(cls.dirName, file))
            os.rmdir(cls.dirName)

    @classmethod
    def setUpClass(cls) -> None:
        cls.createTempDirectory()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.deleteTempDirectory()


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
