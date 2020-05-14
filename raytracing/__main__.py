from .imagingpath import *
from .laserpath import *

from .specialtylenses import *
from .axicon import *
import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
import raytracing.olympus as olympus
import argparse


ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='all', help="Specific example numbers, separated by a comma")

args = vars(ap.parse_args())
examples = args['examples']

if examples == 'all':
    examples = range(1,30)
else:
    examples = [ int(y) for y in examples.split(',')]


class ExampleManager:
    def __init__(self, arguments):
        self.arguments = arguments
        self.exampleDirPath = os.path.dirname(os.path.realpath(__file__)) + "\..\examples\\argsExamples"
        self.parseArguments()

    def exampleCarousel(self):
        pass

    def showExample(self):
        pass

    def generatePdfExample(self):
        pass

    def generateFigureFromCode(self):
        pass

    def generateHighlightedCodePdf(self):
        pass

    def highlightCode(self):
        pass

    def parseArguments(self):
        pass

