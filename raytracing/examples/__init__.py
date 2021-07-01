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
that is different (no TITLE and not constrined to a single function).
"""
topDir      = os.path.dirname(os.path.realpath(__file__))
allFiles    = os.listdir(topDir)
allFiles.sort()

short = []
long = []
for file in allFiles:
    pattern = r'^(ex\d+|fig.+)\.py$'
    matchObj = re.match(pattern, file)
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

        short.append({"name":name, 
                     "title":module.TITLE,
                     "code":module.exampleCode,
                     "sourceCode":srcCode,
                     "terminalSourceCode":highlight(srcCode, PythonLexer(), TerminalFormatter()),
                     "bmpSourceCode":Image.open(BytesIO(bmpSrcCode)),
                     "path":"{0}/{1}".format(topDir, file)
                     })
    else:
        matchObj = re.match(r'^(.+)\.py$', file)
        if matchObj:
            # Other more complete examples:
            name = matchObj.group(1)
            if name in ["__init__","template", "envexamples"]:
                continue

            with open("{0}/{1}".format(topDir, file)) as f:
                srcCode = f.readlines()

            srcCode = str.join('', srcCode)
            bmpSrcCode = highlight(srcCode, PythonLexer(), BmpImageFormatter())

            long.append({"name":name, 
                         "sourceCode":srcCode,
                         "terminalSourceCode":highlight(srcCode, PythonLexer(), TerminalFormatter()),
                         "bmpSourceCode":Image.open(BytesIO(bmpSrcCode)),
                         "path":"{0}/{1}".format(topDir, file)
                         })
