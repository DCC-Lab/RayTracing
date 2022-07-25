import os
import json
import platform

class Preferences(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        prefFilename = "ca.dcclab.python.raytracing.json"
        prefDir = "."

        try:
            if platform.system() == 'Darwin':
                home = os.path.expanduser("~")
                prefDir = os.path.join(home, "Library","Preferences")
            elif platform.system() == 'Windows':
                from win32com.shell import shell, shellcon
                prefDir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)
            elif platform.system() == 'Linux':
                home = os.path.expanduser("~")
                prefDir = os.path.join(home, ".config")
                if not os.path.exists(prefDir):
                    os.mkdir(prefDir)
        except Exception as err:
            prefDir = "."

        self.path = os.path.join(prefDir, prefFilename)
        self.readFromDisk()

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __getitem__(self, key):
        self.readFromDisk()
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.writeToDisk()

    def resetPreferences(self):
        try:
            os.remove(self.path)
        except Exception as err:
            pass
        self.clear()
        self.writeToDisk()

    def readFromDisk(self):
        if os.path.exists(self.path):
            with open(self.path, "r+") as prefFile:
                try:
                    data = json.load(prefFile)
                except Exception as err:
                    data = dict()
            self.update(data)
        else:
            self.clear()
            self.writeToDisk()

    def writeToDisk(self):
        with open(self.path, "w+") as prefFile:
            json.dump(self, prefFile)
