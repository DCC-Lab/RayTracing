import numpy as np
from .ray import Ray
from .rays import Rays

class CompactRay(Ray):

    Struct = np.dtype([("y", np.float32),
                      ("theta", np.float32),
                      ("z", np.float32),
                      ("isBlocked", np.int32),
                      ("apertureDiameter", np.float32),
                      ("wavelength", np.float32)
                      ])

    def __init__(self, raysSource, index):
        super().__init__()
        self.rays = raysSource
        self.index = index
        self.array = np.frombuffer(self.rays.buffer, dtype=CompactRay.Struct, count=1, offset=CompactRay.Struct.itemsize * self.index)

    @property
    def elementAsStruct(self):
        if self.array is None:
            self.array = np.frombuffer(self.rays.buffer, dtype=CompactRay.Struct, count=1, offset=CompactRay.Struct.itemsize * self.index)
        return self.array[0]

    @property
    def y(self):
        return self.elementAsStruct[0]
    @y.setter
    def y(self, value):
        self.elementAsStruct[0] = value

    @property
    def theta(self):
        return self.elementAsStruct[1]
    @theta.setter
    def theta(self, value):
        self.elementAsStruct[1] = value

    @property
    def z(self):
        return self.elementAsStruct[2]
    @z.setter
    def z(self, value):
        self.elementAsStruct[2] = value

    @property
    def isBlocked(self):
        return self.elementAsStruct[3] != 0
    @isBlocked.setter
    def isBlocked(self, value):
        self.elementAsStruct[3] = (value != 0)

    @property
    def apertureDiameter(self):
        return self.elementAsStruct[4]
    @apertureDiameter.setter
    def apertureDiameter(self, value):
        self.elementAsStruct[4] = value

    @property
    def wavelength(self):
        return self.elementAsStruct[5]
    @wavelength.setter
    def wavelength(self, value):
        self.elementAsStruct[5] = value

class CompactRays(Rays):
    def __init__(self, compactRaysStructuredBuffer=None, maxCount=None):
        super().__init__()
        self.maxCount = maxCount

        if compactRaysStructuredBuffer is not None:
            self.buffer = compactRaysStructuredBuffer
            self._rays = np.frombuffer(self.buffer, dtype=CompactRay.Struct)
        elif maxCount is not None:
            self._rays = np.zeros((maxCount,), dtype=CompactRay.Struct)
            self.buffer = self._rays.data
        else:
            raise ValueError('You must provide a buffer or a maxCount')

    def __getitem__(self, index):
        return CompactRay(self, index)

    def __setitem__(self, key, value):
        self._rays[key] = value

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self) -> CompactRay:

        if self.iteration < len(self):
            ray = self[self.iteration] # Again we want to use __getitem__ for self for CompactRays
            self.iteration += 1
            return ray

        raise StopIteration

    def append(self, tuple):
        raise RuntimeError('You can only replace elements from a pre-allocated CompactRays')

class CompactRaytrace:
    def __init__(self, compactRays, firstIndex, traceLength):
        self.compactRays = compactRays
        self.firstIndex = firstIndex
        self.traceLength = traceLength

    def __len__(self):
        return self.traceLength

    def __getitem__(self, rayIndex):
        while (rayIndex < 0):
            rayIndex += self.traceLength
        return self.compactRays[self.firstIndex + rayIndex]


    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self) -> CompactRay:

        if self.iteration < len(self):
            ray = self[self.iteration] # Again we want to use __getitem__ for self for CompactRays
            self.iteration += 1
            return ray

        raise StopIteration


class CompactRaytraces:
    def __init__(self, compactRays, traceLength):
        self.compactRays = compactRays
        self.traceLength = traceLength
        self.traceCount = int(compactRays.maxCount / traceLength)

    def __len__(self):
        return self.traceCount
    def __getitem__(self, traceIndex):
        while (traceIndex < 0):
            traceIndex += self.traceCount
        traceIndex = traceIndex % self.traceCount
        return CompactRaytrace(self.compactRays, traceIndex * self.traceLength, self.traceLength)


    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self) -> CompactRaytrace:

        if self.iteration < len(self):
            raytrace = self[self.iteration]
            self.iteration += 1
            return raytrace

        raise StopIteration
