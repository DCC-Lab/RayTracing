from ABCD import *

# Object at 2f, image at 2f.
path = OpticalPath()
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
