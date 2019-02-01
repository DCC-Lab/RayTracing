# The ABCD module needs to be installed in your "site" path.
# Type: python -m site --user-site
# to see what this directory is (mine on macOS is /Users/dccote/.local/lib/python3.6/site-packages)

from ABCD import *

path = OpticalPath()
path.name = "Systeme 4f, objet de 1 cm, petites lentilles"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=2.5))
path.append(Space(d=10))
path.display()
#path.save('object-smallLenses.png')

path = OpticalPath()
path.name = "Systeme 4f, objet de 1 cm, petite lentille suivi de grande lentille"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=5))
path.append(Space(d=10))
path.display()
#path.save('object-smallLargeLenses.png')

path = OpticalPath()
path.name = "Systeme 4f, champ de vue, petites lentilles"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=2.5))
path.append(Space(d=10))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
#path.save('fov-smallLenses.png', onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)

path = OpticalPath()
path.name = "Systeme 4f, champ de vue, petite lentille suivi de grande lentille"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=5.0))
path.append(Space(d=10))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
#path.save('fov-smallLargeLenses.png', onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)

path = OpticalPath()
path.name = "Systeme 4f, champ de vue, grandes lentilles"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=5.0))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=5.0))
path.append(Space(d=10))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
#path.save('fov-largeLenses.png', onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
