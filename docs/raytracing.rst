RayTracing
========================


This code aims to provide a simple ray tracing module for calculating various properties of optical paths (object, image, aperture stops, field stops). It makes use of ABCD matrices and does not consider aberrations (spherical or chromatic). Since it uses the ABCD formalism (or Ray matrices, or Gauss matrices) it can perform tracing of rays and gaussian laser beams.

It is not a package to do "Rendering in 3D with raytracing".

The code has been developed first for teaching purposes and is used in my "`Optique <https://books.apple.com/ca/book/optique/id949326768>`_
" Study Notes (french only), but also for actual use in my research. There are `tutorials <https://www.youtube.com/playlist?list=PLUxTghemi4Ft0NzQwuufpU-EGgkmaInAf>`_ (in french, with English subtitles) on YouTube. I have made no attempts at making high-performance code. **Readability** and **simplicity of usage** are the key here. It is a module with only a few files, and only matplotlib as a dependent module.

The module defines ``Ray``, ``Matrix``, ``MatrixGroup`` and ``ImagingPath`` as the main elements for tracing rays. ``Matrix`` and ``MatrixGroup`` are either one or a sequence of many matrices into which ``Ray`` will propagate. ``ImagingPath`` is also a sequence of elements, with an object at the front edge. Specific subclasses of ``Matrix`` exists: ``Space``, ``Lens``, ``ThicklLens``, and ``Aperture``. Finally, a ray fan is a collection of rays, originating from a given point with a range of angles.

If you want to perform calculations with coherent laser beams, then you use ``GaussianBeam`` and ``LaserPath``. Everything is essentially the same, except that the formalism does not allow for the gaussian beam to be "blocked", hence any calculation of stops with aperture is not available in ``LaserPath``.

by [Daniel Côté](mailto:dccote@cervo.ulaval.ca?subject=Raytracing python module)