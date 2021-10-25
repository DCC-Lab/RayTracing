from raytracing import *

rays = RandomUniformRays(yMax=10, maxCount=1)#[Ray(y, y) for y in range(1000000)]
path = ImagingPath()
path.append(Space(d=2))
path.append(Lens(f=10, diameter=1))
path.append(Space(d=2))
path.append(Lens(f=20))
path.append(Space(d=3))
path.append(Lens(f=30))
path.append(Space(d=4))
m = MatrixGroup(path.transferMatrices())
outputRaytraces = m.traceMany(rays, useOpenCL=False)
print("Done {0} {1} {2}".format(len(outputRaytraces), len(rays), outputRaytraces))

for ray in outputRaytraces[0]:
    print("{0} {1} {2}".format(ray.y, ray.theta, ray.isBlocked))

outputRaytraces = m.traceMany(rays, useOpenCL=True)
print("Done {0} {1} {2}".format(len(outputRaytraces), len(rays), outputRaytraces))

for ray in outputRaytraces[0]:
    print("{0} {1} {2}".format(ray.y, ray.theta, ray.isBlocked))


#path.display(raysList=outputRaytraces)