from raytracing import *
import re
from struct import *

class Surface(NamedTuple):
    """ A Zemax surface-tuple, to somplify management """
    number:int = 0
    R:float = float("+inf")
    diameter:float = float("+inf")
    mat:Material = None
    spacing:float = 0

class ZMXReader:
    """
    Zemax file (ZMX) reader for compound lenses.  The reader is not 
    complete, but it can return a `MatrixGroup` that will behave like a
    compound lens with the spherical interfaces and spacing between
    elements.

    This only works with ZMX files, not ZMF files.  The ZMX files are 
    text-based and the ZMF files are binary without documentation.

    It is not particularly robust: many parameters are currently ignored
    and it could fail for files not from Thorlabs or Edmund (the only
    files tested).
    """
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

        wavelengths = self.designWavelengths()
        self.designWavelength = wavelengths[len(wavelengths)//2]

    def designWavelengths(self):
        """ Obtain the design wavelength(s) from the file.
        Thorlabs appears to leave many useless wavelengths (0.55 µm) so
        we remove them. """

        wavelengths = self.value("WAVM", index=1)
        if isinstance(wavelengths, list):
            while float(wavelengths[-1]) == 0.55:
                wavelengths.pop()
            return [ float(x) for x in wavelengths]
        else:
            return [float(wavelengths)]

    def determineEncoding(self, filepath):
        """ Zemax files can be in UTF-16 (e.g., Edmund Optics)
        We try to open it as UTF-16, we will get an error if it cannot.
        """
        with open(self.filepath,"r",encoding='utf-16') as reader:     
            try:
                line = reader.readline()
                return "utf-16"
            except:
                return "utf-8"

    def matrixGroup(self):
        """ Build and return a raytracing MatrixGroup with the interfaces and
        spacing as prescribed. 

        Returns
        -------
        group : MatrixGroup
            The created group that acts like a lens.
        """

        group = MatrixGroup(label=self.name)

        wavelength = self.designWavelength
        previousSurface = Surface(mat=Air())
        for surface in self.lensSurfaces():
            mat1 = previousSurface.mat
            mat2 = surface.mat
            interface = DielectricInterface(R=surface.R, 
                                n1=mat1.n(wavelength),
                                n2=mat2.n(wavelength),
                                diameter=surface.diameter)
            group.append(interface)

            if not isinstance(mat2, Air):
                spacing = Space(d=surface.spacing, n=mat2.n(wavelength))
                group.append(spacing)

            previousSurface = surface

        return group

    def prescription(self):
        """ A text-based prescription, mostly for information purposes. 

        Returns
        -------
        prescription : multi-line string
            A prescription in text-based form

        """
        prescription = "\n{0:>10}\t{1:>10}\t{2:>10}\t{3:>10}\n".format("R","Material","d","diameter")
        for surface in self.lensSurfaces():
            prescription += "{0:>10.2f}\t{1:>10}\t{2:>10.2f}\t{3:>10.2f}\n".format(surface.R, str(surface.mat), surface.spacing, surface.diameter)
        return prescription

    def lensSurfaces(self):
        """ Make sense of surfaceInfo from the Zemax file to figure
        out what makes up a lens.
        
        This will not be particularly robust: it assumes it is a compound lens
        but that is sufficient for now.

        Returns
        -------
        lensSurfaces : List of Surface elements that make up the lens.
        """
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
        """ List of all surface elements from the Zemax file.

        Returns
        -------

        List of Surfaces
        """
        surfaces = []
        for i in range(1000):
            surface = self.surfaceInfo(i)
            if surface is not None:
                surfaces.append(surface)
            else:
                break

        return surfaces

    def surfaceInfo(self, index):
        """ Make sense of rawSurfaceInfo from the Zemax file to put it together
        into a Surface-namedtuple that makes more sense.
        
        1. We figure out the material and replace it with Raytracing Material subclass.
        2. We convert CURV into a radius.
        3. We use DIAM as the diameter of the element.  For some reason DIAM is half
        the diameter.
        4. The distance to the next interface is read as well. 

        Returns
        -------
        A Surface Named-tuple.

        """
        rawInfo = self.rawSurfaceInfo(index)
        if rawInfo is None:
            return None

        if "GLAS" in rawInfo:
            mat = Material.findByName(name=rawInfo["GLAS"][0])
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
        """ Extract the raw information for surfaces from the file.
        All SURF elements from the file are extracted in order.
        No analysis is performed: making sense of the information
        in the context of a lens is the job of `surfaceInfo`.
        """
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
        """ Convenience function to access the information in the file
        with the Zemax 4-letter parameters.

        If an element has several items, element [index] is 
        returned, defaults to zero.
        """
        values = []
        for line in self.lines:
            if areTheSame(line["NAME"],key):
                values.append(line["PARAM"][index])
        if len(values) == 1:
            return values[0]

        return values