from raytracing import *
from raytracing.thorlabs import *

#DielectricInterface(n1=1,n2=1.5, R=10).display()
thorlabs.AC508_150_B().display()

ThickLens(n=1.5, R1=10, R2=-20, thickness=4, label='Thick Lens').display()
eo.PN_33_921().display()
thorlabs.ACN254_075_A().display()
thorlabs.AC254_030_A().display()
thorlabs.AC254_075_A().display()
thorlabs.AC254_200_A().display()

Lens(f=10).display()