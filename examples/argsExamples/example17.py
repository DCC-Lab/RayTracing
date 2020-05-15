from raytracing import ImagingPath, Space, Lens, thorlabs, eo, olympus

'''
Demo #17 - Vendor Lenses
'''


path = ImagingPath()
path.label = "Demo #17: Vendor Lenses"
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=50))
path.append(thorlabs.AC254_050_A())
path.append(Space(d=150))
path.append(eo.PN_33_921())
path.append(Space(d=50))
path.append(eo.PN_88_593())
path.append(Space(180))
path.append(olympus.LUMPlanFL40X())
path.append(Space(10))
path.display()
