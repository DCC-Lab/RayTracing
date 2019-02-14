import unittest
import env # modifies path
from raytracing import *

inf = float("+inf")

class TestRay(unittest.TestCase):
    def testRay(self):
        ray = Ray()
        self.assertIsNotNone(Ray())
        self.assertEqual(ray.y, 0)
        self.assertEqual(ray.theta, 0)
        self.assertEqual(ray.z, 0)
        self.assertEqual(ray.apertureDiameter, inf)
        self.assertFalse(ray.isBlocked)
        self.assertTrue(ray.isNotBlocked)

    def testFan(self):
        fan = Ray.fan(y=0, radianMin=-0.1, radianMax=0.1, N=5)
        self.assertIsNotNone(fan)                
        self.assertEqual(len(fan), 5)
        self.assertEqual(min(map(lambda r: r.theta, fan)), -0.1)        
        self.assertEqual(max(map(lambda r: r.theta, fan)), 0.1)        
        self.assertEqual(min(map(lambda r: r.y, fan)), 0)        
        self.assertEqual(max(map(lambda r: r.y, fan)), 0)        
    
    def testFanGroup(self):
        fanGroup = Ray.fanGroup(yMin=0, yMax=1, M=10, radianMin=-0.1, radianMax=0.1, N=5)
        self.assertIsNotNone(fanGroup)                


if __name__ == '__main__':
    unittest.main()