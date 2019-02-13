from raytracing import *

path = ImagingPath()
path.label = "Object at 2f, image at 2f"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
#path.save('Figure1.png')

path = ImagingPath()
path.label = "Object at 4f, image at 4f/3"
path.append(Space(d=20))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
#path.save('Figure2.png')

path = ImagingPath()
path.label = "Object at 4f, virtual image at"
path.append(Space(d=2.5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
#path.save('Figure2.png')

path = ImagingPath()
path.label = "4f system"
path.append(Space(d=5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=5))
path.display()
#path.save('Figure3.png')

path = ImagingPath()
path.fanAngle = 0.1
path.append(Space(d=40))
path.append(Lens(f=-10, label='Div'))
path.append(Space(d=4))
path.append(Lens(f=5, label='Foc'))
path.append(Space(d=18))
focal = -1.0/path.transferMatrix().C
path.label = "Retrofocus system with f={0:.2f} cm".format(focal)
path.display()

path = ImagingPath()
path.label = "Thick diverging lens"
path.objectHeight = 20
path.append(Space(d=50))
path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
path.append(Space(d=50))
path.display(onlyChiefAndMarginalRays=True)

path = ImagingPath()
path.label = "Thick diverging lens, made with individual elements"
path.objectHeight = 20
path.append(Space(d=50))
path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
path.append(Space(d=10, diameter=25, label='Lens'))
path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
path.append(Space(d=50))
path.display(onlyChiefAndMarginalRays=True)

path = ImagingPath()
path.label = "Microscope system"
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
