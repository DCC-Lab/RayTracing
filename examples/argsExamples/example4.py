from raytracing import ImagingPath, Space, Lens, Aperture

'''Demo #4 - Aperture behind lens
Notice the aperture stop (AS) identified after the lens, not at the lens. Again, since there is no field stop,
we cannot restrict the object to the field of view because it is infinite.'''


path = ImagingPath()
path.label = "Demo #4: Aperture behind lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=3))
path.append(Space(d=3))
path.append(Aperture(diameter=3))
path.append(Space(d=17))
path.display()