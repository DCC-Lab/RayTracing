from raytracing import ImagingPath, Space, Lens, Aperture, DielectricSlab

'''
    Demo #7: Focussing through a dielectric slab
'''


path = ImagingPath()
path.label = "Demo #7: Focussing through a dielectric slab"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=3))
path.append(DielectricSlab(n=1.5, thickness=4))
path.append(Space(d=10))
path.display()
