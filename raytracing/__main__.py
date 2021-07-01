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

from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from . import examples # 'all' will gather all example files dynamically

# We start by figuring out what the user really wants. If they don't know,
# we offer some help
ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='all',
                help="Specific example numbers, separated by a comma")
ap.add_argument("-c", "--classes", required=False, action='store_const',
                const=True, help="Print the class hierarchy in graphviz format")
ap.add_argument("-l", "--list", required=False, action='store_const',
                const=True, help="List all the accessible examples")
ap.add_argument("-t", "--tests", required=False, action='store_const',
                const=True, help="Run all Unit tests")

args = vars(ap.parse_args())
runExamples = args['examples']
runTests = args['tests']
printClasses = args['classes']
listExamples = args['list']

if runExamples == 'all':
    runExamples = range(1, len(examples.short)+1)
elif runExamples == '':
    runExamples = []
else:
    runExamples = [int(y) for y in runExamples.split(',')]

if printClasses:
    printClassHierarchy(Rays)
    printClassHierarchy(Matrix)
elif runTests:
    moduleDir = os.path.dirname(os.path.realpath(__file__))
    err = os.system('cd {0}/tests; {1} -m unittest'.format(moduleDir, sys.executable))
elif listExamples:
    topDir = os.path.dirname(os.path.realpath(examples.__file__))
    all = []
    all.extend(examples.short)
    all.extend(examples.short)
    
    print("\nAll examples")
    print("==============")
    for i, entry in enumerate(examples.short):
        print("{0:2d}. {1}.py {2}".format(i+1, entry["name"], entry["title"]))

    print("\nMore examples code available in: {0}".format(topDir))
elif runExamples:
    # Some decent parameters for plots
    # See https://matplotlib.org/api/font_manager_api.html#matplotlib.font_manager.FontProperties.set_size
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (10, 7),
             'axes.labelsize': 'x-large',
             'axes.titlesize':'x-large',
             'xtick.labelsize':'x-large',
             'ytick.labelsize':'x-large',
             'font.family':'helvetica'}
    plt.rcParams.update(params)

    print("Running example code : {0}".format(runExamples))
    for i in runExamples:
        entry = examples.short[i-1]
        print("\nScript '{0}.py' - begin source code".format(entry["name"]))
        print(entry["terminalSourceCode"],end='')
        print("\nScript '{0}.py' - end source code".format(entry["name"]))
        print("\nScript '{0}.py' - begin output".format(entry["name"]))
        entry["code"](comments=entry["bmpSourceCode"])        
        print("Script '{0}.py' - end output".format(entry["name"]))

