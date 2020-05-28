class Interface:
    def __init__(self, n, z):
        self.n = n
        self.z = z

class SphericalInterface:
    def __init__(self, R, n, z):
        self.R = R
        super(SphericalInterface, self).__init__(n=n, z=z)

class FlatInterface:
    def __init__(self, n, z):
        super(FlatInterface, self).__init__(R=float("+inf", n=n, z=z))

class ConicalInterface:
    def __init__(self, alpha, n, z):
        self.alpha = alpha
        super(ConicalInterface, self).__init__(R=float(n=n, z=z))
