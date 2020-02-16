from .ray import *
from numpy import *
import random

class Rays:
    def __init__(self, rays):
        self.rays = rays
        if rays is not None:
            self.N = len(rays)
        else:
            self.N = None
            
        self.iteration = 0

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
    def __init__(self, yMax=1.0, yMin=None, thetaMax=pi/2, thetaMin=None, M=100, N=100):
        self.yMax = yMax
        self.yMin = yMin
        if yMin is None:
            yMin = -yMax
        self.thetaMax = thetaMax
        self.thetaMin = thetaMin
        if thetaMin is None:
            thetaMin = -thetaMin

        self.M = M
        self.N = N
        rays = []
        for y in linspace(yMin, yMax, M, endpoint=True):
            for theta in linspace(thetaMin, thetaMax, N, endpoint=True):
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
            intensity = int( I * cos(theta) * cos(theta) )
            for y in linspace(yMin, yMax, M, endpoint=True):
                for k in range(intensity):
                    rays.append(Ray(y,theta))
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

    def computeNext(self) -> Ray :
        if self.iteration >= self.M:
            raise StopIteration 

        theta = 0
        while (True):
            theta = random.uniform(self.thetaMin, self.thetaMax)
            threshold = cos(theta) * cos(theta)
            seed = random.random()
            if seed < threshold:
                break

        y = random.uniform(self.yMin, self.yMax)
        return Ray(y,theta)

