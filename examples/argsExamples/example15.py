from raytracing import ImagingPath, Space, Lens, olympus

'''
#DEMO 15 - Path with LUMPlanFL40X
'''


path = ImagingPath()
path.fanAngle = 0.0
path.fanNumber = 1
path.rayNumber = 15
path.objectHeight = 10.0
path.label = "Demo #15 Path with LUMPlanFL40X"
path.append(Space(180))
path.append(olympus.LUMPlanFL40X())
path.display()