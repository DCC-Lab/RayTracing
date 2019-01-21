import ABCD as rt

path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=20))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=10))
path.display()
