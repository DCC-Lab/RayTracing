.. raytracing documentation master file, created by
   sphinx-quickstart on Wed May 13 15:07:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RayTracing
======================================
This code aims to provide a simple ray tracing module for calculating various
properties of optical paths (object, image, aperture stops, field stops). It
makes use of ABCD matrices and does not consider aberrations (spherical or
chromatic). Since it uses the ABCD formalism (or Ray matrices, or Gauss
matrices) it can perform tracing of rays and gaussian laser beams.
This package is developed by `DCClab <http://dcclab.ca>`_ members.  The many contributions cannot be described in all their details, but a list is provided here in no particular order:

* Elahe Parham: Documentation and examples writing
* Shadi Masoumi: Tutorials, Examples and usage
* Valérie Pineau Noël: Tutorials, Examples and usage
* Gabriel Genest: Extensive Unit Testing and BugFinder Extraordinaire
* Ludovick Bégin: Layout Artist Class Designer
* Francois Cote: Bug finding, layout and Bob Ross look-alike
* Mathieu Fournier: Unit Testing
* Marc-André Vigneault: Examples
* Daniel Côté: Official Designer & Merger, and "Gunnery Sergeant Hartman" Impersonator


Contents
^^^^^^^^

.. toctree::
   :maxdepth: 1

   raytracing
   gettingStarted
   reference
   examples
   contribute
   FAQ

Indices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
