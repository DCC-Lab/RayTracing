import unittest
import env # modifies path
from raytracing import *


class TestMaterial(unittest.TestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)


class TestN_BK7(unittest.TestCase):
    def testN_BK7TypeErrors(self):
        self.assertRaises(TypeError, N_BK7.n, None)
        self.assertRaises(TypeError, N_BK7.n, 'test')

    def testN_BK7ValueErrors(self):
        self.assertRaises(ValueError, N_BK7.n, 100)
        self.assertRaises(ValueError, N_BK7.n, 0)
        self.assertRaises(ValueError, N_BK7.n, -100)

    def testN_BK7(self):
        self.assertEqual(1.3965252243506636, N_BK7.n(5))


class TestN_SF2(unittest.TestCase):
    def testN_SF2TypeErrors(self):
        self.assertRaises(TypeError, N_SF2.n, None)
        self.assertRaises(TypeError, N_SF2.n, 'test')

    def testN_SF2ValueErrors(self):
        self.assertRaises(ValueError, N_SF2.n, 100)
        self.assertRaises(ValueError, N_SF2.n, 0)
        self.assertRaises(ValueError, N_SF2.n, -100)

    def testN_SF2(self):
        self.assertEqual(1.5178527121226975, N_SF2.n(5))


class TestSF2(unittest.TestCase):
    def testSF2TypeErrors(self):
        self.assertRaises(TypeError, SF2.n, None)
        self.assertRaises(TypeError, SF2.n, 'test')

    def testSF2ValueErrors(self):
        self.assertRaises(ValueError, SF2.n, 100)
        self.assertRaises(ValueError, SF2.n, 0)
        self.assertRaises(ValueError, SF2.n, -100)

    def testSF2(self):
        self.assertEqual(1.5385861348077337, SF2.n(5))


class TestSF5(unittest.TestCase):
    def testSF5TypeErrors(self):
        self.assertRaises(TypeError, SF5.n, None)
        self.assertRaises(TypeError, SF5.n, 'test')

    def testSF5ValueErrors(self):
        self.assertRaises(ValueError, SF5.n, 100)
        self.assertRaises(ValueError, SF5.n, 0)
        self.assertRaises(ValueError, SF5.n, -100)

    def testSF5(self):
        self.assertEqual(1.5612286489801115, SF5.n(5))


class TestN_SF5(unittest.TestCase):
    def testN_SF5TypeErrors(self):
        self.assertRaises(TypeError, N_SF5.n, None)
        self.assertRaises(TypeError, N_SF5.n, 'test')

    def testN_SF5ValueErrors(self):
        self.assertRaises(ValueError, N_SF5.n, 100)
        self.assertRaises(ValueError, N_SF5.n, 0)
        self.assertRaises(ValueError, N_SF5.n, -100)

    def testN_SF5(self):
        self.assertEqual(1.539610715563772, N_SF5.n(5))


class TestN_SF6HT(unittest.TestCase):
    def testN_SF6HTTypeErrors(self):
        self.assertRaises(TypeError, N_SF6HT.n, None)
        self.assertRaises(TypeError, N_SF6HT.n, 'test')

    def testN_SF6HTValueErrors(self):
        self.assertRaises(ValueError, N_SF6HT.n, 100)
        self.assertRaises(ValueError, N_SF6HT.n, 0)
        self.assertRaises(ValueError, N_SF6HT.n, -100)

    def testN_SF6HT(self):
        self.assertEqual(1.664053106820355, N_SF6HT.n(5))


class TestN_SF10(unittest.TestCase):
    def testN_SF10TypeErrors(self):
        self.assertRaises(TypeError, N_SF10.n, None)
        self.assertRaises(TypeError, N_SF10.n, 'test')

    def testN_SF10ValueErrors(self):
        self.assertRaises(ValueError, N_SF10.n, 100)
        self.assertRaises(ValueError, N_SF10.n, 0)
        self.assertRaises(ValueError, N_SF10.n, -100)

    def testN_SF10(self):
        self.assertEqual(1.5948478106562147, N_SF10.n(5))


class TestN_SF11(unittest.TestCase):
    def testN_SF11TypeErrors(self):
        self.assertRaises(TypeError, N_SF11.n, None)
        self.assertRaises(TypeError, N_SF11.n, 'test')

    def testN_SF11ValueErrors(self):
        self.assertRaises(ValueError, N_SF11.n, 100)
        self.assertRaises(ValueError, N_SF11.n, 0)
        self.assertRaises(ValueError, N_SF11.n, -100)

    def testN_SF11(self):
        self.assertEqual(1.6396821789377511, N_SF11.n(5))


class TestN_BAF10(unittest.TestCase):
    pass


class TestE_BAF11(unittest.TestCase):
    pass


class TestN_BAK1(unittest.TestCase):
    pass


class TestN_BAK4(unittest.TestCase):
    pass


class TestFK51A(unittest.TestCase):
    pass


class TestLAFN7(unittest.TestCase):
    pass


class TestN_LASF9(unittest.TestCase):
    pass


class TestN_LAK22(unittest.TestCase):
    pass


class TestN_SSK5(unittest.TestCase):
    pass


class TestE_FD10(unittest.TestCase):
    pass


class TestFusedSilica(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()



