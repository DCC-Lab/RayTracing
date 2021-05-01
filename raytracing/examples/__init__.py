import os
import re
import importlib

topDir      = os.path.dirname(os.path.realpath(__file__))
allFiles    = os.listdir(topDir)

for file in allFiles:
    matchObj = re.match(r'^(ex\d+)\.py$', file)
    if matchObj:
        importlib.import_module(".{0}".format(matchObj.group(1)),package="examples")

