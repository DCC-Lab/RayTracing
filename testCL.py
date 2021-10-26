from raytracing import *
import time

rays = RandomUniformRays(yMax=10, maxCount=1000000)#[Ray(y, y) for y in range(1000000)]
rays[-1]
path = ImagingPath()
path.append(Space(d=2))
path.append(Lens(f=10, diameter=1))
path.append(Space(d=2))
path.append(Lens(f=20))
path.append(Space(d=3))
path.append(Lens(f=30))
path.append(Space(d=4))
m = MatrixGroup(path.transferMatrices())

# startTime = time.time()
# outputRaytraces = m.traceMany(rays, useOpenCL=False)
# print("Python Done {0}/{1}".format(len(outputRaytraces), len(rays)))
# print("{0:0.1f}".format(time.time()-startTime))

startTime = time.time()
outputRaytraces = m.traceMany(rays, useOpenCL=True)
print("OpenCL Done {0}/{1}".format(len(outputRaytraces), len(rays)))
print("{0:0.1f}".format(time.time()-startTime))

