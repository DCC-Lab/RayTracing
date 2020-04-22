try:
    from raytracing import *
except ImportError:
    raise ImportError('Raytracing module not found: "pip install raytracing"')

from raytracing import *
import raytracing.thorlabs as thorlabs
import raytracing.eo as eo
import raytracing.olympus as olympus
import raytracing.nikon as nikon

class VMS:
    @staticmethod
    def detectionBliq():
        detection = ImagingPath()
        detection.label = "VMS Base detection"
        detection.objectHeight = 0.5+0.2 # mm maximum, include diffuse spot size
        detection.fanAngle = 1.05 # NA = 1.05
        detection.fanNumber = 11
        detection.rayNumber = 3
        detection.showImages = False

        obj = olympus.XLUMPlanFLN20X()
        obj.flipOrientation()
        detection.append(obj)
        detection.append(Space(d=140)) 
        detection.append(Lens(f=55,diameter=30, label='$L_1$'))
        detection.append(Space(d=110))
        detection.append(Lens(f=40, diameter=30, label='$L_c$'))
        detection.append(Space(d=150))
        detection.append(Lens(f=30, diameter=30, label='$L_d$'))
        detection.append(Space(d=30))
        detection.append(Aperture(diameter=8,label="PMT"))

        return detection

    def detectionCERVO():
        detection = ImagingPath()
        detection.label = "CERVO VMS 2-inch system, detection path"
        detection.objectHeight = 2 # mm maximum, should probably model with 0.5
        detection.fanAngle = 1.05 # NA = 1.05
        detection.fanNumber = 11
        detection.rayNumber = 3
        detection.showImages = True

        cage1 = MatrixGroup(elements=[Aperture(diameter=25),
                                      Space(d=50,diameter=30),
                                      Aperture(diameter=25)],
                                      label="Cage 1")
        cage2 = MatrixGroup(elements=[Aperture(diameter=25),
                                      Space(d=50,diameter=30),
                                      Aperture(diameter=25)],
                                      label="Cage 2")

        obj = olympus.XLUMPlanFLN20X()
        obj.flipOrientation()
        detection.append(obj)
        detection.append(cage1)
        detection.append(thorlabs.AC254_050_A())
        detection.append(cage2)
        detection.append(Space(d=50))
        detection.append(thorlabs.AC254_030_A())
        detection.append(Space(d=25))
        detection.append(Aperture(diameter=8,label="PMT R3896"))

        return detection

    @staticmethod
    def scanningCERVO():
        vms = ImagingPath()
        vms.label = "CERVO VMS 2-inch system, scanning path"
        vms.objectHeight = 3
        vms.fanAngle = 0.2
        vms.fanNumber = 7
        vms.rayNumber = 5
        vms.showImages = False

        f1 = 75.0
        f2 = 150.0
        f3 = 200.0
        f4 = 200.0
        fs = 54.0
        ft = 180.0
        fo = 180/20.0

        vms.append(Aperture(diameter=8, label='Polygon'))
        vms.append(Space(d=f1))
        vms.append(Lens(f=f1, diameter=50, label='F1'))
        vms.append(Space(d=f1))
        vms.append(Space(d=f2))
        vms.append(Lens(f=f2, diameter=50, label='F2'))
        vms.append(Space(d=f2))
        vms.append(Aperture(diameter=20, label='Galvo'))
        vms.append(Space(d=f3))
        vms.append(Lens(f=f3, diameter=50, label='Relay 1'))
        vms.append(Space(d=f3))
        vms.append(Space(d=f4))
        vms.append(Lens(f=f4, diameter=50, label='Relay 2'))
        vms.append(Space(d=f4))
        vms.append(Space(d=fs))
        vms.append(Lens(f=fs, diameter=35.4, label='LSM54-850'))  
        vms.append(Space(d=fs))
        vms.append(Space(d=ft))
        vms.append(Lens(f=ft, diameter=36.8, label='TTL200MP'))
        vms.append(Space(d=ft))
        vms.append(olympus.XLUMPlanFLN20X())

        return vms

    def scanningSpencer():
        vms = ImagingPath()
        vms.label = "Spencer VMS 2-inch system, scanning path"
        vms.objectHeight = 3
        vms.fanAngle = 0.2
        vms.fanNumber = 7
        vms.rayNumber = 5
        vms.showImages = False

        f1 = 75.0
        f2 = 150.0
        f3 = 200.0
        f4 = 200.0
        fs = 54.0
        ft = 180.0
        fo = 180/20.0

        vms.append(Aperture(diameter=8, label='Polygon'))
        vms.append(Space(d=f1))
        vms.append(Lens(f=f1, diameter=50, label='F1'))
        vms.append(Space(d=f1))
        vms.append(Space(d=f2))
        vms.append(Lens(f=f2, diameter=50, label='F2'))
        vms.append(Space(d=f2))
        vms.append(Aperture(diameter=20, label='Galvo'))
        vms.append(Space(d=f3))
        vms.append(Lens(f=f3, diameter=50, label='Relay 1'))
        vms.append(Space(d=f3))
        vms.append(Space(d=f4))
        vms.append(Lens(f=f4, diameter=50, label='Relay 2'))
        vms.append(Space(d=f4))
        vms.append(Space(d=fs))
        vms.append(Lens(f=fs, diameter=35.4, label='LSM54-850'))  
        vms.append(Space(d=fs))
        vms.append(Space(d=ft))
        vms.append(Lens(f=ft, diameter=36.8, label='TTL200MP'))
        vms.append(Space(d=ft))
        vms.append(olympus.XLUMPlanFLN20X())

        return vms

    @staticmethod
    def scanningDCCLab():
        vms = OpticalPath()
        vms.label = "DCCLab VMS 1-inch system, scanning path"
        vms.objectHeight = 3
        vms.fanAngle = 0.2
        vms.fanNumber = 7
        vms.rayNumber = 5
        vms.showImages = False

        f1 = 45.0
        f2 = 75.0
        fs = 100.0
        ft = 150.0

        vms.append(Aperture(diameter=8, label='Polygon'))
        vms.append(Space(d=f1))
        vms.append(Lens(f=f1, diameter=25, label='F1'))
        vms.append(Space(d=f1))
        vms.append(Space(d=f2))
        vms.append(Lens(f=f2, diameter=25, label='F2'))
        vms.append(Space(d=f2))
        vms.append(Aperture(diameter=12, label='Galvo'))
        vms.append(Space(d=fs))
        vms.append(Lens(f=fs, diameter=25, label='Scan Lens'))
        vms.append(Space(d=fs))
        vms.append(Space(d=ft))
        vms.append(Lens(f=ft, diameter=25, label='Tube Lens'))
        vms.append(Space(d=ft))
        vms.append(olympus.LUMPlanFL40X())

        return vms

    @staticmethod
    def scanningLargeFOV():
        vms = ImagingPath()
        vms.label = "Bliq VMS"
        vms.objectHeight = 6
        vms.fanAngle = 0.2
        vms.fanNumber = 7
        vms.rayNumber = 5
        vms.showImages = False

        f1 = 100
        f2 = 100
        f3 = 200.0
        f4 = 200.0
        fs = 54.0
        ft = 180.0
        fo = 180/20.0

        vms.append(Aperture(diameter=8, label='Polygon'))
        vms.append(Space(d=f1))
        vms.append(Lens(f=f1, diameter=50, label='F1'))
        vms.append(Space(d=f1))
        vms.append(Space(d=f2))
        vms.append(Lens(f=f2, diameter=50, label='F2'))
        vms.append(Space(d=f2))
        vms.append(Aperture(diameter=20, label='Galvo'))
        vms.append(Space(d=f3))
        vms.append(Lens(f=f3, diameter=75, label='Relay 1'))
        vms.append(Space(d=f3))
        vms.append(Space(d=f4))
        vms.append(Lens(f=f4, diameter=75, label='Relay 2'))
        vms.append(Space(d=f4))
        vms.append(Space(d=fs))
        vms.append(Lens(f=fs, diameter=35.4, label='LSM54-850'))  
        vms.append(Space(d=fs))
        vms.append(Space(d=ft))
        vms.append(Lens(f=ft, diameter=36.8, label='TTL200MP'))
        vms.append(Space(d=ft))
        vms.append(olympus.XLUMPlanFLN20X())

        return vms

    def fovScanningSystem(scanning):
        marginalRay = Ray(y=0, theta =10*radPerDeg)
        rayTrace = scanning.trace(marginalRay)
        rayAtSample = rayTrace[-1]
        if rayAtSample.isBlocked:
            print("Vignetting occurs: ", rayAtSample)
        else:
            print("Field of view for {0} design: {1:0.3} µm".format(scanning.label, abs(rayAtSample.y)*2*1000))

    def detectionDIC():
        detection = ImagingPath()
        detection.label = "VMS DIC detection with camera"
        detection.objectHeight = 8+0.2 # mm maximum, include diffuse spot size
        #detection.fanAngle = 0.8 # NA obj
        detection.fanNumber = 11
        detection.rayNumber = 3
        detection.showImages = False

        obj = nikon.LWD16X()
        obj.flipOrientation()
        detection.append(obj)
        detection.append(Space(d=148))
        detection.append(Lens(f=200,diameter=36.8, label='$L_1$'))
        detection.append(Space(d=200))
        detection.append(Aperture(diameter=17.5,label="chip camera"))

        return detection


if __name__ == "__main__":

    # VMS.scanningDCCLab().display()
    # VMS.scanningSpencer().display()
    # VMS.scanningCERVO().display()
    # VMS.detectionCERVO().display()
    VMS.detectionDIC().display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)
    # bliq = VMS.scanningSpencer()
    bliq.showImages = True
    # bliq.objectHeight = 1
    bliq.rayNumber = 5
    bliq.fanNumber = 5

    bliq.display()

    bliq.LaserPath().display(GaussianBeam(w=2))

    # VMS.fovScanningSystem(VMS.scanningDCCLab())
