import math

""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0 / math.pi
radPerDeg = math.pi / 180.0


def isAlmostZero(value, epsilon=1e-3):
    return abs(value) < epsilon


def isNotZero(value, epsilon=1e-3):
    return abs(value) > epsilon


def areAlmostEqual(left, right, epsilon=1e-3):
    return abs(left - right) < epsilon


def areAlmostEqualRelative(left, right, epsilon=1e-3):
    absDiff = abs(left - right)
    relTol1 = absDiff / left
    relTol2 = absDiff / right
    return relTol1 < epsilon or relTol2 < epsilon


def areNotEqual(left, right, epsilon=1e-3):
    return abs(left - right) > epsilon


def areNotEqualRelative(left, right, epsilon=1e-3):
    return not areAlmostEqualRelative(left, right, epsilon)
