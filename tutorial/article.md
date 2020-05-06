# Tutorial article on ray tracing

Here is the skeleton of the article.

[TOC]

## Abstract

1. Simple optical design, 0th order: objects, images, but also apertures, field stops and invariant
2. **For students and non optical designers**
3. Simple Python library for tracing rays, few dependencies: only depends on `matplotlib`
4. Documented code, simplicity before power, but still, very powerful.

## Introduction

- Optical design is everywhere, although not referred to by this name. Students need to know certain system properties to successfully build their systems. However, not everyone has the knowledge from undergraduate courses or experience. Of course, when needed eventually, many people dig in and figure it out, but not everyone actually digs in. This in fact, includes many people such as the last author of this article.

- This Python module is designed to provide answers (and teach) to non-experts to identify weaknesses in their optical systems such as microscopes but also fiber-based devices. 

## Objects, images, and rays

This section contains a very short primer on imaging and ray matrices. It has definition of rays, ABCD matrices and a table gathering all useful matrices.

Definitions and illustration of how to use formalism:

1. $C = -1/f$, measured from principal planes
2. An imaging matrix has $ B= 0$
   1. When it is imaging, A = transverse magnification
   2. When it is imaging, D = angular magnification
   3. Principal planes distances

We need a figure that shows a group of arbitrary optical elements, with all the important properties (ACBD) in addition to all the properties that are considered in `Matrix` such as vertices, length.

Simple example (?): recovering thick lens equation from interface and space.

Other example: achromats from EO and Thorlabs can be modelled.

Optical invariant: the product $n ( y_1 \theta_2 - y_2 \theta_1)$ is a constant.  Therefore if a component cannot "support" a certain product, then it becomes clear the ray will be blocked.



## Apertures

This section contains a description of apertures, how they are not considered in ABCD formalism but can easily be added and how they lead to **Aperture Stop** and **Field Stop**. A section describes the procedure to find the aperture and field stop.

**Chief** and **axial** rays (validate definitions, especially axial or marginal ray?). Simple proof to obtain chief and axial ray and that these two rays are sufficient to describe the light through whole system.

## Collection of rays: as inputs and outputs

To obtain the (relative) intensity of a point on an object, we can trace many rays and collect a histogram of rays as a function of position.

Example: Uniform (validate math!), LambertianRays, 

## Gaussian beams

Free bonus: gaussian beams can use ray matrices (but not apertures).

## `raytracing` module

**A section describes the design goals:** 

1. Simplicity of usage
2. Simplicity of implementation (i.e. code)
3. Provides answers to common questions encountered in the lab
4. Useful teaching tool in optics
   1. Illustration of strategies with real-life examples
   2. Validation of strategies to be taught
   3. Provides real figures to be used in presentations.
   4. Real lenses from real vendors with calculated properties
5. Useful teaching tool in programming
   1. Good object-oriented design that matches "the problem at hand"
   2. Simple, clear implementation following Clean Code practices.
   3. Properly documented
   4. Properly unit tested
   5. Implanted as an easy installable Python module and PyPi.
6. Open sourced



## Object-oriented design

*Everything is a matrix.  Ray matrices combine to give another ray matrix. Yet, not every matrix (or optical path) is an imaging system (for instance, with can model an illumination system, which does not consist of an object and an image). Describe the class hierarchy and show a figure.* `Matrix`, `MatrixGroup`, `OpticalPath`, `ImagingPath`, `Laserpath`.

Explain difference between matrix multiplications and tracing: tracing considers apertures but multiplications do not.



## Example use:

Relevant examples of how to use the code.

Prepare many different examples, keep them in a directory and show figures.



## Practical examples solved with module

Widefield microscope

Simple scanning system

Laser scanning microscope

Confocal pinhole detection

Diffuse source from scattering medium

Two-photon descanned detector

​	Big detectors (R3896) versus small detectors (GaAsP)

Illumination system

Axicon

Fiber-based collection system







Discussion and outlook:

Examples of things that could be added:

1. Scanning mirrors.

2. Extract wavefronts 

3. GUI, but not within main code: avoid Zawinski's law of software envelopment (also known as *Zawinski's law*) and [software bloating](https://en.wikipedia.org/wiki/Software_bloat) with popular features:[[13\]](https://en.wikipedia.org/wiki/Jamie_Zawinski#cite_note-aoup-13)[[14\]](https://en.wikipedia.org/wiki/Jamie_Zawinski#cite_note-jf-14)

   > Every program attempts to expand until it can read [mail](https://en.wikipedia.org/wiki/E-mail). Those programs which cannot so expand are replaced by ones which can.

4. Misaligned matrices

5. Polarization

6. 3D rays and 3D rendering 3D export of optical systems

7. Reflections

8. 

