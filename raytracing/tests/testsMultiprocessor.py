import envtest  # modifies path
from raytracing import *
import itertools
import matplotlib.pyplot as plt

inf = float("+inf")


def multiplyBy2(value) -> float:
    return 2 * value


def mul(value1, value2) -> float:
    return value1 * value2


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

    @envtest.skipIf(sys.platform == 'darwin' and sys.version_info.major == 3 and sys.version_info.minor <= 7,
                    "Endless loop on macOS")
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testMultiPoolWith2Args(self):
        processes = 4
        inputValues = [1, 2, 3, 4]
        with multiprocessing.Pool(processes=processes) as pool:
            outputValues = pool.starmap(mul, itertools.product(inputValues, [2]))
        func = lambda val1: mul(val1, 2)
        self.assertEqual(outputValues, list(map(func, inputValues)))

class TestSingleAndMultiProcessorCalculation(envtest.RaytracingTestCase):
    #@envtest.skipUnless(envtest.performanceTests)
    # Some information here: https://github.com/gammapy/gammapy/issues/2453
    def testShortPath(self):
        path = ImagingPath()
        path.append(Space(d=100))
        path.append(Lens(f=50, diameter=25))

        import time
        photons = [10, 100, 1000, 3000, 10000, 30000]
        single = []
        for N in photons:
            rays = UniformRays(N=N)
            start = time.time()
            path.traceManyThrough(rays, progress=False)
            single.append(time.time()-start)

        multi = []
        for N in photons:
            rays = UniformRays(N=N)
            start = time.time()
            path.traceManyThroughInParallel(rays, progress=False)
            multi.append(time.time()-start)

        fig, axis = plt.subplots(1)
        axis.plot(photons, single,'k-',label="Single processor")
        axis.plot(photons, multi,'k-.',label="Multiprocessor")
        axis.set_title("Performance for short OpticalPath")
        axis.set_xlabel("Number of photons")
        axis.set_ylabel("Time [s]")
        axis.legend()
        plt.show()

    def testLongPath(self):
        path = ImagingPath()
        path.append(Space(d=100))
        path.append(Lens(f=50, diameter=25))
        path.append(Space(d=100))
        path.append(Lens(f=25, diameter=25))
        path.append(Space(d=100))
        path.append(Space(d=100))
        path.append(Lens(f=25, diameter=25))
        path.append(Space(d=100))
        path.append(Lens(f=25, diameter=25))
        path.append(thorlabs.AC254_100_A())

        import time
        photons = [10, 100, 1000, 3000]
        single = []
        for N in photons:
            rays = UniformRays(N=N)
            start = time.time()
            path.traceManyThrough(rays, progress=False)
            single.append(time.time()-start)

        multi = []
        for N in photons:
            rays = UniformRays(N=N)
            start = time.time()
            path.traceManyThroughInParallel(rays, progress=False)
            multi.append(time.time()-start)

        fig, axis = plt.subplots(1)
        axis.plot(photons, single,'k-',label="Single processor")
        axis.plot(photons, multi,'k-.',label="Multiprocessor")
        axis.set_title("Performance for Long OpticalPath")
        axis.set_xlabel("Number of photons")
        axis.set_ylabel("Time [s]")
        axis.legend()
        plt.show()

if __name__ == '__main__':
    envtest.main()
