import unittest
import envtest  # modifies path

from raytracing import *

inf = float("+inf")

testSaveHugeFile = True


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

    def testMatrixGroupDoesNotAcceptRandomClass(self):
        class Toto:
            def __init__(self):
                self.L = "Hello"

        with self.assertRaises(TypeError) as exception:
            MatrixGroup([Toto(), Matrix()])
        self.assertEqual(str(exception.exception), "'matrix' must be a Matrix instance.")

    def testMatrixGroupDoesnNotAcceptStr(self):
        with self.assertRaises(TypeError) as exception:
            MatrixGroup(["Matrix", Matrix()])
        self.assertEqual(str(exception.exception), "'matrix' must be a Matrix instance.")

    def testMatrixGroupDoesNotAcceptNonIterable(self):
        with self.assertRaises(TypeError) as exception:
            MatrixGroup(123)
        self.assertEqual(str(exception.exception),
                         "'elements' must be iterable (i.e. a list or a tuple of Matrix objects).")

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
        transferMat = otherElement * element
        msg = "If this fails, it is because the appended object is copied or it is not the right object: it is not" \
              "the same instance. At the time this test was written, the original object is appended." \
              "It is a short way to check if it is the right one at the end of the list."
        self.assertEqual(len(mg.elements), 2)
        self.assertIs(mg.elements[-1], otherElement, msg=msg)
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
        with self.assertWarns(UserWarning):
            mg.append(otherElement)

    def testAppendSpaceMustAdoptIndexOfRefraction(self):
        mEquivalent = MatrixGroup()
        d1 = DielectricInterface(n1=1, n2=1.55, R=100)
        s = Space(d=3)
        d2 = DielectricInterface(n1=1.55, n2=1.0, R=-100)
        mEquivalent.append(d1)
        mEquivalent.append(s)
        mEquivalent.append(d2)
        self.assertEqual(d1.backIndex, s.frontIndex)
        self.assertEqual(d2.frontIndex, s.backIndex)

    def testAppendNotSpaceIndexOfRefractionMismatch(self):
        mg = MatrixGroup([Space(10)])
        with self.assertRaises(ValueError):
            mg.append(DielectricInterface(1.33, 1.22))

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
        transferMat = s4 * l2 * s3 * s2 * l1 * s1
        self.assertEqual(len(mg.elements), len(elements))
        self.assertEqual(mg.L, transferMat.L)
        self.assertAlmostEqual(mg.A, transferMat.A, places=10)
        self.assertAlmostEqual(mg.B, transferMat.B, places=10)
        self.assertAlmostEqual(mg.C, transferMat.C, places=10)
        self.assertAlmostEqual(mg.D, transferMat.D, places=10)

    def testTransferMatricesNoElements(self):
        mg = MatrixGroup()
        self.assertListEqual(mg.transferMatrices(), [])

    def testTransferMatricesOneElement(self):
        msg = "The equality of matrices is based upon their id. It was sufficient when writing this test, because" \
              "the matrix was not copied or changed: it was the 'whole' object that was appended (i.e. the original " \
              "object and the appended object is the same object, same memory spot). If this fails, either" \
              "they are not the same object anymore (but can still be 'equal') or they are purely different."
        element1 = Space(10)
        mg = MatrixGroup([element1])
        transferMatrices = mg.transferMatrices()
        self.assertEqual(len(transferMatrices), 1)
        self.assertListEqual(transferMatrices, [element1], msg=msg)

    def transferMatrixTwoElements(self):
        msg = "The equality of matrices is based upon their id. It was sufficient when writing this test, because" \
              "the matrix was not copied or changed: it was the 'whole' object that was appended (i.e. the original " \
              "object and the appended object is the same object, same memory spot). If this fails, either" \
              "they are not the same object anymore (but can still be 'equal') or they are purely different."
        element1 = Space(10)
        mg = MatrixGroup([element1])
        element2 = Lens(2)
        mg.append(element2)
        transferMatrices = mg.transferMatrices()
        self.assertEqual(len(transferMatrices), 2)
        self.assertListEqual(transferMatrices, [element1, element2], msg=msg)

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

    def testTraceAlreadyTraced(self):
        s = Space(2, diameter=5)
        l = Lens(6, diameter=5)
        ray = Ray(2, 2)
        mg = MatrixGroup([s, l])
        trace = [ray, ray, Ray(6, 2), Ray(6, 1)]
        mgTrace1 = mg.trace(ray)

        mgTrace2 = mg.trace(ray)  # Trace a 2nd time
        self.assertListEqual(mg._lastRayTrace, trace)
        self.assertListEqual(mgTrace2, trace)
        self.assertListEqual(mgTrace1, mgTrace2)
        self.assertEqual(mg._lastRayToBeTraced, trace[0])
        self.assertTrue(mgTrace2[-1].isBlocked)

    def testTraceIncorrectType(self):
        s = Space(2, diameter=5)
        l = Lens(6, diameter=5)
        mg = MatrixGroup([s, l])
        with self.assertRaises(TypeError):
            mg.trace("Ray")

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

    def testFlipOrientation_1(self):
        space = Space(10)
        mg = MatrixGroup([space])
        mg.flipOrientation()
        self.assertListEqual(mg.elements, [space])
        self.assertEqual(mg.A, space.A)
        self.assertEqual(mg.B, space.B)
        self.assertEqual(mg.C, space.C)
        self.assertEqual(mg.D, space.D)
        self.assertEqual(mg.L, space.L)

    def testFlipOrientation_2(self):
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

    def testLenEmptyGroup(self):
        mg = MatrixGroup()
        self.assertEqual(len(mg), 0)

    def testLenNotEmpty(self):
        nbElements = 10
        mg = MatrixGroup([Lens(10) for _ in range(nbElements)])
        self.assertEqual(len(mg), nbElements)

    def testGetItemOutOfBoundsSingleIndex(self):
        mg = MatrixGroup([Lens(10) for _ in range(10)])
        index = len(mg)
        with self.assertRaises(IndexError):
            mg[index]

    def testGetItemOutOfBoundsEmpty(self):
        mg = MatrixGroup()
        with self.assertRaises(IndexError):
            mg[0]

    def testGetItem(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg = MatrixGroup(listOfElements)
        for i in range(len(mg)):
            self.assertIsInstance(mg[i], Matrix)
            self.assertEqual(mg[i], listOfElements[i])

    def testGetItemSlice(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg = MatrixGroup(listOfElements)
        sliceMG = mg[:]
        self.assertIsInstance(sliceMG, MatrixGroup)
        self.assertListEqual(sliceMG.elements, mg.elements)

    def testRemoveElementPositiveIndexOutOfBounds(self):
        nbElements = 10
        mg = MatrixGroup([Lens(10) for _ in range(nbElements)])
        with self.assertRaises(IndexError):
            mg.removeElement(len(mg))

    def testRemoveElementNegativeIndexOutOfBounds(self):
        nbElements = 10
        mg = MatrixGroup([Lens(10) for _ in range(nbElements)])
        with self.assertRaises(IndexError):
            mg.removeElement(-(len(mg) + 1))

    def testRemoveElementLastNoPad(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg1 = MatrixGroup(listOfElements)
        mg2 = MatrixGroup(listOfElements)
        mg1.removeElement(-1)
        mg2.removeElement((len(mg2) - 1))
        self.assertListEqual(mg1.elements, [space, lens])
        self.assertListEqual(mg1.elements, mg2.elements)

    def testRemoveElementFirstNoPad(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg1 = MatrixGroup(listOfElements)
        mg2 = MatrixGroup(listOfElements)
        mg1.removeElement(0)
        mg2.removeElement(-len(mg2))
        self.assertListEqual(mg1.elements, [lens, space])
        self.assertListEqual(mg1.elements, mg2.elements)

    def testRemoveAllNoPad(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg = MatrixGroup(listOfElements)
        mg.removeElement(1)
        mg.removeElement(0)
        mg.removeElement(0)
        self.assertListEqual(mg.elements, [])

    def testRemoveElementPad(self):
        space = Space(10)
        lens = Lens(10)
        listOfElements = [space, lens, space]
        mg1 = MatrixGroup(listOfElements)
        mg2 = MatrixGroup(listOfElements)
        mg3 = MatrixGroup(listOfElements)
        mg1.removeElement(0, True)
        mg2.removeElement(1, True)
        mg3.removeElement(2, True)
        self.assertIsInstance(mg1[0], Space)
        self.assertEqual(mg1[0].L, 10)
        self.assertEqual(len(mg2), 2)
        self.assertIsInstance(mg1[2], Space)
        self.assertEqual(mg1[2].L, 10)

    def testInsertElementNotMatrix(self):
        mg = MatrixGroup()
        with self.assertRaises(TypeError):
            mg.insertElement(0, Ray())

    def testInsertElementNegativeIndexOutOfBounds(self):
        mg = MatrixGroup([Lens(10)])
        with self.assertRaises(IndexError):
            mg.insertElement(-2, Space(10))

    def testInsertElementPositiveIndexOutOfBounds(self):
        mg = MatrixGroup([Lens(10)])
        with self.assertRaises(IndexError):
            mg.insertElement(2, Space(10))

    def testInsertElementAtTheEnd(self):
        space = Space(10)
        lens = Lens(10)
        mg = MatrixGroup([space, lens])
        mg.insertElement(2, space)
        self.assertListEqual(mg.elements, [space, lens, space])

    def testInsertElementAtFirst(self):
        space = Space(10)
        lens = Lens(10)
        mg = MatrixGroup([lens, space])
        mg.insertElement(0, space)
        self.assertListEqual(mg.elements, [space, lens, space])

    def testInsertElementIterable(self):
        space = Space(10)
        lens = Lens(10)
        mg = MatrixGroup([space, space, lens, space])
        insertion = MatrixGroup([lens, space])
        mg.insertElement(1, insertion)
        self.assertListEqual(mg.elements, [space, lens, space, space, lens, space])

    def testReplaceSingleWrongInputType(self):
        mg = MatrixGroup([Lens(10)])
        with self.assertRaises(TypeError):
            mg.replaceSingle(0, Ray())

    def testReplaceSingleNegativeIndexOutOfBounds(self):
        mg = MatrixGroup([Space(100)])
        with self.assertRaises(IndexError):
            mg.replaceSingle(-2, Space(101))

    def testReplaceSinglePositiveIndexOutOfBounds(self):
        mg = MatrixGroup([Space(9)])
        with self.assertRaises(IndexError):
            mg.replaceSingle(1, Space(9.01))

    def testReplaceSingleLengthMismatch(self):
        space = Space(10)
        wrongSpace = Space(15)
        rightSpace = Space(20)
        lens = Lens(10)
        mg = MatrixGroup([space, lens, wrongSpace, lens, space])
        with self.assertWarns(UserWarning):
            mg.replaceSingle(2, rightSpace)
        self.assertListEqual(mg.elements, [space, lens, rightSpace, lens, space])

    def testReplaceSingleNoMismatchLength(self):
        space = Space(10)
        wrongLens = Lens(9)
        rightLens = Lens(10)
        mg = MatrixGroup([space, wrongLens, space])
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                mg.replaceSingle(1, rightLens)
            except UserWarning:
                self.fail("Lengths should match!")
        self.assertListEqual(mg.elements, [space, rightLens, space])

    def testReplaceSingleWithMultipleMatrices(self):
        space = Space(10)
        lens = Lens(10)
        mg = MatrixGroup([space, lens, Space(20), lens, space])
        mg.replaceSingle(2, [space, space])
        self.assertListEqual(mg.elements, [space, lens, space, space, lens, space])

    def testReplaceChunkWrongInputType(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(20), Lens(10), Space(10)])
        with self.assertRaises(TypeError):
            mg.replaceChunk(0, 2, [ThickLens(1.22, 10, 10, 2), TypeError])

    def testReplaceChunkNegativeStartIndexOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10)])
        with self.assertRaises(IndexError):
            mg.replaceChunk(-4, -1, Lens(10))

    def testReplaceChunkNegativeStopIndexOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10)])
        with self.assertRaises(IndexError):
            mg.replaceChunk(0, -4, Lens(10))

    def testReplaceChunkPositiveStartIndexOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10)])
        with self.assertRaises(IndexError):
            mg.replaceChunk(3, 2, Lens(10))

    def testReplaceChunkPositiveStopIndexOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10)])
        with self.assertRaises(IndexError):
            mg.replaceChunk(0, 3, Lens(10))

    def testReplaceChunkSameIndices(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10)])
        with self.assertRaises(IndexError):
            mg.replaceChunk(0, 0, Space(10))

    def testReplaceChunkSwapIndicesNoMismatch(self):
        space10 = Space(10)
        lens = Lens(10)
        space20 = Space(20)
        elements = [space10, lens, space10, space10, lens, space10]
        mg = MatrixGroup(elements)
        newMG = MatrixGroup([space20])
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                mg.replaceChunk(3, 2, newMG)
            except UserWarning:
                self.fail("Lengths should match!")

        self.assertListEqual(mg.elements, [space10, lens, space20, lens, space10])

    def testReplaceChunkMismatch(self):
        space10 = Space(10)
        lens10 = Lens(10)
        space8 = Space(8)
        lens8 = Lens(8)
        mg = MatrixGroup([space10, lens10, space10, space10, lens10, space10])
        newMG = MatrixGroup([space8, lens8, space8])
        with self.assertWarns(UserWarning):
            mg.replaceChunk(3, -1, newMG)
        self.assertListEqual(mg.elements, [space10, lens10, space10, space8, lens8, space8])

    def testSetPositiveSingleIndexOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10), Space(5), ThickLens(1.33, 10, -10, 2)])
        with self.assertRaises(IndexError):
            mg[12] = CurvedMirror(5, 20)

    def testSetPositiveSliceOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10), Space(5), ThickLens(1.33, 10, -10, 2)])
        with self.assertRaises(IndexError):
            mg[10:12] = Aperture(50)  # First index out of bounds

        with self.assertRaises(IndexError):
            mg[0:10] = Aperture(80)  # Second index out of bounds

    def testSetNegativeSliceOutOfBounds(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10), Space(5), ThickLens(1.33, 10, -10, 2)])
        with self.assertRaises(IndexError):
            mg[-20:-1] = Aperture(50)

        with self.assertRaises(IndexError):
            mg[-1:-7] = Aperture(100)

    def testSetStepWarning(self):
        space10 = Space(10)
        lens10 = Lens(10)
        space5 = Space(5)
        lens5 = Lens(5)
        mg = MatrixGroup([space10, lens10, space5, space10, ThickLens(1.33, 10, -10, 2), space5])
        with self.assertWarns(UserWarning) as w:
            mg[2:4:2] = [space10, space5, lens5]
        self.assertEqual(str(w.warning), "Not using the step of the slice.")
        self.assertListEqual(mg.elements, [space10, lens10, space10, space5, lens5, space5])


