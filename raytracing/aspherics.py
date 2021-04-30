from .matrix import *

class AsphericInterface(DielectricInterface):
    """An aspheric dielectric interface of radius R, and a conical factor
    kappa with an index n1  before and n2 after the interface.  The plan here is
    simple: in the paraxial approximation, any conical  surface will look like a
    spherical surface, therefore we set the elements the exactly that: a spherical
    surface of radius R. For all calculations involving aperture stops, image
    conjuagtes, etc... we will always use the paraxial form of this matrix (the
    non-paraxial rays are just a correction). However, when we trace the rays,
    then that's a different story: we will use the mul_ray_nonparaxial function
    that is not a matrix multiplication but close to the axis, it gives similar
    results to the mul_ray_paraxial function.

    We use the following definitions:
    https://en.wikipedia.org/wiki/Aspheric_lens

    Parameters
    ----------
    n1 : float
        The refraction index before the surface
    n2 : float
        The refraction index after the interface
    R : float (Optional, default infinity)
        The radius of the dielectric interface
    kappa : float (default 0, sphere)
        The conical parameter of the interface
        kappa < -1    : hyperbola
        kappa == -1   : parabola
        -1 < kappa < 0: prolate ellipse
        kappa == 0    : sphere
        kappa > 0     : oblate ellipse
    Notes
    -----
    A convex interface from the perspective of the ray has R > 0
    """

    def __init__(self, n1, n2, R=float('+Inf'), kappa = 0,
                 diameter=float('+Inf'), label=''):
        self.kappa = kappa
        super(AsphericInterface, self).__init__(n1=n1, n2=n2, R=R,
                                                diameter=float('+Inf'),
                                                label='')

    def z(self, y):
        """ This z represents the surface of the interface 
        as a function of y, the distance from the axis.  

        Obtained from https://en.wikipedia.org/wiki/Aspheric_lens

        """
        z = y*y/(self.R*(1+sqrt(1-(1+self.kappa)*y*y/self.R/self.R)))   
        if isnan(z):
            return None
        else:
            return z

    def dzdr(self, y):
        """ This approximates the slope of the surface which 
        we can then use to calculate the tangent or normal 
        to the surface.

        An analytical expression is possible and should be derived.
        """

        if self.z(y) is None:
            return None, None

        dy1 = 0.000001
        dy2 = 0.000001
        z1 = self.z(y+dy1)
        if z1 is None:
            dy1 = 0
            z1 = self.z(y) 

        z2 = self.z(y-dy2) 
        if z2 is None:
            dy2 = 0
            z2 = self.z(y) 

        dz = z1-z2
        return dz, dy1+dy2

    def surfaceNormal(self, y):
        """ Returns the surface normal at y, pointing backward.
        (between -pi/2 and pi/2).
        The angle is measured with respect to the optical axis
        (i.e. the propagation axis).  For incidence on a convex
        interface above axis (y>0), the angle will be negative.
        """ 
        dz, dy = self.dzdr(y)
        if dz is not None:
            return -arctan2(dz, dy)        
        return None

    def mul_ray_nonparaxial(self, rightSideRay):
        """ Instead of performing a matrix multiplication like
        mul_ray_paraxial, we pass the inputray and transform it any which way we want.
        In this case, this is simple: we find the normal to the surface at the height
        of the ray, then apply Snell's law of refraction, n₁sinθ₁ = n₂sinθ₂, without
        forgetting  that these angles are with respect to the surface normal, so 
        we need to correct them before returning.

        """
        angleNormal = self.surfaceNormal(y=rightSideRay.y)

        incidentAngle = rightSideRay.theta - angleNormal
        refractedAngle = arcsin(self.n1/self.n2*sin(incidentAngle))

        ray = Ray(y=rightSideRay.y, theta=refractedAngle+angleNormal,z=self.L + rightSideRay.z)
        ray.apertureDiameter = rightSideRay.apertureDiameter

        return ray
