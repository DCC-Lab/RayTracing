import math
import cmath

class GaussianBeam(object):
    """A gaussian laser beam using the ABCD formalism for propagation of complex radius of curvature q.

    w is the 1/e beam size in electric field extracted from q
    R is the radius of curvature (positive means diverging) extracted from q
    n is index in which the beam is. Necessary to compute beam size.
    wavelength must be in the same units as z.
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
        invQReal = (1/self.q).real
        if invQReal == 0:
            return float("+Inf")

        return 1/invQReal

    @property
    def isFinite(self):
        return (-1/self.q).imag > 0
    
    @property
    def w(self):
        qInv = (-1/self.q).imag
        if qInv > 0:
            return math.sqrt( self.wavelength/self.n/(math.pi * qInv))
        else:
            return float("+Inf")            

    @property
    def wo(self):
        if self.zo > 0:
            return math.sqrt( self.zo * self.wavelength/math.pi )
        else:
            return None

    @property
    def waist(self):
        return self.wo

    @property
    def waistPosition(self):
        return -self.q.real

    @property
    def zo(self):
        return float(self.q.imag)

    @property
    def confocalParameter(self):
        return self.zo

    @property
    def rayleighRange(self):
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
