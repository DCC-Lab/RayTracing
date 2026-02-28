"""Compact, contiguous-memory representations of rays for GPU computation.

In pure Python, each ``Ray`` is an independent object with its own attributes
stored in the Python heap. This is natural and convenient, but completely
incompatible with GPU programming (OpenCL, CUDA), where all data must live in
a single, contiguous block of memory that can be transferred to the device.

This module solves the problem with a **view pattern**:

- ``CompactRays`` allocates one flat numpy structured array that holds *all*
  ray data side by side in memory, exactly like a C array of structs.
- ``CompactRay`` is a lightweight *view* into that buffer: it looks and
  behaves like a regular ``Ray`` (same properties: ``y``, ``theta``, ``z``,
  etc.) but every read and write goes directly into the shared buffer.

This way, Python code can keep using familiar ``ray.y`` syntax while the
underlying memory layout is ready to be sent to the GPU in a single transfer.

``CompactRaytrace`` and ``CompactRaytraces`` add a second level of
organisation on top of the output buffer, slicing it into per-ray traces
(one trace = one input ray propagated through all optical elements).

See Also
--------
raytracing.ray : The base ``Ray`` class.
raytracing.rays : The base ``Rays`` collection.
"""

import numpy as np
from .ray import Ray
from .rays import Rays, RayTrace, RayTraces

class CompactRay(Ray):
    """A view into a shared buffer that behaves like a ``Ray``.

    A regular ``Ray`` stores its data in normal Python attributes.
    A ``CompactRay`` instead reads and writes directly into a position
    inside a ``CompactRays`` buffer. From the outside it feels identical
    — you can still write ``ray.y = 1.0`` or ``print(ray.theta)`` — but
    under the hood every access goes through the contiguous numpy array.

    The memory layout of a single ray is defined by ``CompactRay.Struct``,
    a numpy structured dtype with fields: *y*, *theta*, *z*, *isBlocked*,
    *apertureDiameter*, and *wavelength* (all 32-bit).

    Parameters
    ----------
    raysSource : CompactRays
        The owning buffer that holds the actual data.
    index : int
        Position of this ray inside the buffer (0-based).

    See Also
    --------
    CompactRays : The contiguous buffer that owns the data.
    Ray : The base class whose interface is preserved.
    """

    Struct = np.dtype([("y", np.float32),
                      ("theta", np.float32),
                      ("z", np.float32),
                      ("isBlocked", np.int32),
                      ("apertureDiameter", np.float32),
                      ("wavelength", np.float32)
                      ])

    def __init__(self, raysSource, index):
        """Create a view for one ray inside the shared buffer.

        Parameters
        ----------
        raysSource : CompactRays
            The buffer that holds all ray data contiguously in memory.
        index : int
            Which ray in the buffer this view refers to (0-based).
        """
        super().__init__()
        self.rays = raysSource
        self.index = index
        self.array = np.frombuffer(self.rays.buffer, dtype=CompactRay.Struct, count=1, offset=CompactRay.Struct.itemsize * self.index)

    @property
    def elementAsStruct(self):
        if self.array is None:
            self.array = np.frombuffer(self.rays.buffer, dtype=CompactRay.Struct, count=1, offset=CompactRay.Struct.itemsize * self.index)
        return self.array[0]

    def assign(self, ray):
        """Copy all fields from a regular ``Ray`` into this buffer position.

        This is the bridge between the object-oriented world (a ``Ray`` with
        Python attributes) and the GPU-friendly world (a slot in a contiguous
        numpy buffer).

        Parameters
        ----------
        ray : Ray
            The source ray whose fields will be copied.
        """
        self.y = ray.y
        self.theta = ray.theta
        self.z = ray.z
        self.wavelength = ray.wavelength
        self.isBlocked = ray.isBlocked
        self.apertureDiameter = ray.apertureDiameter

    @property
    def y(self):
        return self.elementAsStruct['y']
    @y.setter
    def y(self, value):
        self.elementAsStruct['y'] = value

    @property
    def theta(self):
        return self.elementAsStruct['theta']
    @theta.setter
    def theta(self, value):
        self.elementAsStruct['theta'] = value

    @property
    def z(self):
        return self.elementAsStruct['z']
    @z.setter
    def z(self, value):
        self.elementAsStruct['z'] = value

    @property
    def isBlocked(self):
        return self.elementAsStruct['isBlocked'] != 0
    @isBlocked.setter
    def isBlocked(self, value):
        self.elementAsStruct['isBlocked'] = (value != 0)

    @property
    def apertureDiameter(self):
        return self.elementAsStruct['apertureDiameter']
    @apertureDiameter.setter
    def apertureDiameter(self, value):
        self.elementAsStruct['apertureDiameter'] = value

    @property
    def wavelength(self):
        return self.elementAsStruct['wavelength']
    @wavelength.setter
    def wavelength(self, value):
        self.elementAsStruct['wavelength'] = value

