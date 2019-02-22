import unittest
import env # modifies path
from raytracing import *

inf = float("+inf")


class TestLens(unittest.TestCase):
    def testObjective(self):
        m = Objective()
        self.assertIsNotNone(m)

if __name__ == '__main__':
    unittest.main()
