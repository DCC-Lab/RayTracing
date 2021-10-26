from raytracing import *
import time

rays = RandomUniformRays(yMax=10, maxCount=100)#[Ray(y, y) for y in range(1000000)]
rays[-1]
path = ImagingPath()
path.append(Space(d=2))
path.append(Lens(f=10, diameter=20))
path.append(Space(d=2))
path.append(Lens(f=20))
path.append(Space(d=3))
path.append(Lens(f=30))
path.append(Space(d=4))
m = MatrixGroup(path.transferMatrices())

startTime = time.time()
outputRaytraces = m.traceManyThrough(rays, useOpenCL=False)
print("Python Done {0}/{1}".format(len(outputRaytraces), len(rays)))
print("{0:0.1f}".format(time.time()-startTime))

startTime = time.time()
outputRaytraces = m.traceManyThrough(rays, useOpenCL=True)

# for outputRays in outputRaytraces:
# for r in outputRays:
#     print("{0}".format(r))

# final = [ trace for trace in outputRaytraces if trace[-1].isNotBlocked]
print("OpenCL Done {0}/{1}".format(len(outputRaytraces), len(rays)))
print("{0:0.1f}".format(time.time()-startTime))

