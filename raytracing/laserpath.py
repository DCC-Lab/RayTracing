from .matrixgroup import MatrixGroup
from .figure import Figure


class LaserPath(MatrixGroup):
    """The main class of the module for coherent
    laser beams: it is the combination of Matrix() or MatrixGroup()
    to be used as a laser path with a laser beam (GaussianBeam)
    at the entrance.

    Usage is to create the LaserPath(), then append() elements
    and display(). You may change the inputBeam to any GaussianBeam(),
    or provide one to display(beam=GaussianBeam())

    Parameters
    ----------
    elements : list of elements
        A list of ABCD matrices in the imaging path
    label : string
        the label for the imaging path (Optional)

    Attributes
    ----------
    inputBeam : object of GaussianBeam class
        the input beam of the imaging path is defined using this parameter.
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
    Gaussian laser beams are not "blocked" by aperture. The formalism
    does not explicitly allow that.  However, if it appears that a 
    GaussianBeam() would be clipped by  finite aperture, a property 
    is set to indicate it, but it will propagate nevertheless
    and without diffraction due to that aperture.
    """

    def __init__(self, elements=None, label=""):
        self.inputBeam = None
        self.showElementLabels = True
        self.showPointsOfInterest = True
        self.showPointsOfInterestLabels = True
        self.showPlanesAcrossPointsOfInterest = True

        self.figure = Figure(opticalPath=self)
        self.design = self.figure.design
        super(LaserPath, self).__init__(elements=elements, label=label)

    def display(self, beams=None, comments=None):  # pragma: no cover
        """ Display the optical system and trace the laser beam. 
        If comments are included they will be displayed on a
        graph in the bottom half of the plot.

        Parameters
        ----------
        inputBeam : object of GaussianBeam class
        inputBeams : list of object of GaussianBeam class
            A list of Gaussian beams
        comments : string
            If comments are included they will be displayed on a graph in the bottom half of the plot. (default=None)

        """
        if beams is None:
            beams = [self.inputBeam]

        self.figure.displayGaussianBeam(beams=beams,
                                        comments=comments, title=self.label, backend='matplotlib', display3D=False)
