from .abcd import *
from math import  *
import matplotlib.transforms as transforms

"""
General classes for making special lenses: achromat doublet lenses
and objective lenses. Each of these remain an approximation of the
actual optical element: for instance, achromats are approximated
and do not exhibit chromatic aberrations because there is a single
index of refraction (at the design wavelength). Similarly, objectives
are approximated to have the same physical characteristics but do not
exhibit field curvature, aberrations and all.

Each class is the base class for specific manufacturers class:
for instance, thorlabs achromats or edmund optics achromats both 
derive from AchromatDoubletLens(). Olympus objectives derive from
the Objective() class.

"""

class AchromatDoubletLens(MatrixGroup):
    """ 
    General Achromat doublet lens with an effective focal length of fa, back focal
    length of fb

    Nomenclature from Thorlabs:
    https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120 

    """

    def __init__(self,fa, fb, R1, R2, R3, tc1, tc2, n1, n2, diameter, url=None, label=''):
        self.fa = fa
        self.fb = fb
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.tc1 = tc1
        self.tc2 = tc2
        self.url = url

        elements = []
        elements.append(DielectricInterface(n1=1, n2=n1, R=R1, diameter=diameter))
        elements.append(Space(d=tc1))
        elements.append(DielectricInterface(n1=n1, n2=n2, R=R2, diameter=diameter))
        elements.append(Space(d=tc2))
        elements.append(DielectricInterface(n1=n2, n2=1, R=R3, diameter=diameter))
        super(AchromatDoubletLens, self).__init__(elements=elements, label=label)
        self.apertureDiameter = diameter

        if abs(self.tc1 + self.tc2 - self.L) / self.L > 0.02:
            print("Obtained focal distance {0:.4} is not within 1%% of\
                expected {1:.4}".format(f, fa))

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f, f) = self.focalDistances()
        if abs((f-fa)/fa) > 0.01:
            print("Obtained focal distance {0:.4} is not within 1%% of\
                expected {1:.4}".format(f, fa))

    def drawAt(self, z, axes, showLabels=False):
        """ Draw a faint blue box with slightly curved interfaces
        of length 'thickness' starting at 'z'.

        """
        tc1 = self.tc1

        halfHeight = self.largestDiameter()/2.0
        apexHeight = self.L * 0.2
        frontVertex = z + apexHeight * (-self.R1/abs(self.R1))
        middleVertex = z + self.tc1 + tc1/3 * (-self.R2/abs(self.R2))
        backVertex = z + self.L + apexHeight * (-self.R3/abs(self.R3))

        Path = mpath.Path
        p1 = patches.PathPatch(
            Path([(z, -halfHeight), (frontVertex, 0), (z, halfHeight),
                  (z+tc1, halfHeight), (middleVertex, 0),
                  (z+tc1, -halfHeight), (z, -halfHeight)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            facecolor=[0.85, 0.95, 0.95],
            edgecolor = [0.5, 0.5, 0.5],
            fill=True,
            transform=axes.transData)
        p2 = patches.PathPatch(
            Path([(z+tc1, -halfHeight), (middleVertex, 0), (z+tc1, halfHeight),
                  (z+self.L, halfHeight), (backVertex, 0),
                  (z+self.L, -halfHeight), (z, -halfHeight)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            facecolor=[0.80, 0.90, 0.95],
            edgecolor = [0.5, 0.5, 0.5],
            fill=True,
            transform=axes.transData)

        axes.add_patch(p1)
        axes.add_patch(p2)
        if showLabels:
            self.drawLabels(z,axes)

        self.drawAperture(z, axes)

class Objective(MatrixGroup):
    def __init__(self, f, NA, focusToFocusLength, backAperture, workingDistance, url=None, label=''):
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
        self.frontAperture = 1.2 * (2.0 * NA * workingDistance)  # 20% larger
        self.isFlipped = False
        self.url = url

        elements = [Aperture(diameter=backAperture,label="frontVertex"),
                    Space(d=f),
                    Matrix(1,0,0,1, physicalLength=focusToFocusLength-2*f),
                    Lens(f=f),
                    Space(d=f-workingDistance),
                    Aperture(diameter=self.frontAperture,label="backVertex"),
                    Space(d=workingDistance)]

        super(Objective, self).__init__(elements=elements, label=label)
        
        self.frontVertex = 0
        self.backVertex = focusToFocusLength - workingDistance

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:
        'z':position
        'label':the label to be used.  Can include LaTeX math code.
        """
        if self.isFlipped:
            return [{'z': z+self.focusToFocusLength, 'label': '$F_b$'}, {'z': z, 'label': '$F_f$'}]            
        else:
            return [{'z': z, 'label': '$F_b$'}, {'z': z+self.focusToFocusLength, 'label': '$F_f$'}]

    def flipOrientation(self):
        self.isFlipped = not self.isFlipped
        self.elements.reverse()
        z = 0
        for element in self.elements:
            if element.label == "frontVertex":
                self.frontVertex = z
            elif element.label == "backVertex":
                self.backVertex = z
            z = z + element.L

    def drawAt(self, z, axes, showLabels=False):
        L = self.focusToFocusLength
        f = self.f
        wd = self.workingDistance
        halfHeight = self.backAperture/2

        points = [[0, halfHeight],
                  [(L - 5*wd), halfHeight],
                  [(L - wd), self.frontAperture/2],
                  [(L - wd), -self.frontAperture/2],
                  [(L - 5*wd), -halfHeight],
                  [0, -halfHeight]]

        if self.isFlipped:
            trans = transforms.Affine2D().scale(-1).translate(tx=z+L,ty=0) + axes.transData
        else:
            trans = transforms.Affine2D().translate(tx=z,ty=0) + axes.transData

        axes.add_patch(patches.Polygon(
               points,
               linewidth=1, linestyle='--',closed=True,
               color='k', fill=False, transform=trans))

        self.drawCardinalPoints(z, axes)


        for element in self.elements:
            element.drawAperture(z, axes)
            z += element.L

