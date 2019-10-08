from raytracing import *

inputBeam = GaussianBeam(w=5)
beamAfterLens = Lens(f=100)*inputBeam
zo = beamAfterLens.zo
delta = zo / 100
path = LaserPath()
path.append(Lens(f=100))
path.append(Space(d=100-delta))
N = 1000
for i in range(2*N):
	path.append(Space(d=delta/N))

trace = path.trace(inputRay=inputBeam)

fig, axes = plt.subplots(figsize=(10, 7))
axes.set(xlabel='Distance', ylabel='Radius')
axes.set_xlim(100-delta,100+delta)

x = []
y = []
for q in trace:
    x.append(q.z)
    y.append(q.R)
axes.plot(x, y, 'r', linewidth=1)
plt.show()

# for beam in trace:
# 	print(beam.z, beam.R)

#path.display()