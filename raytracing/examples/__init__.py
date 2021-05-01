import os
import re
import importlib

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, BmpImageFormatter

import PIL

""" This module is only here to support examples, so it dynamically
loads all files that appear to be example files from the directory.
We get the title, the description and the entry function 
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
        srcCode = ''.join(srcCode)
        module.__SRC_CODE = srcCode
        all.append({"name":name, 
                     "title":module.TITLE,
                     "description":module.DESCRIPTION,
                     "code":module.exempleCode,
                     "sourceCode":srcCode,
                     "terminalSourceCode":highlight(srcCode, PythonLexer(), TerminalFormatter()),
                     "bmpSourceCode":highlight(srcCode, PythonLexer(), BmpImageFormatter())
                     })
