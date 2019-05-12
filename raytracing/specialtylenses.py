from .matrixgroup import *
from .materials import *
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
    length of fb.  The values fa and fb are used to validate the final focal lengths
    and back focal lengths that are obtained from the combination of elements.
    Most manufacturer's specifiy 1% tolerance, so if fa is more than 1% different
    from the final focal length, a warning is raised.

    Nomenclature from Thorlabs:
    https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120 

    With Edmund optics, the sign of the various radii can change depending on
    some of the components (i.e. PN_85_877 for instance)

    """

    def __init__(self,fa, fb, R1, R2, R3, tc1, tc2, te, n1, n2, diameter, mat1=None, mat2=None, wavelengthRef=None, url=None, label=''):
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
        self.url = url

        elements = []
        elements.append(DielectricInterface(n1=1, n2=n1, R=R1, diameter=diameter))
        elements.append(Space(d=tc1,n=n1))
        elements.append(DielectricInterface(n1=n1, n2=n2, R=R2, diameter=diameter))
        elements.append(Space(d=tc2,n=n2))
        elements.append(DielectricInterface(n1=n2, n2=1, R=R3, diameter=diameter))
        super(AchromatDoubletLens, self).__init__(elements=elements, label=label)
        self.apertureDiameter = diameter

        if abs(self.tc1 + self.tc2 - self.L) / self.L > 0.02:
            print("Obtained thickness {0:.4} is not within 2%% of\
                expected {1:.4}".format(self.tc1 + self.tc2, self.L))

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f, f) = self.focalDistances()
        if abs((f-fa)/fa) > 0.01:
            print("Warning {2}: Obtained effective focal length {0:.4} is not within 1% of \
expected {1:.4}".format(f, fa, self.label))
        BFL = self.backFocalLength()
        if abs((BFL-fb)/fb) > 0.01:
            print("Warning {2}: Obtained back focal length {0:.4} is not within 1% of \
expected {1:.4}".format(BFL, fb, self.label))

        h = self.largestDiameter()/2.0
        phi1 = math.asin(h/abs(self.R1))
        corner1 = self.frontVertex + self.R1*(1.0-math.cos(phi1))

        phi3 = math.asin(h/abs(self.R3))
        corner3 = self.backVertex + self.R3*(1.0-math.cos(phi3))
        if abs(((corner3-corner1)/self.te)-1.0) > 0.05:
            print("Warning {2}: obtained thickness {0:.1f} does not match expected \
{1:0.1f}".format(corner3-corner1, self.te,self.label))

    def drawAt(self, z, axes, showLabels=False):
        """ Draw the doublet as two dielectric of different colours.

        An arc would be perfect, but matplotlib does not allow to fill
        an arc, hence we must use a patch and Bezier curve.
        We might as well draw it properly: it is possible to draw a
        quadratic bezier curve that looks like an arc, see:
        https://pomax.github.io/bezierinfo/#circles_cubic

        Because the element can be flipped with flipOrientation()
        we collect information from the list of elements.
        """
        R1 = self.elements[0].R
        tc1 = self.elements[1].L
        R2 = self.elements[2].R
        tc2 = self.elements[3].L
        R3 = self.elements[4].R

        h = self.largestDiameter()/2.0
        v1 = z 
        phi1 = math.asin(h/abs(R1))
        delta1 = R1*(1.0-math.cos(phi1))
        ctl1 = abs((1.0-math.cos(phi1))/math.sin(phi1)*R1)
        corner1 = v1 + delta1

        v2 = v1 + tc1
        phi2 = math.asin(h/abs(R2))
        delta2 = R2*(1.0-math.cos(phi2))
        ctl2 = abs((1.0-math.cos(phi2))/math.sin(phi2)*R2)
        corner2 = v2 + delta2

        v3 = z + tc1 + tc2
        phi3 = math.asin(h/abs(R3))
        delta3 = R3*(1.0-math.cos(phi3))
        ctl3 = abs((1.0-math.cos(phi3))/math.sin(phi3)*R3)
        corner3 = v3 + delta3

        Path = mpath.Path
        p1 = patches.PathPatch(
            Path([(corner1, -h), (v1, -ctl1), (v1, 0), 
                  (v1, 0), (v1, ctl1), (corner1, h),
                  (corner2, h), (v2, ctl2), (v2, 0),
                  (v2, 0), (v2, -ctl2), (corner2, -h), 
                  (corner1, -h)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            color=[0.85, 0.95, 0.95],
            fill=True,
            transform=axes.transData)

        p2 = patches.PathPatch(
            Path([(corner2, -h), (v2, -ctl2), (v2, 0), 
                  (v2, 0), (v2, ctl2), (corner2, h),
                  (corner3, h), (v3, ctl3), (v3, 0),
                  (v3, 0), (v3, -ctl3), (corner3, -h), 
                  (corner2, -h)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO, Path.CURVE3, Path.CURVE3,
                  Path.LINETO]),
            color=[0.80, 0.90, 0.95],
            fill=True,
            transform=axes.transData)

        axes.add_patch(p1)
        axes.add_patch(p2)
        if showLabels:
            self.drawLabels(z,axes)

        self.drawAperture(z, axes)

    def drawAperture(self, z, axes):
        """ Draw the aperture size for this element.
        The lens requires special care because the corners are not
        separated by self.L: the curvature makes the edges shorter.
        We are picky and draw it right.
        """

        if self.apertureDiameter != float('+Inf'):
            R1 = self.elements[0].R
            tc1 = self.elements[1].L
            R2 = self.elements[2].R
            tc2 = self.elements[3].L
            R3 = self.elements[4].R

            h = self.largestDiameter()/2.0
            phi1 = math.asin(h/abs(R1))
            corner1 = z + R1*(1.0-math.cos(phi1))

            phi3 = math.asin(h/abs(R3))
            corner3 = z + tc1 + tc2 + R3*(1.0-math.cos(phi3))

            axes.add_patch(patches.Polygon(
                           [[corner1, h],[corner3, h]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))
            axes.add_patch(patches.Polygon(
                           [[corner1, -h],[corner3, -h]],
                           linewidth=3,
                           closed=False,
                           color='0.7'))

    def pointsOfInterest(self, z):
        """ List of points of interest for this element as a dictionary:
        'z':position
        'label':the label to be used.  Can include LaTeX math code.
        """
        (f1, f2) = self.focusPositions(z)
        return [{'z': f1, 'label': '$F_f$'}, {'z': f2, 'label': '$F_b$'}]


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

        elements = [Aperture(diameter=backAperture,label="backAperture"),
                    Space(d=f),
                    Matrix(1,0,0,1, physicalLength=focusToFocusLength-2*f),
                    Lens(f=f),
                    Space(d=f-workingDistance),
                    Aperture(diameter=self.frontAperture,label="frontAperture"),
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
        super(Objective,self).flipOrientation()
        self.isFlipped = not self.isFlipped

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

