from .abcd import *
from .lens import *
from .materials import *

class ACN254_100_A(AchromatDoubletLens):
    def __init__(self):
        super(ACN254_100_A,self).__init__(fa=-100.0,fb=-103.6, R1=-52.0, R2=49.9, R3=600.0, 
                                    tc1=2.0, tc2=4.0, n1=N_BAK4.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254_100_A")

class ACN254_075_A(AchromatDoubletLens):
    def __init__(self):
        super(ACN254_075_A,self).__init__(fa=-75.1,fb=-78.8, R1=-39.0, R2=39.2, R3=489.8, 
                                    tc1=2.0, tc2=4.3, n1=N_BAK4.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254_075_A")

class ACN254_050_A(AchromatDoubletLens):
    def __init__(self):
        super(ACN254_050_A,self).__init__(fa=-50.0,fb=-53.2, R1=-34.0, R2=32.5, R3=189.2, 
                                    tc1=2.0, tc2=4.5, n1=N_BAF10.n(0.5876), n2=N_SF6HT.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254_050_A")

class ACN254_040_A(AchromatDoubletLens):
    def __init__(self):
        super(ACN254_040_A,self).__init__(fa=-40.1,fb=-43.6, R1=-27.1, R2=27.1, R3=189.2, 
                                    tc1=2.0, tc2=5.0, n1=N_BAF10.n(0.5876), n2=N_SF11.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254_040_A")


class AC254_030_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_030_A,self).__init__(fa=30.0,fb=22.9, R1=20.9, R2=-16.7, R3=-79.8, 
                                    tc1=12, tc2=2.0, n1=N_BAF10.n(0.5876), n2=N_SF6HT.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-030-A")

class AC254_035_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_035_A,self).__init__(fa=35.2,fb=27.3, R1=24.0, R2=-19.1, R3=-102.1, 
                                    tc1=12, tc2=2.0, n1=N_BAF10.n(0.5876), n2=N_SF6HT.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-035-A")

class AC254_040_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_040_A,self).__init__(fa=40.1,fb=33.4, R1=23.7, R2=-20.1, R3=-57.7, 
                                    tc1=12, tc2=2.0, n1=N_BK7.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-040-A")

class AC254_045_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_045_A,self).__init__(fa=45.0,fb=40.2, R1=31.2, R2=-25.90, R3=-130.6, 
                                    tc1=7, tc2=2.0, n1=N_BAF10.n(0.5876), n2=N_SF6HT.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-045-A")

class AC254_050_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_050_A,self).__init__(fa=50.2,fb=43.4, R1=33.3,R2=-22.28, R3=-291.07, 
                                    tc1=9, tc2=2.5, n1=N_BAF10.n(0.5876), n2=N_SF10.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-050-A")


class AC254_060_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_060_A,self).__init__(fa=60.1,fb=54.3, R1=41.7,R2=-25.9, R3=-230.7, 
                                    tc1=8, tc2=2.5, n1=E_BAF11.n(0.5876), n2=E_FD10.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_060_A")

class AC254_075_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_075_A,self).__init__(fa=74.9,fb=70.3, R1=46.5,R2=-33.9, R3=-95.5, 
                                    tc1=7.0, tc2=2.5, n1=N_BK7.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_075_A")

class AC254_080_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_080_A,self).__init__(fa=80.0,fb=75.3, R1=49.6,R2=-35.5, R3=-101.2, 
                                    tc1=7.0, tc2=3.0, n1=N_BK7.n(0.5876), n2=N_SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_080_A")

class AC254_100_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_100_A,self).__init__(fa=100.1,fb=97.1, R1=62.8,R2=-45.7, R3=-128.2, 
                                    tc1=4.0, tc2=2.5, n1=N_BK7.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_100_A")

class AC254_125_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_125_A,self).__init__(fa=125.0,fb=122.0, R1=77.6,R2=-55.9, R3=-160.8, 
                                    tc1=4.0, tc2=2.8, n1=N_BK7.n(0.5876), n2=N_SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_125_A")

class AC254_150_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_150_A,self).__init__(fa=150,fb=-146.1, R1=91.6,R2=-66.7, R3=-197.7, 
                                    tc1=5.7, tc2=2.2, n1=N_BK7.n(0.5876), n2=SF5.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_150_A")

class AC254_200_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_200_A,self).__init__(fa=200.2,fb=194.0, R1=77.4,R2=-87.6, R3=291.1, 
                                    tc1=4.0, tc2=2.5, n1=N_SSK5.n(0.5876), n2=LAFN7.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_200_A")

class AC254_250_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_250_A,self).__init__(fa=250,fb=246.7, R1=137.1,R2=-111.5, R3=-459.2, 
                                    tc1=4.0, tc2=2.0, n1=N_BK7.n(0.5876), n2=SF2.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_250_A")

class AC254_300_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_300_A,self).__init__(fa=300.2,fb=297.0, R1=165.2,R2=-137.1, R3=-557.4, 
                                    tc1=4.0, tc2=2.0, n1=N_BK7.n(0.5876), n2=SF2.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_300_A")

class AC254_400_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_400_A,self).__init__(fa=399.3,fb=396.0, R1=219.8,R2=-181.6, R3=-738.5, 
                                    tc1=4.0, tc2=2.0, n1=N_BK7.n(0.5876), n2=SF2.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_400_A")

class AC254_500_A(AchromatDoubletLens):
    def __init__(self):
        super(AC254_500_A,self).__init__(fa=502.5,fb=499.9, R1=337.3,R2=-186.8, R3=-557.4, 
                                    tc1=4.0, tc2=2.0, n1=N_BK7.n(0.5876), n2=SF2.n(0.5876), diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254_500_A")


