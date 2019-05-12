"""A simple module for ray tracing with ABCD matrices.
https://github.com/DCC-Lab/RayTracing

Create an ImagingPath(), append matrices (optical elements or other
group of elements), and then display(). This helps determine of
course simple things like focal length of compound systems,
object-image, etc... but also the aperture stop, field stop, field
of view and any clipping issues that may occur.

When displaying the result with an ImagingPath(), the  objectHeight,
fanAngle, and fanNumber are used if the field of view is not
defined. You may adjust the values to suit your needs in ImagingPath().

Create a LaserPath() to analyse gaussian beams using the complex radius
of curvature q and the same matrices.

The class hierarchy can be seen on http://webgraphviz.com with the
following description:

digraph G {
   rankdir="LR";

    subgraph elements {
        "Matrix" -> "Space"
        "Matrix" -> "Lens"
        "Matrix" -> "Aperture"
        "Matrix" -> "ThickLens"
        "Matrix" -> "CurvedMirror"
        "Matrix" -> DielectricInterface
        "Matrix" -> "MatrixGroup"
        "ThickLens" -> "DielectricSlab"

        "MatrixGroup" -> "AchromaticDoubletLens"
        "AchromaticDoubletLens" -> "thorlabs.part#"
        "AchromaticDoubletLens" -> "eo.part#"
        "MatrixGroup" -> "Objective"
        "Objective" -> "olympus.part#"
    }

    subgraph mathview {
        "Matrix" -> "MatrixGroup"
        "MatrixGroup" -> ImagingPath
    }

}

To use the package, either:
1) pip install raytracing
or
2) copy to the raytracing package to the directory where you want to use it
or
3) python setup.py install from the source code directory
"""

import math

""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0/math.pi
radPerDeg = math.pi/180.0

""" We import almost everything by default, in the general namespace because it is simpler for everyone """

""" General matrices and groups for tracing rays and gaussian beams"""
from .matrix import *
from .matrixgroup import *

""" Ray matrices for geometrical optics """
from .ray import *
from .imagingpath import *

""" ABCD matrices for gaussian beams """
from .gaussianbeam import *
from .laserpath import *

""" Specialty lenses : objectives and achromats, but we keep the namespace for the vendor lenses """
from .specialtylenses import *
from .axicon import *

import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
import raytracing.olympus as olympus

""" Synonym of Matrix: Element 

We can use a mathematical language (Matrix) or optics terms (Element)
"""
Element = Matrix
Group = MatrixGroup
OpticalPath = ImagingPath

__version__ = "1.1.8"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

