import argparse
from pygments import highlight
import pygments.lexers
import pygments.formatters
import webbrowser
import os


ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='', help="Specific example numbers, separated by a comma")

args = vars(ap.parse_args())
examples = args['examples']


class ExampleManager:
    def __init__(self, arguments):
        self.arguments = arguments
        self.exampleDirPath = os.path.dirname(os.path.realpath(__file__)) + "\..\examples\\argsExamples"
        self.outputExampleFilePath = self.exampleDirPath + "\exampleFile.html"
        self.selectedFile = None
        self.formatter = pygments.formatters.get_formatter_by_name('html',full=True, linenos=True, cssclass="source", style='default')
        self.lexer = pygments.lexers.get_lexer_by_name('python', stripall=True)
        self.parseArguments()

    def exampleCarousel(self, exampleIndexList):
        for i in exampleIndexList:
            self.selectedFile = self.exampleDirPath + '\example{}'.format(i)
            self.showExample()

    def showExample(self):
        self.generateExample()
        webbrowser.open(self.outputExampleFilePath)

    def generateExample(self):
        self.generateFigureFromCode()
        self.generateHTMLHighlightedCode()
        self.mergeFigureAndHTML()
        # OPEN HTML FILE.

    def mergeFigureAndHTML(self):
        pass

    def generateFigureFromCode(self):
        pass

    def generateHTMLHighlightedCode(self, code):
        with open(self.outputExampleFilePath, 'w') as f:
            highlightedCode = highlight(code, self.lexer, self.formatter, outfile=f)
            f.close()
        return highlightedCode

    def getExampleCode(self):
        pass

    def parseArguments(self):
        print(self.arguments)
        if 'examples' in self.arguments:
            print(list(self.arguments['examples']))
            self.exampleCarousel(list(self.arguments['examples']))


manager = ExampleManager(args)
manager.generateHTMLHighlightedCode("print ('Hello World')\nclass Hello:\n\tdef __init__(self):\n\tpass")

