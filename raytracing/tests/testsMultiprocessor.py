import envtest  # modifies path
from raytracing import *

inf = float("+inf")


def multiplyBy2(value) -> float:
    return 2 * value


class TestMultiProcessorSupport(envtest.RaytracingTestCase):
    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testMultiPool(self):
        processes = 8
        inputValues = [1, 2, 3, 4]
        with multiprocessing.Pool(processes=processes) as pool:
            outputValues = pool.map(multiplyBy2, inputValues)
        self.assertEqual(outputValues, list(map(multiplyBy2, inputValues)))


if __name__ == '__main__':
    envtest.main()
