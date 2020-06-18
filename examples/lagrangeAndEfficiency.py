import envexamples
from raytracing import *

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
    axis1.plot(xs, ys, 'ko')
    axis1.set_xlabel("Values")
    axis1.set_ylabel("Count")
    plt.show()


N = 100000
p = 1000

path = ImagingPath()
path.append(System4f(f1=30, diameter1=20, f2=50, diameter2=10))
path.append(Aperture(diameter=10, label='Camera'))
path.display()

axialAngle = path.axialRay()
maxAngle = axialAngle.theta
halfFOV = path.fieldOfView()/2

rays1 = RandomUniformRays(yMax=halfFOV, yMin=-halfFOV, thetaMax=maxAngle, thetaMin=-maxAngle, maxCount=N)
rays2 = RandomUniformRays(yMax=halfFOV, yMin=-halfFOV, thetaMax=maxAngle, thetaMin=-maxAngle, maxCount=N)

lagrangeThrough = []
lagrangeBlocked = []
lagrangeValues = []
blockedZ = []
blockByAS = 0 # How many went through AS

asPosition, size = path.apertureStop()

for i in range(N):
    if (i+1) % p == 0:
        print("{0:.1f}%".format(i/N*100),file=sys.stderr)
        p *= 10

    ray1 = rays1[i]
    ray2 = rays2[i]
    lagrange = path.lagrangeInvariant(ray1, ray2)
    ray1Out = path.traceThrough(ray1)
    ray2Out = path.traceThrough(ray2)

    if ray1Out.isBlocked or ray2Out.isBlocked:
        lagrangeBlocked.append(abs(lagrange))
    if ray1Out.isNotBlocked and ray2Out.isNotBlocked:
        lagrangeThrough.append(abs(lagrange))
    lagrangeValues.append(abs(lagrange))

    if ray1Out.isBlocked:
        if ray1Out.z == asPosition:
            blockByAS += 1

        blockedZ.append(ray1Out.z)

    if ray2Out.isBlocked:
        if ray2Out.z == asPosition:
            blockByAS += 1

        blockedZ.append(ray2Out.z)



print("Efficiency: {0:.1f}%".format(len(blockedZ)/(2*N)*100))
print("Efficiency relative to AS: {0:.1f}%".format(100-(len(blockedZ)-blockByAS)/len(blockedZ)*100))
print("Efficiency AS: {0:.1f}%".format(blockByAS/(2*N)*100))
showHistogram(lagrangeBlocked,"Lagrange invariant when one ray blocked")
showHistogram(lagrangeThrough,"Lagrange invariant when both rays pass")
showHistogram(lagrangeValues,"All Lagrange values")
showHistogram(blockedZ,"Positions of light-blockers")