class CompactRays(Rays):
    """A contiguous buffer holding many rays, ready for GPU transfer.

    Where a regular ``Rays`` is a Python list of independent ``Ray`` objects,
    ``CompactRays`` stores all ray data in a single numpy structured array
    so that the memory can be sent to an OpenCL or CUDA device in one call.

    Individual rays are accessed with ``compact_rays[i]``, which returns a
    ``CompactRay`` view — not a copy. Modifying the view modifies the buffer.

    Three construction modes are supported:

    1. **From an existing buffer** (``compactRaysStructuredBuffer``) — wraps
       raw bytes, typically received back from the GPU after computation.
    2. **From a count** (``maxCount``) — allocates a zero-filled buffer of
       the requested size, to be filled later.
    3. **From a list of ``Ray`` objects** (``rays``) — allocates a buffer and
       copies each ray into it, converting from Python objects to the compact
       layout.

    Parameters
    ----------
    compactRaysStructuredBuffer : buffer, optional
        A pre-existing contiguous buffer of ``CompactRay.Struct`` data.
    maxCount : int, optional
        Number of ray slots to allocate (zero-filled).
    rays : list of Ray, optional
        Regular ``Ray`` objects to convert into the compact layout.

    Raises
    ------
    ValueError
        If none of the three construction arguments is provided.

    See Also
    --------
    CompactRay : A view into one slot of this buffer.
    """

    def __init__(self, compactRaysStructuredBuffer=None, maxCount=None, rays=None):
        super().__init__()

        if compactRaysStructuredBuffer is not None:
            self.buffer = compactRaysStructuredBuffer
            self._rays = np.frombuffer(self.buffer, dtype=CompactRay.Struct)
            self.maxCount = len(self._rays)
        elif maxCount is not None:
            self._rays = np.zeros((maxCount,), dtype=CompactRay.Struct)
            self.buffer = self._rays.data
            self.maxCount = maxCount
        elif rays is not None:
            self._rays = np.zeros((len(rays),), dtype=CompactRay.Struct)
            self.buffer = self._rays.data
            self.maxCount = len(rays)

            for i, ray in enumerate(rays):
                CompactRay(self, i).assign(ray)

        else:
            raise ValueError('You must provide a buffer or a maxCount')

    def fillWithRandomUniform(self, yMax=1.0, yMin=None, thetaMax=np.pi / 2, thetaMin=None):
        """Fill the buffer with rays at random heights and angles.

        Each ray receives a uniformly distributed height in [yMin, yMax]
        and angle in [thetaMin, thetaMax]. If the minimum values are not
        given, symmetric ranges around zero are used.

        Parameters
        ----------
        yMax : float
            Maximum height. (Default=1.0)
        yMin : float, optional
            Minimum height. Defaults to ``-yMax``.
        thetaMax : float
            Maximum angle in radians. (Default=pi/2)
        thetaMin : float, optional
            Minimum angle in radians. Defaults to ``-thetaMax``.
        """
        if yMin is None:
            yMin = -yMax
        if thetaMin is None:
            thetaMin = -thetaMax

        for i in range(len(self._rays)):
            ray = self[i]
            ray.y = yMin + np.random.random() * (yMax - yMin)
            ray.theta = thetaMin + np.random.random() * (thetaMax - thetaMin)

    def __getitem__(self, index):
        return CompactRay(self, index)

    def __setitem__(self, index, value):
        CompactRay(self, index).assign(value)

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self) -> CompactRay:

        if self.iteration < len(self):
            ray = self[self.iteration] # Again we want to use __getitem__ for self for CompactRays
            self.iteration += 1
            return ray

        raise StopIteration

    @property
    def yValues(self):
        if self._yValues is None:
            self._yValues = self._rays['y'].tolist()
        return self._yValues

    @property
    def thetaValues(self):
        if self._thetaValues is None:
            self._thetaValues = self._rays['theta'].tolist()
        return self._thetaValues

    def append(self, tuple):
        raise RuntimeError('You can only replace elements from a pre-allocated CompactRays')

class CompactRaytrace(RayTrace):
    """A view into a slice of a ``CompactRays`` buffer representing one ray trace.

    When a single input ray is propagated through *N* optical elements, it
    produces *N* output rays (one after each element). These *N* consecutive
    entries in the output buffer form one *trace*. ``CompactRaytrace`` gives
    convenient access to that slice without copying any data.

    Inherits ``__str__``, ``__repr__``, ``__iter__``, and ``__next__`` from
    ``RayTrace``. Overrides ``__len__`` and ``__getitem__`` for buffer access.

    Parameters
    ----------
    compactRays : CompactRays
        The output buffer containing all traces laid out end to end.
    firstIndex : int
        Index of the first ray in this trace inside the buffer.
    traceLength : int
        Number of rays in this trace (equals the number of optical elements).
    """

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


class CompactRaytraces(RayTraces):
    """A collection of all ray traces from a GPU computation.

    After propagating *M* input rays through *N* optical elements, the GPU
    produces an output buffer of *M x N* rays. ``CompactRaytraces`` organises
    this flat buffer into *M* individual ``CompactRaytrace`` slices, one per
    input ray, so that ``traces[i]`` gives the full journey of the *i*-th ray
    through the optical system.

    Inherits ``__str__``, ``__repr__``, ``__iter__``, and ``__next__`` from
    ``RayTraces``. Overrides ``__len__`` and ``__getitem__`` for buffer access.

    Parameters
    ----------
    compactRays : CompactRays
        The flat output buffer of size *M x N*.
    traceLength : int
        Number of optical elements (*N*), i.e. the length of each trace.
    """

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
