import re
from .utils import *

""" Materials and their indices of refraction

Everything here comes from the excellent site http://refractiveindex.info.
The link with the Python formulas is in the Data section, [Expressions for n]

Thorlabs has a list of glasses they use in their achromatic doublets:
https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=6973
Not all glasses are entered here, simply because of the time commitment.

Thorlabs glasses
Substrate "Range"  "Abbe Number"

CaF2    180 nm - 8.0 µm 95.31
UVFS    185 nm - 2.1 µm 67.82
N-BK7   350 nm - 2 µm   64.17
N-K5    350 nm - 2.1 µm 59.48
N-KZFS5 350 nm - 2.1 µm 39.7
N-LAK22 350 nm - 2.1 µm 55.89
N-SK2   350 nm - 2.3 µm 56.65
N-SSK2  350 nm - 2.3 µm 53.27
N-SSK5  350 nm - 2.2 µm 50.88
SF2 350 nm - 2.2 µm 33.85
SF5 350 nm - 2.3 µm 32.21
ZnS 370 nm - 13 µm  19.86
FD10 (SF10) 400 nm - 2.3 µm 28.41
LAFN7   400 nm - 2 µm   34.95
N-BAF10 400 nm - 2.1 µm 47.11
N-BAF4  400 nm - 2.1 µm 43.72
N-BAF52 400 nm - 2.1 µm 46.6
N-BAK4  400 nm - 2.2 µm 43.72
N-BALF4 400 nm - 2.3 µm 53.87
N-F2    400 nm - 2.1 µm 36.36
N-KZFS8 400 nm - 2.2 µm 34.7
N-LAK10 400 nm - 2 µm   50.62
N-SF1   400 nm - 2 µm   29.62
N-SF2   400 nm - 2.3 µm 33.82
N-SF4   400 nm - 2.1 µm 27.38
N-SF5   400 nm - 2.2 µm 32.25
N-SF6HT 400 nm - 2.1 µm 25.36
N-SF8   400 nm - 2.1 µm 31.31
N-SF10  400 nm - 2.3 µm 28.53
N-SSK8  400 nm - 2.1 µm 49.83
SF6HT   400 nm - 2.3 µm 25.43
SF10    400 nm - 2.3 µm 28.41
N-SF11  420 nm - 2.3 µm 25.68
N-SF56  450 nm - 2.2 µm 26.1
N-SF57  450 nm - 2.1 µm 23.78
ZnSe    600 nm - 16 µm  -
Silicon 1.2 µm - 8.0 µm -
Germanium   2.0 - 16 µm -
E-BAF11 -   48.31

"""


class Material:
    @classmethod
    def n(cls, wavelength):
        """ The index of a material is implemented as a classmethod. 
        Return the value for the wavelength in microns."""
        raise TypeError("Use Material subclass, not Material")
    
    @classmethod
    def abbeNumber(cls):
        """ Abbe number of the glass, which is a measure of how dispersive
        the glass is."""
        return None

    @classmethod
    def Vd(cls):
        """ Synonym of Abbe number of the glass. """
        return cls.abbeNumber()

    @classmethod
    def all(cls):
        """ Returns the class names of all materials implemented. """
        materials = []
        for materialClass in cls.__subclasses__():
            matchObj = re.match(r".+\.(\S+)'", "{0}".format(materialClass))
            if matchObj is not None:
                materials.extend(matchObj.groups(1))
        return materials

    def __str__(self):
        """ Print the name of the class as a string """
        className = type(self)
        matchObj = re.match(r".+\.(\S+)'", "{0}".format(className))
        if matchObj is not None:
            return matchObj.groups(1)[0]
        else:
            return "Unknown"

    @classmethod
    def findByName(self, name):
        """ Identify the material and match it with a class used in Raytracing.
        This can fail if we do not have that material in the materials.py. """
        if name is None:
            return Air()

        simplifiedName = name.replace('-','')
        for className in Material.all():
            shortName = className.replace('_','')
            if areTheSame(simplifiedName, shortName):
                cls = globals()[className]
                return cls()

        raise ValueError("The requested material '{0}' is not recognized \
in the list of materials of raytracing: {1}.  You need to implement it as a \
subclass of Material, see materials.py for examples.".format(name, Material.all()))

    @classmethod
    def findByIndex(cls, n, wavelength, tolerance=0.05):
        """ Identify the material based on a index value and a tolerance."""
        match = []
        for materialName in cls.all():
            mat = globals()[materialName]()
            nmat = mat.n(wavelength)
            if abs(n-nmat) < tolerance:
                match.append((materialName, nmat, mat.abbeNumber()))
        return match

class Air(Material):
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        return 1.0

    @classmethod
    def abbeNumber(cls):
        return 0.0

