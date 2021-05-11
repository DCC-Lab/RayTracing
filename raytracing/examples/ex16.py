TITLE       = "Commercial doublets from Thorlabs and Edmund"
DESCRIPTION = """ Several achromatic doublets from Thorlabs and Edmund Optics
have been included (the visible series AC254-xxx-A from thorlabs for
instance). They have been modelled according to the specifications from both
manufacturers using the complete dispersion curve for glasses through a
Material class and the curvatures of the surfaces. It is possible to show the
focal shifts from chromatic aberrations. A Zemax file reader (ZMXReader) also
exists to read other lenses. """

def exampleCode(comments=None):
    from raytracing import thorlabs, eo

    thorlabs.AC254_050_A().display()
    thorlabs.AC254_100_A().showChromaticAberrations()
    eo.PN_33_921().display()

if __name__ == "__main__":
    import envexamples
    exampleCode()

