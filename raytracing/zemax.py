from raytracing import *
import re

class ZMXReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []
        with open(self.filepath,"r") as reader:     
            while True:
                line = reader.readline()
                if len(line) == 0 or line is None:
                    break
                else:
                    fields = re.split(r"\s+", line.strip())                    
                    self.lines.append({"NAME":fields[0], "PARAM":fields[1:]})

    def surfaces(self):
        surfaces = []
        for i in range(1000):
            surface = self.surfaceInfo(i)
            if surface is not None:
                surfaces.append(surface)
            else:
                break

        return surfaces

    def surfaceInfo(self, index):
        startMarkerFound = False

        surface = {}

        for line in self.lines:
            if line["NAME"] == "SURF":
                if not startMarkerFound:
                    if index == int(line["PARAM"][0]):
                        startMarkerFound = True
                        surface["SURF"] = int(index)
                        continue 
                else:
                    break
            if startMarkerFound:
                key = line["NAME"]
                value = line["PARAM"]
                surface[key] = value

        if not startMarkerFound:
            return None

        return surface
