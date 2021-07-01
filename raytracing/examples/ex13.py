TITLE       = "Obtain the forward and backward conjugates"
DESCRIPTION = """ This example does not show a plot, it calculates the
position of the image.  forwardConjugate() finds the position and transfer
matrix assuming an object at the front of the matrix/element.  The distance is
given  from the end of the element. This is typically when we wish to obtain
the image position and the transfer matrix to the image. With
backwardConjugate(), we can also assume an image at the end of the
matrix/element, and calculate where the object is to obtain an image at the
poin (the distance is given from the front of the element). """

from raytracing import *

def exampleCode(comments=None):
    M1 = Space(d=10)
    M2 = Lens(f=5)
    M3 = M2 * M1
    print("Image is at distance and transfer matrix: {0} ".format(M3.forwardConjugate()))
    print("Object is at distance and transfer matrix: {0} ".format(M3.backwardConjugate()))

if __name__ == "__main__":
    exampleCode()