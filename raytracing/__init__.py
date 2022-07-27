r"""A simple module for ray tracing with ABCD matrices.
https://github.com/DCC-Lab/RayTracing

Create an `ImagingPath()`, append matrices (optical elements or other
group of elements), and then `display()`. This helps determine of
course simple things like focal length of compound systems,
object-image, etc... but also the aperture stop, field stop, field
of view and any clipping issues that may occur.

When displaying the result with an `ImagingPath()`, the  `objectHeight`,
`fanAngle`, and `fanNumber` are used if the field of view is not
defined. You may adjust the values to suit your needs in `ImagingPath()`.

Create a `LaserPath()` to analyse gaussian beams using the complex radius
of curvature q and the same matrices.

The class hierarchy can be obtained with `python -m raytracing --classes`
"""

import math

""" We import almost everything by default, in the general namespace because it is simpler for everyone """

""" General matrices and groups for tracing rays and gaussian beams"""
from .matrix import *
from .matrixgroup import *

""" Ray matrices for geometrical optics """
from .ray import *
from .rays import *
from .imagingpath import *

""" ABCD matrices for gaussian beams """
from .gaussianbeam import *
from .laserpath import *
from .lasercavity import *

""" Matrices for components: System4f (synonym: Telescope), System2f """
from .components import *

""" Specialty lenses : objectives and achromats, but we keep the namespace for the vendor lenses """
from .specialtylenses import *
from .axicon import *

from . import thorlabs
from . import eo
from . import olympus

from .zemax import *

from .utils import *
from .preferences import *

import os
from datetime import datetime
    
""" Synonym of Matrix: Element 

We can use a mathematical language (Matrix) or optics terms (Element)
"""
Element = Matrix
Group = MatrixGroup
OpticalPath = ImagingPath

__version__ = "1.3.9"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"

import os.path as path
import time
import tempfile

def lastCheckMoreThanADay():
    if "lastVersionCheck" in prefs:
        then = datetime.fromisoformat(prefs["lastVersionCheck"])
        difference = datetime.now() - then
        if difference.days > 1:
            return True
        else:
            return False
    else:
        return True


prefs = Preferences()
if lastCheckMoreThanADay():
    checkLatestVersion()
    prefs["lastVersionCheck"] = datetime.now().isoformat()

if "RAYTRACING_EXPERT" in os.environ:
    prefs["mode"] = "expert"
    
try:
    if prefs["mode"] == "silent":
        silentMode()
    elif prefs["mode"] == "expert":
        expertMode()
    else:
        beginnerMode()
except Exception as err:
    pass


