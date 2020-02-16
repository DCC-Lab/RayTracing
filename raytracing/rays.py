from .ray import *
from numpy import *
import random

class Rays:
    def __init__(self, rays):
        self.rays = rays
        self.N = len(rays)
        self.iteration = 0

    def __iter__(self):
        return self

    def __next__(self) -> Ray :
        if len(self.rays) == 0:
            raise StopIteration
        else:
            self.iteration += 1
            return self.rays.pop()

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
    def __init__(self, yMax, yMin=None, M=1000):
        self.yMax = yMax
        self.yMin = yMin
        if yMin is None:
            self.yMin = -yMax

        self.thetaMax = -pi/2
        self.thetaMin = pi/2
        self.M = M
        rays = []
        for i in range(M):
            theta = 0
            while (True):
                theta = random.uniform(self.thetaMin, self.thetaMax)
                threshold = cos(theta) * cos(theta)
                seed = random.random()
                if seed < threshold:
                    break

            y = random.uniform(self.yMin, self.yMax)
            rays.append(Ray(y,theta))

        super(RandomLambertianRays, self).__init__(rays=rays)
