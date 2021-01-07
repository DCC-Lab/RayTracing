import envexamples
from raytracing import *
import numpy as np
import math

def histogramValues(values):
    counts, binEdges = histogram(values, bins=40, density=True)
    ys = list(counts)
    xs = []
    for i in range(len(binEdges) - 1):
        xs.append((binEdges[i] + binEdges[i + 1]) / 2)
    nonzeroy = np.nonzero(asarray(ys))[0]
    yout = asarray(ys)[nonzeroy]
    xout = asarray(xs)[nonzeroy]
    return xout, yout


def showHistogram(values1, values2, title1="", title2="", imagetitle=""):
    fig, axis1 = plt.subplots(1)
    fig.tight_layout(pad=3.0)
    xs1, ys1 = histogramValues(values1)
    xs2, ys2 = histogramValues(values2)
    plt.scatter(xs1,ys1,marker='^',label=title1)
    plt.scatter(xs2,ys2,marker='o',label=title2)
    plt.legend()
    axis1.set_title(imagetitle)
    axis1.set_xlabel("Values")
    axis1.set_ylabel("Count")
    plt.show()


N = 1000

path = ImagingPath()
path.append(System4f(f1=30, diameter1=20, f2=50, diameter2=10))
path.append(Aperture(diameter=10, label='Camera'))
prncplRay = path.principalRay()
axlRay = path.axialRay()

axialAngle = path.axialRay()
maxAngle = axialAngle.theta
halfFOV = path.fieldOfView()/2

rays1 = RandomUniformRays(yMax=halfFOV, yMin=-halfFOV, thetaMax=maxAngle, thetaMin=-maxAngle, maxCount=N)
lagrangeBlocked = []
lagrangeNotBlocked = []
asPosition, size = path.apertureStop()

## first approach

# calculations for the principal ray
for i in range(N):
    ray1 = prncplRay
    ray2 = rays1[i]
    ray2Out = path.traceThrough(ray2)
    LI = path.lagrangeInvariant(ray1, ray2)
    if ray2Out.isBlocked:
        lagrangeBlocked.append(LI)
    else:
        lagrangeNotBlocked.append(LI)
print('something')

showHistogram(lagrangeBlocked,lagrangeNotBlocked,"blocked rays", "none blocked rays", "LI for all rays Vs. principal ray")


# calculations for the axial ray
for i in range(N):
    ray1 = axlRay
    ray2 = rays1[i]
    ray2Out = path.traceThrough(ray2)
    LI = path.lagrangeInvariant(ray1, ray2)
    if ray2Out.isBlocked:
        lagrangeBlocked.append(LI)
    else:
        lagrangeNotBlocked.append(LI)
print('something')

showHistogram(lagrangeBlocked, lagrangeNotBlocked, "blocked rays" , "none blocked rays"
              , "LI for all rays Vs. axial ray")


## second approach

lagrangeBlocked = []
lagrangeNotBlocked = []
ray1 = prncplRay
ray2 = axlRay
for i in range(N):
    ray3 = rays1[i]
    ray3Out = path.traceThrough(ray3)
    I12 = ray1.theta*ray2.y-ray2.theta*ray1.y
    I13 = ray1.theta * ray3.y - ray3.theta * ray1.y
    I32 = ray3.theta * ray2.y - ray2.theta * ray3.y
    A = I32/I12
    B = I13/I12
    lagrangeVal = (abs(A*math.sin(ray3.theta)**2)/3.14)**0.5
    if ray3Out.isBlocked:
        lagrangeBlocked.append(lagrangeVal)
    else:
        lagrangeNotBlocked.append(lagrangeVal)
print('something')

showHistogram(lagrangeBlocked, lagrangeNotBlocked, "blocked rays" , "none blocked rays"
              , "comparing LI for the third ray")

