import argparse
from pygments import highlight
import pygments.lexers
import pygments.formatters
import webbrowser
from unittest.mock import patch
from matplotlib import pyplot as plt
import tempfile
import base64
import os


ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='', help="Specific example numbers, separated by a comma")
args = vars(ap.parse_args())


class ExampleManager:
    def __init__(self, arguments):
        self.arguments = arguments
        self.exampleDirPath = os.path.dirname(os.path.realpath(__file__)) + "\..\examples\\argsExamples"
        self.htmlTemporaryExampleFile = None
        self.selectedFileIndex = 0
        self.figureObject = None
        self.base64Figure = None
        self.selectedFile = None
        self.formatter = pygments.formatters.get_formatter_by_name('html',full=True, linenos=True, cssclass="source", style='default')
        self.lexer = pygments.lexers.get_lexer_by_name('python', stripall=True)
        self.parseArguments()

    def exampleCarousel(self, exampleIndexList):
        for i in exampleIndexList:
            self.selectedFileIndex = i
            self.selectedFile = self.exampleDirPath + '\example{}.py'.format(i)
            self.showExample()

    def showExample(self):
        self.generateExample()
        webbrowser.open("file://" + self.htmlTemporaryExampleFile)

    def generateExample(self):
        self.generateFigureFromCode()
        self.generateHTMLHighlightedCode()
        self.mergeFigureAndHTML()

    def mergeFigureAndHTML(self):
        with open(self.htmlTemporaryExampleFile, 'a+') as f:
            f.write(''''<img class="icon" src="data:image/png;base64,{} ">'''.format(self.base64Figure))
            f.close()

    def generateFigureFromCode(self):
        self.runExampleCode()
        fig, axes = plt.subplots(figsize=(10, 7))
        self.figureObject.createRayTracePlot(axes=axes)
        with tempfile.TemporaryFile(suffix=".png") as tmpfile:
            plt.savefig(tmpfile, format="png")
            tmpfile.seek(0)
            self.base64Figure = base64.b64encode(tmpfile.read()).decode()

    def generateHTMLHighlightedCode(self, code=""):
        if not code:
            code = self.getExampleCode()
        temp = tempfile.NamedTemporaryFile(delete=False)
        path = temp.name + '.html'
        self.htmlTemporaryExampleFile = path
        with open(path, 'w') as f:
            highlightedCode = highlight(code, self.lexer, self.formatter)
            f.write(highlightedCode)
            f.close()

        return highlightedCode

    def runExampleCode(self):
        with patch('matplotlib.pyplot.show') as p:
            global path
            exec(open(self.selectedFile).read(), globals())
            self.figureObject = path

    def getExampleCode(self):
        with open(self.selectedFile, 'r') as f:
            codeString = f.read()
            f.close()
            #TODO:should do a parsing job here to remove docstring and if __name__ == __main__
        return codeString

    def parseArguments(self):
        if self.arguments['examples']:
            if self.arguments['examples'] == 'all':
                examplesIndexes = range()
            else:
                examplesIndexes = list((self.arguments['examples'].replace(" ", "").split(",")))
            self.exampleCarousel(examplesIndexes)


if __name__ == "__main__":
    manager = ExampleManager(args)


