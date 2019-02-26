# We import everything by default, in the general namespace
# because it is simpler for everyone

from .abcd import *
from .lens import *
from .axicon import *
import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
import raytracing.olympus as olympus

__version__ = "1.0.8"
__author__ = "Daniel Cote <dccote@cervo.ulaval.ca>"
print("Main documentation at https://github.com/DCC-Lab/RayTracing")

