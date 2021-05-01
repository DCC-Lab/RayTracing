TITLE       = ""
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.fanAngle = 0.05
    path.append(Space(d=20))
    path.append(Lens(f=-10, label='Div'))
    path.append(Space(d=7))
    path.append(Lens(f=10, label='Foc'))
    path.append(Space(d=40))
    (focal, focal) = path.effectiveFocalLengths()
    bfl = path.backFocalLength()
    path.label = "Demo #10: Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}".format(focal, bfl)
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()