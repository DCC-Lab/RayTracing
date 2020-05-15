from raytracing import ImagingPath, Space, Lens

'''Demo #2 - Two lenses, infinite diameters
An object at z=0 (front edge) is used with default properties (see Demo #1).'''


path = ImagingPath()
path.label = "Demo #2: Two lenses, infinite diameters"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=20))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()

