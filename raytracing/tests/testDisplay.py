import envtest  # modifies path
from raytracing import *
from numpy import linspace, pi
from raytracing.materials import *

inf = float("+inf")

def exampleCodeThatUsedToCrashe():
    # I created the same lens manually to see what it looked like
    # From the prescription, valid only at 405 nm.
    asl5040 = MatrixGroup()

    asl5040.append(DielectricInterface(R=17.37,n1=1.0, n2=materials.FusedSilica.n(0.405), diameter=50))
    asl5040.append(Space(d=29.85, n=materials.FusedSilica.n(0.405)))
    asl5040.append(DielectricInterface(R=float("+inf"),n1=materials.FusedSilica.n(0.405),n2=1.0,diameter=50))

    # The calculated focal length is not 40 mm, it is rather 36.99, probably
    # because I do not consider the real, complete surface I only approximate
    # with a spherical surface
    print("We expect f=40mm from the specs if we use the full surface")
    print("f_e = {0}".format(asl5040.effectiveFocalLengths()))
    print("FFL = {0}".format(asl5040.frontFocalLength()))
    print("BFL = {0}".format(asl5040.backFocalLength()))


    collimationPath = ImagingPath(label="Lens constructed manually")
    # Start at front focal spot where we would put the source to collimate
    collimationPath.append(Space(d=asl5040.frontFocalLength()))
    collimationPath.append(asl5040)
    collimationPath.append(Space(d=50))
    # Again, I fixed the bug and will release a new version today or tomorrow.
    # I included the graph in the email I sent you. It looks the same and behaves as expected
    collimationPath.display(ObjectRays(diameter=1, halfAngle=0.5,H=5,T=5))
    
class TestDisplay(envtest.RaytracingTestCase):
    def testIfFixedDoesNotCrash(self):
        exampleCodeThatUsedToCrashe()


if __name__ == '__main__':
    envtest.main()

