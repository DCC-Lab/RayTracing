import math
import warnings
import inspect
import sys
from .preferences import Preferences

""" Two constants: deg and rad to quickly convert to degrees
or radians with angle*degPerRad or angle*radPerDeg """

degPerRad = 180.0 / math.pi
radPerDeg = math.pi / 180.0


class BeginnerHint(UserWarning):
    pass

class ExpertNote(UserWarning):
    pass

def warningLineFormat(message, category, filename, lineno, line=None):
    return '{2}: {3}\n'.format(filename, lineno, category.__name__, message)

def beginnerMode(saveToPrefs=False):
    """
    Simple function to set Raytracing into beginner mode. It will print warnings when it suspects you
    are making a mistake or are not using the module properly.

    Parameters
    ----------
    saveToPrefs : Bool
        If True, this will be saved to the Preferences and retained for next time.

    """

    warnings.formatwarning = warningLineFormat
    warnings.filterwarnings("always", category=BeginnerHint)
    warnings.filterwarnings("default", category=ExpertNote)
    warnings.filterwarnings("default", category=DeprecationWarning)
    warnings.filterwarnings("default", category=UserWarning)
    if saveToPrefs:
        prefs = Preferences()
        prefs["mode"] = "beginner"

def expertMode(saveToPrefs=False):
    """
    Simple function to set Raytracing into expert mode: very little warnings printed to screen.

    Parameters
    ----------
    saveToPrefs : Bool
        If True, this will be saved to the Preferences and retained for next time.

    """
    warnings.formatwarning = warningLineFormat
    warnings.filterwarnings("ignore", category=BeginnerHint)
    warnings.filterwarnings("once", category=ExpertNote)
    warnings.filterwarnings("once", category=DeprecationWarning)
    warnings.filterwarnings("once", category=UserWarning)
    if saveToPrefs:
        prefs = Preferences()
        prefs["mode"] = "expert"

def silentMode(saveToPrefs=False):
    """
    Simple function to set Raytracing into silent mode: no warnings printed to screen

    Parameters
    ----------
    saveToPrefs : Bool
        If True, this will be saved to the Preferences and retained for next time.

    """
    warnings.formatwarning = warningLineFormat
    warnings.filterwarnings("ignore", category=BeginnerHint)
    warnings.filterwarnings("ignore", category=ExpertNote)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    if saveToPrefs:
        prefs = Preferences()
        prefs["mode"] = "silent"
    
def isAlmostZero(value, epsilon=1e-3):
    """
    Convenience function for readability: checks if a number is almost zero by comparing to epsilon.

    Parameters
    ----------
    value : float
        If value is less than epsilon, returns True.

    Returns
    -------
    bool
        If the value is almost zero, returns True

    """
    return abs(value) < epsilon


def isNotZero(value, epsilon=1e-3):
    """
    Convenience function for readability: checks if a number is not zero by comparing to epsilon.

    Parameters
    ----------
    value : float
        If value is more than epsilon, returns True.

    Returns
    -------
    bool
        If the value is not zero, returns True

    """
    return abs(value) > epsilon


def areAbsolutelyAlmostEqual(left, right, epsilon=1e-3):
    """
    Convenience function for readability: checks if a two numbers are almost equal by comparing their difference to epsilon.

    Parameters
    ----------
    left : float
        A value

    right : float
        Another value

    Returns
    -------
    bool
        If the difference between the two values is almost zero, returns True

    """

    return abs(left - right) < epsilon


def areRelativelyAlmostEqual(left, right, epsilon=1e-3):
    """
    Convenience function for readability: checks if a two numbers are almost equal in relative terms (epsilon is a percentage).
    Does not work when one value is zero.

    Parameters
    ----------
    left : float
        A value

    right : float
        Another value

    Returns
    -------
    bool
        If the difference between the two values is almost zero, returns True

    """
    absDiff = abs(left - right)
    relTol1 = absDiff / abs(left)
    relTol2 = absDiff / abs(right)
    return relTol1 < epsilon or relTol2 < epsilon

def areAbsolutelyNotEqual(left, right, epsilon=1e-3):
    return abs(left - right) > epsilon

def areRelativelyNotEqual(left, right, epsilon=1e-3):
    return not areRelativelyAlmostEqual(left, right, epsilon)

def areTheSame(a, b):
    """ Simplification to match strings in case-insensitive manner """
    return a.lower() == b.lower()

def deprecated(reason: str):
    def deprecatedFunc(func):
        def wrapper(*args, **kwargs):
            warnings.warn(reason, DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    return deprecatedFunc

def allSubclasses(aClass):
    """
    A function to obtain all the subclasses of a given class

    Parameters
    ----------

    aClass : any class

    Returns
    -------

    A list of classes that are subclasses
     """

    subc = []
    for child in aClass.__subclasses__():
        if len(child.__subclasses__()) == 0:
            subc.append(child.__name__)
        else:
            subc.extend(allSubclasses(child))
    return subc

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


def warnDeprecatedObjectReferences():
    warnings.warn("Object references (fanAngle, fanNumber, rayNumber) will be removed from ImagingPath in future "
                  "versions. Create an ObjectRays(...) instead and provide it to the display "
                  "with ImagingPath.display(rays=...)", category=DeprecationWarning)

def checkLatestVersion():
    """
    Warns the user on screen that a new version exists if the current version is older than the version on PyPi

    """
    try:
        import json
        import urllib.request
        from packaging.version import Version

        url = "https://pypi.org/pypi/raytracing/json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=1) as response:
            data = json.load(response)
            versions = [ Version(version) for version in data["releases"].keys() ]
            latestVersion = versions[-1]
            if Version(__version__) < latestVersion:
                print("Latest version {0} available on PyPi (you are using {1}).".format(latestVersion, __version__))
                print("run `pip install --upgrade raytracing` to update.")

    except Exception as err:
        print("Unable to check for latest version of raytracing on pypi.org")
        print(err)
