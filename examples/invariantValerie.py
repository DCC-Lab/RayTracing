import envexamples  # modifies path
from raytracing import *

"""
The Lagrange invariant is a constant defining the collection efficiency of an optical system. The Lagrange 
invariant is calculated using the principal and axial rays, whether the optical invariant is calculated with
anyother combination of rays. This code uses the optical invariant to characterise the ray transmission in a
4f system and shows that the optical invariant is greatly affected by the used optics. Indeed, changing the
diameter of the first lens affects the number of detected rays at the imaged plane. 
"""

path = ImagingPath()
path.append(System4f(f1=10, diameter1=25.4, f2=20, diameter2=25.4))
path.reportEfficiency()
path.display()

path2 = ImagingPath()
path2.append(System4f(f1=10, diameter1=12.7, f2=20, diameter2=25.4))
path2.reportEfficiency()
path2.display()