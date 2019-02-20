from .abcd import *
from .thorlabs import *

class EO_33_921(DoubletAchromatLens):
    # Stock number #33-921 
    def __init__(self):
        super(EO_33_921,self).__init__(fa=100.00,fb=78.32, R1=64.67,R2=-64.67, R3=-343.59, 
                                    tc1=26.00, tc2=12.7, n1=1.6700, n2=1.8467, diameter=75)

class EO_88_593(DoubletAchromatLens):
    # Stock number #88-593  
    def __init__(self):
        super(EO_88_593,self).__init__(fa=200.00,fb=187.69, R1=118.81, R2=-96.37, R3=-288.97, 
                                    tc1=17.94, tc2=6.00, n1=1.5168, n2=1.6727, diameter=75)

