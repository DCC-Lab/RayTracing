## Adding a new material to the Raytracing module

If you attempt to read a Zemax file with ZMXReader, you may encounter an error if the material is not recognized:

```shell
ValueError: The requested material 'SomeWeirdMaterial' is not recognized in the list of materials of raytracing: ['Air', 'N_BK7', 'N_SF2', 'N_SF8', 'SF2', 'SF5', 'N_SF5', 'N_SF6', 'N_SF6HT', 'N_SF10', 'N_SF11', 'N_SF57', 'N_BAF10', 'E_BAF11', 'N_BAK1', 'N_BAK4', 'FK51A', 'LAFN7', 'N_LASF9', 'N_LAK22', 'N_SSK5', 'E_FD10', 'FusedSilica'].  You need to implement it as asubclass of Material, see materials.py for examples.
```



The reason is that there are tons of materials available and it is ridiculous to enter them all ifthey are not used in optical components.  With the excellent http://refractiveindex.info, we are always just one click away from an answer. 

## How do you add a new material?

It is in fact quite simple:

1. Take a look at `materials.py` for many examples.

2. Derive a class from material, give it the name of your material (e.g., `N_LAK21`)

3. Then you need to define  `n()` and the Abbe number:

   ```python
   @classmethod
   def n(cls, wavelength): # Wavelengths are always in microns (like Zemax, refractiveindex.info, etc).
   		return calculate the value
   		
   @classmethod
   def abbeNumber(cls):
       return aValue		
   ```

4. All you need to define is in this example for N_BK7:

   ```python
   class N_BK7(Material):
       """ All data from https://refractiveindex.info/tmp/data/glass/schott/N-BK7.html """
       @classmethod
       def n(cls, wavelength):
           if wavelength > 10 or wavelength < 0.01:
               raise ValueError("Wavelength must be in microns")
           x = wavelength
   
           n=(1+1.03961212/(1-0.00600069867/x**2)+0.231792344/(1-0.0200179144/x**2)+1.01046945/(1-103.560653/x**2))**.5
           return n
       
       @classmethod
       def abbeNumber(cls):
           return 64.17
   ```

## Will Raytracing know about my new material?

Yes it will, through the magic of Python, it is possible to know when subclasses are created.

There are functions to find materials (such as `Material.findByName()` or `Material.findByIndex()`.  You actually don't need to include your code into the main raytracing code: if you derive a class from Material (as above) it will be included in the search without having to do anything.

You can then send it to us, we'll include it if it is relevant. Send to  dccote@cervo.ulaval.ca, or create an [Issue on GitHub](https://github.com/DCC-Lab/RayTracing/issues) and paste your code.

