class Interface:
    def __init__(self, z, n):
        self.n = n
        self.z = z

class SphericalInterface(Interface):
    def __init__(self, z, n, R):
        self.R = R
        super(SphericalInterface, self).__init__(z=z, n=n)

class FlatInterface(SphericalInterface):
    def __init__(self, z, n):
        super(FlatInterface, self).__init__(R=float("+inf",z=z, n=n))

class ConicalInterface(Interface):
    def __init__(self, z, n, alpha):
        self.alpha = alpha
        super(ConicalInterface, self).__init__(R=float(z=z, n=n))
