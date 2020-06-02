import math
import cmath

class GaussianBeam(object):
    """A gaussian laser beam using the ABCD formalism for propagation of complex radius of curvature q.

    Parameters
    ----------
    q : complex
        The complex beam parameter (default=None)
    w : float
        The 1/e beam size in electric field extracted from q. (default=None)
    R : float
        The radius of curvature (positive means diverging) extracted from q. (default=+Inf)
    n : float
        The index of refraction in which the beam is. (default=1.0)
    wavelength : float
        The wave length of the laser beam. This parameter is necessary to compute the beam size (default=632.8e-6)
    z : float
        The axial distance from the waist (default=0)

    Attributes
    ----------
    isClipped : bool
        #fixme: If True, what have happened? (default=False)

    Notes
    -----
    wavelength and z must be in the same units.
    """

    def __init__(self, q:complex=None, w:float=None, R:float=float("+Inf"), n:float=1.0, wavelength=632.8e-6, z=0):
        # Gaussian beam matrix formalism
        if q is not None:
            self.q = q
        elif w is not None:
            self.q = 1/( 1.0/R - complex(0,1)*wavelength/n/(math.pi*w*w))
        else:
            self.q = None 

        self.wavelength = wavelength
        
        # We track the position for tracing purposes 
        self.z = z
        self.n = n
        self.isClipped = False

    @property
    def R(self):
        """
        The radius of curvature (positive means diverging) extracted from q.
        """
        invQReal = (1/self.q).real
        if invQReal == 0:
            return float("+Inf")

        return 1/invQReal

    @property
    def isFinite(self):
        """
        #fixme : If True, what would be finite?
        """
        return (-1/self.q).imag > 0
    
    @property
    def w(self):
        """
        The 1/e beam size in electric field extracted from q.
        """
        qInv = (-1/self.q).imag
        if qInv > 0:
            return math.sqrt( self.wavelength/self.n/(math.pi * qInv))
        else:
            return float("+Inf")            

    @property
    def wo(self):
        """
        The 1/e beam size in electric field extracted from q at the waist of the beam.
        """
        if self.zo > 0:
            return math.sqrt( self.zo * self.wavelength/math.pi )
        else:
            return None

    @property
    def waist(self):
        """
        The same as the wo.
        """
        return self.wo

    @property
    def waistPosition(self):
        """The position of the waist of the beam."""
        return -self.q.real

    @property
    def zo(self):
        """
        The same as rayleighRange.
        """
        return float(self.q.imag)

    @property
    def confocalParameter(self):
        """
        The same as rayleighRange.
        """
        return self.zo

    @property
    def rayleighRange(self):
        """
        Returns the rayleigh range of the beam.
        """
        return self.zo

    def __str__(self):
        """ String description that allows the use of print(Ray()) """
        if self.wo is not None:
            description = "Complex radius: {0:.3}\n".format(self.q)
            description += "w(z): {0:.3f}, ".format(self.w)
            description += "R(z): {0:.3f}, ".format(self.R)
            description += "z: {0:.3f}, ".format(self.z)
            description += "λ: {0:.1f} nm\n".format(self.wavelength*1e6)
            description += "zo: {0:.3f}, ".format(self.zo)
            description += "wo: {0:.3f}, ".format(self.wo)
            description += "wo position: {0:.3f} ".format(self.waistPosition)
            return description
        else:
            return "Not valid complex radius of curvature"
