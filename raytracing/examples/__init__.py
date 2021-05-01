import os
import re
import importlib

topDir      = os.path.dirname(os.path.realpath(__file__))
allFiles    = os.listdir(topDir)
allFiles.sort()

all = []
for file in allFiles:
    matchObj = re.match(r'^(ex\d+)\.py$', file)
    if matchObj:
        name = matchObj.group(1)
        module = importlib.import_module(".{0}".format(name),package="raytracing.examples")
        all.append({"name":name, 
                     "title":module.TITLE,
                     "description":module.DESCRIPTION,
                     "code":module.exempleCode})
