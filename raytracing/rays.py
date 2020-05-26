from .ray import *
from numpy import *
import matplotlib.pyplot as plt
import pickle
import time
import os
import collections.abc as collections
import warnings

""" A source or a detector of rays

We can obtain intensity distributions at from given plane by propagating
many rays and collecting them at another plane. `Rays` is the base class
that provides the essential mechanisms to obtain histograms on a list 
of rays (created or collected). This list of rays is a property of the base
class.  Subclasses are specific to a given ray distribution (Lambertian for 
instance) and will create each ray on demand, then store them as they go
in the rays list. 

It is an iterable object, which means it can be used in an expression 
like `for ray in rays:` which is convenient both when propagating rays 
or when analysing the resulting rays that reached a plane in ImagingPath, 
MatrixGroup or any tracing function. 
"""


class Rays:
    def __init__(self, rays=None):
        if rays is None:
            self._rays = []
        else:
            if isinstance(rays, collections.Iterable):
                if all([isinstance(ray, Ray) for ray in rays]):
                    self._rays = list(rays)
                else:
                    raise TypeError("'rays' elements must be of type Ray.")
            else:
                raise TypeError("'rays' must be iterable (i.e. a list or a tuple of Ray).")

        self.iteration = 0
        self.progressLog = 10000

        # We cache these because they can be lengthy to calculate
        self._yValues = None
        self._thetaValues = None
        self._yHistogram = None
        self._thetaHistogram = None
        self._directionBinEdges = None

        self._countHistogramParameters = None
        self._xValuesCountHistogram = None

        self._anglesHistogramParameters = None
        self._xValuesAnglesHistogram = None

    def __len__(self) -> int:
        if self._rays is None:
            return 0
        return len(self._rays)

    @property
    def rays(self):
        # Even if "read only" property, we can change the content of the list.
        # We return a copy with [:]
        return self._rays[:]

    @property
    def count(self):
        return len(self)

    @property
    def yValues(self):
        if self._yValues is None:
            self._yValues = list(map(lambda x: x.y, self))

        return self._yValues

    @property
    def thetaValues(self):
        if self._thetaValues is None:
            self._thetaValues = list(map(lambda x: x.theta, self))

        return self._thetaValues

    def rayCountHistogram(self, binCount=None, minValue=None, maxValue=None):

        if binCount is None:
            binCount = 40

        if minValue is None:
            minValue = min(self.yValues)

        if maxValue is None:
            maxValue = max(self.yValues)

        if self._countHistogramParameters != (binCount, minValue, maxValue):
            self._countHistogramParameters = (binCount, minValue, maxValue)

            (self._yHistogram, binEdges) = histogram(self.yValues,
                                                     bins=binCount,
                                                     range=(minValue, maxValue))
            self._yHistogram = list(self._yHistogram)
            xValues = []
            for i in range(len(binEdges) - 1):
                xValues.append((binEdges[i] + binEdges[i + 1]) / 2)
            self._xValuesCountHistogram = xValues

        return (self._xValuesCountHistogram, self._yHistogram)

    def rayAnglesHistogram(self, binCount=None, minValue=None, maxValue=None):
        if binCount is None:
            binCount = 40

        if minValue is None:
            minValue = min(self.thetaValues)

        if maxValue is None:
            maxValue = max(self.thetaValues)

        if self._anglesHistogramParameters != (binCount, minValue, maxValue):
            self._anglesHistogramParameters = (binCount, minValue, maxValue)

            (self._thetaHistogram, binEdges) = histogram(self.thetaValues, bins=binCount, range=(minValue, maxValue))
            self._thetaHistogram = list(self._thetaHistogram)
            xValues = []
            for i in range(len(binEdges) - 1):
                xValues.append((binEdges[i] + binEdges[i + 1]) / 2)
            self._xValuesAnglesHistogram = xValues

        return (self._xValuesAnglesHistogram, self._thetaHistogram)

    def display(self, title="Intensity profile", showTheta=True):  # pragma: no cover
        plt.ioff()
        fig, axes = plt.subplots(2)
        fig.suptitle(title)
        fig.tight_layout(pad=3.0)

        axis1 = axes[0]
        axis2 = axes[1]

        (x, y) = self.rayCountHistogram()
        # axis1.set_title('Intensity profile')
        axis1.plot(x, y, 'k-', label="Intensity")
        axis1.set_ylim([0, max(y) * 1.1])
        axis1.set_xlabel("Distance")
        axis1.set_ylabel("Ray count")
        axis1.legend(["Intensity"])

        (x, y) = self.rayAnglesHistogram()
        # axis2.set_title('Angle histogram')
        axis2.plot(x, y, 'k--', label="Orientation profile")
        axis2.set_ylim([0, max(y) * 1.1])
        axis2.set_xlim([-pi / 2, pi / 2])
        axis2.set_xlabel("Angles [rad]")
        axis2.set_ylabel("Ray count")
        axis2.legend(["Angle"])

        plt.show()

    def displayProgress(self):
        nRays = len(self)
        if self.iteration % self.progressLog == 0:
            self.progressLog *= 3
            if self.progressLog > nRays:
                self.progressLog = nRays

            print("Progress {0}/{1} ({2:.0f}%) ".format(self.iteration, nRays, self.iteration / nRays * 100))

    def __iter__(self):
        self.iteration = 0
        self.progressLog = 10000
        return self

    def __next__(self) -> Ray:
        if self._rays is None:
            raise StopIteration

        if self.iteration < len(self._rays):
            ray = self._rays[self.iteration]
            self.iteration += 1
            return ray

        raise StopIteration

    def __getitem__(self, item):
        return self._rays[item]

    def append(self, ray):
        if not isinstance(ray, Ray):
            raise TypeError("'ray' must be a 'Ray' object.")
        if self._rays is not None:
            self._rays.append(ray)

        # Invalidate cached values
        self._yValues = None
        self._thetaValues = None
        self._yHistogram = None
        self._thetaHistogram = None
        self._directionBinEdges = None

        self._countHistogramParameters = None
        self._xValuesCountHistogram = None

        self._anglesHistogramParameters = None
        self._xValuesAnglesHistogram = None

    def load(self, filePath, append=False):
        with open(filePath, 'rb') as infile:
            loadedRays = pickle.Unpickler(infile).load()
            if not isinstance(loadedRays, collections.Iterable):
                raise IOError(f"{filePath} does not contain an iterable of Ray objects.")
            if not all([isinstance(ray, Ray) for ray in loadedRays]):
                raise IOError(f"{filePath} must contain only Ray objects.")
            if append and self._rays is not None:
                self._rays.extend(loadedRays)
            else:
                self._rays = loadedRays

    def save(self, filePath):
        with open(filePath, 'wb') as outfile:
            pickle.Pickler(outfile).dump(self._rays)

        # We save the data to disk using a module called Pickler
        # Some asynchronous magic is happening here with Pickle
        # and sometimes, access to files is wonky, especially
        # when the files are very large.
        # Make sure file exists
        while not os.path.exists(filePath):
            time.sleep(0.1)

        oldSize = None
        # Make sure file is not still being written to
        while True:
            try:
                currentSize = os.path.getsize(filePath)
                if currentSize == oldSize:
                    break

                time.sleep(1)
                oldSize = currentSize
            except:
                # Not possible, yet: sometimes we get here
                time.sleep(0.1)

    # For 2D histogram:
    # https://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm
    # and https://stackoverflow.com/questions/3122049/drawing-an-anti-aliased-line-with-thepython-imaging-library