class N_BK7(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-BK7.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength

        n=(1+1.03961212/(1-0.00600069867/x**2)+0.231792344/(1-0.0200179144/x**2)+1.01046945/(1-103.560653/x**2))**.5
        return n
    
    @classmethod
    def abbeNumber(cls):
        return 64.17


class N_SF2(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF2.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.47343127/(1-0.0109019098/x**2)+0.163681849/(1-0.0585683687/x**2)+1.36920899/(1-127.404933/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 33.82

class N_SF8(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF8.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.55075812/(1-0.0114338344/x**2)+0.209816918/(1-0.0582725652/x**2)+1.46205491/(1-133.24165/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 31.31


class SF2(Material):
    """  All data from https://refractiveindex.info/tmp/data/glass/schott/SF2.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.40301821/(1-0.0105795466/x**2)+0.231767504/(1-0.0493226978/x**2)+0.939056586/(1-112.405955/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 33.85


class SF5(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/SF5.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.46141885/(1-0.0111826126/x**2)+0.247713019/(1-0.0508594669/x**2)+0.949995832/(1-112.041888/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 32.21


class N_SF5(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF5.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.52481889/(1-0.011254756/x**2)+0.187085527/(1-0.0588995392/x**2)+1.42729015/(1-129.141675/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 32.25

class N_SF6(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF6HT.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.55912923/(1-0.0121481001/x**2)+0.284246288/(1-0.0534549042/x**2)+0.968842926/(1-112.174809/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 29.51


class N_SF6HT(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF6HT.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.77931763/(1-0.0133714182/x**2)+0.338149866/(1-0.0617533621/x**2)+2.08734474/(1-174.01759/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 25.36

class N_SF10(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF10.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.62153902/(1-0.0122241457/x**2)+0.256287842/(1-0.0595736775/x**2)+1.64447552/(1-147.468793/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 28.53

class N_SF11(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF11.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.73759695/(1-0.013188707/x**2)+0.313747346/(1-0.0623068142/x**2)+1.89878101/(1-155.23629/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 25.68

class N_SF57(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SF57.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.87543831/(1-0.0141749518/x**2)+0.37375749/(1-0.0640509927/x**2)+2.30001797/(1-177.389795/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 23.78

class N_BAF10(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-BAF10.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.5851495/(1-0.00926681282/x**2)+0.143559385/(1-0.0424489805/x**2)+1.08521269/(1-105.613573/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 47.11

class E_BAF11(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/hikari/E-BAF11.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(2.71954649-0.0100472501*x**2+0.0200301385*x**-2+0.000465868302*x**-4-7.51633336e-06*x**-6+1.77544989e-06*x**-8)**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 46.48

class N_BAK1(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-BAK1.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.12365662/(1-0.00644742752/x**2)+0.309276848/(1-0.0222284402/x**2)+0.881511957/(1-107.297751/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 57.55

class N_BAK4(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-BAK4.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.28834642/(1-0.00779980626/x**2)+0.132817724/(1-0.0315631177/x**2)+0.945395373/(1-105.965875/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 55.97

class FK51A(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-FK51A.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+0.971247817/(1-0.00472301995/x**2)+0.216901417/(1-0.0153575612/x**2)+0.904651666/(1-168.68133/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 84.47


class LAFN7(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/LAFN7.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.66842615/(1-0.0103159999/x**2)+0.298512803/(1-0.0469216348/x**2)+1.0774376/(1-82.5078509/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 34.95

class N_LASF9(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-LASF9.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+2.00029547/(1-0.0121426017/x**2)+0.298926886/(1-0.0538736236/x**2)+1.80691843/(1-156.530829/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 32.17

class N_LAK22(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-LAK22.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.14229781/(1-0.00585778594/x**2)+0.535138441/(1-0.0198546147/x**2)+1.04088385/(1-100.834017/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 55.89


class N_SSK5(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-SSK5.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.59222659/(1-0.00920284626/x**2)+0.103520774/(1-0.0423530072/x**2)+1.05174016/(1-106.927374/x**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 50.88

class E_FD10(Material):
    """ All data from https://refractiveindex.info/tmp/data/glass/hoya/E-FD10.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(2.881518-0.013228312*x**2+0.03145559*x**-2+0.0026851666*x**-4-0.00022577544*x**-6+2.4693268e-05*x**-8)**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 28.32

class FusedSilica(Material):
    """ All data from https://refractiveindex.info/tmp/data/main/SiO2/Malitson.html """
    @classmethod
    def n(cls, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+0.6961663/(1-(0.0684043/x)**2)+0.4079426/(1-(0.1162414/x)**2)+0.8974794/(1-(9.896161/x)**2))**.5
        return n

    @classmethod
    def abbeNumber(cls):
        return 67.82
