from raytracing import ImagingPath, Space, Lens, Aperture


'''
    Demo #8: Virtual image at -2f with object at f/2
'''


path = ImagingPath()
path.label = "Demo #8: Virtual image at -2f with object at f/2"
path.append(Space(d=2.5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()

