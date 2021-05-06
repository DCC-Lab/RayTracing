import os
import re
import importlib

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, BmpImageFormatter

from PIL import Image
from io import BytesIO

""" This module is only here to support examples, so it dynamically
loads all files that appear to be example files from the directory.
We get the title, the description and the entry function.

TODO: all other examples from the article are in the diretory
but are not added to the list because they have a structure
that is different (no TITLE and now constrined to a single function).
"""
topDir      = os.path.dirname(os.path.realpath(__file__))
allFiles    = os.listdir(topDir)
allFiles.sort()

all = []
for file in allFiles:
    matchObj = re.match(r'^(ex\d+)\.py$', file)
    if matchObj:
        name = matchObj.group(1)
        module = importlib.import_module(".{0}".format(name),package="raytracing.examples")
        with open("{0}/{1}".format(topDir, file)) as f:
            srcCode = f.readlines()
        # The last three lines are always the main() call
        srcCode = srcCode[:-3]
        srcCode = str.join('', srcCode)
        module.__SRC_CODE = srcCode

        bmpSrcCode = highlight(srcCode, PythonLexer(), BmpImageFormatter())
        module.__IMG_CODE = Image.open(BytesIO(bmpSrcCode))

        all.append({"name":name, 
                     "title":module.TITLE,
                     "code":module.exempleCode,
                     "sourceCode":srcCode,
                     "terminalSourceCode":highlight(srcCode, PythonLexer(), TerminalFormatter()),
                     "bmpSourceCode":Image.open(BytesIO(bmpSrcCode))
                     })