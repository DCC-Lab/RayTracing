import envtest  # modifies path
from raytracing import *
import numpy as np

def distHist(rays):
    localRays = list(rays)
    lagrange = []
    while len(localRays) >= 2:
        ray1 = localRays.pop()
        ray2 = localRays.pop()
        lagrange.append(ray1.y*ray2.theta - ray1.theta*ray2.y)
    showHistogram(lagrange)

def histogramValues(values):
    counts, binEdges = histogram(values, bins=40, density=True)
    ys = list(counts)
    xs = []
    for i in range(len(binEdges) - 1):
        xs.append((binEdges[i] + binEdges[i + 1]) / 2)
    return xs, ys

def showHistogram(values,title=""):
    fig, axis1 = plt.subplots(1)
    fig.tight_layout(pad=3.0)
    xs, ys = histogramValues(values)
    axis1.set_title(title)
    axis1.plot(xs, (ys), 'ko')
    axis1.set_xlabel("Values")
    axis1.set_ylabel("Count")
    plt.show()

def printTrace(trace):
    for r in trace:
        print(r.y, r.theta, r.z, r.isBlocked)
    print()

def rayTraceFromCalculation(ray, principalTrace, axialTrace):
    principal = principalTrace[0]
    axial = axialTrace[0]

    I12 = principal.theta * axial.y - axial.theta * principal.y
    I13 = principal.theta * ray.y - ray.theta * principal.y
    I32 = ray.theta * axial.y - axial.theta * ray.y
    A = I32/I12
    B = I13/I12
    trace = []
    # print(A,B)
    for i in range(len(principalTrace)):
        r1 = principalTrace[i]
        r2 = axialTrace[i]
        r3 = Ray(y=A*r1.y + B*r2.y, theta = A*r1.theta + B*r2.theta)
        r3.z = r1.z
        trace.append(r3)

    return trace

def reportEfficiency(path, objectDiameter=None, nRays=10000):
    principal = path.principalRay()
    axial = path.axialRay()
    maxInvariant = abs(path.lagrangeInvariant(principal, axial)) 

    maxAngle = np.pi/2
    if objectDiameter is not None:
        maxHeight = objectDiameter/2
    else:
        maxHeight = principal.y

    rays = RandomUniformRays(yMax=maxHeight, 
                             yMin=-maxHeight,
                             thetaMax=maxAngle,
                             thetaMin=-maxAngle,
                             maxCount=nRays)
    expectedBlocked = []
    notBlocked = []
    vignettedBlocked = []
    vignettePositions = []
    for ray in rays:
        #fixme : I recall from the website that I12 is in fact I32. Confusing a bit. 
        I31 = (path.lagrangeInvariant(ray, principal)) 
        I12 = (path.lagrangeInvariant(axial, ray))
        outputRay = path.traceThrough(ray)

        if abs(I31) > maxInvariant or abs(I12) > maxInvariant:
            expectedBlocked.append((I31/maxInvariant,I12/maxInvariant))
            continue

        if outputRay.isBlocked:
            vignettedBlocked.append((I31/maxInvariant,I12/maxInvariant))
            vignettePositions.append(outputRay.z)
        else:
            notBlocked.append((I31/maxInvariant,I12/maxInvariant))

    
    print("Absolute efficiency: {0:.1f}% of ±π radian, over field of view of {1:.1f}".format(100*len(notBlocked)/rays.maxCount, 2*maxHeight))
    stopPosition, stopDiameter = path.apertureStop()
    print("  Efficiency limited by {0:.1f} mm diameter of AS at z={1:.1f}".format(stopDiameter, stopPosition))
    print("Relative efficiency: {0:.1f}% of maximal for this system".format(100*len(notBlocked)/(len(vignettedBlocked)+len(notBlocked))))
    print("  Loss to vignetting: {0:.1f}%".format(100*len(vignettedBlocked)/(len(vignettedBlocked)+len(notBlocked))))
    print("  Vignetting is due to blockers at positions: {0}".format(set(vignettePositions)))
    fig, axis1 = plt.subplots(1)
    fig.tight_layout(pad=3.0)
    (x,y) = list(zip(*expectedBlocked))
    plt.scatter(x,y,marker='.')
    (x,y) = list(zip(*notBlocked))
    plt.scatter(x,y,marker='.')
    if len(vignettedBlocked) >= 2:
        (x,y) = list(zip(*vignettedBlocked))
        plt.scatter(x,y,marker='.')
    # fixme : I32 replaced by I12 and I12 replaced by I32 ? 
    axis1.set_xlabel(r"${I_{31}}/{I_{32}}$")
    axis1.set_ylabel(r"${I_{12}}/{I_{32}}$")
    plt.show()


class TestLagrange(envtest.RaytracingTestCase):
    def testLagrange(self):
        path = ImagingPath()
        path.objectHeight = 50
        path.append(System4f(f1=30, diameter1=50, f2=40, diameter2=40))
        path.append(Aperture(diameter=10, label='Camera'))
        path.display()
        path.reportEfficiency()

if __name__ == '__main__':
    envtest.main()
