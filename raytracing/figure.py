import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Figure:
    def __init__(self, opticPath, comments=None, title=None):
        self.path = opticPath
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)

        self.createFigure(comments=comments, title=title)

    def createFigure(self, comments=None, title=None):
        if comments is not None:
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def initializeDisplay(self, limitObjectToFieldOfView=False,
                          onlyChiefAndMarginalRays=False):
        """ *Renamed and refactored version of createRayTracePlot*
        Configure the imaging path and the figure according to the display conditions.

            Three optional parameters:
            limitObjectToFieldOfView=False, to use the calculated field of view
            instead of the objectHeight
            onlyChiefAndMarginalRays=False, to only show principal rays
            removeBlockedRaysCompletely=False to remove rays that are blocked.
         """

        note1 = ""
        note2 = ""
        if limitObjectToFieldOfView:
            fieldOfView = self.path.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.path.objectHeight = fieldOfView
                note1 = "FOV: {0:.2f}".format(self.path.objectHeight)
            else:
                raise ValueError(
                    "Infinite field of view: cannot use\
                    limitObjectToFieldOfView=True.")

            imageSize = self.path.imageSize()
            if imageSize != float('+Inf'):
                note1 += " Image size: {0:.2f}".format(imageSize)
            else:
                raise ValueError(
                    "Infinite image size: cannot use\
                    limitObjectToFieldOfView=True.")

        else:
            note1 = "Object height: {0:.2f}".format(self.path.objectHeight)

        if onlyChiefAndMarginalRays:
            (stopPosition, stopDiameter) = self.path.apertureStop()
            if stopPosition is None:
                raise ValueError(
                    "No aperture stop in system: cannot use\
                    onlyChiefAndMarginalRays=True since they\
                    are not defined.")
            note2 = "Only chief and marginal rays shown"

        self.addFigureInfo(text=note1 + "\n" + note2)

    def addFigureInfo(self, text):
        """Text note in the bottom left of the figure. This note is fixed and cannot be moved."""
        # fixme: might be better to put it out of the axes since it only shows object height and display conditions
        self.axes.text(0.05, 0.15, text, transform=self.axes.transAxes,
                       fontsize=12, verticalalignment='top', clip_box=self.axes.bbox, clip_on=True)

    def display(self, limitObjectToFieldOfView=False, onlyChiefAndMarginalRays=False,
                removeBlockedRaysCompletely=False, filepath=None):
        """ Display the optical system and trace the rays.

        Parameters
        ----------
        limitObjectToFieldOfView : bool (Optional)
            If True, the object will be limited to the field of view and
            the calculated field of view will be used instead of the objectHeight(default=False)
        onlyChiefAndMarginalRays : bool (Optional)
            If True, only the principal rays will appear on the plot (default=False)
        removeBlockedRaysCompletely : bool (Optional)
            If True, the blocked rays are removed (default=False)

        """
        self.initializeDisplay(limitObjectToFieldOfView=limitObjectToFieldOfView,
                               onlyChiefAndMarginalRays=onlyChiefAndMarginalRays)

        self.drawLines(self.path.rayTraceLines(onlyChiefAndMarginalRays=onlyChiefAndMarginalRays,
                                               removeBlockedRaysCompletely=removeBlockedRaysCompletely))

        self.drawDisplayObjects()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        self.axes.set_ylim([-self.displayRange() / 2 * 1.5, self.displayRange() / 2 * 1.5])

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def displayRange(self):
        """ We return the largest object in the ImagingPath for display purposes.
        The object is considered only "half" because it starts on axis and goes up.

        Returns
        -------
        displayRange : float
            The maximum height of the objects in an imaging path

        Examples
        --------
        In the following example, we have defined three elements in an imaging path:
        An object (height=3), a first lens (height=5) and a second lens (height=7).
        The height of the second lens is returned as the display range.

        >>> from raytracing import *
        >>> path = ImagingPath() # define an imaging path
        >>> # use append() to add elements to the imaging path
        >>> path.objectHeight=3
        >>> path.append(Space(d=10))
        >>> path.append(Lens(f=10,diameter=5,label="f=10"))
        >>> path.append(Space(d=30))
        >>> path.append(Lens(f=20,diameter=7,label="f=20"))
        >>> path.append(Space(d=20))
        >>> print('display range :', path.displayRange())
        display range : 7

        """

        displayRange = self.path.largestDiameter

        if displayRange == float('+Inf') or displayRange <= 2 * self.path._objectHeight:
            displayRange = 2 * self.path._objectHeight

        conjugates = self.path.intermediateConjugates()
        if len(conjugates) != 0:
            for (planePosition, magnification) in conjugates:
                magnification = abs(magnification)
                if displayRange < self.path._objectHeight * magnification:
                    displayRange = self.path._objectHeight * magnification

        return displayRange

    def drawLines(self, lines):
        for line in lines:
            self.axes.add_line(line)

    def axesToDataScale(self):
        """ Display dimensions in data units.
        Used to properly draw elements on the display
        with appropriate data coordinates.

        Returns
        -------
        xScale: float
            The scale of x axes
        yScale : float
            The scale of y axes
        """

        xScale, yScale = self.axes.viewLim.bounds[2:]

        return xScale, yScale

    def _showPlot(self):
        try:
            plt.plot()
            if sys.platform.startswith('win'):
                plt.show()
            else:
                plt.draw()
                while True:
                    if plt.get_fignums():
                        plt.pause(0.001)
                    else:
                        break

        except KeyboardInterrupt:
            plt.close()

