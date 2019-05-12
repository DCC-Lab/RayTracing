from .matrix import *
from .ray import *

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.transforms as transforms

class MatrixGroup(Matrix):
    """MatrixGroup: A group of Matrix(), allowing
    the combination of several elements to be treated as a 
    whole, or treated explicitly as a sequence when needed.
    """

    def __init__(self, elements=[], label=""):
        super(MatrixGroup, self).__init__(1,0,0,1,label=label)
        self.elements = []

        for element in elements:
            self.append(element)

    def append(self, matrix):
        """ Add an element at the end of the path """
        self.elements.append(matrix)
        transferMatrix = self.transferMatrix()
        self.A = transferMatrix.A
        self.B = transferMatrix.B
        self.C = transferMatrix.C
        self.D = transferMatrix.D
        self.L = transferMatrix.L
        self.frontVertex = transferMatrix.frontVertex
        self.backVertex = transferMatrix.backVertex

    def ImagingPath(self):
        return ImagingPath(elements=self.elements, label=self.label)

    def LaserPath(self):
        return LaserPath(elements=self.elements, label=self.label)

    def transferMatrix(self, upTo=float('+Inf')):
        """ The transfer matrix between front edge and distance=upTo

        If "upTo" falls inside an element of finite length, then 
        it will request from that element a "partial" transfer matrix
        for a fraction of the length.  It is up to the Matrix() or 
        MatrixGroup() to define such partial transfer matrix when possible.
        Quite simply, Space() defines a partial matrix as Space(d=upTo).
        """
        transferMatrix = Matrix(A=1, B=0, C=0, D=1)
        distance = upTo
        for element in self.elements:
            if element.L <= distance:
                transferMatrix = element * transferMatrix
                distance -= element.L
            else:
                transferMatrix = element.transferMatrix(upTo=distance) * transferMatrix
                break

        return transferMatrix

    def transferMatrices(self):
        """ The list of Matrix() that corresponds to the propagation through 
        this element (or group). For a Matrix(), it simply returns a list 
        with a single element [self].
        For a MatrixGroup(), it returns the transferMatrices for 
        each individual element and appends them to a list for this group."""

        transferMatrices = []
        for element in self.elements:
            elementTransferMatrices = element.transferMatrices()
            transferMatrices.extend(elementTransferMatrices)
        return transferMatrices

    def trace(self, inputRay):
        """Trace the input ray from first element until after the last element

        Returns a ray trace (i.e. [Ray()]) starting with inputRay, followed by the ray after
        each element. If an element is composed of sub-elements, the ray will also be
        traced in several steps.
        """
        ray = inputRay
        rayTrace = [ray]
        for element in self.elements:
            rayTraceInElement = element.trace(ray)
            rayTrace.extend(rayTraceInElement)
            ray = rayTraceInElement[-1]  # last

        return rayTrace

    def hasFiniteApertureDiameter(self):
        """ True if ImagingPath has at least one element of finite diameter """
        for element in self.elements:
            if element.hasFiniteApertureDiameter():
                return True
        return False

    def largestDiameter(self):
        """ Largest finite diameter in all elements """

        maxDiameter = 0.0
        if self.hasFiniteApertureDiameter():
            for element in self.elements:
                diameter = element.largestDiameter()
                if diameter != float('+Inf') and diameter > maxDiameter:
                    maxDiameter = diameter
        else:
            maxDiameter = self.elements[0].displayHalfHeight() * 2

        return maxDiameter

    def flipOrientation(self):
        """ Flip the orientation (forward-backward) of this group of elements.
        Each element is also flipped individually. """

        allElements = self.elements
        allElements.reverse()
        self.elements = []

        for element in allElements:
            element.flipOrientation()
            self.append(element)

        return self

    def drawAt(self, z, axes, showLabels=True):
        """ Draw each element of this group """
        for element in self.elements:
            element.drawAt(z, axes)
            element.drawAperture(z, axes)

            if showLabels:
                element.drawLabels(z, axes)
            z += element.L

    def drawPointsOfInterest(self, z, axes):
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.

        AS and FS are drawn at 110% of the largest diameter
        """
        labels = {}  # Gather labels at same z

        zElement = 0
        # For the group as a whole, then each element
        for pointOfInterest in self.pointsOfInterest(z=zElement):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label


        # Points of interest for each element
        for element in self.elements:
            pointsOfInterest = element.pointsOfInterest(zElement)

            for pointOfInterest in pointsOfInterest:
                zStr = "{0:3.3f}".format(pointOfInterest['z'])
                label = pointOfInterest['label']
                if zStr in labels:
                    labels[zStr] = labels[zStr] + ", " + label
                else:
                    labels[zStr] = label
            zElement += element.L

        halfHeight = self.largestDiameter()/2
        for zStr, label in labels.items():
            z = float(zStr)
            axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                         xycoords='data', fontsize=12,
                         ha='center', va='bottom')
