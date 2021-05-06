import envtest
import doctest
import raytracing
from unittest.mock import Mock, patch

## if a new python file is added to the module, please add it in a new line



class TestMatrix(envtest.RaytracingTestCase):
    def test1(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.axicon,verbose=False)
    def test2(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.components,verbose=False)
    def test3(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.eo,verbose=False)
    def test4(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.figure,verbose=False)
    def test5(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.gaussianbeam,verbose=False)
    def test6(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.imagingpath,verbose=False)
    def test7(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.lasercavity,verbose=False)
    def test8(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.laserpath,verbose=False)
    def test9(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.materials,verbose=False)
    def test10(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.matrix,verbose=False)
    def test11(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.matrixgroup,verbose=False)
    def test12(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.ray,verbose=False)
    def test13(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.rays,verbose=False)
    def test14(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.specialtylenses,verbose=False)
    def test15(self):
        with patch('matplotlib.pyplot.show', new=Mock()):
            doctest.testmod(m=raytracing.utils,verbose=False)

if __name__ == '__main__':
    envtest.main()

