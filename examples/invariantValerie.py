import envexamples  # modifies path
from raytracing import *

path = ImagingPath()
path.append(System4f(f1=10, diameter1=50, f2=20, diameter2=50))
path.reportEfficiency()
path.display()

path2 = ImagingPath()
path2.append(System4f(f1=10, diameter1=50, f2=20, diameter2=20))
path2.reportEfficiency()
path2.display()