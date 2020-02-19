from .ray import *
from numpy import *
import matplotlib.pyplot as plt

""" A group of rays kept as a list, to be used as a starting
point (i.e. an object) or as a cumulative detector (i.e. at an image
or output plane) for ImagingPath, MatrixGroup or any tracing function.
Subclasses can provide a computed ray for Monte Carlo simulation.
"""

class Rays:
    def __init__(self, rays=[], histogramOnly=False):
        self.rays = rays
        self.iteration = 0
        self.histogramOnly = histogramOnly

        self._yValues = None
        self._thetaValues = None
        self._intensityValues = None
        self._intensityProfile = None
        self._intensityBinEdges = None
        self._directionProfile = None
        self._directionBinEdges = None

    @property
    def count(self):
        return len(self.rays)

    @property
    def yValues(self):
        if self._yValues is None:
            self._yValues = list(map(lambda x : x.y, self.rays))

        return self._yValues

    @property
    def thetaValues(self):
        if self._thetaValues is None:
            self._thetaValues = list(map(lambda x : x.theta, self.rays))

        return self._thetaValues

    @property
    def intensityValues(self):
        if self._intensityValues is None:
            self._intensityValues = list(map(lambda x : x.intensity, self.rays))

        return self._intensityValues

    
    def intensityProfile(self, binCount=None, minValue=None, maxValue=None):
        if self._intensityProfile is None:
            if binCount is None:
                binCount = 40

            if minValue is None:
                minValue = min(self.yValues)

            if maxValue is None:
                maxValue = max(self.yValues)

            (self._intensityProfile, binEdges) = histogram(self.yValues, 
                                bins=binCount, weights=self.intensityValues, 
                                range=(minValue, maxValue))
            self._intensityProfile = list(self._intensityProfile)
            xValues = []
            for i in range(len(binEdges)-1):
                xValues.append((binEdges[i] + binEdges[i+1])/2 )

        return (self._intensityProfile, xValues)


    def directionProfile(self, binCount=None, minValue=None, maxValue=None):
        if self._directionProfile is None:
            if binCount is None:
                binCount = 10

            if minValue is None:
                minValue = min(self.thetaValues)

            if maxValue is None:
                maxValue = max(self.thetaValues)

            (self._directionProfile, self._directionBinEdges) = histogram(self.thetaValues, bins=binCount, range=(minValue, maxValue))

        return (self._directionProfile, self._directionBinEdges)

    def display(self, title="Intensity profile"):
        plt.ioff()
        (y,x) = self.intensityProfile()
        plt.plot(x,y,'k.')
        plt.ylim(bottom = 0)
        plt.xlabel("Distance")
        plt.ylabel("Intensity [arb.u]")
        plt.title(title)
        plt.show()
    
    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self) -> Ray :
        if self.iteration < len(self.rays):
            ray = self.rays[self.iteration]
            self.iteration += 1
            return ray

        raise StopIteration

    def append(self, ray):
        if self.histogramOnly:
            raise NotImplemented
        else:
            self.rays.append(ray)

            # Invalidate cached values
            self._yValues = None
            self._thetaValues = None
            self._intensityValues = None            
            self._intensityProfile = None
            self._intensityBinEdges = None
            self._directionProfile = None
            self._directionBinEdges = None

    def whichBin(self, value):
        if value <= self.min:
            return 0
        elif value >= self.max:
            return len(self.distribution)-1
        
        return int((value - self.min)/self.delta)


    # For 2D histogram:
    # https://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm
    # and https://stackoverflow.com/questions/3122049/drawing-an-anti-aliased-line-with-thepython-imaging-library

    # @property
    # def intensityError(self):
    #     return list(map(lambda x : sqrt(x), self.distribution))

    # @property
    # def normalizedIntensity(self):
    #     maxValue = max(self.values)
    #     return list(map(lambda x : x/maxValue, self.distribution))

    # @property
    # def normalizedIntensityError(self):
    #     maxValue = max(self.distribution)
    #     return list(map(lambda x : x/maxValue, self.error))


class UniformRays(Rays):
    def __init__(self, yMax=1.0, yMin=None, thetaMax=pi/2, thetaMin=None, M=1000, N=1000):
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
                rays.append(Ray(y,theta))
        super(UniformRays, self).__init__(rays=rays)

class LambertianRays(Rays):
    def __init__(self, yMax, yMin=None, M=100, N=100, I=100):
        self.yMax = yMax
        self.yMin = yMin
        if yMin is None:
            self.yMin = -yMax

        self.thetaMax = -pi/2
        self.thetaMin = pi/2
        self.M = M
        self.N = N
        self.I = I
        rays = []
        for theta in linspace(self.thetaMin, self.thetaMax, N, endpoint=True):
            intensity = int( I * cos(theta) )
            for y in linspace(self.yMin, self.yMax, M, endpoint=True):
                for k in range(intensity):
                    rays.append(Ray(y,theta, intensity))
        super(LambertianRays, self).__init__(rays=rays)

class RandomLambertianRays(Rays):
    def __init__(self, yMax, yMin=None, M=10000):
        self.yMax = yMax
        self.yMin = yMin
        if yMin is None:
            self.yMin = -yMax

        self.thetaMax = -pi/2
        self.thetaMin = pi/2
        self.M = M

        super(RandomLambertianRays, self).__init__(rays=None)

    @property
    def count(self):
        return self.M

    def __next__(self) -> Ray :
        if self.iteration >= self.M:
            raise StopIteration 
        self.iteration += 1

        theta = 0
        intensity = 1.0
        while (True):
            theta = self.thetaMin + random.random() * (self.thetaMax - self.thetaMin)
            intensity = cos(theta)
            seed = random.random()
            if seed < intensity:
                break

        y = self.yMin + random.random() * (self.yMax - self.yMin) 
        return Ray(y, theta, 1.0)
  

