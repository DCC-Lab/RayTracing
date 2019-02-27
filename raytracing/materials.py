""" Everything here comes from the excellent site http://refractiveindex.info.
The link with the Python formulas is in the Data sectin, [Expressions for n]
"""

class BK7:
    """ https://refractiveindex.info/tmp/data/glass/schott/N-BK7.html
    """
    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength

        n=(1+1.03961212/(1-0.00600069867/x**2)+0.231792344/(1-0.0200179144/x**2)+1.01046945/(1-103.560653/x**2))**.5
        return n

class SF5:
    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.52481889/(1-0.011254756/x**2)+0.187085527/(1-0.0588995392/x**2)+1.42729015/(1-129.141675/x**2))**.5
        return n

class SF10:
    """ https://refractiveindex.info/tmp/data/glass/schott/N-SF10.html
    """

    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.62153902/(1-0.0122241457/x**2)+0.256287842/(1-0.0595736775/x**2)+1.64447552/(1-147.468793/x**2))**.5
        return n

class SF11:
    """ https://refractiveindex.info/tmp/data/glass/schott/N-SF11.html
    """
    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.73759695/(1-0.013188707/x**2)+0.313747346/(1-0.0623068142/x**2)+1.89878101/(1-155.23629/x**2))**.5
        return n

class BAF10:
    """ https://refractiveindex.info/tmp/data/glass/schott/N-BAF10.html

    """
    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.5851495/(1-0.00926681282/x**2)+0.143559385/(1-0.0424489805/x**2)+1.08521269/(1-105.613573/x**2))**.5
        return n

class BAK1:
    """

    """
    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+1.12365662/(1-0.00644742752/x**2)+0.309276848/(1-0.0222284402/x**2)+0.881511957/(1-107.297751/x**2))**.5
        return n

class FK51A:

    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+0.971247817/(1-0.00472301995/x**2)+0.216901417/(1-0.0153575612/x**2)+0.904651666/(1-168.68133/x**2))**.5
        return n

class LASF9:
    """ https://refractiveindex.info/tmp/data/glass/schott/N-LASF9.html
    """

    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+2.00029547/(1-0.0121426017/x**2)+0.298926886/(1-0.0538736236/x**2)+1.80691843/(1-156.530829/x**2))**.5
        return n

class FusedSilica:

    @classmethod
    def n(self, wavelength):
        if wavelength > 10 or wavelength < 0.01:
            raise ValueError("Wavelength must be in microns")
        x = wavelength
        n=(1+0.6961663/(1-(0.0684043/x)**2)+0.4079426/(1-(0.1162414/x)**2)+0.8974794/(1-(9.896161/x)**2))**.5
        return n
