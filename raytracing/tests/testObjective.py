import unittest
import env # modifies path
from raytracing import *

inf = float("+inf")


class TestObjective(unittest.TestCase):
    def testCreateObjectiveWithoutArgument(self):
        with self.assertRaises(Exception) as context:
            obj = Objective()

    def testCreateObjective(self):
        obj = Objective(f=180/20, NA=0.5, focusToFocusLength=50, backAperture=12, workingDistance=2)
        self.assertIsNotNone(obj)
        path = ImagingPath()
        path.append(Space(30))
        path.append(obj)
        path.append(Space(30))
        trace = path.trace(Ray())

if __name__ == '__main__':
    unittest.main()