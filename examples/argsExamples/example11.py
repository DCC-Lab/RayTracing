from raytracing import ImagingPath, Space, ThickLens

'''
Demo #11: Thick diverging lens
'''


path = ImagingPath()
path.label = "Demo #11: Thick diverging lens"
path.objectHeight = 20
path.append(Space(d=50))
path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
path.append(Space(d=50))
path.display()
