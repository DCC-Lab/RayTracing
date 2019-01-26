import ABCD as rt

path = rt.OpticalPath()
path.name = "Object at 2f, image at 2f"
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=10))
path.display()
#path.save('Figure1.png')

path = rt.OpticalPath()
path.name = "Object at 4f, image at 4f/3"
path.append(rt.Space(d=20))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=10))
path.display()
#path.save('Figure2.png')

path = rt.OpticalPath()
path.name = "4f system"
path.append(rt.Space(d=5))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=5))
path.display()
#path.save('Figure3.png')

path = rt.OpticalPath()
path.name = "Microscope system"
path.objectHeight = 0.1
path.append(rt.Space(d=1))
path.append(rt.Lens(f=1,label='Obj'))
path.append(rt.Space(d=19))
path.append(rt.Lens(f=18,label='Tube Lens'))
path.append(rt.Space(d=18))
path.display()

#path.save('Figure4.png')

path = rt.OpticalPath()
path.fanAngle = 0.1
path.append(rt.Space(d=40))
path.append(rt.Lens(f=-10, label='Div'))
path.append(rt.Space(d=4))
path.append(rt.Lens(f=5, label='Foc'))
path.append(rt.Space(d=18))
focal = -1.0/path.transferMatrix().C
path.name = "Retrofocus system with f={0:.2f} cm".format(focal)
path.display()

