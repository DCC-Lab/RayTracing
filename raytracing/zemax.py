from raytracing import *
import re
from struct import *

class Surface(NamedTuple):
    number:int = 0
    R:float = float("+inf")
    diameter:float = float("+inf")
    mat:Material = None
    spacing:float = 0

def areTheSame(a, b):
    return a.lower() == b.lower()

class ZMXReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = filepath
        self.lines = []

        encoding = self.determineEncoding(filepath)

        with open(self.filepath,"r",encoding=encoding) as reader:     
            while True:
                line = reader.readline()
                if len(line) == 0 or line is None:
                    break
                else:
                    fields = re.split(r"\s+", line.strip())                    
                    self.lines.append({"NAME":fields[0], "PARAM":fields[1:]})

        units = self.value("UNIT")
        self.factor = 1
        if units is None:
            self.factor = 1
        elif areTheSame("IN", units):
            self.factor = 25.4

    def determineEncoding(self, filepath):
        """ The zemax files can be in UTF-16 (e.g., Edmund Optics)
        We try to open it as UTF-16, we will get an error if it cannot.
        """
        with open(self.filepath,"r",encoding='utf-16') as reader:     
            try:
                line = reader.readline()
                return "utf-16"
            except:
                return "utf-8"

    def matrixGroup(self):
        group = MatrixGroup(label=self.name)

        previousSurface = Surface(mat=Air())
        for surface in self.lensSurfaces():
            mat1 = previousSurface.mat
            mat2 = surface.mat
            interface = DielectricInterface(R=surface.R, 
                                n1=mat1.n(0.5876),
                                n2=mat2.n(0.5876),
                                diameter=surface.diameter)
            group.append(interface)

            if not isinstance(mat2, Air):
                spacing = Space(d=surface.spacing, n=mat2.n(0.5876))
                group.append(spacing)

            previousSurface = surface

        return group

    def prescription(self):
        prescription = "\n{0:>10}\t{1:>10}\t{2:>10}\t{3:>10}\n".format("R","Material","d","diameter")
        for surface in self.lensSurfaces():
            prescription += "{0:>10.2f}\t{1:>10}\t{2:>10.2f}\t{3:>10.2f}\n".format(surface.R, str(surface.mat), surface.spacing, surface.diameter)
        return prescription

    def identifyMaterial(self, matname):
        if matname is None:
            return Air()

        matname = matname.replace('-','')
        for className in Material.all():
            shortName = className.replace('_','')
            if areTheSame(matname, shortName):
                cls = globals()[className]
                return cls()
        return None

    def lensSurfaces(self):
        lensSurfaces = []
        firstSurfaceFound = False
        previousSurface = None
        for surface in self.surfaces():
            if not isinstance(surface.mat, Air):
                firstSurfaceFound = True
            
            if isinstance(surface.mat, Air):
                if firstSurfaceFound:
                    lensSurfaces.append(surface)
                    break
                else:
                    continue

            if firstSurfaceFound:
                lensSurfaces.append(surface)
        return lensSurfaces

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
        rawInfo = self.rawSurfaceInfo(index)
        if rawInfo is None:
            return None

        if "GLAS" in rawInfo:
            mat = self.identifyMaterial(rawInfo["GLAS"][0])
        else:
            mat = Air()

        curvature = float(rawInfo["CURV"][0])
        if curvature == 0.0:
            radius = float("+inf")
        else:
            radius = 1/curvature*self.factor
        
        if "DIAM" in rawInfo:
            diameter = 2*float(rawInfo["DIAM"][0])*self.factor
        else:
            diameter = float("+inf")

        spacing = float(rawInfo["DISZ"][0])*self.factor

        return Surface(number=index, 
                       R=radius,
                       mat=mat,
                       spacing=spacing,
                       diameter=diameter)

    def rawSurfaceInfo(self, index):
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

    def value(self, key, index=0):
        for line in self.lines:
            if areTheSame(line["NAME"],key):
                return line["PARAM"][index]
        return None