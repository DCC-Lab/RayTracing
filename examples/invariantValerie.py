import envexamples  # modifies path
from raytracing import *

path = ImagingPath()
path.append(Space(d=10))
path.append(Lens(f=10, diameter=30))
path.append(Space(d=20))
path.append(Aperture(diameter=10))
path.display()

path2 = ImagingPath()
path2.append(Space(d=10))
path2.append(Lens(f=10, diameter=30))
path2.append(Space(d=20))
path2.display()