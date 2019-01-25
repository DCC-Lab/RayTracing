import ABCD as rt

# Object at 2f, image at 2f.
path = rt.OpticalPath()
path.append(rt.Space(d=10))
path.append(rt.Lens(f=5))
path.append(rt.Space(d=10))
path.display()
