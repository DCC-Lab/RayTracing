from .abcd import *
from .objectives import *
from .axicon import *

path = ImagingPath()
path.label = "Demo #1: lens f = 5cm, infinite diameter"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display(comments= """Demo #1: lens with f=5 cm, infinite diameter

An object at z=0 (front edge) is used. It is shown in blue. The image (or any intermediate images) are shown in red.\n\
This will use the default objectHeight and fanAngle but they can be changed with:
path.objectHeight = 1.0
path.fanAngle = 0.5
path.fanNumber = 5
path.rayNumber = 3

Code:
path = ImagingPath()
path.label = "Demo #1: lens f = 5cm, infinite diameter"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
""")

path = ImagingPath()
path.label = "Demo #2: Two lenses, infinite diameters"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=20))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display(comments="""Demo #2: Two lenses, infinite diameters
An object at z=0 (front edge) is used with default properties (see Demo #1).

Code:
path = ImagingPath()
path.label = "Demo #2: Two lenses, infinite diameters"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=20))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
""")
# or
#path.save("Figure 2.pdf")

path = ImagingPath()
path.label = "Demo #3: Finite lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=3))
path.append(Space(d=17))
path.display(comments="""Demo #3: A finite lens
An object at z=0 (front edge) is used with default properties (see Demo #1). Notice the aperture stop (AS)
identified at the lens which blocks the cone of light. There is no field stop to restrict the field of view,
which is why we must use the default object and cannot restrict the field of view. Notice how the default
rays are blocked.

path = ImagingPath()
path.objectHeight = 1.0    # object height (full).
path.objectPosition = 0.0  # always at z=0 for now.
path.fanAngle = 0.5        # full fan angle for rays
path.fanNumber = 9         # number of rays in fan
path.rayNumber = 3         # number of points on object
path.label = "Demo #3: Finite lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=3))
path.append(Space(d=17))
path.display()
""")

path = ImagingPath()
path.label = "Demo #4: Aperture behind lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=3))
path.append(Space(d=3))
path.append(Aperture(diameter=3))
path.append(Space(d=17))
path.display(comments="""Demo #4: Aperture behind lens

Notice the aperture stop (AS) identified after the lens, not at the lens. Again, since there is no field stop,
we cannot restrict the object to the field of view because it is infinite.

Code:
path = ImagingPath()
path.label = "Demo #4: Aperture behind lens"
path.append(Space(d=10))
path.append(Lens(f=5, diameter=3))
path.append(Space(d=3))
path.append(Aperture(diameter=3))
path.append(Space(d=17))
path.display()
""")

path = ImagingPath()
path.label = "Demo #5: Simple microscope system"
path.fanAngle = 0.1        # full fan angle for rays
path.fanNumber = 5         # number of rays in fan
path.rayNumber = 5         # number of points on object
path.append(Space(d=4))
path.append(Lens(f=4, diameter=0.8, label='Obj'))
path.append(Space(d=4 + 18))
path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.display(limitObjectToFieldOfView=True, comments="""# Demo #5: Simple microscope system
The aperture stop (AS) is at the entrance of the objective lens, and the tube lens, in this particular microscope, is 
the field stop (FS) and limits the field of view. Because the field stop exists, we can use limitObjectToFieldOfView=True
when displaying, which will set the objectHeight to the field of view, but will still trace all the rays using our parameters.

path = ImagingPath()
path.label = "Demo #5: Simple microscope system"
path.fanAngle = 0.1        # full fan angle for rays
path.fanNumber = 5         # number of rays in fan
path.rayNumber = 5         # number of points on object
path.append(Space(d=4))
path.append(Lens(f=4, diameter=0.8, label='Obj'))
path.append(Space(d=4 + 18))
path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.display()
""")

