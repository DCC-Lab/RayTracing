import envtest
from raytracing.utils import deprecated


def simpleDecoratorReturnsTuple(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs), func(*args, **kwargs)

    return wrapper


def decoratorWithOneArgument(arg):
    def simpleDecoratorReturnsTuple(func):
        def wrapper(*args, **kwargs):
            return arg, func(*args, **kwargs)

        return wrapper

    return simpleDecoratorReturnsTuple


class TestDecorators(envtest.RaytracingTestCase):

    def testSimpleDecorator(self):
        @simpleDecoratorReturnsTuple
        def toto(x):
            return x * x

        self.assertTupleEqual(toto(2), (4, 4))

    def testDecoratorWithOneArgument(self):
        @decoratorWithOneArgument(0)
        def toto(a, b, c):
            return a, b, c

        self.assertTupleEqual(toto(1, 2, 3), (0, (1, 2, 3)))


class TestDeprecatedDecorator(envtest.RaytracingTestCase):

    def testDeprecated(self):
        reason = "This is deprecated because it is a test."

        @deprecated(reason)
        def deprecatedFunction():
            return "This is deprecated"

        with self.assertWarns(DeprecationWarning) as deprec:
            retVal = deprecatedFunction()

        self.assertEqual(retVal, "This is deprecated")
        self.assertEqual(str(deprec.warning), reason)
