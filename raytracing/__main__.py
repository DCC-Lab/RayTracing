from .imagingpath import *
from .laserpath import *
from .lasercavity import *

from .specialtylenses import *
from .axicon import *
from . import thorlabs
from . import eo
from . import olympus
from . import utils

import os 
import sys
import argparse
import re

from . import examples # __all__ will gather all example files dynamically
exampleScriptNames = examples.__all__
print(exampleScriptNames)
print(examples.ex01)

exit(0)
# We start by figuring out what the user really wants. If they don't know,
# we offer some help
ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='all',
                help="Specific example numbers, separated by a comma")
ap.add_argument("-c", "--classes", required=False, action='store_const',
                const=True, help="Print the class hierarchy in graphviz format")
ap.add_argument("-l", "--list", required=False, action='store_const',
                const=True, help="List all the accessible examples")

args = vars(ap.parse_args())
examples = args['examples']
printClasses = args['classes']
listExamples = args['list']

if printClasses:
    printClassHierarchy(Rays)
    printClassHierarchy(Matrix)
    exit(0)
elif listExamples:
    # List example code
    for i, name in enumerate(exampleScriptNames):
        print(name, globals())
        mod = [name]
        print("{0:2d}. {1} {2}".format(i+1, name, mod))
    exit(0)
else:
    # Run examples
    for scriptName in exampleScripts:
        scriptPath = "{0}/{1}".format(examplesDir, scriptName)
        print(pythonExec)
        os.system('{0} {1}'.format(pythonExec, scriptPath))

