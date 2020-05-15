from raytracing import ImagingPath, Space, Lens, Aperture

'''
    Demo #9 - Infinite telecentric 4f telescope
'''


path = ImagingPath()
path.label = "Demo #9: Infinite telecentric 4f telescope"
path.append(Space(d=5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=5))
path.display()