path = ImagingPath()
path.label = "Demo #6: Simple microscope system, only principal rays"
path.append(Space(d=4))
path.append(Lens(f=4, diameter=0.8, label='Obj'))
path.append(Space(d=4 + 18))
path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True, 
	comments="""# Demo #6: Simple microscope system, only principal rays
The aperture stop (AS) is at the entrance of the objective lens, and the tube lens, in this particular microscope, is 
the field stop (FS) and limits the field of view. Because the field stop exists, we can use limitObjectToFieldOfView=True
when displaying, which will set the objectHeight to the field of view. We can also require that only the principal rays are drawn: chief ray
marginal ray (or axial ray).

path = ImagingPath()
path.label = "Demo #6: Simple microscope system, only principal rays"
path.append(Space(d=4))
path.append(Lens(f=4, diameter=0.8, label='Obj'))
path.append(Space(d=4 + 18))
path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
path.append(Space(d=18))
path.display()
""")

path = ImagingPath()
path.label = "Demo #7: Focussing through a dielectric slab"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=3))
path.append(DielectricSlab(n=1.5, thickness=4))
path.append(Space(d=10))
path.display(comments=path.label+"""\n
path = ImagingPath()
path.label = "Demo #7: Focussing through a dielectric slab"
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=3))
path.append(DielectricSlab(n=1.5, thickness=4))
path.append(Space(d=10))"""
)

# Demo #8: Virtual image
path = ImagingPath()
path.label = "Demo #8: Virtual image at -2f with object at f/2"
path.append(Space(d=2.5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display(comments=path.label+"""\n
path = ImagingPath()
path.label = "Demo #8: Virtual image at -2f with object at f/2"
path.append(Space(d=2.5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()""")

# Demo #9: Infinite telecentric 4f telescope
path = ImagingPath()
path.label = "Demo #9: Infinite telecentric 4f telescope"
path.append(Space(d=5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=5))
path.display(comments=path.label+"""\n
path = ImagingPath()
path.label = "Demo #9: Infinite telecentric 4f telescope"
path.append(Space(d=5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.append(Lens(f=5))
path.append(Space(d=5))
""")

path = ImagingPath()
path.fanAngle = 0.05
path.append(Space(d=20))
path.append(Lens(f=-10, label='Div'))
path.append(Space(d=7))
path.append(Lens(f=10, label='Foc'))
path.append(Space(d=40))
(focal,focal) = path.effectiveFocalLengths()
bfl = path.backFocalLength()
path.label = "Demo #10: Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}".format(focal, bfl)
path.display(comments=path.label+"""\n
A retrofocus has a back focal length longer than the effective focal length. It comes from a diverging lens followed by a converging
lens. We can always obtain the effective focal lengths and the back focal length of a system.

path = ImagingPath()
path.fanAngle = 0.05
path.append(Space(d=20))
path.append(Lens(f=-10, label='Div'))
path.append(Space(d=7))
path.append(Lens(f=10, label='Foc'))
path.append(Space(d=40))
(focal,focal) = path.effectiveFocalLengths()
bfl = path.backFocalLength()
path.label = "Demo #10: Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}".format(focal, bfl)
path.display()
""")

# Demo #11: Thick diverging lens
path = ImagingPath()
path.label = "Demo #11: Thick diverging lens"
path.objectHeight = 20
path.append(Space(d=50))
path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
path.append(Space(d=50))
path.display(onlyChiefAndMarginalRays=True, comments=path.label+"""\n
path = ImagingPath()
path.label = "Demo #11: Thick diverging lens"
path.objectHeight = 20
path.append(Space(d=50))
path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
path.append(Space(d=50))
path.display()""")

# Demo #12: Thick diverging lens built from individual elements
path = ImagingPath()
path.label = "Demo #12: Thick diverging lens built from individual elements"
path.objectHeight = 20
path.append(Space(d=50))
path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
path.append(Space(d=10, diameter=25, label='Lens'))
path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
path.append(Space(d=50))
path.display(onlyChiefAndMarginalRays=True, comments=path.label+"""\n
path = ImagingPath()
path.label = "Demo #12: Thick diverging lens built from individual elements"
path.objectHeight = 20
path.append(Space(d=50))
path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
path.append(Space(d=10, diameter=25, label='Lens'))
path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
path.append(Space(d=50))
path.display()""")


# Demo #13, forward and backward conjugates
# We can obtain the position of the image for any matrix
# by using forwardConjugate(): it calculates the distance 
# after the element where the image is, assuming an object 
# at the front surface.
M1 = Space(d=10)
M2 = Lens(f=5)
M3 = M2*M1
print(M3.forwardConjugate())
print(M3.backwardConjugate())
