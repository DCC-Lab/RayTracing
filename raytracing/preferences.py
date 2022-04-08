import os
from os.path import expanduser
import json
import platform

class Preferences:
    def __init__(self):
        prefFilename = "ca.dcclab.python.raytracing.json"
        if platform.system() == 'Darwin':
            home = expanduser("~")
            prefDir = os.path.join(home, "Library","Preferences")
        elif platform.system() == 'Windows':
            from win32com.shell import shell, shellcon
            prefDir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)
        elif platform.system() == 'Linux':
            home = expanduser("~")
            prefDir = os.path.join(home, ".config")
            if not os.path.exists(prefDir):
                os.mkdir(prefDir)
        else:
            prefDir = "."
        
        self.path = os.path.join(prefDir, prefFilename)
        self.variables = self.readPreferences()

    def resetPreferences(self):
        os.remove(self.path)
        self.writePreferences(dict())

    def readPreferences(self):
        if not os.path.exists(self.path):
            self.writePreferences(dict())

        with open(self.path, "r") as prefFile:
            try:
                data = json.load(prefFile)
            except Exception as err:
                data = dict()

        return data

    def writePreferences(self, preferencesData):
        with open(self.path, "w+") as prefFile:
            json.dump(preferencesData, prefFile)
