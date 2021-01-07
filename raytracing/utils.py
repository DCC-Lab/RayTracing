import math
import warnings
import inspect
import sys

""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0 / math.pi
radPerDeg = math.pi / 180.0


def isAlmostZero(value, epsilon=1e-3):
    return abs(value) < epsilon


def isNotZero(value, epsilon=1e-3):
    return abs(value) > epsilon


def areAbsolutelyAlmostEqual(left, right, epsilon=1e-3):
    return abs(left - right) < epsilon


def areRelativelyAlmostEqual(left, right, epsilon=1e-3):
    absDiff = abs(left - right)
    relTol1 = absDiff / abs(left)
    relTol2 = absDiff / abs(right)
    return relTol1 < epsilon or relTol2 < epsilon


def areAbsolutelyNotEqual(left, right, epsilon=1e-3):
    return abs(left - right) > epsilon


def areRelativelyNotEqual(left, right, epsilon=1e-3):
    return not areRelativelyAlmostEqual(left, right, epsilon)


def deprecated(reason: str):
    def deprecatedFunc(func):
        def wrapper(*args, **kwargs):
            warnings.warn(reason, DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    return deprecatedFunc


def printClassHierarchy(aClass):
    def printAllChilds(aClass):
        for child in aClass.__subclasses__():
            print("\"{0}\" -> \"{1}\"".format(aClass.__name__, child.__name__))
            printAllChilds(child)
    print("# Paste this in the text field of http://www.graphviz.org")
    print("digraph G {")
    print("  rankdir=\"LR\";")
    printAllChilds(aClass)
    print("}")

def printModuleClasses(moduleName):
    for name, obj in inspect.getmembers(sys.modules[moduleName]):
        if inspect.isclass(obj) and obj.__module__.startswith(moduleName):
            print(obj)
