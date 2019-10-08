class Ray:
    """A vector and a light ray as transformed by ABCD matrices

    The Ray() has a height (y) and an angle with the optical axis (theta).
    It also has a position (z), the diameter of the aperture at that point
    when it propagated through, and a marker if it has been blocked by the
    aperture.

    Simple static functions are defined to obtain a group of rays: fans
    originate from the same height but sweep a range of angles; fan groups
    are fans originating from different heights.
    """

    def __init__(self, y=0, theta=0, z=0, isBlocked=False):
        # Ray matrix formalism
        self.y = y
        self.theta = theta

        # Position of this ray and the diameter of the aperture at that 
        # position
        self.z = z
        self.apertureDiameter = float("+Inf")
        self.isBlocked = isBlocked

    @property
    def isNotBlocked(self):
        """Opposite of isBlocked.  Convenience function for readability

        """

        return not self.isBlocked

    @staticmethod
    def fan(y, radianMin, radianMax, N):
        """A list of rays spanning from radianMin to radianMax to be used
        with Matrix.trace() or Matrix.traceMany()

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
            rays.append(Ray(y, theta, z=0))

        return rays

    @staticmethod
    def fanGroup(yMin, yMax, M, radianMin, radianMax, N):
        """ A list of rays spanning from yMin to yMax and radianMin to
        radianMax to be used with Matrix.trace() or Matrix.traceMany()
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
                rays.append(Ray(y, theta, z=0))

        return rays

    def __str__(self):
        """ String description that allows the use of print(Ray()) """

        description = "\n /       \\ \n"
        description += "| {0:6.3f}  |\n".format(self.y)
        description += "|         |\n"
        description += "| {0:6.3f}  |\n".format(self.theta)
        description += " \\       /\n\n"

        description += "z = {0:4.3f}\n".format(self.z)
        if self.isBlocked:
            description += " (blocked)"

        return description

