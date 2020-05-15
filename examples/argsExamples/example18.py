from raytracing import ImagingPath, Space, Lens, LaserPath, thorlabs, eo, olympus


'''
Demo #18: Laser beam and vendor lenses
'''


path = LaserPath()
path.label = "Demo #18: Laser beam and vendor lenses"
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=150))
path.append(eo.PN_33_921())
path.append(Space(d=50))
path.append(eo.PN_88_593())
path.append(Space(d=180))
path.append(olympus.LUMPlanFL40X())
path.append(Space(d=10))
path.display()
