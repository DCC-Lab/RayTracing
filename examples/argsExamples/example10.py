from raytracing import ImagingPath, Space, Lens, Aperture

'''
    Demo #10 - A retrofocus has a back focal length longer than the effective focal length. It comes from a diverging lens followed by a converging
    lens. We can always obtain the effective focal lengths and the back focal length of a system.
'''


path = ImagingPath()
path.fanAngle = 0.05
path.append(Space(d=20))
path.append(Lens(f=-10, label='Div'))
path.append(Space(d=7))
path.append(Lens(f=10, label='Foc'))
path.append(Space(d=40))
(focal, focal) = path.effectiveFocalLengths()
bfl = path.backFocalLength()
path.label = "Demo #10: Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}".format(focal, bfl)
path.display()
