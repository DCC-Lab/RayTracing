import envtest  # modifies path

from raytracing import *

inf = float("+inf")

class TestMatrixGroup(envtest.RaytracingTestCase):

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
        self.assertEqual(len(mg.elements), 2)
        self.assertEqual(mg.elements[-1], otherElement)
        self.assertEqual(mg.elements[-1], otherElement)
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
            self.assertDoesNotRaise(mg.append, UserWarning, otherElement)

    @envtest.skip("We do not emit this warning anymore")
    def testAppendRefractionIndicesMismatch(self):
        mg = MatrixGroup()
        element = DielectricInterface(n1=1, n2=1.33, R=10)
        mg.append(element)
        otherElement = Space(d=10)
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
        element1 = Space(10)
        mg = MatrixGroup([element1])
        transferMatrices = mg.transferMatrices()
        self.assertEqual(len(transferMatrices), 1)
        self.assertListEqual(transferMatrices, [element1])

    def testTransferMatrixTwoElements(self):
        element1 = Space(10)
        mg = MatrixGroup([element1])
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
        mg = MatrixGroup([Matrix(1, 1, -1, 0, 1)])
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

    def testIntermediateConjugatesDuplicates(self):
        elements = [Space(10), Lens(10), Space(15), Lens(5), Space(5)]
        mg = MatrixGroup(elements)
        intermediateConj = mg.intermediateConjugates()
        self.assertListEqual(intermediateConj, [[30.0, -0.5]])

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
        self.assertEqual(mg.flipOrientation(), mg)

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

    def testPopPositiveIndexOutOfBounds(self):
        mg = MatrixGroup([Lens(5)])
        with self.assertRaises(IndexError):
            mg.pop(2)

    def testPopNegativeIndexOutOfBounds(self):
        mg = MatrixGroup([Lens(5)])
        with self.assertRaises(IndexError):
            mg.pop(-2)

    def testPopFirstElement(self):
        lens = Lens(10)
        mg = MatrixGroup([lens])
        poppedElement = mg.pop(0)
        self.assertEqual(poppedElement, lens)
        self.assertListEqual(mg.elements, [])

    def testPopLastElement(self):
        space = Space(10)
        lens = Lens(10)
        mg = MatrixGroup([space, lens, space])
        poppedElement = mg.pop(2)
        self.assertEqual(poppedElement, space)
        self.assertListEqual(mg.elements, [space, lens])

    def testPopElements(self):
        space10 = Space(10)
        lens10 = Lens(10)
        space5 = Space(5)
        lens5 = Lens(5)
        mg = MatrixGroup([space5, lens5, space5, space10, lens10, space10])
        pop3 = mg.pop(3)
        popLast = mg.pop(-1)
        self.assertEqual(pop3, popLast)
        self.assertListEqual(mg.elements, [space5, lens5, space5, lens10])

    def testInsertPositiveIndexOutOfBoundsNoError(self):
        space = Space(10)
        mg = MatrixGroup()
        mg.insert(10, space)
        self.assertListEqual(mg.elements, [space])

    def testInsertNegativeIndexOutOfBoundsNoErrors(self):
        space = Space(10)
        mg = MatrixGroup()
        mg.insert(-1000, space)
        self.assertListEqual(mg.elements, [space])

    def testInsertBeforeFirst(self):
        space10 = Space(10)
        lens10 = Lens(10)
        space20 = Space(20)
        lens20 = Lens(20)
        space5 = Space(5)
        lens5 = Lens(5)
        space15 = Space(15)
        lens15 = Lens(15)
        mg = MatrixGroup([space10, lens10, space10, space20, lens20, space20, space5, lens5, space5])
        mg.insert(0, [lens15, space15, lens15])
        allElements = [lens15, space15, lens15, space10, lens10, space10, space20, lens20, space20, space5, lens5,
                       space5]
        self.assertListEqual(mg.elements, allElements)

    def testInsertAfterLast(self):
        space10 = Space(10)
        lens10 = Lens(10)
        space20 = Space(20)
        lens20 = Lens(20)
        space5 = Space(5)
        lens5 = Lens(5)
        space15 = Space(15)
        lens15 = Lens(15)
        mg = MatrixGroup([space10, lens10, space10, space20, lens20, space20, space5, lens5, space5])
        mg.insert(10, [lens15, space15, lens15])
        allElements = [space10, lens10, space10, space20, lens20, space20, space5, lens5,
                       space5, lens15, space15, lens15]
        self.assertListEqual(mg.elements, allElements)

    def testInsertInMiddle(self):
        space10 = Space(10)
        lens10 = Lens(10)
        mg = MatrixGroup([space10, space10])
        mg.insert(1, lens10)
        self.assertListEqual(mg.elements, [space10, lens10, space10])

    def testSetItemSingleIndexOutOfBounds(self):
        mg = MatrixGroup()
        with self.assertRaises(IndexError):
            mg[0] = Lens(100)

    def testSetItemSliceIndexOutOfBounds(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup()
        mg[0:2] = [space, lens, space]
        self.assertListEqual(mg.elements, [space, lens, space])

    def testSetItemSliceWithStepWarning(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([space, lens, space, Space(20), Lens(20), Space(20)])
        with self.assertWarns(UserWarning):
            mg[3:len(mg):2] = [space, lens, space]
        self.assertListEqual(mg.elements, [space, lens, space, space, lens, space])

    def testSetItemSliceWithStepIsOne(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([space, lens, space, Space(20), Lens(20), Space(20)])

        def toto():
            mg[3:len(mg):1] = [space, lens, space]

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertDoesNotRaise(toto, UserWarning)
            self.assertListEqual(mg.elements, [space, lens, space, space, lens, space])

    def testSetItemStartIndexIsNone(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([Space(20), Lens(20), space])
        mg[:2] = [space, lens]
        self.assertListEqual(mg.elements, [space, lens, space])

    def testSetItemStopIndexIsNone(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([space, Lens(20), Space(20)])
        mg[1:] = [lens, space]
        self.assertListEqual(mg.elements, [space, lens, space])

    def testSetItemAll(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([CurvedMirror(10), DielectricInterface(1, 1.33), Space(20, 1.33)])
        mg[:] = [space, lens, space]
        self.assertListEqual(mg.elements, [space, lens, space])

    def testSetItemSingleIndex(self):
        lens = Lens(10)
        space = Space(10)
        mg = MatrixGroup([CurvedMirror(10), lens, space])
        mg[0] = space
        self.assertListEqual(mg.elements, [space, lens, space])

    def testEqualityDifferentClassInstance(self):
        mg = MatrixGroup()
        self.assertNotEqual(mg, Matrix())
        self.assertNotEqual(mg, Ray())
        self.assertNotEqual(mg, [Space(10), Lens(10), Space(10)])
        self.assertNotEqual(mg, complex(10, 20.12))

    def testEqualityDifferentListLength(self):
        mg1 = MatrixGroup()
        mg2 = MatrixGroup([Space(10)])
        self.assertNotEqual(mg1, mg2)

    def testEqualitySameLengthDifferentElements(self):
        mg1 = MatrixGroup([Space(10), Lens(10), Space(10), Space(10), Lens(10), Space(10)])
        mg2 = MatrixGroup([Space(20), Lens(20), Space(20), Space(20), Lens(20), Space(20)])
        self.assertNotEqual(mg1, mg2)

    def testEqualitySameGroup(self):
        mg1 = MatrixGroup([Space(10), Lens(10), Space(10), Space(10), Lens(10), Space(10)])
        mg2 = MatrixGroup([Space(10), Lens(10), Space(10), Space(10), Lens(10), Space(10)])
        self.assertEqual(mg1, mg2)

    def testEqualityGroupIs4f(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10), Space(10), Lens(10), Space(10)])
        system4f = System4f(10, 10)
        self.assertEqual(mg, system4f)

    def testMatrixGroupCanDisplay(self):
        mg = MatrixGroup([Space(10), Lens(10), Space(10), Space(10), Lens(10), Space(10)])
        mg.display()


class TestSaveAndLoadMatrixGroup(envtest.RaytracingTestCase):

    def setUp(self) -> None:
        self.testMG = MatrixGroup([Space(10), Lens(10), Space(10)])
        self.fileName = self.tempFilePath("testMG.pkl")
        with open(self.fileName, 'wb') as file:
            pickle.Pickler(file).dump(self.testMG.elements)
        time.sleep(0.5)  # Make sure everything is ok
        super().setUp()

    def assertSaveNotFailed(self, matrixGroup: MatrixGroup, name: str):
        self.assertDoesNotRaise(matrixGroup.save, None, name)

    def assertLoadNotFailed(self, matrixGroup: MatrixGroup, name: str = None, append: bool = False):
        if name is None:
            name = self.fileName
        self.assertDoesNotRaise(matrixGroup.load, None, name, append)

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
        fname = self.tempFilePath("emptyMG.pkl")
        mg = MatrixGroup()
        self.assertSaveNotFailed(mg, fname)

    def testSaveNotEmpty(self):
        fname = self.tempFilePath("notEmptyMG.pkl")
        mg = MatrixGroup([Space(10), Lens(10, 20), Space(20), Lens(10, 21), Space(10)])
        self.assertSaveNotFailed(mg, fname)

    def testSaveInFileNotEmpty(self):
        mg = MatrixGroup([Space(20), ThickLens(1.22, 10, 10, 10)])
        self.assertSaveNotFailed(mg, self.fileName)

    @envtest.skipIf(not envtest.performanceTests, "Don't test saving a lot of matrices")
    def testSaveHugeFile(self):
        fname = self.tempFilePath("hugeFile.pkl")
        spaces = [Space(10) for _ in range(200)]
        lenses = [Lens(10) for _ in range(200)]
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
        fname = self.tempFilePath("wrongObj.pkl")
        with open(fname, 'wb') as file:
            pickle.Pickler(file).dump(wrongObj)
        time.sleep(0.5)  # Make sure everything is ok

        def toto():
            with self.assertRaises(IOError):
                MatrixGroup().load(fname)

        self.assertDoesNotRaise(toto, AssertionError)

    def testLoadWrongIterType(self):
        fname = self.tempFilePath("wrongObj.pkl")
        wrongIterType = [Lens(5), Lens(10), Ray()]
        with open(fname, 'wb') as file:
            pickle.Pickler(file).dump(wrongIterType)
        time.sleep(0.5)

        def toto():
            with self.assertRaises(IOError):
                MatrixGroup().load(fname)

        self.assertDoesNotRaise(toto, AssertionError)

    def testSaveThenLoad(self):
        fname = self.tempFilePath("saveThenLoad.pkl")
        mg1 = MatrixGroup([Space(10), Lens(10, 100), Space(10), Aperture(50)])
        mg2 = MatrixGroup()
        self.assertSaveNotFailed(mg1, fname)
        self.assertLoadNotFailed(mg2, fname)
        self.assertLoadEqualsMatrixGroup(mg2, mg1)

    @envtest.skipIf(not envtest.performanceTests, "Don't test saving a lot of matrices")
    def testSaveThenLoadHugeFile(self):
        fname = self.tempFilePath("hugeFile.pkl")
        spaces = [Space(10) for _ in range(125)]
        lenses = [Lens(10) for _ in range(125)]
        elements = spaces + lenses
        mg1 = MatrixGroup(elements)
        mg2 = MatrixGroup()
        self.assertSaveNotFailed(mg1, fname)
        self.assertLoadNotFailed(mg2, fname)
        self.assertLoadEqualsMatrixGroup(mg2, mg1)


if __name__ == '__main__':
    envtest.main()
