import unittest
import envtest # modifies path
from raytracing import *


class TestMaterial(unittest.TestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)


class TestMaterialSubclasses(unittest.TestCase):
    @property
    def subclasses(self):
        return Material.__subclasses__()
    
    def testMaterialSubclassesTypeError(self):
        fails = []
        for subclass in self.subclasses:
            try:
                self.assertRaises(TypeError, subclass.n, None)
                self.assertRaises(TypeError, subclass.n, 'test')
            except AssertionError:
                fails.append('TypeError for subclass {}'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testMaterialSubclassesValueErrors(self):
        fails = []
        for subclass in self.subclasses:
            try:
                self.assertRaises(ValueError, subclass.n, 100)
                self.assertRaises(ValueError, subclass.n, 0)
                self.assertRaises(ValueError, subclass.n, -100)
            except AssertionError:
                fails.append('ValueError for subclass {}'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testMaterialSubclasses(self):
        ''' These are sample values of refractive indexes for each subclass of material for a wavelength of 5 micron.
        In case of a new category of material, make sure to add the sample value to the list. '''
        fails = []
        refractiveIndexes = [1.3965252243506636, 1.5178527121226975, 1.5385861348077337, 1.5612286489801115,
                             1.539610715563772, 1.664053106820355, 1.5948478106562147, 1.6396821789377511,
                             1.5469302146171202, 1.5713583894047798, 1.4716376125966693, 1.459391121152617,
                             1.4251526811342752, 1.5810761652641074, 1.7197092324835102, 1.528065402814606,
                             1.541289278092723, 1.5975207997018837, 1.3404572894914368]

        for subclass in self.subclasses:
            n = subclass.n(5)
            if n not in refractiveIndexes:
                fails.append('Wrong value for subclass {}, {} not a valid n value.'.format(subclass.__name__, str(n)))
        self.assertEqual([], fails)


if __name__ == '__main__':
    unittest.main()



