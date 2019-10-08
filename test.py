from raytracing import *

class ObjTest(Objective):
    """ Olympus UMPLanFN 20XW immersion objective

    Immersion not considered at this point.

    """
    def __init__(self):
        super(ObjTest, self).__init__(f=180 / 20,
                                         NA=0.5,
                                         focusToFocusLength=45,
                                         backAperture=5,
                                         workingDistance=3.5,
                                         label='UMPLFN20XW',
                                         url="https://www.olympus-lifescience.com/en/objectives/lumplfln-w/")

l = ObjTest()
path = ImagingPath()
path.append(Space(10))
path.append(l)
path.append(Space(10))

path.display(onlyChiefAndMarginalRays=True)
# inputBeam = GaussianBeam(w=5)
# beamAfterLens = Lens(f=100)*inputBeam
# zo = beamAfterLens.zo
# delta = zo / 100
# path = LaserPath()
# path.append(Lens(f=100))
# path.append(Space(d=100-delta))
# N = 1000
# for i in range(2*N):
# 	path.append(Space(d=delta/N))

# trace = path.trace(inputRay=inputBeam)

# fig, axes = plt.subplots(figsize=(10, 7))
# axes.set(xlabel='Distance', ylabel='Radius')
# axes.set_xlim(100-delta,100+delta)

# x = []
# y = []
# for q in trace:
#     x.append(q.z)
#     y.append(q.R)
# axes.plot(x, y, 'r', linewidth=1)
# plt.show()

# # for beam in trace:
# # 	print(beam.z, beam.R)

# #path.display()