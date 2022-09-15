# Frequently Asked Questions



1. **What is the formalism used and where can I learn about it?**

   We use the ray matrix formalism and you can learn about it in most optics books as well as in the publication:

   > ["Tools and tutorial on practical ray tracing for microscopy"](https://doi.org/10.1117/1.NPh.8.1.010801) 
   >
   > by V. Pineau Noël\*, S. Masoumi\*, E. Parham*, G. Genest, L. Bégin, M.-A. Vigneault, D. C. Côté, 
   > Neurophotonics, 8(1), 010801 (2021). 
   > *Equal contributions.
   > Permalink: https://doi.org/10.1117/1.NPh.8.1.010801

   If you happen to speak French, D.C. Côté's Optique notes are available [online](https://books.apple.com/ca/book/optique/id949326768) and as PDF and there is a chapter on it.

2. **Can you do spherical aberrations?**

   No we cannot. It may appear at first sight that it is possible (we could easily correct the sinθ ≅ θ approximation when off-axis) but the ray matrix formalism does not allow us to consider the different propagation distances of the off-axis rays.  By definition, for exemple, a element of `Space` has a given length `d` and it is the same for all rays.  When considering spherical aberrations, this varying distance for rays that are off-axis is part of the aberration, which is not given solely by the correction to the angle.  Since we cannot have a different distance for all rays (i.e. it is a matrix multiplication), then spherical aberrations are not possible (as far as we know). ***You think we are wrong? Teach us how to do it!***

3. **Can you do chromatic aberrations?**

   Yes we can, when the lenses are built from dielectric interfaces and materials with `Materials`.  The Thorlabs and Edmund Optics lenses are built with a radius of curvature and the proper material as obtained from the excellent site http://refractiveindex.info.
   It is not possible however to consider chromatic aberrations for a thin lens. The thin lens is created directly with a given focal length and no material at all (it is infinitely thin). The focal length is fixed. To create a lens with chromatic aberration, you need to use `SingletLens` or `AchromaticDoubletLens`.
   
4. **Can I perform more complex calculations than just tracing rays?**
   Of course you can. Although the display functions are central to the module, you can also extract more information in a script.  For instance, the example [lsmConfocalPinhole.py](https://github.com/DCC-Lab/RayTracing/blob/master/raytracing/examples/fig6-lsmConfocalpinhole.py) is a good example where the transmission efficacy of a pinhole is calculated as a function of distance from the focal plane.

5. **Can you perform a 2D efficiency calculation that will apply to my real-life optical system?**
   Yes, but you need to use a ray distribution that considers the cylindrical symmetry (currently in preparation). This will provide proper numbers for the 2D energy efficiency, but it will not be "traceable" easily. To trace your rays, use the `RandomUniformRays` class for instance.

6. **There are stored preferences. Where are they?**
   Some variables can be "saved" into a Preferences file on disk.  Where it is depends on the platform. The file is always the same (it is a JSON dictionary) but the location is platform-specific:

   * macOS: `(username)/Library/Preferences/ca.dcclab.python.raytracing.json`

   * Windows: `(username)/AppData(something-something)/ca.dcclab.python.raytracing.json`

   * linux:  `(username)/.config/ca.dcclab.python.raytracing.json`

   
   Some of the variables that are stored are: `lastVersionCheck` (date of the last version check on PyPI) and `mode` which can be `beginner`, `expert`, or `silent`.
   
7. **There are a lot of warnings printed on screen, and I don't like it because I know what I am doing. Can I get rid of that?**
   Yes you can. There are three modes: `beginner` (many warnings), `expert` (very few, but some), and `silent` (nothing). Call `silentMode(saveToPrefs=True)` or `expertMode(saveToPrefs=True)` and you will be all set.

8. **What is the front and the back of a lens?**
   A lens has a focus on both sides.  The side where the light enters is called the front side, and therefore the focus on that side is at a distance "front focal length (or FFL)" away from the physical surface of the lens. Similarly (and possibly surprisingly) the focus to which the light will go after having propagated through the lens is the "back focus" and is a distance "back focal length or (BFL)" away from the last physical surface of the lens.

   These terms are standard terms in optical design.

