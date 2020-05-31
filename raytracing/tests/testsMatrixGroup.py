import unittest
import envtest  # modifies path

from raytracing import *

inf = float("+inf")


class TestMatrixGroup(unittest.TestCase):

    def testMatrixGroup(self):
        mg = MatrixGroup()
        self.assertIsInstance(mg, MatrixGroup)
        self.assertIsNone(mg._lastRayToBeTraced)
        self.assertIsNone(mg._lastRayTrace)
        self.assertEqual(mg.A, 1)
        self.assertEqual(mg.B, 0)
        self.assertEqual(mg.C, 0)
        self.assertEqual(mg.D, 1)
        self.assertListEqual(mg.elements, [])

    def testMatrixGroupAcceptsAnything(self):
        class Toto:
            def __init__(self):
                self.L = "Hello"

        with self.assertRaises(TypeError) as exception:
            MatrixGroup(["Matrix", Matrix()])
        self.assertEqual(str(exception.exception), "'matrix' must be a Matrix instance.")

        with self.assertRaises(TypeError) as exception2:
            MatrixGroup([Toto(), Matrix()])
        self.assertEqual(str(exception2.exception), str(exception.exception))

        with self.assertRaises(TypeError) as exception:
            MatrixGroup(123)
        self.assertEqual(str(exception.exception),
                         "'elements' must be iterable (i.e. a list or a tuple of Matrix objects).")

        with self.assertRaises(TypeError) as exception2:
            MatrixGroup(TypeError)
        self.assertEqual(str(exception2.exception), str(exception.exception))

    def testTransferMatrixNoElements(self):
        mg = MatrixGroup()
        transferMat = mg.transferMatrix()
        self.assertEqual(transferMat.A, 1)
        self.assertEqual(transferMat.B, 0)
        self.assertEqual(transferMat.C, 0)
        self.assertEqual(transferMat.D, 1)

    def testTransferMatrix(self):
        upTo = inf
        mg = MatrixGroup()
        space = Space(10)
        # We want to test transferMatrix, so we "artificially" put elements in the group
        # We should use MatrixGroup.append, but in order to use it, we need to test it, but it requires transferMatrix

        # Don't use it like that, it is not the right way.
        mg.elements.append(space)
        mirror = CurvedMirror(6)
        mg.elements.append(mirror)
        transferMatrix = mg.transferMatrix(upTo)
        supposedTransfer = mirror * space
        self.assertEqual(transferMatrix.apertureDiameter, supposedTransfer.apertureDiameter)
        self.assertEqual(transferMatrix.L, supposedTransfer.L)
        self.assertEqual(transferMatrix.A, supposedTransfer.A)
        self.assertEqual(transferMatrix.B, supposedTransfer.B)
        self.assertEqual(transferMatrix.C, supposedTransfer.C)
        self.assertEqual(transferMatrix.D, supposedTransfer.D)

    def testTransferMatrixUpToInGroup(self):
        upTo = 10
        mg = MatrixGroup()
        space = Space(2)
        # We want to test transferMatrix, so we "artificially" put elements in the group
        # We should use MatrixGroup.append, but in order to use it, we need to test it, but it requires transferMatrix

        # Don't use it like that, it is not the right way.
        mg.elements.append(space)
        ds = DielectricSlab(1, 12)
        mg.elements.append(ds)
        transferMatrix = mg.transferMatrix(upTo)
        supposedTransfer = ds.transferMatrix(8) * space
        self.assertEqual(transferMatrix.A, supposedTransfer.A)
        self.assertEqual(transferMatrix.B, supposedTransfer.B)
        self.assertEqual(transferMatrix.C, supposedTransfer.C)
        self.assertEqual(transferMatrix.D, supposedTransfer.D)
        self.assertEqual(transferMatrix.A, supposedTransfer.A)
        self.assertEqual(transferMatrix.frontIndex, supposedTransfer.frontIndex)
        self.assertEqual(transferMatrix.backIndex, supposedTransfer.backIndex)
        self.assertEqual(transferMatrix.frontVertex, supposedTransfer.frontVertex)
        self.assertEqual(transferMatrix.backVertex, supposedTransfer.backVertex)
        self.assertEqual(transferMatrix.L, supposedTransfer.L)

    def testAppendNoElementInit(self):
        mg = MatrixGroup()
        element = DielectricInterface(1.33, 1, 10)
        mg.append(element)
        self.assertEqual(len(mg.elements), 1)
        self.assertEqual(mg.L, element.L)
        self.assertEqual(mg.A, element.A)
        self.assertEqual(mg.B, element.B)
        self.assertEqual(mg.C, element.C)
        self.assertEqual(mg.D, element.D)

        otherElement = Space(10)
        mg.append(otherElement)
        self.assertEqual(len(mg.elements), 2)
        msg = "If this fails, it is because the appended object is copied or it is not the right object: it is not" \
              "the same instance. At the time this test was written, the original object is appended." \
              "It is a short way to check if it is the right one at the end of the list."
        self.assertIs(mg.elements[-1], otherElement, msg=msg)
        transferMat = otherElement * element
        self.assertEqual(mg.L, transferMat.L)
        self.assertEqual(mg.A, transferMat.A)
        self.assertEqual(mg.B, transferMat.B)
        self.assertEqual(mg.C, transferMat.C)
        self.assertEqual(mg.D, transferMat.D)

    def testAppendNoRefractionIndicesMismatch(self):
        mg = MatrixGroup()
        element = DielectricInterface(1, 1.33, 10)
        mg.append(element)
        otherElement = Space(10, 1.33)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                mg.append(otherElement)
            except UserWarning:
                self.fail("Refraction indices should match!")

    def testAppendRefractionIndicesMismatch(self):
        mg = MatrixGroup()
        element = DielectricInterface(1, 1.33, 10)
        mg.append(element)
        otherElement = Space(10)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(UserWarning):
                mg.append(otherElement)

    def testAppendSpaceMustAdoptIndexOfRefraction(self):
        mEquivalent = MatrixGroup()
        d1 = DielectricInterface(n1=1, n2=1.55, R=100)
        s  = Space(d=3)
        d2 = DielectricInterface(n1=1.55, n2=1.0, R=-100)
        mEquivalent.append(d1)
        mEquivalent.append(s)
        mEquivalent.append(d2)
        self.assertEqual(d1.backIndex, s.frontIndex)
        self.assertEqual(d2.frontIndex, s.backIndex)

    def testAppendNotCorrectType(self):
        mg = MatrixGroup()

        with self.assertRaises(TypeError):
            mg.append(10)

    def testMatrixGroupWithElements(self):
        elements = []
        f1 = 10
        f2 = 12
        diameter1 = 34
        diameter2 = 22
        s1, l1, s2 = Space(d=f1), Lens(f=f1, diameter=diameter1), Space(d=f1),
        s3, l2, s4 = Space(d=f2), Lens(f=f2, diameter=diameter2), Space(d=f2)
        elements.append(s1)
        elements.append(l1)
        elements.append(s2)
        elements.append(s3)
        elements.append(l2)
        elements.append(s4)
        mg = MatrixGroup(elements, label="Test")
        self.assertEqual(len(mg.elements), len(elements))
        transferMat = s4 * l2 * s3 * s2 * l1 * s1
        self.assertEqual(mg.L, transferMat.L)
        self.assertAlmostEqual(mg.A, transferMat.A, places=10)
        self.assertAlmostEqual(mg.B, transferMat.B, places=10)
        self.assertAlmostEqual(mg.C, transferMat.C, places=10)
        self.assertAlmostEqual(mg.D, transferMat.D, places=10)

    def testTransferMatricesNoElements(self):
        mg = MatrixGroup()
        self.assertListEqual(mg.transferMatrices(), [])

    def testTransferMatrices(self):
        msg = "The equality of matrices is based upon their id. It was sufficient when writing this test, because" \
              "the matrix was not copied or changed: it was the 'whole' object that was appended (i.e. the original " \
              "object and the appended object is the same object, same memory spot). If this fails, either" \
              "they are not the same object anymore (but can still be 'equal') or they are purely different."
        element1 = Space(10)
        mg = MatrixGroup([element1])
        transferMatrices = mg.transferMatrices()
        self.assertEqual(len(transferMatrices), 1)
        self.assertListEqual(transferMatrices, [element1], msg=msg)

        element2 = Lens(2)
        mg.append(element2)
        transferMatrices = mg.transferMatrices()
        self.assertEqual(len(transferMatrices), 2)
        self.assertListEqual(transferMatrices, [element1, element2])

    def testTraceEmptyMatrixGroup(self):
        mg = MatrixGroup()
        ray = Ray(10, 10)
        trace = [ray]
        self.assertListEqual(mg.trace(ray), trace)
        self.assertEqual(mg._lastRayToBeTraced, ray)
        self.assertListEqual(mg._lastRayTrace, trace)

    def testTrace(self):
        s = Space(2, diameter=5)
        l = Lens(6, diameter=5)
        ray = Ray(2, 2)
        mg = MatrixGroup([s, l])
        trace = [ray, ray, Ray(6, 2), Ray(6, 1)]
        mgTrace = mg.trace(ray)
        self.assertEqual(len(mgTrace), 4)
        self.assertListEqual(mgTrace, trace)
        self.assertTrue(mgTrace[-1].isBlocked)
        self.assertListEqual(mg._lastRayTrace, trace)
        self.assertEqual(mg._lastRayToBeTraced, trace[0])

        mgTrace = mg.trace(ray)
        self.assertListEqual(mg._lastRayTrace, trace)
        self.assertListEqual(mgTrace, trace)
        self.assertEqual(mg._lastRayToBeTraced, trace[0])
        self.assertTrue(mgTrace[-1].isBlocked)

    def testTraceIncorrectType(self):
        s = Space(2, diameter=5)
        l = Lens(6, diameter=5)
        mg = MatrixGroup([s, l])
        with self.assertRaises(TypeError):
            mg.trace("Ray")

    @unittest.skip("Importation problem...")
    def testImagingPath(self):
        mg = MatrixGroup()
        path = mg.ImagingPath()
        self.assertIsNotNone(path)

    @unittest.skip("Importation problem...")
    def testLaserPath(self):
        mg = MatrixGroup()
        path = mg.LaserPath()
        self.assertIsNotNone(path)

    def testIntermediateConjugatesEmptyGroup(self):
        mg = MatrixGroup()
        self.assertListEqual(mg.intermediateConjugates(), [])

    def testIntermediateConjugatesNoThickness(self):
        mg = MatrixGroup([Lens(4), DielectricInterface(1, 1.33, 1)])
        self.assertListEqual(mg.intermediateConjugates(), [])

    def testIntermediateConjugatesNoConjugate(self):
        mg = MatrixGroup([Matrix(1, 1, 1, 0, 1)])
        self.assertListEqual(mg.intermediateConjugates(), [])

    def testIntermediateConjugates(self):
        mg = [Space(10), Lens(9)]
        mg = MatrixGroup(mg)
        intermediateConjugates = mg.intermediateConjugates()
        results = [[10 / (10 / 9 - 1) + 10, 1 + (10 / 9) / (-10 / 9 + 1)]]
        self.assertEqual(len(intermediateConjugates), 1)
        self.assertEqual(len(intermediateConjugates[0]), 2)
        self.assertAlmostEqual(intermediateConjugates[0][0], results[0][0])
        self.assertAlmostEqual(intermediateConjugates[0][1], results[0][1])

    def testHasFiniteApertutreDiameter(self):
        space = Space(10, 1.2541255)
        mg = MatrixGroup([space])
        self.assertFalse(mg.hasFiniteApertureDiameter())

        mg.append(DielectricInterface(1.2541255, 1.33, 2, 1e5))
        self.assertTrue(mg.hasFiniteApertureDiameter())

    def testLargestDiameter(self):
        smallDiam = 10
        bigDiam = 25
        mg = MatrixGroup([Space(14, diameter=smallDiam), Lens(5), Space(5, diameter=bigDiam)])
        self.assertEqual(mg.largestDiameter, bigDiam)

    def testLargestDiameterNoFiniteAperture(self):
        mg = MatrixGroup([Space(10), Lens(5)])
        self.assertEqual(mg.largestDiameter, 8)

    def testLargestDiameterWithEmptyGroup(self):
        m = MatrixGroup()
        self.assertEqual(m.largestDiameter, float("+inf"))

    def testFlipOrientationEmptyGroup(self):
        mg = MatrixGroup()
        self.assertIs(mg.flipOrientation(), mg)

    def testFlipOrientation(self):
        space = Space(10)
        mg = MatrixGroup([space])
        mg.flipOrientation()
        self.assertListEqual(mg.elements, [space])
        self.assertEqual(mg.A, space.A)
        self.assertEqual(mg.B, space.B)
        self.assertEqual(mg.C, space.C)
        self.assertEqual(mg.D, space.D)
        self.assertEqual(mg.L, space.L)

        space = Space(10)
        slab = DielectricSlab(1, 10)
        interface = DielectricInterface(1, 1.33)
        mg = MatrixGroup([space, slab, interface])
        mg.flipOrientation()
        supposedMatrix = space * slab * interface
        self.assertListEqual(mg.elements, [interface, slab, space])
        self.assertEqual(mg.A, supposedMatrix.A)
        self.assertEqual(mg.B, supposedMatrix.B)
        self.assertEqual(mg.C, supposedMatrix.C)
        self.assertEqual(mg.D, supposedMatrix.D)
        self.assertEqual(mg.L, supposedMatrix.L)

    def testInitWithAnotherMatrixGroup(self):
        mg = MatrixGroup([Lens(5)])
        mg2 = MatrixGroup(mg)
        self.assertListEqual(mg.elements, mg2.elements)


if __name__ == '__main__':
    unittest.main()
