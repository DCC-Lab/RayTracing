import envtest # modifies path
from raytracing import *


class TestMaterial(envtest.RaytracingTestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)

class TestMaterialSubclasses(envtest.RaytracingTestCase):
    def setUp(self) -> None:
        self.materials = Material.__subclasses__()

    def testMaterialsList(self):
        self.assertTrue(len(self.materials) > 10)

    def testMaterialsList2(self):
        self.assertTrue(Material.all())

    def testFindMaterialByName(self):
        self.assertIsNotNone(Material.findByName('NSF10'))

    def testFindMaterialByIndex(self):
        match = Material.findByIndex(n=1.6, wavelength=0.5, tolerance=0.1)
        self.assertIsNotNone(match)
        self.assertTrue(len(match) > 2)

        match = Material.findByIndex(n=5.6, wavelength=0.5, tolerance=0.1)
        self.assertIsNotNone(match)
        self.assertTrue(len(match) == 0)

    def testMaterialAbbeNumber(self):
        for material in self.materials:
            self.assertIsNotNone(material().abbeNumber())
            self.assertIsNotNone(material().Vd())

    def testMaterialSubclassesTypeError(self):
        fails = []
        for material in self.materials:
            try:
                self.assertRaises(TypeError, material.n, None)
                self.assertRaises(TypeError, material.n, 'test')
            except AssertionError:
                fails.append('TypeError for subclass {}'.format(material.__name__))
        self.assertEqual([], fails)

    def testMaterialSubclassesValueErrors(self):
        fails = []
        for material in self.materials:
            try:
                self.assertRaises(ValueError, material.n, 100)
                self.assertRaises(ValueError, material.n, 0)
                self.assertRaises(ValueError, material.n, -100)
            except AssertionError:
                fails.append('ValueError for subclass {}'.format(material.__name__))
        self.assertEqual([], fails)

    def testMaterialSubclasses(self):
        ''' These are sample values of refractive indices for each subclass of material for a wavelength of 0.6 micron.
        In case of a new category of material, make sure to add the sample value to the list. Indices can be found on :
        https://refractiveindex.info/ '''
        fails = []
        refractiveIndices = {'N_BK7': 1.5163, 'N_SF2': 1.6465, 'SF2': 1.6465, 'SF5': 1.6714, 'N_SF5': 1.6714,
                             'N_SF6HT': 1.8033, 'N_SF10': 1.7267, 'N_SF11': 1.7829, 'N_BAF10': 1.6692,
                             'E_BAF11': 1.6659, 'N_BAK1': 1.5719, 'N_BAK4': 1.5682, 'FK51A': 1.4862, 'LAFN7': 1.7482,
                             'N_LASF9': 1.8486,'N_LAK22': 1.6504, 'N_SSK5': 1.6576, 'E_FD10': 1.7267,
                             'FusedSilica': 1.4580,'N_SF6':1.7159, 'N_SF8':1.6876,'N_SF57':1.8445, 'Air':1.0}

        for material in self.materials:
            name = material.__name__
            n = material.n(0.6)

            if name not in refractiveIndices:
                fails.append('No test value for {0}'.format(name))

            if areRelativelyNotEqual(n, refractiveIndices[name], 1e-4):
                fails.append('Wrong value for subclass {}, {} not a valid n value.'.format(name, n))
        self.assertEqual([], fails)


if __name__ == '__main__':
    envtest.main()