class UniformRays(Rays):
    def __init__(self, yMax=1.0, yMin=None, thetaMax=pi / 2, thetaMin=None, M=100, N=100):
        self.yMax = yMax
        self.yMin = yMin
        if self.yMin is None:
            self.yMin = -yMax
        self.thetaMax = thetaMax
        self.thetaMin = thetaMin
        if thetaMin is None:
            self.thetaMin = -thetaMax

        self.M = M
        self.N = N
        rays = []
        for y in linspace(self.yMin, self.yMax, self.M, endpoint=True):
            for theta in linspace(self.thetaMin, self.thetaMax, self.N, endpoint=True):
                rays.append(Ray(y, theta))
        super(UniformRays, self).__init__(rays=rays)


class LambertianRays(Rays):
    def __init__(self, yMax=1.0, yMin=None, M=100, N=100, I=100):
        self.yMax = yMax
        self.yMin = yMin
        if yMin is None:
            self.yMin = -yMax

        self.thetaMin = -pi / 2
        self.thetaMax = pi / 2
        self.M = M
        self.N = N
        self.I = I
        rays = []
        for theta in linspace(self.thetaMin, self.thetaMax, N, endpoint=True):
            intensity = int(I * cos(theta))
            for y in linspace(self.yMin, self.yMax, M, endpoint=True):
                for k in range(intensity):
                    rays.append(Ray(y, theta))
        super(LambertianRays, self).__init__(rays=rays)


