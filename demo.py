from ABCD import *

path = OpticalPath()
path.name = "Object at 2f, image at 2f"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
#path.save('Figure1.png')

path = OpticalPath()
path.name = "Object at 4f, image at 4f/3"
path.append(Space(d=20))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
#path.save('Figure2.png')

path = OpticalPath()
path.name = "4f system"
path.append(Space(d=5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=5))
path.display()
#path.save('Figure3.png')

path = OpticalPath()
path.fanAngle = 0.1
path.append(Space(d=40))
path.append(Lens(f=-10, label='Div'))
path.append(Space(d=4))
path.append(Lens(f=5, label='Foc'))
path.append(Space(d=18))
focal = -1.0/path.transferMatrix().C
path.name = "Retrofocus system with f={0:.2f} cm".format(focal)
path.display()

path = OpticalPath()
path.name = "Microscope system"
path.objectHeight = 0.1
path.append(Space(d=1))
path.append(Lens(f=1, diameter=0.8, label='Obj'))
path.append(Space(d=19))
path.append(Lens(f=18,diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.append(Aperture(diameter=2))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
(r1,r2) = path.marginalRays(y=0)
print(r1, r2)


M1 = Space(d=10)
M2 = Lens(f=5)
M3 = M2*M1
print(M3.forwardConjugate())


M1 = Space(d=10)
M2 = Lens(f=5)
M3 = M1*M2
print(M3.backwardConjugate())
