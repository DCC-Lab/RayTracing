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
        path.append(System4f(f1=30, diameter1=25, f2=50, diameter2=30))
        path.append(Aperture(diameter=10, label='Camera'))
        
        principal = path.principalRay()
        # principal.y -= 0.1
        principalRayTrace = path.trace(principal)

        axial = path.axialRay()
        # axial.theta -= 0.01
        axialRayTrace = path.trace(axial)

        maxInvariant = abs(path.lagrangeInvariant(principal, axial))

        maxAngle = axial.theta
        halfFOV = principal.y
        rays = RandomUniformRays(yMax=halfFOV, yMin=-halfFOV, thetaMax=maxAngle, thetaMin=-maxAngle, maxCount=1000000)
        blocked = 0
        for ray in rays:
            rayTrace = path.trace(ray)
            I31 = abs(path.lagrangeInvariant(ray, principal))
            I12 = abs(path.lagrangeInvariant(axial, ray))

            calculatedTrace = rayTraceFromCalculation(ray, principalRayTrace, axialRayTrace)

            if I31 > maxInvariant or I12 > maxInvariant:
                self.assertTrue(rayTrace[-1].isBlocked)
                continue

            for i in range(len(rayTrace)):
                print("Max = {0:.2f} I31 = {1:.2f}, I12 = {2:.2f} SQR={3:.2f}".format(maxInvariant, I31, I12,sqrt(I31*I31+I12*I12)))
                if rayTrace[i].z == calculatedTrace[i].z:
                    self.assertAlmostEqual(rayTrace[i].y, calculatedTrace[i].y)
                    self.assertAlmostEqual(rayTrace[i].theta, calculatedTrace[i].theta)
                else:
                    print("Max = {0:.2f} I31 = {1:.2f}, I12 = {2:.2f} SQR={3:.2f}".format(maxInvariant, I31, I12,sqrt(I31*I31+I12*I12)))
                    blocked += 1
                    break


if __name__ == '__main__':
    envtest.main()
