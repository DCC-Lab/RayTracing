import ABCD as rt

path = rt.OpticalPath()
path.append(rt.Space(10))
path.append(rt.Lens(5))
path.append(rt.Space(20))
path.append(rt.Lens(5))
path.append(rt.Space(10))
path.append(rt.Space(10))
path.display()
