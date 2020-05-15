import argparse
from pygments import highlight
import pygments.lexers
import pygments.formatters
import webbrowser
from unittest.mock import patch
from matplotlib import pyplot as plt
from pylatexenc import latexencode
import tempfile
import base64
import re
import os


ap = argparse.ArgumentParser(prog='python -m raytracing')
ap.add_argument("-e", "--examples", required=False, default='', help="Specific example numbers, separated by a comma")
args = vars(ap.parse_args())


class ArgumentsManager:
    def __init__(self, arguments):
        self.arguments = arguments
        self.exampleDirPath = os.path.dirname(os.path.realpath(__file__)) + "\..\examples\\argsExamples"

        self.selectedFileIndex = 0
        self.htmlTemporaryExampleFile = None
        self.HTMLDescription = None
        self.figureObject = None
        self.base64Figure = None
        self.selectedFile = None
        self.HTMLFigure = None

        self.formatter = pygments.formatters.get_formatter_by_name('html',full=True, linenos=True, cssclass="source", style='default')
        self.lexer = pygments.lexers.get_lexer_by_name('python', stripall=True)

        self.parseArguments()

    def exampleCarousel(self, exampleIndexList):
        for i in exampleIndexList:
            self.selectedFileIndex = i
            self.selectedFile = self.exampleDirPath + '\example{}.py'.format(i)
            self.generateExample()
            self.showExample()

    def showExample(self):
        webbrowser.open("file://" + self.htmlTemporaryExampleFile)

    def generateExample(self):
        self.createTemporaryHTML()
        self.generateFigureFromCode()
        self.generateHTMLHighlightedCode()
        self.generateHTMLDescription()
        self.mergeComponentsToHTML()

    def mergeComponentsToHTML(self):
        with open(self.htmlTemporaryExampleFile, 'a+') as f:
            f.write(self.HTMLDescription)
            f.write(self.HTMLFigure)
            f.write(self.HTMLHighlightedCode)
            f.close()

    def createTemporaryHTML(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        path = temp.name + '.html'
        with open(path, 'w') as f:
            f.write(''''<head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"></head>''')

        self.htmlTemporaryExampleFile = path

    def generateFigureFromCode(self):
        self.runExampleCode()
        fig, axes = plt.subplots(figsize=(7, 5))
        self.figureObject.createRayTracePlot(axes=axes)
        with tempfile.TemporaryFile(suffix=".png") as tmpfile:
            plt.savefig(tmpfile, format="png")
            tmpfile.seek(0)
            self.base64Figure = base64.b64encode(tmpfile.read()).decode()
        self.HTMLFigure = ''''<div style="display:inline-block; vertical-align:top"><img class="icon" src="data:image/png;base64,{} "></div>'''.format(
            self.base64Figure)

    def generateHTMLHighlightedCode(self, code=""):
        if not code:
            code = self.getExampleCode()
            code = re.sub("'''(.+?[\s\S]+?)'''\n+", "", code)
        self.HTMLHighlightedCode = highlight(code, self.lexer, self.formatter)

        return self.HTMLHighlightedCode

    def generateHTMLDescription(self):
        code = self.getExampleCode()
        docString = self.getDocstring(code)
        self.HTMLDescription = '''<div class="alert alert-success" role="alert"><h4 class="alert-heading">Example Description</h4><div style="word-wrap: break-word;
   width: 600px;">{}</div></div>'''.format(docString)

    def runExampleCode(self):
        with patch('matplotlib.pyplot.show') as p:
            global path
            exec(open(self.selectedFile).read(), globals())
            self.figureObject = path

    def getExampleCode(self):
        with open(self.selectedFile, 'r') as f:
            codeString = f.read()
            f.close()
        return codeString

    def getDocstring(self, code):
        matches = re.search("'''(.+?[\s\S]+?)'''", code)
        return(matches.group(1))

    def parseArguments(self):
        if self.arguments['examples']:
            if self.arguments['examples'] == 'all':
                examplesIndexes = list(range(20))
            else:
                examplesIndexes = list((self.arguments['examples'].replace(" ", "").split(",")))
            self.exampleCarousel(examplesIndexes)


if __name__ == "__main__":
    manager = ArgumentsManager(args)


