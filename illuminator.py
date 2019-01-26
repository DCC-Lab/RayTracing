import ABCD as rt

path = rt.OpticalPath()
path.name = "Kohler illumination"
path.objectHeight = 1.0
path.fanAngle = 0.5
path.rayNumber = 5
path.append(rt.Space(d=4))
path.append(rt.Lens(f=4,diameter=2.5))
path.append(rt.Space(d=4+25))
path.append(rt.Lens(f=25, diameter=7.5))
path.append(rt.Space(d=25))

path.append(rt.Space(d=9))
path.append(rt.Lens(f=9, diameter=8))
path.append(rt.Space(d=9))

path.display()
