from .abcd import *
from math import  *
import matplotlib.transforms as transforms

class Objective(MatrixGroup):
    def __init__(self, f, NA, focusToFocusLength, backAperture, workingDistance, label=''):
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

        elements = [Aperture(diameter=backAperture),
                    Space(d=f),
                    Matrix(1,0,0,1, physicalLength=focusToFocusLength-2*f),
                    Lens(f=f),
                    Space(d=f-workingDistance),
                    Aperture(diameter=self.frontAperture),
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
            z += L


class LUMPLFL40X(Objective):
    """ Olympus 40x immersion objective

    Immersion not considered at this point.
    """

    def __init__(self):
        super(LUMPLFL40X, self).__init__(f=180/40,
                                         NA=0.8,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=2,
                                         label='LUMPLFL40X')

class XLUMPlanFLN20X(Objective):
    """ Olympus XLUMPlanFLN20X (Super 20X) 1.0 NA with large 
    back aperture.

    Immersion not considered at this point.
    """
    def __init__(self):
        super(XLUMPlanFLN20X, self).__init__(f=180/20,
                                         NA=1.0,
                                         focusToFocusLength=80,
                                         backAperture=22,
                                         workingDistance=2,
                                         label='XLUMPlanFLN20X')
