import unittest
import envtest # modifies path
from raytracing import *

inf = float("+inf")

class TestLimits(unittest.TestCase):
    def testInfinityAndZero(self):
        # Limits that exist
        self.assertEqual(inf, float('+inf'))
        self.assertEqual(0/inf, 0)
        self.assertEqual(inf*inf, inf)
        self.assertEqual(inf*10, inf)
        self.assertEqual(inf*(-10), -inf)
        self.assertEqual(inf+10, inf)
        self.assertEqual(inf*(-inf), -inf)
        self.assertEqual((-inf)*(-inf), inf)

        # Limits that do not exist
        self.assertTrue(isnan(inf-inf))
        self.assertTrue(isnan(inf*0))

        # Dividing by zero is never allowed
        with self.assertRaises(Exception) as context:
            inf/0



if __name__ == '__main__':
    unittest.main()
