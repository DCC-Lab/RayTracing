import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms
import math
import cmath
import sys

if sys.version_info[0] < 3:
    print("Warning: you should really be using Python 3. \
        No guarantee this will work in 2.x")

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

The class hierarchy can be seen on http://webgraphviz.com with the
following description:

digraph G {

    subgraph mathview {
        "Matrix" -> "MatrixGroup"
        "MatrixGroup" -> ImagingPath
    }

    subgraph opticsview {
        "Element" -> "Group"
        "Group" -> ImagingPath
    }
}

To use the package, either:
1) pip install raytracing
or
2) copy to the raytracing package to the directory where you want to use it
or
3) python setup.py install from the source code directory
"""


""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0/math.pi
radPerDeg = math.pi/180.0

from .ray import *
from .gaussianbeam import *
from .matrix import *
from .matrixgroup import *
from .imagingpath import *
from .laserpath import *

""" Synonym of Matrix: Element 

We can use a mathematical language (Matrix) or optics terms (Element)
"""
Element = Matrix
Group = MatrixGroup
OpticalPath = ImagingPath
