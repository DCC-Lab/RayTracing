GPU-Accelerated Ray Tracing with OpenCL
========================================

As of version 1.4.0, the module supports GPU-accelerated batch ray tracing
via `OpenCL <https://www.khronos.org/opencl/>`_. When tracing large numbers
of rays (100k--1M+) through an optical system, the GPU can provide
10--100x speedup over the pure-Python path.

Installation
------------

OpenCL support is optional. Install ``pyopencl`` to enable it::

    pip install pyopencl

The rest of the module works without it. If ``pyopencl`` is not installed
or no GPU is available, ``traceMany()`` silently falls back to native
Python tracing.

How it works
------------

The standard ``Ray`` class stores data in Python attributes on the heap.
This is convenient but incompatible with GPU programming, where all data
must live in a single contiguous block of memory.

The ``compact`` module solves this with a **view pattern**:

- ``CompactRays`` allocates one flat numpy structured array that holds
  all ray data side by side in memory (24 bytes per ray), exactly like
  a C array of structs.
- ``CompactRay`` is a lightweight view into that buffer: it looks and
  behaves like a regular ``Ray`` (same properties: ``y``, ``theta``, ``z``,
  etc.) but every read and write goes directly into the shared buffer.

This way, Python code can keep using the familiar ``ray.y`` syntax while
the underlying memory layout is ready to be sent to the GPU in a single
transfer.

Quick example
-------------

.. code-block:: python

    from raytracing import *
    from raytracing.compact import CompactRays

    # Build an optical system
    path = ImagingPath()
    path.append(Space(d=10))
    path.append(Lens(f=50, diameter=25))
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=25))
    path.append(Space(d=10))
    group = MatrixGroup(path.transferMatrices())

    # Create 1 million rays in a contiguous buffer
    rays = CompactRays(maxCount=1_000_000)
    rays.fillWithRandomUniform(yMax=5)

    # Trace through the system (uses GPU if available, falls back to CPU)
    traces = group.traceMany(rays)

    # Display the output profile
    traces.lastRays.display("Output profile")

Key methods
-----------

``traceMany(inputRays, useOpenCL=True)``
    The main entry point. Tries the GPU path first; if anything fails
    (missing ``pyopencl``, no GPU, kernel error), it silently falls back
    to ``traceManyNative()``. Works with both regular ``Rays`` and
    ``CompactRays``.

``traceManyOpenCL(inputRays)``
    Traces rays on the GPU. Requires ``CompactRays`` input and ``pyopencl``.
    Raises a clear ``RuntimeError`` if dependencies are missing.

``traceManyNative(inputRays)``
    Pure-Python fallback. Works with any iterable of rays.

Output classes
--------------

``CompactRaytrace``
    A view into a slice of the output buffer representing one ray's path
    through all optical elements. No data is copied.

``CompactRaytraces``
    Organises the flat GPU output buffer into individual traces.
    ``traces.lastRays`` returns a ``Rays`` collection of the final ray
    from each trace, ready for ``display()`` or histogram analysis.

``RayTrace`` / ``RayTraces``
    The equivalent classes for native (non-GPU) tracing, providing the
    same interface.

Performance tips
----------------

- Use ``CompactRays`` with large ray counts (100k+) to benefit from GPU
  acceleration. Smaller batches may be slower due to transfer overhead.
- ``CompactRays.yValues`` and ``CompactRays.thetaValues`` read directly
  from the numpy array, avoiding per-ray Python overhead.
- ``fillWithRandomUniform()`` uses vectorized numpy operations internally.

See also
--------

- :class:`~raytracing.compact.CompactRay`
- :class:`~raytracing.compact.CompactRays`
- :class:`~raytracing.compact.CompactRaytrace`
- :class:`~raytracing.compact.CompactRaytraces`
