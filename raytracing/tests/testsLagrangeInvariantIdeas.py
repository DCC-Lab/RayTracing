import envtest  # modifies path
from raytracing import *

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
    def testLagrange(self):
        path = ImagingPath()
        path.objectHeight = 50
        path.append(System4f(f1=30, diameter1=25, f2=20, diameter2=30))
        path.append(Aperture(diameter=10, label='Camera'))
        path.display()

        principal = path.principalRay()
        principalRayTrace = path.trace(principal)

        axial = path.axialRay()
        axialRayTrace = path.trace(axial)

        maxInvariant = abs(path.lagrangeInvariant(principal, axial))

        maxAngle = axial.theta*2
        maxHeight = principal.y*1.2
        rays = RandomUniformRays(yMax=maxHeight, yMin=-maxHeight, thetaMax=maxAngle, thetaMin=-maxAngle, maxCount=10000)
        blocked = []
        notBlocked = []
        vignetted = []
        for ray in rays:
            rayTrace = path.trace(ray)
            I31 = (path.lagrangeInvariant(ray, principal))
            I12 = (path.lagrangeInvariant(axial, ray))

            calculatedTrace = rayTraceFromCalculation(ray, principalRayTrace, axialRayTrace)

            if abs(I31) > maxInvariant or abs(I12) > maxInvariant:
                self.assertTrue(rayTrace[-1].isBlocked)
                blocked.append((I31/maxInvariant,I12/maxInvariant))
                continue

            isBlocked = False
            for i in range(len(rayTrace)):
                #print("Max = {0:.2f} I31 = {1:.2f}, I12 = {2:.2f} SQR={3:.2f}".format(maxInvariant, I31, I12,sqrt(I31*I31+I12*I12)))
                if rayTrace[i].z == calculatedTrace[i].z:
                    self.assertAlmostEqual(rayTrace[i].y, calculatedTrace[i].y)
                    self.assertAlmostEqual(rayTrace[i].theta, calculatedTrace[i].theta)
                else:
                    #print("Max = {0:.2f} I31 = {1:.2f}, I12 = {2:.2f} SQR={3:.2f}".format(maxInvariant, I31, I12,sqrt(I31*I31+I12*I12)))
                    isBlocked = True
                    break
            if isBlocked:
                vignetted.append((I31/maxInvariant,I12/maxInvariant))
            else:
                notBlocked.append((I31/maxInvariant,I12/maxInvariant))

        
        print("Absolute efficiency: {0:.1f}% of 2π".format(100*len(notBlocked)/rays.maxCount))
        print("Relative efficiency: {0:.1f}% of maximal for this system".format(100*len(notBlocked)/(len(vignetted)+len(notBlocked))))
        print("Loss to vignetting: {0:.1f}%".format(100*len(vignetted)/(len(vignetted)+len(notBlocked))))
        fig, axis1 = plt.subplots(1)
        fig.tight_layout(pad=3.0)
        (x,y) = list(zip(*blocked))
        plt.scatter(x,y,marker='.')
        (x,y) = list(zip(*notBlocked))
        plt.scatter(x,y,marker='.')
        (x,y) = list(zip(*vignetted))
        plt.scatter(x,y,marker='.')
        axis1.set_xlabel(r"${I_{31}}/{I_{32}}$")
        axis1.set_ylabel(r"${I_{12}}/{I_{32}}$")
        plt.show()

if __name__ == '__main__':
    envtest.main()
