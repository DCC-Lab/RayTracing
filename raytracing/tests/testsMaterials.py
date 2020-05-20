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
        self.assertEqual(N_BK7.n(5), 1.3965252243506636)


class TestN_SF2(unittest.TestCase):
    def testN_SF2TypeErrors(self):
        self.assertRaises(TypeError, N_SF2.n, None)
        self.assertRaises(TypeError, N_SF2.n, 'test')

    def testN_SF2ValueErrors(self):
        self.assertRaises(ValueError, N_SF2.n, 100)
        self.assertRaises(ValueError, N_SF2.n, 0)
        self.assertRaises(ValueError, N_SF2.n, -100)

    def testN_SF2(self):
        self.assertEqual(N_SF2.n(5), 1.5178527121226975)


class TestSF2(unittest.TestCase):
    def testSF2TypeErrors(self):
        self.assertRaises(TypeError, SF2.n, None)
        self.assertRaises(TypeError, SF2.n, 'test')

    def testSF2ValueErrors(self):
        self.assertRaises(ValueError, SF2.n, 100)
        self.assertRaises(ValueError, SF2.n, 0)
        self.assertRaises(ValueError, SF2.n, -100)

    def testSF2(self):
        self.assertEqual(SF2.n(5), 1.5385861348077337)


class TestSF5(unittest.TestCase):
    pass


class TestN_SF5(unittest.TestCase):
    pass


class TestN_SF6HT(unittest.TestCase):
    pass


class TestN_SF10(unittest.TestCase):
    pass


class TestN_SF11(unittest.TestCase):
    pass


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



