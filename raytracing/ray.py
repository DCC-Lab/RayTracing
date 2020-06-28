import warnings


class Ray:
    """A vector and a light ray as transformed by ABCD matrices.

    The Ray() has a height (y) and an angle with the optical axis (theta).
    It also has a position (z) initially at z=0, the diameter of the aperture at that point
    when it propagated through, and a marker if it has been blocked by the
    aperture.

    Simple static functions are defined to obtain a group of rays: fans
    originate from the same height but sweep a range of angles; fan groups
    are fans originating from different heights.

    Parameters
    ----------
    y : float
        Initial height of the ray. (Default=0)
    theta : float
        Initial angle of the ray. (Default=0)

    Attributes
    ----------
    z : float
        Position of the ray along the optical axis. Initialized at 0.
    apertureDiameter : float
        The diameter of any blocking aperture at the present position z. Initialized at +Inf.
    isBlocked : bool
        Whether or not the ray was blocked by an aperture. Initialized to False.

    See Also
    --------
    raytracing.rays

    """

    def __init__(self, y: float = 0, theta: float = 0, z: float = 0, isBlocked: bool = False):
        self.y = y
        self.theta = theta

        self.z = z
        self.isBlocked = isBlocked
        self.apertureDiameter: float = float("+Inf")

    @property
    def isNotBlocked(self) -> bool:
        """Opposite of isBlocked. Convenience function for readability.

        Examples
        --------
        >>> from raytracing import *
        >>> # define an input ray
        >>> ray1=Ray(y=1,theta=0.1)
        >>> # define a lens to propagate the ray through
        >>> mat=Matrix(A=1,B=0,C=-1/5,D=1,physicalLength=2,apertureDiameter=2,label='Lens')
        >>> ray1Output=mat.mul_ray(ray1)
        >>> print('the ray is not blocked? :', ray1Output.isNotBlocked)
        the ray is not blocked? : True

        """

        return not self.isBlocked

    @staticmethod
    def fan(y: float, radianMin: float, radianMax: float, N: int):
        """This function generates a list of rays spanning from radianMin to radianMax.
        This is usually used with Matrix.trace() or Matrix.traceMany() to trace the rays
        through an element or group of elements.

        Parameters
        ----------
        y : float
            Height of the ray
        radianMin : float
            Minimum angle in radians of the fan.
        radianMax : float
            Maximum angle in radians of the fan.
        N : int
            The number of rays to create inside the fan.

        Returns
        -------
        rays : list of ray
            The created list of rays that define this fan.

        Notes
        -----
        This method is deprecated. The class Rays and its subclasses should be used to generate multiple Ray objects.

        See Also
        --------
        raytracing.Matrix.trace()
        raytracing.Matrix.traceMany().

        """
        warnings.warn("The creation of a group of rays with this method is deprecated. Usage of the class Rays and its "
                      "subclasses is recommended.", DeprecationWarning)

        if N >= 2:
            deltaRadian = float(radianMax - radianMin) / (N - 1)
        elif N == 1:
            deltaRadian = 0.0
        else:
            raise ValueError("N must be 1 or larger.")

        rays = []
        for i in range(N):
            theta = radianMin + float(i) * deltaRadian
            rays.append(Ray(y, theta))

        return rays

    @staticmethod
    def fanGroup(yMin: float, yMax: float, M: int, radianMin: float, radianMax: float, N: int):
        """This function creates a list of rays spanning from yMin to yMax and radianMin to radianMax.
        This is usually used with Matrix.trace() or Matrix.traceMany() to trace the rays
        through an element or group of elements.


        Parameters
        ----------
        yMin : float
            Minimum height of the fans.
        yMax : float
            Maximum height of the fans.
        M : int
            The number of fans to create inside yMin and yMax.
        radianMin : float
            Minimum angle in radians of each fan.
        radianMax : float
            Maximum angle in radians of each fan.
        N : int
            The number of rays to create inside each fan.

        Returns
        -------
        rays : list of ray
            The created list of rays that define these fan groups.

        Notes
        -----
        This method is deprecated. The class Rays and its subclasses should be used to generate multiple Ray objects.

        See Also
        --------
        raytracing.Matrix.trace()
        raytracing.Matrix.traceMany().

        """
        warnings.warn("The creation of a group of rays with this method is deprecated. Usage of the class Rays and its"
                      "subclasses is recommended.", DeprecationWarning)

        if N >= 2:
            deltaRadian = float(radianMax - radianMin) / (N - 1)
        elif N == 1:
            deltaRadian = 0.0
        else:
            raise ValueError("N must be 1 or larger.")

        if M >= 2:
            deltaHeight = float(yMax - yMin) / (M - 1)
        elif M == 1:
            deltaHeight = 0.0
        else:
            raise ValueError("M must be 1 or larger.")

        rays = []
        for j in range(M):
            for i in range(N):
                theta = radianMin + float(i) * deltaRadian
                y = yMin + float(j) * deltaHeight
                rays.append(Ray(y, theta))

        return rays

    def __str__(self):
        """String description that allows the use of print(Ray())."""

        description = "\n /       \\ \n"
        description += "| {0:6.3f}  |\n".format(self.y)
        description += "|         |\n"
        description += "| {0:6.3f}  |\n".format(self.theta)
        description += " \\       /\n\n"

        description += "z = {0:4.3f}\n".format(self.z)
        if self.isBlocked:
            description += " (blocked)"

        return description

    def __eq__(self, other):
        """Define rays to be equal if they the same height and angle."""

        if not isinstance(other, Ray):
            return False
        elif self.y != other.y:
            return False
        elif self.theta != other.theta:
            return False

        return True
