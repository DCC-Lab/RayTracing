from raytracing import ImagingPath, Space, Lens, LaserPath, DielectricSlab, CurvedMirror

'''Demo #19 - Calculation of cavity laser modes'''


cavity = LaserPath(label="Laser cavity: round trip\nCalculated laser modes")
cavity.isResonator = True
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))
cavity.append(CurvedMirror(R=400))
cavity.append(Space(d=160))
cavity.append(DielectricSlab(thickness=100, n=1.8))
cavity.append(Space(d=160))
cavity.display()