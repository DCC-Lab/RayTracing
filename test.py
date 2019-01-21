import ABCD as rt

path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5, diameter=2.5))
path.append(rt.Space(d=12))
path.append(rt.Lens(f=7))
path.append(rt.Space(d=10))
path.display()
