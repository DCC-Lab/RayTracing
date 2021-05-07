# Documents & Examples

## Documentation

All the documentation is [available online](https://raytracing.readthedocs.io/). 

The class hierarchy for optical elements (with parameters and defaults) is:

![class](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/hierarchy.png)

You may obtain help by:

1. Reading the documentation for the code ([API reference](https://raytracing.readthedocs.io/en/latest/reference.html)).
   1. Core: 
      1. `Ray`: a ray for geometrical optics with a height and angle $y$ and $\theta$.
      2. `Rays`: ray distributions to ray trace an object through the optical system.
         1.  `UniformRays`, `RandomUniformRays`, `LambertianRays` and `RandomLambertianRays` are currently available.  See example above.
      3. `GaussianBeam`: a gaussian laser beam with complex radius of curvature $q$.
      4. `Matrix`: any 2x2 matrix.
      5. `MatrixGroup`: treats a group of matrix as a unit (draws it as a unit too)
      6. `ImagingPath`: A `MatrixGroup` with an object at the front for geometrical optics 
      7. `LaserPath`: A `MatrixGroup` with a laser beam input at the front or a Resonator.
   2. Optical elements: `Aperture`, `Space`, `Lens`, `DielectricInterface`, `DielectricSlab`, `ThickLens`
   3. Specialty lenses: Defines a general achromat and objective lens
   4. Thorlabs lenses: Achromat doublet lenses from Thorlabs.
   5. Edmund Optics lenses: Achromat doublet lenses from Edmund Optics
   6. Olympus objectives: A few objectives from Olympus.
   7. Glasses: A few glasses used by Thorlabs to make achromatic doublets. They all have a single function `n(wavelength)` that returns the index at that wavelength.  All data obtained from http://refractiveindex.info.
   8. Zemax ZMX file reader: to read text-based Zemax files of lenses.
2. typing (interactively): `help(Matrix)`,`help(MatrixGroup)` `help(Ray)`,`help(ImagingPath)` to get the API, 
3. look at the examples with `python -m raytracing` 
4. simply look at the code.

```python
python
>>> help(Matrix)
Help on class Matrix in module raytracing.abcd:

class Matrix(builtins.object)
 |  Matrix(A, B, C, D, physicalLength=0, apertureDiameter=inf, label='')
 |  
 |  A matrix and an optical element that can transform a ray or another
 |  matrix.
 |  
 |  The general properties (A,B,C,D) are defined here. The operator "*" is
 |  overloaded to allow simple statements such as:
 |  
 |  ray2 = M1 * ray
 |  or
 |  M3 = M2 * M1
 |  
 |  The physical length is included in the matrix to allow simple management of
 |  the ray tracing. IF two matrices are multiplied, the resulting matrice
 |  will have a physical length that is the sum of both matrices.
 |  
 |  In addition finite apertures are considered: if the apertureDiameter
 |  is not infinite (default), then the object is assumed to limit the
 |  ray height to plus or minus apertureDiameter/2 from the front edge to the back
 |  edge of the element.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, A, B, C, D, physicalLength=0, apertureDiameter=inf, label='')
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __mul__(self, rightSide)
 |      Operator overloading allowing easy to read matrix multiplication
 |      
 |      For instance, with M1 = Matrix() and M2 = Matrix(), one can write
 |      M3 = M1*M2. With r = Ray(), one can apply the M1 transform to a ray
 |      with r = M1*r
 |  
 |  __str__(self)
 |      String description that allows the use of print(Matrix())
 |  
 |  backwardConjugate(self)
 |      With an image at the back edge of the element,
 |      where is the object ? Distance before the element by
 |      which a ray must travel to reach the conjugate plane at
 |      the back of the element. A positive distance means the
 |      object is "distance" in front of the element (or to the
 |      left, or before).
 |      
 |      M2 = M1*Space(distance)
 |      # M2.isImaging == True

```

## Examples

You can list several examples `python -m raytracing -l`:

```shell
All example code on your machine is found at: /somedirectory/on/your/machine
 1. ex01.py A single lens f = 50 mm, infinite diameter
 2. ex02.py Two lenses, infinite diameters
 3. ex03.py Finite-diameter lens
 4. ex04.py Aperture behind lens acting as Field Stop
 5. ex05.py Simple microscope system
 6. ex06.py Kohler illumination
 7. ex07.py Focussing through a dielectric slab
 8. ex08.py Virtual image at -f with object at f/2
 9. ex09.py Infinite telecentric 4f telescope
10. ex10.py Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}
11. ex11.py Thick diverging lens computed from the Lensmaker equation
12. ex12.py Thick diverging lens built from individual elements
13. ex13.py Obtain the forward and backward conjugates
14. ex14.py Generic objectives
15. ex15.py Model Olympus objective LUMPlanFL40X
16. ex16.py Commercial doublets from Thorlabs and Edmund
17. ex17.py An optical system with vendor lenses
18. ex18.py Laser beam and vendor lenses
19. ex19.py Cavity round trip and calculated laser modes
.... and more complete examples at /somedirectory/on/your/machine
```

 You can run them all with `python -m raytracing -e all` (see them all below) to get a flavour of what is possible (note: in the US, it will give you a flavor of what is possible instead). Notice the command will tell you where the directory with all the tests is on your machine. **You will find more complete examples** in that [examples](https://github.com/DCC-Lab/RayTracing/tree/master/raytracing/examples) directory, distributed with the module.  For instance, `illuminator.py` to see a Kohler illuminator, and `invariant.py` to see an example of the role of lens diameters to determine the field of view.



![ex01](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex01.png)

![ex02](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex02.png)

![ex03](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex03.png)

![ex04](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex04.png)

![ex05](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex05.png)

![ex06](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex06.png)

![ex07](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex07.png)

![ex08](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex08.png)

![ex09](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex09.png)

![ex10](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex10.png)

![ex11](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex11.png)

![ex12](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex12.png)

![ex14](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex14.png)

![ex15](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex15.png)

![ex16.1](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.1.png)

![ex16.2](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.2.png)

![ex16.3](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex16.3.png)

![ex17](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex17.png)

![ex18](https://github.com/DCC-Lab/RayTracing/raw/master/README.assets/ex18.png)