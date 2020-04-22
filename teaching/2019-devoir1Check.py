import sys
import os
sys.path.insert(0, os.path.abspath('../'))

import ABCD as rt
import devoir1Sol as dev

flatAirGlassInterface = dev.DielectricInterface(n1=1.0, n2=1.55,R=float('+Inf'))
flatGlassAirInterface = dev.DielectricInterface(n1=1.55, n2=1.0,R=float('+Inf'))
convexAirGlassInterface = dev.DielectricInterface(n1=1.0, n2=1.55,R=5.0)
concaveAirGlassInterface = dev.DielectricInterface(n1=1.0, n2=1.55,R=-5.0)
convexGlassAirInterface = dev.DielectricInterface(n1=1.55, n2=1.0,R=5.0)
concaveGlassAirInterface = dev.DielectricInterface(n1=1.55, n2=1.0,R=-5.0)

parallelRay = rt.Ray(y=1, theta=0)
obliqueRay = rt.Ray(y=1, theta=0.1)
onAxisRay = rt.Ray(y=0, theta=0)
obliqueFromAxis = rt.Ray(y=0, theta=0.1)


# Un rayon parallel a l'axe ressort parallele sur une interface rayon courb ure infini ('flat')
checkParallel = flatAirGlassInterface*parallelRay
if checkParallel.theta == parallelRay.theta and checkParallel.y == parallelRay.y:
	print("Check")
else:
	print("Test #1 erreur: diel + space not consistent") 

checkParallel = flatGlassAirInterface*parallelRay
if checkParallel.theta == parallelRay.theta and checkParallel.y == parallelRay.y:
	print("Check")
else:
	print("Test #2 erreur: diel + space not consistent") 

checkCurveDown = flatAirGlassInterface*obliqueRay
if checkCurveDown.theta < obliqueRay.theta and checkCurveDown.y == obliqueRay.y:
	print("Check")
else:
	print("Test #3 erreur: diel + space not consistent") 

checkCurveUp = flatGlassAirInterface*obliqueRay
if checkCurveUp.theta > obliqueRay.theta and checkCurveUp.y == obliqueRay.y:
	print("Check")
else:
	print("Test #4 erreur: diel + space not consistent") 

# Un rayon parallel a l'axe courbera vers l'axe avec une interface convexe air-verre
checkCurveDown = convexAirGlassInterface*parallelRay
if checkCurveDown.theta < 0 and checkCurveDown.y == parallelRay.y:
	print("Check")
else:
	print("Test #5 erreur: curved dielectric not correct") 

checkCurveDown = convexGlassAirInterface*parallelRay
if checkCurveDown.theta > 0 and checkCurveDown.y == parallelRay.y:
	print("Check")
else:
	print("Test #6 erreur: curved dielectric not correct") 


M1 = dev.DielectricInterface(n1=1.0, n2=1.55,R=5.0)
M2 = rt.Space(d=2)
M3 = dev.DielectricInterface(n1=1.55, n2=1.0,R=-5.0)
lens1 = M3*M2*M1
lens2 = dev.ThickLens(n=1.55, R1=5.0, R2=-5.0,thickness=2.0)

if lens1.C == lens2.C:
	print("Check")
else:
	print("Erreur: diel + space not consistent") 


thinLens1 = M3*M1
thinLens2 = rt.Lens(f=10.0)

if lens1.C == lens2.C:
	print("Check")
else:
	print("Erreur: diel + space not consistent") 