class RandomRays(Rays):
    def __init__(self, yMax=1.0, yMin=None, thetaMax=pi / 2, thetaMin=None, maxCount=100000):
        self.maxCount = maxCount
        self.yMax = yMax
        self.yMin = yMin
        if self.yMin is None:
            self.yMin = -yMax
        self.thetaMax = thetaMax
        self.thetaMin = thetaMin
        if thetaMin is None:
            self.thetaMin = -thetaMax
        super(RandomRays, self).__init__()

    def __len__(self) -> int:
        return self.maxCount

    def __getitem__(self, item):
        if item < 0:
            # Convert negative index to positive (i.e. -1 == len - 1)
            item += self.maxCount

        if item < 0 or item >= self.maxCount:
            raise IndexError(f"Index {item} out of bound, min = 0, max {self.maxCount}.")

        while len(self._rays) <= item:
            warnings.warn(f"Generating missing rays. This can take a few seconds.", UserWarning)
            self.randomRay()

        return self._rays[item]

    def __next__(self) -> Ray:
        if self.iteration >= self.maxCount:
            raise StopIteration
        # This should be able to know if enough rays. If not enough, generate them
        ray = self[self.iteration]
        self.iteration += 1
        return ray

    def randomRay(self) -> Ray:
        raise NotImplementedError("You must implement randomRay() in your subclass")


class RandomUniformRays(RandomRays):
    def __init__(self, yMax=1.0, yMin=None, thetaMax=pi / 2, thetaMin=None, maxCount=100000):
        super(RandomUniformRays, self).__init__(yMax=yMax, yMin=yMin, thetaMax=thetaMax, thetaMin=thetaMin,
                                                maxCount=maxCount)

    def randomRay(self) -> Ray:
        if len(self._rays) == self.maxCount:
            raise AttributeError("Cannot generate more random rays, maximum count achieved")

        theta = self.thetaMin + random.random() * (self.thetaMax - self.thetaMin)
        y = self.yMin + random.random() * (self.yMax - self.yMin)
        ray = Ray(y=y, theta=theta)
        self.append(ray)
        return ray


class RandomLambertianRays(RandomRays):
    def __init__(self, yMax=1.0, yMin=None, maxCount=10000):
        super(RandomLambertianRays, self).__init__(yMax=yMax, yMin=yMin, thetaMax=pi / 2, thetaMin=-pi / 2,
                                                   maxCount=maxCount)

    def randomRay(self) -> Ray:
        if len(self._rays) == self.maxCount:
            raise AttributeError("Cannot generate more random rays, maximum count achieved")

        theta = 0
        while (True):
            theta = self.thetaMin + random.random() * (self.thetaMax - self.thetaMin)
            intensity = cos(theta)
            seed = random.random()
            if seed < intensity:
                break

        y = self.yMin + random.random() * (self.yMax - self.yMin)
        ray = Ray(y, theta)
        self.append(ray)
        return ray
