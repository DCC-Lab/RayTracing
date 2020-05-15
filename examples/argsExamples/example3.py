from raytracing import ImagingPath, Space, Lens

'''Demo #3: A finite lens
   An object at z=0 (front edge) is used with default properties (see Demo #1). Notice the aperture stop (AS)
   identified at the lens which blocks the cone of light. There is no field stop to restrict the field of view,
   which is why we must use the default object and cannot restrict the field of view. Notice how the default
   rays are blocked.'''


path = ImagingPath()
path.label = "Demo #3: Finite lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=3))
path.append(Space(d=17))
path.display()
