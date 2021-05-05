TITLE       = "Commercial doublets from Thorlabs and Edmund"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode(comments=None):
    thorlabs.AC254_050_A().display()
    eo.PN_33_921().display()

if __name__ == "__main__":
    exempleCode()
