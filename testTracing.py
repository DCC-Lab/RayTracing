from raytracing import *
import numpy
import matplotlib.pyplot as plt

from matplotlib import pyplot as plt
import signal
import os

def sig(a, b):
    print("got sigint, exitting!")
    os._exit(0)

def timercb(e):
    print("timer")
signal.signal(signal.SIGINT, sig)


f = 50
f_obj = 5
f_tube = 100
f_galvo = 100
f_poly2 = 75
f_poly1 = 45



x = numpy.linspace(-20,20,21)
y = []

for d in x:
    nRays = 1000 # You can change this
    inputRays = RandomUniformRays(yMax=0.25e-3, maxCount=nRays) # at center
    outputRays = Rays() # output histogram

    path = OpticalPath()
    path.append(Space(d=d*1e-3))
    path.append(System2f(f=f_obj))    
    path.append(System4f(f1=f_tube,f2=f_galvo))
    path.append(System4f(f1=f_poly2,f2=f_poly1))
    path.append(Space(d=300))
    path.append(System2f(f=40))
    path.append(Aperture(diameter=40e-3))
    outputRays = path.traceManyThrough(inputRays,progress=False)
    y.append(outputRays.count/inputRays.count)
    print('.')
plt.plot(x,y)
plt.show(block=True)