class TestSaveAndLoadMatrixGroup(unittest.TestCase):
    dirName = ""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dirName = "tempDir"
        try:
            os.mkdir(cls.dirName)
        except:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        for file in os.listdir(cls.dirName):
            os.remove(os.path.join(cls.dirName, file))
        os.rmdir(cls.dirName)

    def setUp(self) -> None:
        self.testMG = MatrixGroup([Space(10), Lens(10), Space(10)])
        self.fileName = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "testMG.pkl")
        with open(self.fileName, 'wb') as file:
            pickle.Pickler(file).dump(self.testMG.elements)
        time.sleep(0.5)  # Make sure everything is ok

    def assertSaveNotFailed(self, matrixGroup: MatrixGroup, name: str):
        try:
            matrixGroup.save(name)
        except Exception as exception:
            self.fail(f"An exception was raised:\n{exception}")

    def assertLoadNotFailed(self, matrixGroup: MatrixGroup, name: str = None, append: bool = False):
        if name is None:
            name = self.fileName
        try:
            matrixGroup.load(name, append)
        except Exception as exception:
            self.fail(f"An exception was raised:\n{exception}")

    def assertLoadEqualsMatrixGroup(self, loadMatrixGroup: MatrixGroup, supposedMatrixGroup: MatrixGroup):
        tempList = supposedMatrixGroup.elements
        self.assertEqual(len(loadMatrixGroup.elements), len(tempList))
        for i in range(len(tempList)):
            self.assertIsInstance(loadMatrixGroup.elements[i], type(tempList[i]))
            self.assertEqual(loadMatrixGroup.elements[i].A, tempList[i].A)
            self.assertEqual(loadMatrixGroup.elements[i].B, tempList[i].B)
            self.assertEqual(loadMatrixGroup.elements[i].C, tempList[i].C)
            self.assertEqual(loadMatrixGroup.elements[i].D, tempList[i].D)
            self.assertEqual(loadMatrixGroup.elements[i].L, tempList[i].L)
            self.assertEqual(loadMatrixGroup.elements[i].apertureDiameter, tempList[i].apertureDiameter)
            self.assertEqual(loadMatrixGroup.elements[i].backIndex, tempList[i].backIndex)
            self.assertEqual(loadMatrixGroup.elements[i].frontIndex, tempList[i].frontIndex)
            self.assertEqual(loadMatrixGroup.elements[i].frontVertex, tempList[i].frontVertex)
            self.assertEqual(loadMatrixGroup.elements[i].backVertex, tempList[i].backVertex)

    def testSaveEmpty(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "emptyMG.pkl")
        mg = MatrixGroup()
        self.assertSaveNotFailed(mg, fname)

    def testSaveNotEmpty(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "notEmptyMG.pkl")
        mg = MatrixGroup([Space(10), Lens(10, 20), Space(20), Lens(10, 21), Space(10)])
        self.assertSaveNotFailed(mg, fname)

    def testSaveInFileNotEmpty(self):
        mg = MatrixGroup([Space(20), ThickLens(1.22, 10, 10, 10)])
        self.assertSaveNotFailed(mg, self.fileName)

    @unittest.skipIf(not testSaveHugeFile, "Don't test saving a lot of matrices")
    def testSaveHugeFile(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "hugeFile.pkl")
        spaces = [Space(10) for _ in range(500)]
        lenses = [Lens(10) for _ in range(500)]
        elements = spaces + lenses
        mg = MatrixGroup(elements)
        self.assertSaveNotFailed(mg, fname)

    def testLoadFileDoesNotExist(self):
        fname = r"this\file\does\not\exist.pkl"
        mg = MatrixGroup()
        with self.assertRaises(FileNotFoundError):
            mg.load(fname)

    def testLoadInEmptyMatrixGroup(self):
        mg = MatrixGroup()
        self.assertLoadNotFailed(mg)
        self.assertLoadEqualsMatrixGroup(mg, self.testMG)

    def testLoadOverrideMatrixGroup(self):
        mg = MatrixGroup([Lens(10), Space(10)])
        self.assertLoadNotFailed(mg)
        self.assertLoadEqualsMatrixGroup(mg, self.testMG)

    def testLoadAppend(self):
        mg = MatrixGroup([Lens(10), Space(10)])
        supposedMatrixGroup = MatrixGroup(mg.elements + self.testMG.elements)
        self.assertLoadNotFailed(mg, append=True)
        self.assertLoadEqualsMatrixGroup(mg, supposedMatrixGroup)

    def testLoadWrongObjectType(self):
        wrongObj = 7734
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, 'wrongObj.pkl')
        with open(fname, 'wb') as file:
            pickle.Pickler(file).dump(wrongObj)
        time.sleep(0.5)  # Make sure everything is ok

        try:
            with self.assertRaises(IOError):
                MatrixGroup().load(fname)
        except AssertionError as exception:
            self.fail(str(exception))

    def testLoadWrongIterType(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, 'wrongObj.pkl')
        wrongIterType = [Lens(5), Lens(10), Ray()]
        with open(fname, 'wb') as file:
            pickle.Pickler(file).dump(wrongIterType)
        time.sleep(0.5)
        try:
            with self.assertRaises(IOError):
                MatrixGroup().load(fname)
        except AssertionError as exception:
            self.fail(str(exception))

    def testSaveThenLoad(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "saveThenLoad.pkl")
        mg1 = MatrixGroup([Space(10), Lens(10, 100), Space(10), Aperture(50)])
        mg2 = MatrixGroup()
        self.assertSaveNotFailed(mg1, fname)
        self.assertLoadNotFailed(mg2, fname)
        self.assertLoadEqualsMatrixGroup(mg2, mg1)

    @unittest.skipIf(not testSaveHugeFile, "Don't test saving a lot of matrices")
    def testSaveThenLoadHugeFile(self):
        fname = os.path.join(TestSaveAndLoadMatrixGroup.dirName, "hugeFile.pkl")
        spaces = [Space(10) for _ in range(500)]
        lenses = [Lens(10) for _ in range(500)]
        elements = spaces + lenses
        mg1 = MatrixGroup(elements)
        mg2 = MatrixGroup()
        self.assertSaveNotFailed(mg1, fname)
        self.assertLoadNotFailed(mg2, fname)
        self.assertLoadEqualsMatrixGroup(mg2, mg1)


if __name__ == '__main__':
    unittest.main()
