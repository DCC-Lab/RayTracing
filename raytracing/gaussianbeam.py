import math
import cmath
from .utils import *


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
        The formalism of gaussian beams does not consider any apertures: the beam
        remains gaussian no matter what.  This variable will indicate if the beam
        diameter was too close to the apertures in the system.

    Notes
    -----
    wavelength and z must be in the same units.
    """

    def __init__(self, q: complex = None, w: float = None, R: float = float("+Inf"), n: float = 1.0,
                 wavelength=632.8e-6, z=0):
        # Gaussian beam matrix formalism
        relTol = 0.5 / 100
        if q is not None:
            self.q = q
        if w is not None:
            self.q = 1 / (1.0 / R - complex(0, 1) * wavelength / n / (math.pi * w * w))
        if q is None and w is None:
            raise ValueError("Please specify 'q' or 'w'.")

        if q is not None and w is not None:
            if areRelativelyNotEqual(self.q, q, relTol):
                msg = f"Mismatch between the given q '{q}' and the computed q '{self.q}' ({relTol * 100}% tolerance)."
                raise ValueError(msg)

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
        if self.q == 0:
            return float("+inf")

        invQReal = (1 / self.q).real
        if invQReal == 0:
            return float("+Inf")

        return 1 / invQReal

    @property
    def isFinite(self):
        """
        Using the complex radius, the imaginary part of -1/q is the beam size.
        If this value is negative, the calculation will yield a exp(x**2/w**2)
        which grows exponentially instead of being a gaussian.  Hence, this
        is not a finite and reasonable complex radius.  This is used for
        resonator and cavity calculations to discard unphysical solutions.
        """
        if self.q == 0:
            return False

        return (-1 / self.q).imag > 0

    @property
    def w(self):
        """
        The 1/e beam size in electric field extracted from q.
        """
        if not self.isFinite:
            return float("+Inf")

        qInv = (-1 / self.q).imag
        return math.sqrt(self.wavelength / self.n / (math.pi * qInv))

    @property
    def wo(self):
        """
        The 1/e beam size in electric field extracted from q at the waist of the beam.
        """
        if self.zo > 0:
            return math.sqrt(self.zo * self.wavelength / math.pi)
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
            description += "λ: {0:.1f} nm\n".format(self.wavelength)
            description += "zo: {0:.3f}, ".format(self.zo)
            description += "wo: {0:.3f}, ".format(self.wo)
            description += "wo position: {0:.3f} ".format(self.waistPosition)
            return description
        else:
            return "Beam is not finite: q={0}".format(self.q)
