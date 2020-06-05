from .matrix import *

import collections.abc as collections


class MatrixGroup(Matrix):
    """MatrixGroup: A group of Matrix(), allowing
    the combination of several elements to be treated as a
    whole, or treated explicitly as a sequence when needed.
    """

    def __init__(self, elements=None, label=""):
        self.iteration = 0
        super(MatrixGroup, self).__init__(1, 0, 0, 1, label=label)

        self.elements = []

        if elements is not None:
            if not isinstance(elements, collections.Iterable):
                raise TypeError("'elements' must be iterable (i.e. a list or a tuple of Matrix objects).")

            for element in elements:
                self.append(element)

        # Solely for performance reason: it is common to raytrace
        # groups of rays that are similar (to mimick intensities)
        # We keep the last ray and the last ray trace for optimization
        self._lastRayToBeTraced = None
        self._lastRayTrace = None

    def append(self, matrix):
        """ Add an element at the end of the path """
        lastElement = None
        if not isinstance(matrix, Matrix):
            raise TypeError("'matrix' must be a Matrix instance.")

        if len(self.elements) != 0:
            lastElement = self.elements[-1]
            if lastElement.backIndex != matrix.frontIndex:
                if isinstance(matrix, Space):  # For Space(), we fix it
                    msg = "Fixing mismatched indices between last element and appended Space(). Use Space(d=someDistance, n=someIndex)."
                    warnings.warn(msg, UserWarning)
                    matrix.frontIndex = lastElement.backIndex
                    matrix.backIndex = matrix.frontIndex
                else:
                    msg = "Mismatch of indices between last element and appended element"
                    raise ValueError(msg)

        self.elements.append(matrix)
        transferMatrix = self.transferMatrix()
        self.A = transferMatrix.A
        self.B = transferMatrix.B
        self.C = transferMatrix.C
        self.D = transferMatrix.D
        self.L = transferMatrix.L
        self.frontVertex = transferMatrix.frontVertex
        self.backVertex = transferMatrix.backVertex

    def transferMatrix(self, upTo=float('+Inf')):
        """ The transfer matrix between front edge and distance=upTo

        If "upTo" falls inside an element of finite length, then 
        it will request from that element a "partial" transfer matrix
        for a fraction of the length.  It is up to the Matrix() or 
        MatrixGroup() to define such partial transfer matrix when possible.
        Quite simply, Space() defines a partial matrix as Space(d=upTo).

        When using this transfer matrix, any information related to rays
        that have been blocked is lost: apertures are not part of the 
        ray formalism.  To find out if a ray has been blocked, you must
        use trace().
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

    def intermediateConjugates(self):
        """ The list of position and magnification of conjugate planes """
        transferMatrix = Matrix(A=1, B=0, C=0, D=1)
        matrices = self.transferMatrices()
        planes = []
        for element in matrices:
            transferMatrix = element * transferMatrix
            (distance, conjugate) = transferMatrix.forwardConjugate()
            if distance is not None:
                planePosition = transferMatrix.L + distance
                if planePosition != 0 and conjugate is not None:
                    magnification = conjugate.A
                    planes.append([planePosition, magnification])
        return planes

    def trace(self, inputRay):
        """Trace the input ray from first element until after the last element,
        indicating if the ray was blocked or not

        Returns a ray trace (i.e. [Ray()]) starting with inputRay, followed by 
        the ray after each element. If an element is composed of sub-elements, 
        the ray will also be traced in several steps. If any element blocks the 
        ray, it will be indicated.

        """
        if not isinstance(inputRay, (Ray, GaussianBeam)):
            raise TypeError("'inputRay' must be a Ray or a GaussianBeam.")
        ray = inputRay
        if ray != self._lastRayToBeTraced:
            rayTrace = [ray]
            for element in self.elements:
                rayTraceInElement = element.trace(ray)
                rayTrace.extend(rayTraceInElement)
                ray = rayTraceInElement[-1]  # last
            self._lastRayToBeTraced = inputRay
            self._lastRayTrace = rayTrace
        else:
            rayTrace = self._lastRayTrace

        return rayTrace

    def hasFiniteApertureDiameter(self):
        """ True if ImagingPath has at least one element of finite diameter """
        for element in self.elements:
            if element.hasFiniteApertureDiameter():
                return True
        return False

    @property
    def largestDiameter(self):
        """ Largest finite diameter in all elements """

        maxDiameter = 0
        if self.hasFiniteApertureDiameter():
            for element in self.elements:
                diameter = element.largestDiameter
                if diameter != float('+Inf') and diameter > maxDiameter:
                    maxDiameter = diameter
        elif len(self.elements) != 0:
            maxDiameter = self.elements[0].displayHalfHeight() * 2
        else:
            maxDiameter = float("+inf")

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

    def drawAt(self, z, axes, showLabels=True):  # pragma: no cover
        """ Draw each element of this group """
        for element in self.elements:
            element.drawAt(z, axes)
            element.drawAperture(z, axes)

            if showLabels:
                element.drawLabels(z, axes)
            z += element.L

    def drawPointsOfInterest(self, z, axes):  # pragma: no cover
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

        halfHeight = self.largestDiameter / 2
        for zStr, label in labels.items():
            z = float(zStr)
            axes.annotate(label, xy=(z, 0.0), xytext=(z, -halfHeight * 0.5),
                          xycoords='data', fontsize=12,
                          ha='center', va='bottom')

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self):
        if self.elements is None:
            raise StopIteration
        if self.iteration < len(self.elements):
            element = self.elements[self.iteration]
            self.iteration += 1
            return element
        raise StopIteration

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        if isinstance(item, slice):  # If we get a slice, return a matrix group
            return MatrixGroup(self.elements[item])
        return self.elements[item]

    def removeElement(self, index: int, pad: bool = False):
        maxIndex = len(self)
        if index < 0:
            index += maxIndex
        if index >= maxIndex or index < 0:
            raise IndexError(f"Index {index} out of bound, min = 0, max {maxIndex - 1}.")
        tempElements = self.elements[:]
        self.elements = []
        for i in range(maxIndex):
            element = tempElements[i]
            if i == index:
                length = element.L
                if length > 0 and pad:  # No need to pad if length is null
                    element = Space(length)
                    self.append(element)
            else:
                self.append(element)

    def insertElement(self, index: int, element: Matrix):
        if not isinstance(element, collections.Iterable):
            element = MatrixGroup([element])
        else:
            element = MatrixGroup(element)
        maxIndex = len(self)
        if index < 0:
            index += maxIndex
        if index > maxIndex or index < 0:
            raise IndexError(f"Index {index} out of bound, min = 0, max {maxIndex}.")
        if index == maxIndex:
            for newElement in element:
                self.append(newElement)
        else:
            tempElements = self.elements[:]
            self.elements = []
            for i in range(maxIndex):
                previousElement = tempElements[i]
                if i == index:
                    for newElement in element:
                        self.append(newElement)
                    self.append(previousElement)
                else:
                    self.append(previousElement)

    def replaceSingle(self, index: int, newElement: Matrix):
        if not isinstance(newElement, collections.Iterable):
            newElement = MatrixGroup([newElement])
        else:
            newElement = MatrixGroup(newElement)
        maxIndex = len(self)
        if index < 0:
            index += maxIndex
        if index >= maxIndex or index < 0:
            raise IndexError(f"Index {index} out of bound, min = 0, max {maxIndex - 1}.")
        tempElements = self.elements[:]
        self.elements = []
        for i in range(maxIndex):
            if i == index:
                toReplace = tempElements[i]
                if toReplace.L != newElement.L:
                    warnings.warn("Physical length mismatch. Squeezing or extending the current group.", UserWarning)
                for element in newElement:
                    self.append(element)
            else:
                self.append(tempElements[i])

    def replaceChunk(self, startIndex: int, stopIndex: int, newChunk: Matrix):
        # startIndex and stopIndex are included.
        if not isinstance(newChunk, collections.Iterable):
            newChunk = MatrixGroup([newChunk])
        else:
            newChunk = MatrixGroup(newChunk)
        maxIndex = len(self)
        if startIndex < 0:
            startIndex += maxIndex
        if stopIndex < 0:
            stopIndex += maxIndex
        if startIndex >= maxIndex or startIndex < 0:
            raise IndexError(f"Index {startIndex} out of bound, min = 0, max {maxIndex - 1}.")
        if stopIndex >= maxIndex or stopIndex < 0:
            raise IndexError(f"Index {stopIndex} out of bound, min = 0, max {maxIndex - 1}.")
        if startIndex == stopIndex:
            raise IndexError("The start and stop index must be different.")
        if startIndex > stopIndex:
            temp = startIndex
            startIndex = stopIndex
            stopIndex = temp

        if self[startIndex:stopIndex + 1].L != newChunk.L:
            warnings.warn("Physical length mismatch. Squeezing or extending the current group.", UserWarning)
        tempElements = self.elements[:]
        self.elements = []
        for i in range(maxIndex):
            if i < startIndex or i > stopIndex:
                # Don't disturb the elements we want to keep
                self.append(tempElements[i])
            elif i == startIndex:
                # When we reach the start index, we append every element in newChunk.
                for newElement in newChunk:
                    self.append(newElement)

    def __setitem__(self, key, value: Matrix):
        if isinstance(key, slice):
            if key.step is not None:
                warnings.warn("Not using the step of the slice.", UserWarning)
            self.replaceChunk(key.start, key.stop, value)
        else:
            self.replaceSingle(key, value)
