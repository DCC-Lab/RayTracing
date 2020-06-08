import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class Test4fSystem(envtest.RaytracingTestCase):

    def test4fSystem(self):
        elements = [Space(10), Lens(10), Space(15), Lens(5), Space(5)]
        mg = MatrixGroup(elements, label="4f system")
        system = System4f(10, 5, label="4f system")
        self.assertEqual(system.A, -0.5)
        self.assertEqual(system.B, 0)
        self.assertEqual(system.C, 0)
        self.assertEqual(system.D, -2)
        self.assertEqual(system.L, 30)
        self.assertEqual(mg.backIndex, system.backIndex)
        self.assertEqual(mg.frontIndex, system.frontIndex)
        self.assertEqual(mg.backVertex, system.backVertex)
        self.assertEqual(mg.frontVertex, system.frontVertex)
        self.assertEqual(mg.label, system.label)
        self.assertTrue(system.isImaging)

    def test2fSystem(self):
        elements = [Space(10), Lens(10), Space(10)]
        mg = MatrixGroup(elements, label="2f system")
        system = System2f(10, label="2f system")
        self.assertEqual(system.A, 0)
        self.assertEqual(system.B, 10)
        self.assertEqual(system.C, -1 / 10)
        self.assertEqual(system.D, 0)
        self.assertEqual(system.L, 20)
        self.assertEqual(mg.backIndex, system.backIndex)
        self.assertEqual(mg.frontIndex, system.frontIndex)
        self.assertEqual(mg.backVertex, system.backVertex)
        self.assertEqual(mg.frontVertex, system.frontVertex)
        self.assertEqual(mg.label, system.label)
        self.assertFalse(system.isImaging)

    def test4fIsTwo2f(self):
        f1, f2 = 10, 12
        system4f = System4f(f1=10, f2=12)
        system2f_1 = System2f(f1)
        system2f_2 = System2f(f2)
        composed4fSystem = MatrixGroup(system2f_1.elements + system2f_2.elements)
        self.assertEqual(composed4fSystem.A, system4f.A)
        self.assertEqual(composed4fSystem.B, system4f.B)
        self.assertEqual(composed4fSystem.C, system4f.C)
        self.assertEqual(composed4fSystem.D, system4f.D)
        self.assertEqual(composed4fSystem.L, system4f.L)
        self.assertEqual(composed4fSystem.backIndex, system4f.backIndex)
        self.assertEqual(composed4fSystem.frontIndex, system4f.frontIndex)
        self.assertEqual(composed4fSystem.backVertex, system4f.backVertex)
        self.assertEqual(composed4fSystem.frontVertex, system4f.frontVertex)


if __name__ == '__main__':
    envtest.main()
