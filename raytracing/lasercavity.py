from .matrixgroup import *
from .imagingpath import *
from .laserpath import *

class LaserCavity(LaserPath):
    """A laser cavity (i.e. a resonator).  The beam is considered to go 
    through all elements from first to last, then again through the first element.


    Usage is to create the LaserCavity(), then append() elements
    and display(). You need to include the elements twice: forward then backward
    propagation.  

    Parameters
    ----------
    elements : list of elements
        A list of ABCD matrices in the imaging path
    label : string
        the label for the imaging path (Optional)

    Attributes
    ----------
    showElementLabels : bool
        If True, the labels of the elements will be shown on display. (default=True)
    showPointsOfInterest : bool
        If True, the points of interest will be shown on display. (default=True)
    showPointsOfInterestLabels : bool
        If True, the labels of the points of interest will be shown on display. (default=True)
    showPlanesAcrossPointsOfInterest : bool
        If True, the planes across the points of interest will be shown on display. (default=True)

    See Also
    --------
    raytracing.GaussianBeam

    Notes
    -----

    """

    def __init__(self, elements=None, label=""):
        super(LaserCavity, self).__init__(elements=elements, label=label)

    def eigenModes(self):
        """
        Returns the two complex radii that are identical after a
        round trip, assuming the matrix of the LaserCavity() is one
        round trip: you will need to duplicate elements in reverse
        and append them manually.

        Knowing that q = (Aq + B)/(Cq + d), we get
        Cq^2 + Dq = Aq + B, therefore:
        Cq^2 + (D-A)q - B = 0

        and q = - ((D-A) +- sqrt( (D-A)^2 - 4 C (-B)))/(2C)

        You will typically obtain two values, where only one is physical.
        There could be two modes in a laser with complex matrices (i.e.
        with gain), but this is not considered here.  See "Lasers" by Siegman.
        """
        if not self.hasPower:
            return None, None
        b = self.D - self.A
        sqrtDelta = cmath.sqrt(b * b - 4.0 * self.C * (-self.B))

        q1 = (- b + sqrtDelta) / (2.0 * self.C)
        q2 = (- b - sqrtDelta) / (2.0 * self.C)
        return (GaussianBeam(q=q1), GaussianBeam(q=q2))

    def laserModes(self):
        """
        Returns the laser modes that are physical (finite) when 
        calculating the eigenmodes. 
        """

        (q1, q2) = self.eigenModes()
        q = []
        if q1 is not None and q1.isFinite:
            q.append(q1)

        if q2 is not None and q2.isFinite:
            q.append(q2)

        return q

    def display(self, comments=None):  # pragma: no cover
        """ Display the optical cavity and trace the laser beam. 
        If comments are included they will be displayed on a
        graph in the bottom half of the plot.

        Parameters
        ----------
        comments : string
            If comments are included they will be displayed on a 
            graph in the bottom half of the plot. (default=None)

        """
        beams = self.laserModes()
        if len(beams) == 0:
            print("Cavity is not stable")

        super(LaserCavity, self).display(beams=beams)
