class Interface:
    def __init__(self, L, n):
        self.n = n
        self.L = L


class SphericalInterface(Interface):
    def __init__(self, L, n, R):
        super(SphericalInterface, self).__init__(L=L, n=n)
        self.R = R


class FlatInterface(SphericalInterface):
    def __init__(self, L, n):
        super(FlatInterface, self).__init__(R=float("+inf"), L=L, n=n)


class ConicalInterface(Interface):
    def __init__(self, L, n, alpha):
        super(ConicalInterface, self).__init__(L=L, n=n)
        self.alpha = alpha
