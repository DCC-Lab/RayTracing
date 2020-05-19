class Ray:
    """A vector and a light ray as transformed by ABCD matrices.

    The Ray() has a height (y) and an angle with the optical axis (theta).
    It also has a position (z), the diameter of the aperture at that point
    when it propagated through, and a marker if it has been blocked by the
    aperture.

    Simple static functions are defined to obtain a group of rays: fans
    originate from the same height but sweep a range of angles; fan groups
    are fans originating from different heights.

    Parameters
    ----------
    y : float
        Initial height of the ray (limitations? range? default?).

    theta : float
        Initial angle of the ray (limitation? range? default?)

    Returns
    -------
    output : data
        if there is an output for the function

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    some similar functions

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.
    >>> a+b
    0
    """
    # Attributes
    # ----------
    # y : float
    #     Height, or distance of the ray from the optical axis, corresponding to the
    #     ray matrix formalism.
    #
    # theta : float
    #     Angle the ray makes with the optical axis, corresponding to the
    #     ray matrix formalism. Positive is up.
    #
    # z : float
    #     Position of the ray along the optical axis.
    #
    # apertureDiameter : float
    #     The diameter of any blocking aperture at the present position z.
    #
    # isBlocked : bool
    #     If the ray was blocked by an aperture, isBlocked is True



        """
        A ray with height `y` and angle `theta`, initially at z=0.
         I suggest to remove the docstring for the init function since
         this is the same with the class docstring, unless one of
         the methods is used.
        """
    def __init__(self, y: float = 0, theta: float = 0):
        self.y = y
        self.theta = theta

        self.z: float = 0
        self.isBlocked: bool = False
        self.apertureDiameter: float = float("+Inf")

    @property
    def isNotBlocked(self) -> bool:
        """Opposite of isBlocked. Convenience function for readability."""

        return not self.isBlocked

    @staticmethod
        """A list of rays spanning from radianMin to radianMax to be used
        with Matrix.trace() or Matrix.traceMany()
    def fan(y: float, radianMin: float, radianMax: float, N: int):

        Parameters
        ----------
        y : int
            height
        radianMin : int or None, optional
            definition, range, ....
        radianMax : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
            default?
        N : int
            This is the description of N

        Returns
        -------
        output : data
            if there is an output for the function

        Raises
        ------
        BadException
            Because you shouldn't have done that.

        See Also
        --------
        some similar functions

        Notes
        -----
        Notes about the implementation algorithm (if needed).

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function.
        >>> a+b
        0
        """
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
        """ A list of rays spanning from yMin to yMax and radianMin to
        radianMax to be used with Matrix.trace() or Matrix.traceMany()
    def fanGroup(yMin: float, yMax: float, M: int, radianMin: float, radianMax: float, N: int):


        Parameters
        ----------
        yMin : int
            min height
        yMax : int
            max height
        M : int
            This is the description of M
        radianMin : int or None, optional
            definition, range, ....
        radianMax : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
            default?
        N : int
            This is the description of N

        Returns
        -------
        output : data
            if there is an output for the function

        Raises
        ------
        BadException
            Because you shouldn't have done that.

        See Also
        --------
        some similar functions

        Notes
        -----
        Notes about the implementation algorithm (if needed).

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function.
        >>> a+b
        0
        """
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
