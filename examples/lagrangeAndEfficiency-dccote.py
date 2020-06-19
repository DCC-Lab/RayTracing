import envexamples
from raytracing import *


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


N = 100000
p = 1000

path = ImagingPath()
path.append(System4f(f1=30, diameter1=20, f2=50, diameter2=20))
path.append(Aperture(diameter=10, label='Camera'))
path.display()

axialAngle = path.axialRay()
maxAngle = axialAngle.theta
maxHeight = path.fieldOfView()/2
maxInv = abs(maxHeight*maxAngle)
print(maxHeight, maxAngle, maxInv)

rays1 = RandomUniformRays(yMax=maxHeight, yMin=-maxHeight, thetaMax=maxAngle*2, thetaMin=-maxAngle*2, maxCount=N)
rays2 = RandomUniformRays(yMax=maxHeight, yMin=-maxHeight, thetaMax=maxAngle*2, thetaMin=-maxAngle*2, maxCount=N)
# rays1 = RandomLambertianRays(yMax=maxHeight, yMin=-maxHeight, maxCount=N)
# rays2 = RandomLambertianRays(yMax=maxHeight, yMin=-maxHeight, maxCount=N)

# distHist(rays1)

# exit(1)

lagrangeThrough = []
lagrangeBlocked = []
lagrangeValues = []
angles = []
blockedZ = []
blockByAS = 0 # How many went through AS

asPosition, size = path.apertureStop()

for i in range(N):
    if (i+1) % p == 0:
        print("{0:.1f}%".format(i/N*100),file=sys.stderr)
        p *= 10

    ray1 = rays1[i]
    ray1WillBeBlocked = False
    if abs(ray1.y * maxAngle) > maxInv or abs(ray1.theta * maxHeight) > maxInv:
        ray1WillBeBlocked = True


    ray2 = rays2[i]
    ray2WillBeBlocked = False
    if abs(ray2.y * maxAngle) > maxInv or abs(ray2.theta * maxHeight) > maxInv:
        ray2WillBeBlocked = True

    lagrange = abs(path.lagrangeInvariant(ray1, ray2))
    ray1Out = path.traceThrough(ray1)
    ray2Out = path.traceThrough(ray2)

    # if ray1Out.isBlocked != ray1WillBeBlocked:
    #     print(abs(ray1.y * maxAngle), abs(ray1.theta * maxHeight), maxInv)
    # if ray2Out.isBlocked != ray2WillBeBlocked:
    #     print(abs(ray2.y * maxAngle), abs(ray2.theta * maxHeight), maxInv)


    if ray1Out.isBlocked or ray2Out.isBlocked:
        lagrangeBlocked.append(abs(lagrange))
    if ray1Out.isNotBlocked and ray2Out.isNotBlocked:
        lagrangeThrough.append(abs(lagrange))
    lagrangeValues.append(abs(lagrange))

    if ray1Out.isBlocked:
        if ray1Out.z == asPosition:
            blockByAS += 1

        blockedZ.append(ray1Out.z)
    else:
        angles.append(ray1.theta)

    if ray2Out.isBlocked:
        if ray2Out.z == asPosition:
            blockByAS += 1

        blockedZ.append(ray2Out.z)
    else:
        angles.append(ray2.theta)



print("Efficiency: {0:.1f}%".format(len(blockedZ)/(2*N)*100))
print("Efficiency relative to AS: {0:.1f}%".format(100-(len(blockedZ)-blockByAS)/len(blockedZ)*100))
print("Efficiency AS: {0:.1f}%".format(blockByAS/(2*N)*100))
showHistogram(angles,"Angles")
showHistogram(lagrangeBlocked,"Lagrange invariant when one ray blocked")
showHistogram(lagrangeThrough,"Lagrange invariant when both rays pass")
showHistogram(lagrangeValues,"All Lagrange values")
showHistogram(blockedZ,"Positions of light-blockers")

