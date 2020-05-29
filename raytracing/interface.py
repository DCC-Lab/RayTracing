class Interface:
    def __init__(self, L=0.0, n=1.0):
        self.n = n
        self.L = L


class SphericalInterface(Interface):
    def __init__(self, R: float, L=0.0, n=1.0):
        super(SphericalInterface, self).__init__(L=L, n=n)
        self.R = R


class FlatInterface(SphericalInterface):
    def __init__(self, L=0.0, n=1.0):
        super(FlatInterface, self).__init__(R=float("+inf"), L=L, n=n)


class ConicalInterface(Interface):
    def __init__(self, alpha: float, L=0.0, n=1.0):
        super(ConicalInterface, self).__init__(L=L, n=n)
        self.alpha = alpha
