from .matrixgroup import *
from .materials import *
from math import *
import matplotlib.transforms as transforms
from numpy import linspace
import matplotlib.pyplot as plt

""" 
General classes for making special compound lenses: achromat doublet
lenses, singlet lenses, and objective lenses. Each of these remain an
approximation of the actual optical element. Similarly, objectives
are approximated to have the same physical characteristics but do not exhibit
field curvature, aberrations and all: they are treated as black boxes
to reproduce the known characteristics of the objectives.

Each class is the base class for specific manufacturers class:
for instance, thorlabs achromats or edmund optics achromats both 
derive from AchromatDoubletLens(). Olympus objectives derive from
the Objective() class.

"""

class CompoundLens(MatrixGroup):
    def __init__(self, elements, designFocalLength, wavelengthRef=None, url=None, label=''):
        """ A base class for any lens that we make from its individual elements
        """
        super(CompoundLens, self).__init__(elements=elements, label=label)

        self.designFocalLength = designFocalLength
        self.url = url
        self.wavelengthRef = wavelengthRef

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:

        Parameters
        ----------
        z : float
            The position
        """
        (f1, f2) = self.focusPositions(z)
        return [{'z': f1, 'label': '$F_f$'}, {'z': f2, 'label': '$F_b$'}]

    @property
    def forwardSurfaces(self) -> List[Interface]:
        """ Must be overridden by subclasses """

        return None

    def focalShifts(self, wavelengths=None):
        """ The chromatic aberration shifts to the focal distance from the
        design focal length for a range of wavelengths.

        Parameters
        ----------
        wavelengths : list or list like
            Wavelengths in microns defaults to visible
        """

        if self.designFocalLength is None:
            raise("The design focal length of this lens was not set upon creation. Set it with self.designFocalLength=xx.")

        if wavelengths is None:
            wavelengths = linspace(0.4, 0.8, 100)
        
        focalShifts = []
        for l in wavelengths:
            lens = type(self)(wavelength=l)
            f,f = lens.effectiveFocalLengths()
            focalShifts.append(f-self.designFocalLength)
        
        return wavelengths*1000, focalShifts

    def showChromaticAberrations(self, wavelengths=None):
        """ Show the chromatic aberrations focal shifts for this lens
        as obtained from the function focalShifts()
        
        Parameters
        ----------
        wavelengths : list or list like
            Wavelengths in microns defaults to visible

         """
        wavelengths, focalShifts = self.focalShifts(wavelengths=wavelengths)

        plt.plot(wavelengths, focalShifts,'k-')
        plt.xlabel(r"Wavelength [nm]")
        plt.ylabel(r"Focal shift [mm]")
        plt.title(r"Lens: {0}, design f={1} mm at $\lambda$={2:.1f} nm".format(self.label, self.designFocalLength, self.wavelengthRef*1000))
        plt.show()

    @classmethod
    def all(cls):
        return allSubclasses(cls)

class AchromatDoubletLens(CompoundLens):
    """ 
    General Achromat doublet lens with an effective focal length of fa, back focal
    length of fb.  The values fa and fb are used to validate the final focal lengths
    and back focal lengths that are obtained from the combination of elements.
    Most manufacturer's specifiy 1% tolerance, so if fa is more than 1% different
    from the final focal length, a warning is raised.

    Parameters
    ----------
    fa : float
        The effective focal length
    fb : float
        The back focal length
    R1 : float
        The first radius
    R2 : float
        The second radius
    R3 : float
        The third radius
    tc1 : float
        The first center thickness
    tc2 : float
        The second center thickness
    te : float
        The edge thickness
    n1 : float
        The refraction index of the first material
    n2 : float
        The refractive index of the second material
    diameter : float
        The diameter of the lens
    mat1 : object of Matrix class
        The transfer matrix of the first lens
    mat2 : object of Matrix class
        The transfer matrix of the second lens
    wavelengthRef : float
        The defined wavelength
    url : string
        A link to find more info for the lens
    label : string
        The name of the lens

    Notes
    -----
    Nomenclature from Thorlabs:
    https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120 

    With Edmund optics, the sign of the various radii can change depending on
    some of the components (i.e. PN_85_877 for instance)

    """

    def __init__(self, fa, fb, R1, R2, R3, tc1, tc2, te, diameter, n1=None, n2=None, mat1=None, mat2=None, wavelengthRef=None,
                 url=None, label='', wavelength=None):
        self.fa = fa
        self.fb = fb
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.tc1 = tc1
        self.tc2 = tc2
        self.te = te
        self.n1 = n1
        self.n2 = n2
        self.mat1 = mat1
        self.mat2 = mat2

        if self.mat1 is not None and self.mat2 is not None :
            if wavelength is not None:
                self.n1=self.mat1.n(wavelength)
                self.n2=self.mat2.n(wavelength)
            elif wavelengthRef is not None:
                self.n1=self.mat1.n(wavelengthRef)
                self.n2=self.mat2.n(wavelengthRef)

        if self.n1 is None or self.n2 is None:
            raise ValueError("n1 or n2 not set")

        elements = []
        elements.append(DielectricInterface(n1=1, n2=self.n1, R=R1, diameter=diameter))
        elements.append(Space(d=tc1, n=self.n1))
        elements.append(DielectricInterface(n1=self.n1, n2=self.n2, R=R2, diameter=diameter))
        elements.append(Space(d=tc2, n=self.n2))
        elements.append(DielectricInterface(n1=self.n2, n2=1, R=R3, diameter=diameter))
        super(AchromatDoubletLens, self).__init__(elements=elements, 
                                                  designFocalLength=fa, 
                                                  wavelengthRef=wavelengthRef,
                                                  url=url, 
                                                  label=label)
        self.apertureDiameter = diameter

        if abs(self.tc1 + self.tc2 - self.L) / self.L > 0.02:
            msg = "Obtained thickness {0:.4} is not within 2%% of expected {1:.4}".format(self.tc1 + self.tc2, self.L)
            warnings.warn(msg, ExpertNote)

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f, f) = self.focalDistances()
        if abs((f - fa) / fa) > 0.01:
            msg = "Doublet {2}: Obtained effective focal length {0:.4} is not within 1% of " \
                  "expected {1:.4}".format(f, fa, self.label)
            warnings.warn(msg, ExpertNote)
        BFL = self.backFocalLength()
        if abs((BFL - fb) / fb) > 0.01:
            msg = "Doublet {2}: Obtained back focal length {0:.4} is not within 1% of " \
                  "expected {1:.4}".format(BFL, fb, self.label)
            warnings.warn(msg, ExpertNote)

        h = self.largestDiameter / 2.0
        phi1 = math.asin(h / abs(self.R1))
        corner1 = self.frontVertex + self.R1 * (1.0 - math.cos(phi1))

        phi3 = math.asin(h / abs(self.R3))
        corner3 = self.backVertex + self.R3 * (1.0 - math.cos(phi3))
        if abs(((corner3 - corner1) / self.te) - 1.0) > 0.05:
            msg = "Doublet {2}: obtained thickness {0:.1f} does not match expected " \
                  "{1:0.1f}".format(corner3 - corner1, self.te, self.label)
            warnings.warn(msg, ExpertNote)

    @property
    def forwardSurfaces(self) -> List[Interface]:
        return [SphericalInterface(R=self.R1, L=self.tc1, n=self.n1),
                SphericalInterface(R=self.R2, L=self.tc2, n=self.n2),
                SphericalInterface(R=self.R3)]


class SingletLens(CompoundLens):
    """
    General singlet lens with an effective focal length of f, back focal
    length of fb.  The values f and fb are used to validate the final focal lengths
    and back focal lengths that are obtained from the combination of elements.
    Most manufacturer's specifiy 1% tolerance, so if f is more than 1% different
    from the final focal length, a warning is raised.

        Parameters
    ----------
    f : float
        The effective focal length
    fb : float
        The back focal length
    R1 : float
        The first radius
    R2 : float
        The second radius
    tc : float
        The center thickness
    te : float
        The edge thickness
    n : float
        The refraction index of the material if material not used
    diameter : float
        The diameter of the lens
    mat1 : object of Material class
        The material of the lens
    wavelengthRef : float
        The defined wavelength of reference for the index of refraction
    url : string
        A link to find more info for the lens
    label : string
        The name of the lens
    wavelength : float, in micron
        The wavelength used for the calculations.

    Notes
    -----
    Nomenclature from Thorlabs:
    https://www.thorlabs.com/images/TabImages/Plano-Convex_Lens_Schematic.gif

    """

    def __init__(self, f, fb, R1, R2, tc, te, n, diameter, mat=None, wavelengthRef=None,
                 url=None, label='', wavelength=None):

        self.f = f
        self.fb = fb
        self.R1 = R1
        self.R2 = R2
        self.tc = tc
        self.te = te
        self.n = n
        self.mat = mat

        if self.mat is not None:
            if wavelength is not None:
                self.n=self.mat.n(wavelength)
            elif wavelengthRef is not None:
                self.n=self.mat.n(wavelengthRef)

        if self.n is None:
            raise ValueError("You must provide n or material")

        elements = []
        elements.append(DielectricInterface(n1=1, n2=self.n, R=R1, diameter=diameter))
        elements.append(Space(d=tc, n=self.n))
        elements.append(DielectricInterface(n1=self.n, n2=1, R=R2, diameter=diameter))

        super(SingletLens, self).__init__(elements=elements, 
                                          designFocalLength=f, 
                                          wavelengthRef=wavelengthRef,
                                          url=url, 
                                          label=label)
        self.apertureDiameter = diameter

        if abs(self.tc - self.L) / self.L > 0.02:
            msg = "Obtained thickness {0:.4} is not within 2%% of expected {1:.4}".format(self.tc1, self.L)
            warnings.warn(msg, ExpertNote)

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f_f, f_b) = self.focalDistances()
        if abs((f_f - f) / f) > 0.01:
            msg = "Singlet {2}: Obtained effective focal length {0:.4} is not within 1% of " \
                  "expected {1:.4}".format(f_f, fb, self.label)
            warnings.warn(msg, ExpertNote)
        BFL = self.backFocalLength()
        if abs((BFL - fb) / fb) > 0.01:
            msg = "Singlet {2}: Obtained back focal length {0:.4} is not within 1% of " \
                  "expected {1:.4}".format(BFL, fb, self.label)
            warnings.warn(msg, ExpertNote)

        h = self.largestDiameter / 2.0
        phi1 = math.asin(h / abs(self.R1))
        corner1 = self.frontVertex + self.R1 * (1.0 - math.cos(phi1))

        phi2 = math.asin(h / abs(self.R2))
        corner2 = self.backVertex + self.R2 * (1.0 - math.cos(phi2))
        if abs(((corner2 - corner1) / self.te) - 1.0) > 0.05:
            msg = "Singlet {2}: obtained thickness {0:.1f} does not match expected " \
                  "{1:0.1f}".format(corner2 - corner1, self.te, self.label)
            warnings.warn(msg, ExpertNote)

    @property
    def forwardSurfaces(self) -> List[Interface]:
        return [SphericalInterface(R=self.R1, L=self.tc, n=self.n),
                SphericalInterface(R=self.R2)]


class Objective(MatrixGroup):

    """
    Parameters
    ----------
    f : float
        The focal length
    NA : float
        The numerical aperture
    focusToFocusLength : float
        The distance between the front focal point to the back focal point.
    backAperture : float
        The back aperture
    workingDistance : float
        The distance from the front lens element of the objective to the closest surface.
    url : string
        A link to find more info for the lens
    label : string
        The name of the lens

    """

    def __init__(self, f, NA, focusToFocusLength, backAperture, workingDistance, magnification=None, fieldNumber=None, url=None, label=''):
        """ General microscope objective, approximately correct.

        We model the objective as an ideal lens with back focal point at the entrance
        and front focal plane "working distance" after the last surface.
        In between, we propagate from one principal plane to another with the identity
        matrix, with the planes separated by focusToFocusLength-2*f
        All the elements that describe this objective will cumulate to a total distance
        of focusToFocusLength.  However, the physical length of the objective is shorter:
        the focal point is outside the objective, therefore the objective has an actual
        length of focusToFocusLength-workingDistance.
        The numerical aperture is used to estimate the front aperture.
        """

        self.f = f
        self.NA = NA
        self.focusToFocusLength = focusToFocusLength
        self.backAperture = backAperture
        self.workingDistance = workingDistance

        self.magnification = magnification
        self.fieldNumber = fieldNumber

        self.frontAperture = 2 * (self.NA * self.workingDistance)
        self.isFlipped = False
        self.url = url

        elements = [Aperture(diameter=self.backAperture, label="backAperture"),
                    Space(d=self.f),
                    Matrix(1, 0, 0, 1, physicalLength=self.focusToFocusLength - 2 * self.f),
                    Lens(f=self.f),
                    Space(d=self.f - self.workingDistance),
                    Aperture(diameter=self.frontAperture, label="frontAperture"),
                    Space(d=self.workingDistance)]

        super(Objective, self).__init__(elements=elements, label=label)

        self.frontVertex = 0
        self.backVertex = self.focusToFocusLength - self.workingDistance
        self.apertureDiameter = self.backAperture

        msg = "Objective class not fully tested. \
No guarantee that apertures and field of view will exactly \
reproduce the objective."
        warnings.warn(msg, ExpertNote)

    def maximumOpticalInvariant(self):
        if self.magnification is None or self.fieldNumber is None:
            raise AttributeError("Cannot compute the maximum optical invariant without fieldNumber "
                                 "and magnification defined.")
        else:
            return (self.fieldNumber/2)/self.magnification * self.NA

    def flipOrientation(self):
        super(Objective, self).flipOrientation()

        z = 0
        for element in self.elements:
            if element.label == "frontAperture":
                if not self.isFlipped:
                    self.backVertex = z
                else:
                    self.frontVertex = z
            elif element.label == "backAperture":
                if not self.isFlipped:
                    self.frontVertex = z
                else:
                    self.backVertex = z

            z = z + element.L
        return self

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:

        Parameters
        ----------
        z : float
            The position
        """
        if self.isFlipped:
            return [{'z': z + self.focusToFocusLength, 'label': '$F_b$'}, {'z': z, 'label': '$F_f$'}]
        else:
            return [{'z': z, 'label': '$F_b$'}, {'z': z + self.focusToFocusLength, 'label': '$F_f$'}]
