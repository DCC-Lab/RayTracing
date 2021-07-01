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

class TestLagrange(envtest.RaytracingTestCase):
    @envtest.skip
    def testLagrange(self):
        path = ImagingPath(label="4f system")
        path.objectHeight = 50
        path.append(System4f(f1=30, diameter1=60, f2=40, diameter2=100))
        path.append(Aperture(diameter=10, label='Camera'))
        # path.display()
        path.reportEfficiency(nRays=10000)

    @envtest.redirectStdOutToFile
    @envtest.patch('matplotlib.pyplot.show', new=envtest.Mock())
    def testObjective(self):
        path = ImagingPath(label="Objective")
        path.append(Aperture(diameter=22.5))
        path.append(Space(d=180))
        path.append(Lens(f=180, diameter=50, label='Tube lens'))
        path.append(Space(d=180))
        path.append(olympus.XLUMPlanFLN20X())
        path.flipOrientation()
        self.assertAlmostEqual( abs(path.magnification()[0]), 20)
        self.assertAlmostEqual( path.imageSize(), 22.5,3)
        path.reportEfficiency(nRays=10000)
        path.display(rays=ObjectRays(diameter=10))

if __name__ == '__main__':
    envtest.main()
