import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Figure:
    def __init__(self, opticPath, comments=None, title=None):
        self.path = opticPath
        self.figure = None
        self.axes = None  # Where the optical system is
        self.axesComments = None  # Where the comments are (for teaching)

        self.createFigure(comments=comments, title=title)

