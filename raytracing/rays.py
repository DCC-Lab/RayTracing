from .ray import *
from numpy import *
import matplotlib.pyplot as plt

class Rays:
    def __init__(self, rays):
        self.rays = rays
        if rays is not None:
            self.N = len(rays)
        else:
            self.N = None
            
        self.iteration = 0

    @property
    def count(self):
        return self.N
    
    def __iter__(self):
        return self

    def __next__(self) -> Ray :
        if self.rays is None:
            self.iteration += 1
            return self.computeNext()
        elif len(self.rays) == 0:
            raise StopIteration
        else:
            self.iteration += 1
            return self.rays.pop()

    def computeNext(self) -> Ray :
        raise StopIteration 

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

    @property
    def count(self):
        return self.N*self.M


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
            intensity = int( I * cos(theta) * cos(theta) )
            for y in linspace(yMin, yMax, M, endpoint=True):
                for k in range(intensity):
                    rays.append(Ray(y,theta))
        super(LambertianRays, self).__init__(rays=rays)

    @property
    def count(self):
        return self.N*self.M*self.I

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

    def computeNext(self) -> Ray :
        if self.iteration >= self.M:
            raise StopIteration 

        theta = 0
        while (True):
            theta = self.thetaMin + random.random() * (self.thetaMax - self.thetaMin)
            threshold = cos(theta)
            threshold *= threshold
            seed = random.random()
            if seed < threshold:
                break

        y = self.yMin + random.random() * (self.yMax - self.yMin) 
        return Ray(y,theta)


class RayHistogram:
    def __init__(self, min=None, max=None, binCount=10):
        self.values = [0] * binCount
        self.min = min
        self.max = max
        self.range = linspace(min, max, binCount)
        self.width = abs(max - min)
        self.delta = self.width/binCount
        self.binCount = binCount

    @property
    def error(self):
        return list(map(lambda x : sqrt(x), self.values))

    @property
    def normalizedValues(self):
        maxValue = max(self.values)
        return list(map(lambda x : x/maxValue, self.values))

    @property
    def normalizedError(self):
        maxValue = max(self.values)
        return list(map(lambda x : x/maxValue, self.error))

    def add(self, value):
        if isinstance(value, Ray):
            ray = value
            index = self.whichBin(ray.y)
        else:
            index = self.whichBin(value)
        self.values[index] += 1

    def whichBin(self, value):
        if value <= self.min:
            return 0
        elif value >= self.max:
            return len(self.values)-1
        
        return int((value - self.min)/self.delta)

    def show(self, title="Intensity profile", bins='auto', normalized=True):
        plt.ioff()
        plt.errorbar(self.range, self.normalizedValues, yerr=self.normalizedError, fmt="ko-")
        plt.xlabel("Distance")
        plt.ylabel("Intensity [arb.u]")
        plt.title(title)
        plt.show()

