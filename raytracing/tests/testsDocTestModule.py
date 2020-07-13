import envtest
import doctest
import raytracing

## if a new python file is added to the module, please add it in a new line

doctest.testmod(m=raytracing.axicon,verbose=True)
doctest.testmod(m=raytracing.components,verbose=True)
doctest.testmod(m=raytracing.eo,verbose=True)
doctest.testmod(m=raytracing.figure,verbose=True)
doctest.testmod(m=raytracing.gaussianbeam,verbose=True)
doctest.testmod(m=raytracing.imagingpath,verbose=True)
doctest.testmod(m=raytracing.lasercavity,verbose=True)
doctest.testmod(m=raytracing.laserpath,verbose=True)
doctest.testmod(m=raytracing.materials,verbose=True)
doctest.testmod(m=raytracing.matrix,verbose=True)
doctest.testmod(m=raytracing.matrixgroup,verbose=True)
doctest.testmod(m=raytracing.ray,verbose=True)
doctest.testmod(m=raytracing.rays,verbose=True)
doctest.testmod(m=raytracing.specialtylenses,verbose=True)
doctest.testmod(m=raytracing.utils,verbose=True)



