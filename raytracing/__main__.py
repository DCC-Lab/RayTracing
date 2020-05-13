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

if 19 in examples:
    cavity = LaserPath(label="Laser cavity: round trip\nCalculated laser modes")
    cavity.isResonator = True
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))
    cavity.append(CurvedMirror(R=400))
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))

    # Calculate all self-replicating modes (i.e. eigenmodes)
    (q1,q2) = cavity.eigenModes()
    print(q1,q2)

    # Obtain all physical (i.e. finite) self-replicating modes
    qs = cavity.laserModes()
    for q in qs:
        print(q)

    # Show
    cavity.display()
