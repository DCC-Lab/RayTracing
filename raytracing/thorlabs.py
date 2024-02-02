from .specialtylenses import *
from .materials import *


class ACN254_100_A(AchromatDoubletLens):
    """ ACN254-100-A

    .. csv-table::
        :header: Parameter, value

        "fa", "-100.0"
        "fb", "-103.6"
        "R1", "-52.0"
        "R2", "49.9"
        "R3", "600.0"
        "tc1", "2.0"
        "tc2", "4.0"
        "te", "7.7"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """
    def __init__(self, wavelength=None):
        super(ACN254_100_A,self).__init__(fa=-100.0,fb=-103.6, R1=-52.0, R2=49.9, R3=600.0, 
                                    tc1=2.0, tc2=4.0, te=7.7, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254-100-A", wavelength=wavelength, wavelengthRef=0.5876)


class ACN254_075_A(AchromatDoubletLens):
    """ ACN254-075-A

    .. csv-table::
        :header: Parameter, value

        "fa", "-75.1"
        "fb", "-78.8"
        "R1", "-39.0"
        "R2", "39.2"
        "R3", "489.8"
        "tc1", "2.0"
        "tc2", "4.3"
        "te", "8.6"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """
    def __init__(self, wavelength=None):
        super(ACN254_075_A, self).__init__(fa=-75.1,fb=-78.8, R1=-39.0, R2=39.2, R3=489.8,
                                    tc1=2.0, tc2=4.3, te=8.6, n1=None, n2=None, mat1=N_BAK4, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254-075-A", wavelengthRef=0.5876, wavelength=wavelength)


class ACN254_050_A(AchromatDoubletLens):
    """ ACN254-050-A

    .. csv-table::
        :header: Parameter, value

        "fa", "-50.0"
        "fb", "-53.2"
        "R1", "-34.0"
        "R2", "32.5"
        "R3", "189.2"
        "tc1", "2.0"
        "tc2", "4.5"
        "te", "9.4"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(ACN254_050_A, self).__init__(fa=-50.0, fb=-53.2, R1=-34.0, R2=32.5, R3=189.2,
                                    tc1=2.0, tc2=4.5, te=9.4, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254-050-A", wavelength=wavelength, wavelengthRef=0.5876)

class ACN254_040_A(AchromatDoubletLens):
    """ ACN254-040-A

    .. csv-table::
        :header: Parameter, value

        "fa", "-40.1"
        "fb", "-43.6"
        "R1", "-27.1"
        "R2", "27.1"
        "R3", "189.2"
        "tc1", "2.0"
        "tc2", "5.0"
        "te", "10.6"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(ACN254_040_A,self).__init__(fa=-40.1,fb=-43.6, R1=-27.1, R2=27.1, R3=189.2,
                                    tc1=2.0, tc2=5.0, te=10.6, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF11, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="ACN254-040-A", wavelength=wavelength, wavelengthRef=0.5876)


class AC254_030_A(AchromatDoubletLens):
    """ AC254-030-A

    .. csv-table::
        :header: Parameter, value

        "fa", "30.0"
        "fb", "22.2"
        "R1", "20.89"
        "R2", "-16.7"
        "R3", "-79.8"
        "tc1", "12"
        "tc2", "2.0"
        "te", "8.8"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        """
        Notes
        -----
        As of May 31 2020, there is an error on the product web page at:
        https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
        The expected back focal length is different from the reference PDF on
        the same line which clearly states it should be 22.2.

        We take the PDF ato be the true value
        """

        super(AC254_030_A, self).__init__(fa=30.0, fb=22.2, R1=20.89, R2=-16.7, R3=-79.8,
                                    tc1=12, tc2=2.0, te=8.8, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-030-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_035_A(AchromatDoubletLens):
    """AC254-035-A

    .. csv-table::
        :header: Parameter, value

        "fa", "35.2"
        "fb", "27.3"
        "R1", "24.0"
        "R2", "-19.1"
        "R3", "-102.1"
        "tc1", "12"
        "tc2", "2.0"
        "te", "9.6"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_035_A, self).__init__(fa=35.2, fb=27.3, R1=24.0, R2=-19.1, R3=-102.1,
                                    tc1=12, tc2=2.0, te=9.6, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-035-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_040_A(AchromatDoubletLens):
    """ AC254-040-A

    .. csv-table::
        :header: Parameter, value

        "fa", "40.1"
        "fb", "33.4"
        "R1", "23.7"
        "R2", "-20.1"
        "R3", "-57.7"
        "tc1", "10"
        "tc2", "2.5"
        "te", "7.4"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_040_A, self).__init__(fa=40.1,fb=33.4, R1=23.7, R2=-20.1, R3=-57.7,
                                    tc1=10, tc2=2.5, te=7.4, n1=None, n2=None, mat1=N_BK7, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-040-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_045_A(AchromatDoubletLens):
    """ AC254-045-A

    .. csv-table::
        :header: Parameter, value

        "fa", "45.0"
        "fb", "40.2"
        "R1", "31.2"
        "R2", "-25.9"
        "R3", "-130.6"
        "tc1", "7"
        "tc2", "2.0"
        "te", "5.7"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_045_A,self).__init__(fa=45.0, fb=40.2, R1=31.2, R2=-25.90, R3=-130.6,
                                    tc1=7, tc2=2.0, te=5.7, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-045-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_050_A(AchromatDoubletLens):
    """ AC254-050-A

    .. csv-table::
        :header: Parameter, value

        "fa", "50.2"
        "fb", "43.4"
        "R1", "33.3"
        "R2", "-22.28"
        "R3", "-291.07"
        "tc1", "9"
        "tc2", "2.5"
        "te", "8.7"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_050_A, self).__init__(fa=50.2,fb=43.4, R1=33.3,R2=-22.28, R3=-291.07,
                                    tc1=9, tc2=2.5, te=8.7, n1=None, n2=None, mat1=N_BAF10, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-050-A", wavelength=wavelength, wavelengthRef=0.5876)


class AC254_060_A(AchromatDoubletLens):
    """ AC254-060-A

    .. csv-table::
        :header: Parameter, value

        "fa", "60.1"
        "fb", "54.3"
        "R1", "41.7"
        "R2", "-25.9"
        "R3", "-230.7"
        "tc1", "8"
        "tc2", "2.5"
        "te", "8.2"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_060_A, self).__init__(fa=60.1,fb=54.3, R1=41.7,R2=-25.9, R3=-230.7,
                                    tc1=8, tc2=2.5, te=8.2, n1=None, n2=None, mat1=E_BAF11, mat2=E_FD10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-060-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_075_A(AchromatDoubletLens):
    """ AC254-075-A

    .. csv-table::
        :header: Parameter, value

        "fa", "74.9"
        "fb", "70.3"
        "R1", "46.5"
        "R2", "-33.9"
        "R3", "-95.5"
        "tc1", "7.0"
        "tc2", "2.5"
        "te", "8.8"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_075_A, self).__init__(fa=74.9,fb=70.3, R1=46.5,R2=-33.9, R3=-95.5,
                                    tc1=7.0, tc2=2.5, te=6.9, n1=None, n2=None, mat1=N_BK7, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-075-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_080_A(AchromatDoubletLens):
    """ AC254-080-A

    .. csv-table::
        :header: Parameter, value

        "fa", "80.0"
        "fb", "75.3"
        "R1", "49.6"
        "R2", "-35.5"
        "R3", "-101.2"
        "tc1", "7.0"
        "tc2", "3.0"
        "te", "7.3"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_080_A, self).__init__(fa=80.0,fb=75.3, R1=49.6,R2=-35.5, R3=-101.2,
                                    tc1=7.0, tc2=3.0, te=7.3, n1=None, n2=None, mat1=N_BK7, mat2=N_SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-080-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_100_A(AchromatDoubletLens):
    """ AC254-100-A

    .. csv-table::
        :header: Parameter, value

        "fa", "100.1"
        "fb", "97.1"
        "R1", "62.8"
        "R2", "-45.7"
        "R3", "-128.2"
        "tc1", "4.0"
        "tc2", "2.5"
        "te", "4.7"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_100_A,self).__init__(fa=100.1,fb=97.1, R1=62.75,R2=-45.71, R3=-128.23, 
                                    tc1=4.0, tc2=2.5, te=4.7, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-100-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_125_A(AchromatDoubletLens):
    """ AC254-125-A

    .. csv-table::
        :header: Parameter, value

        "fa", "125.0"
        "fb", "122.0"
        "R1", "77.6"
        "R2", "-55.9"
        "R3", "-160.8"
        "tc1", "4.0"
        "tc2", "2.8"
        "te", "5.0"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
        More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
        As of May 31 2020, the calculated edge thickness does not match
        the product page. There does not seem to be another place where
        the information can be validated (the PDF doesn't show the edge thickness).
        https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120.
        Because everything else is fine in all calculations, to avoid
        warnings, we are setting te=5.3 mm, even if the web site says 5.0 mm.
        All properties are correct except that, and it has no impact on calculations
        (it is just a sanity check).
    """

    def __init__(self, wavelength= None):
        super(AC254_125_A,self).__init__(fa=125.0,fb=122.0, R1=77.63,R2=-55.92, R3=-160.82, 
                                    tc1=4.0, tc2=2.83, te=5.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-125-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_A(AchromatDoubletLens):
    """ AC254-150-A

    .. csv-table::
        :header: Parameter, value

        "fa", "150.0"
        "fb", "146.1"
        "R1", "91.6"
        "R2", "-66.7"
        "R3", "-197.7"
        "tc1", "5.7"
        "tc2", "2.2"
        "te", "6.6"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_150_A,self).__init__(fa=150,fb=146.1, R1=91.6,R2=-66.7, R3=-197.7,
                                    tc1=5.7, tc2=2.2, te=6.6, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-150-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_200_A(AchromatDoubletLens):
    """ AC254-200-A

    .. csv-table::
        :header: Parameter, value

        "fa", "200.2"
        "fb", "194.0"
        "R1", "77.4"
        "R2", "-87.6"
        "R3", "291.1"
        "tc1", "4.0"
        "tc2", "2.5"
        "te", "5.7"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_200_A,self).__init__(fa=200.2,fb=194.0, R1=77.4,R2=-87.6, R3=291.1, 
                                    tc1=4.0, tc2=2.5, te=5.7, n1=None, mat1=N_SSK5, n2=None, mat2=LAFN7, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-200-A", wavelength=wavelength, wavelengthRef= 0.5876)

class AC254_250_A(AchromatDoubletLens):
    """ AC254-250-A

    .. csv-table::
        :header: Parameter, value

        "fa", "250.0"
        "fb", "246.7"
        "R1", "137.1"
        "R2", "-111.5"
        "R3", "-459.2"
        "tc1", "4.0"
        "tc2", "2.0"
        "te", "5.2"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_250_A,self).__init__(fa=250,fb=246.7, R1=137.1,R2=-111.5, R3=-459.2, 
                                    tc1=4.0, tc2=2.0, te=5.2, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-250-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_300_A(AchromatDoubletLens):
    """ AC254-300-A

    .. csv-table::
        :header: Parameter, value

        "fa", "300.2"
        "fb", "297.0"
        "R1", "165.2"
        "R2", "-137.1"
        "R3", "-557.4"
        "tc1", "4.0"
        "tc2", "2.0"
        "te", "5.4"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_300_A,self).__init__(fa=300.2,fb=297.0, R1=165.2,R2=-137.1, R3=-557.4, 
                                    tc1=4.0, tc2=2.0, te=5.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-300-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_400_A(AchromatDoubletLens):
    """ AC254-400-A

    .. csv-table::
        :header: Parameter, value

        "fa", "399.3"
        "fb", "396.0"
        "R1", "219.8"
        "R2", "-181.6"
        "R3", "-738.5"
        "tc1", "4.0"
        "tc2", "2.0"
        "te", "5.5"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_400_A,self).__init__(fa=399.3,fb=396.0, R1=219.8,R2=-181.6, R3=-738.5, 
                                    tc1=4.0, tc2=2.0, te=5.5, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-400-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_500_A(AchromatDoubletLens):
    """ AC254-500-A

    .. csv-table::
        :header: Parameter, value

        "fa", "502.5"
        "fb", "499.9"
        "R1", "337.3"
        "R2", "-186.8"
        "R3", "-557.4"
        "tc1", "4.0"
        "tc2", "2.0"
        "te", "5.6"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "486.1 nm, 587.6 nm, and 656.3 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
    """

    def __init__(self, wavelength=None):
        super(AC254_500_A,self).__init__(fa=502.5,fb=499.9, R1=337.3,R2=-186.8, R3=-557.4, 
                                    tc1=4.0, tc2=2.0, te=5.6, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-500-A", wavelength=wavelength, wavelengthRef= 0.5876)

class AC254_050_B(AchromatDoubletLens):
    """ AC254-050-B

    .. csv-table::
        :header: Parameter, value

        "fa", "50.0"
        "fb", "45.0"
        "R1", "33.55"
        "R2", "-27.05"
        "R3", "-125.60"
        "tc1", "7.5"
        "tc2", "1.8"
        "te", "6.2"
        "n1", "0.5876"
        "n2", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC254_050_B,self).__init__(fa=50.0,fb=45.0, R1=33.55,R2=-27.05, R3=-125.60, 
                                    tc1=7.5, tc2=1.8, te=6.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC254-050-B", wavelength=wavelength, wavelengthRef=0.5876)


class AC508_075_B(AchromatDoubletLens):
    """ AC508-075-B

    .. csv-table::
        :header: Parameter, value

        "fa", "75.0"
        "fb", "65.7"
        "R1", "51.8"
        "R2", "-93.11"
        "R3", "-291.07"
        "tc1", "12.0"
        "tc2", "5.0"
        "te", "9.2"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_075_B,self).__init__(fa=75.0,fb=65.7, R1=51.8,R2=-93.11, R3=-291.07, 
                                    tc1=12.0, tc2=5.0, te=9.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-075-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_080_B(AchromatDoubletLens):
    """ AC508-080-B

    .. csv-table::
        :header: Parameter, value

        "fa", "80.0"
        "fb", "69.5"
        "R1", "51.8"
        "R2", "-44.6"
        "R3", "-312.6"
        "tc1", "16.0"
        "tc2", "2.0"
        "te", "10.3"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_080_B,self).__init__(fa=80.0,fb=69.5, R1=51.8,R2=-44.6, R3=-312.6, 
                                    tc1=16.0, tc2=2.0, te=10.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-080-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_100_B(AchromatDoubletLens):
    """ AC508-100-B

    .. csv-table::
        :header: Parameter, value

        "fa", "100.0"
        "fb", "91.5"
        "R1", "65.8"
        "R2", "-56.0"
        "R3", "-280.6"
        "tc1", "13.0"
        "tc2", "2.0"
        "te", "8.7"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_100_B,self).__init__(fa=100.0,fb=91.5, R1=65.8,R2=-56.0, R3=-280.6, 
                                    tc1=13.0, tc2=2.0, te=8.7, n1=None, n2=None, mat1=N_LAK22, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-100-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_150_B(AchromatDoubletLens):
    """ AC508-150-B

    .. csv-table::
        :header: Parameter, value

        "fa", "150.0"
        "fb", "145.3"
        "R1", "112.2"
        "R2", "-95.9"
        "R3", "-325.1"
        "tc1", "8.2"
        "tc2", "5.0"
        "te", "9.3"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_150_B,self).__init__(fa=150.0,fb=145.3, R1=112.2,R2=-95.9, R3=-325.1, 
                                    tc1=8.2, tc2=5.0, te=9.3, n1=None, n2=None, mat1=N_LAK22, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-150-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_200_B(AchromatDoubletLens):
    """ AC508-200-B

    .. csv-table::
        :header: Parameter, value

        "fa", "200.0"
        "fb", "193.2"
        "R1", "134.0"
        "R2", "-109.2"
        "R3", "-515.2"
        "tc1", "8.2"
        "tc2", "5.0"
        "te", "10.1"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_200_B,self).__init__(fa=200.0,fb=193.2, R1=134.0,R2=-109.2, R3=-515.2, 
                                    tc1=8.2, tc2=5.0, te=10.1, n1=None, n2=None, mat1=N_LAK22, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-200-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_250_B(AchromatDoubletLens):
    """ AC508-250-B

    .. csv-table::
        :header: Parameter, value

        "fa", "250.0"
        "fb", "243.2"
        "R1", "121.2"
        "R2", "-146.1"
        "R3", "1235.9"
        "tc1", "6.6"
        "tc2", "2.6"
        "te", "6.8"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_250_B,self).__init__(fa=250.0,fb=243.2, R1=121.2,R2=-146.1, R3=1235.9, 
                                    tc1=6.6, tc2=2.6, te=6.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-250-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_300_B(AchromatDoubletLens):
    """ AC508-300-B

    .. csv-table::
        :header: Parameter, value

        "fa", "300.0"
        "fb", "295.1"
        "R1", "201.8"
        "R2", "-161.5"
        "R3", "-760.0"
        "tc1", "6.6"
        "tc2", "2.6"
        "te", "7.2"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_300_B,self).__init__(fa=300.0,fb=295.1, R1=201.8,R2=-161.5, R3=-760.0, 
                                    tc1=6.6, tc2=2.6, te=7.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-300-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_400_B(AchromatDoubletLens):
    """ AC508-400-B

    .. csv-table::
        :header: Parameter, value

        "fa", "400.0"
        "fb", "393.6"
        "R1", "280.6"
        "R2", "-208.0"
        "R3", "-859.0"
        "tc1", "4.5"
        "tc2", "2.6"
        "te", "5.6"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_400_B,self).__init__(fa=400.0,fb=393.6, R1=280.6,R2=-208.0, R3=-859.0, 
                                    tc1=4.5, tc2=2.6, te=5.6, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-400-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_500_B(AchromatDoubletLens):
    """ AC508-500-B

    .. csv-table::
        :header: Parameter, value

        "fa", "500.0"
        "fb", "497.0"
        "R1", "346.7"
        "R2", "-259.4"
        "R3", "-1132.4"
        "tc1", "4.5"
        "tc2", "2.6"
        "te", "5.9"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_500_B,self).__init__(fa=500.0,fb=497.0, R1=346.7,R2=-259.4, R3=-1132.4, 
                                    tc1=4.5, tc2=2.6, te=5.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-500-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_750_B(AchromatDoubletLens):
    """ AC5s08-750-B

    .. csv-table::
        :header: Parameter, value

        "fa", "750.0"
        "fb", "745.0"
        "R1", "376.8"
        "R2", "-291.1"
        "R3", "2910.0"
        "tc1", "4.2"
        "tc2", "2.5"
        "te", "6.0"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_750_B,self).__init__(fa=750.0,fb=745.0, R1=376.8,R2=-291.1, R3=2910.0, 
                                    tc1=4.2, tc2=2.5, te=6.0, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-750-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_1000_B(AchromatDoubletLens):
    """ AC508-1000-B

    .. csv-table::
        :header: Parameter, value

        "fa", "1000.0"
        "fb", "993.0"
        "R1", "494.3"
        "R2", "-398.1"
        "R3", "3440.0"
        "tc1", "4.2"
        "tc2", "2.8"
        "te", "6.4"
        "n1", "0.855"
        "n2", "0.855"
        "diameter", "50.8"
        "Design Wavelengths", "706.5 nm, 855 nm, and 1015 nm"
        "Operating Temperature", "-40 °C to 85 °C"

    Notes
    -----
    More info: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259
    """

    def __init__(self, wavelength=None):
        super(AC508_1000_B,self).__init__(fa=1000.0,fb=993.0, R1=494.3,R2=-398.1, R3=3440.0, 
                                    tc1=4.2, tc2=2.8, te=6.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-1000-B", wavelength=wavelength, wavelengthRef=0.855)

class LA1608_A(SingletLens):
    """ LA1608-A

    .. csv-table::
        :header: Parameter, value

        "fa", "75.0"
        "fb", "72.0"
        "R1", "38.6"
        "R2", "+Inf"
        "tc", "4.1"
        "te", "2.0"
        "n", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1608-A
    """

    def __init__(self, wavelength=None):
        super(LA1608_A, self).__init__(f=75.0, fb=72.0, R1=38.6, R2=float("+inf"), tc=4.1, te=2.0, n=None, mat=N_BK7,
                                      diameter=25.4, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1608-A',
                                      label="LA1608_A", wavelength=wavelength, wavelengthRef=0.5876)

class LA1134_A(SingletLens):
    """ LA1134-A

    .. csv-table::
        :header: Parameter, value

        "fa", "60.0"
        "fb", "56.7"
        "R1", "30.9"
        "R2", "+Inf"
        "tc", "4.7"
        "te", "2.0"
        "n", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1134-A
    """

    def __init__(self, wavelength=None):
        super(LA1134_A, self).__init__(f=60.0, fb=56.7, R1=30.9, R2=float("+inf"), tc=4.7, te=2.0, n=None, mat=N_BK7,
                                      diameter=25.4, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1134-A',
                                      label="LA1134_A", wavelength=wavelength, wavelengthRef=0.5876)

class LA1131_A(SingletLens):
    """ LA1131-A

    .. csv-table::
        :header: Parameter, value

        "fa", "50.0"
        "fb", "46.3"
        "R1", "25.8"
        "R2", "+Inf"
        "tc", "5.3"
        "te", "2.0"
        "n", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1131-A
    """

    def __init__(self, wavelength=None):
        super(LA1131_A, self).__init__(f=50.0, fb=46.3, R1=25.8, R2=float("+inf"), tc=5.3, te=2.0, n=None, mat=N_BK7,
                                      diameter=25.4, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1131-A',
                                      label="LA1131_A", wavelength=wavelength, wavelengthRef=0.5876)

class LA1422_A(SingletLens):
    """ LA1422-A

    .. csv-table::
        :header: Parameter, value

        "fa", "40.0"
        "fb", "35.7"
        "R1", "20.6"
        "R2", "+Inf"
        "tc", "6.4"
        "te", "2.0"
        "n", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1422-A
    """

    def __init__(self, wavelength=None):
        super(LA1422_A, self).__init__(f=40.0, fb=35.7, R1=20.6, R2=float("+inf"), tc=6.4, te=2.0, n=None, mat=N_BK7,
                                      diameter=25.4, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1422-A',
                                      label="LA1422_A", wavelength=wavelength, wavelengthRef=0.5876)
        
class LA1805_A(SingletLens):
    """ LA1805-A

    .. csv-table::
        :header: Parameter, value

        "fa", "30.0"
        "fb", "24.2"
        "R1", "15.5"
        "R2", "+Inf"
        "tc", "8.6"
        "te", "2.0"
        "n", "0.5876"
        "diameter", "25.4"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1805-A
    """

    def __init__(self, wavelength=None):
        super(LA1805_A, self).__init__(f=30.0, fb=24.2, R1=15.5, R2=float("+inf"), tc=8.6, te=2.0, n=None, mat=N_BK7,
                                      diameter=25.4, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1805-A',
                                      label="LA1805_A", wavelength=wavelength, wavelengthRef=0.5876)

class LA1274_A(SingletLens):
    """ LA1274-A

    .. csv-table::
        :header: Parameter, value

        "fa", "40.0"
        "fb", "34.0"
        "R1", "20.6"
        "R2", "+Inf"
        "tc", "9.0"
        "te", "2.5"
        "n", "0.5876"
        "diameter", "30.0"
        "Design Wavelengths", "587.6 nm"

    Notes
    -----
    More info: https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1274-A
    """

    def __init__(self, wavelength=None):
        super(LA1274_A, self).__init__(f=40.0, fb=34.0, R1=20.6, R2=float("+inf"), tc=9.0, te=2.5, n=None, mat=N_BK7,
                                      diameter=30.0, url='https://www.thorlabs.com/thorproduct.cfm?partnumber=LA1274-A',
                                      label="LA1274_A", wavelength=wavelength, wavelengthRef=0.5876)


class AC020_004_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC020_004_A,self).__init__(fa=4.0,fb=2.92, R1=2.38, R2=-2.18, R3=-7.87, 
                                    tc1=1.11, tc2=1.3, te=2.13, n1=None, mat1=N_SK16, n2=None, mat2=N_LASF9, diameter=2.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC020-004-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_008_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_A,self).__init__(fa=7.5,fb=5.2, R1=5.3, R2=-3.9, R3=-17.1, 
                                    tc1=2.8, tc2=1.7, te=3.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC050-008-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_010_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_A,self).__init__(fa=10.0,fb=7.9, R1=6.6, R2=-4.3, R3=-15.4, 
                                    tc1=2.5, tc2=1.9, te=3.7, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC050-010-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_015_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_A,self).__init__(fa=15.0,fb=13.6, R1=12.5, R2=-5.3, R3=-12.1, 
                                    tc1=2.7, tc2=2.1, te=4.3, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC050-015-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC060_010_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_A,self).__init__(fa=10.0,fb=7.9, R1=6.2, R2=-4.6, R3=-19.6, 
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC060-010-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_013_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_A,self).__init__(fa=12.7,fb=10.3, R1=7.1, R2=-5.9, R3=-40.4, 
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC064-013-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_015_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_A,self).__init__(fa=15.0,fb=13.0, R1=8.8, R2=-6.6, R3=-21.7, 
                                    tc1=2.5, tc2=1.5, te=3.2, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC064-015-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_010_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_A,self).__init__(fa=10.0,fb=6.7, R1=7.1, R2=-5.3, R3=-22.7, 
                                    tc1=4.5, tc2=2.0, te=4.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC080-010-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_016_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_A,self).__init__(fa=16.0,fb=13.9, R1=11.0, R2=-9.2, R3=-46.8, 
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC080-016-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_020_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_A,self).__init__(fa=20.0,fb=17.8, R1=11.1, R2=-9.2, R3=-34.8, 
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC080-020-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_030_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_A,self).__init__(fa=30.0,fb=27.8, R1=16.0, R2=-13.5, R3=-59.4, 
                                    tc1=2.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC080-030-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_019_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_A,self).__init__(fa=19.0,fb=15.7, R1=12.9, R2=-11.0, R3=-59.3, 
                                    tc1=4.5, tc2=1.5, te=4.0, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=121',
                                    label="AC127-019-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_025_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_A,self).__init__(fa=25.0,fb=21.5, R1=18.8, R2=-10.6, R3=-68.1, 
                                    tc1=5.0, tc2=2.0, te=5.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=122',
                                    label="AC127-025-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_030_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_A,self).__init__(fa=30.0,fb=27.5, R1=17.9, R2=-13.5, R3=-44.2, 
                                    tc1=3.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=123',
                                    label="AC127-030-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_050_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_A,self).__init__(fa=50.0,fb=47.2, R1=27.4, R2=-22.5, R3=-91.8, 
                                    tc1=3.5, tc2=1.5, te=4.0, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=124',
                                    label="AC127-050-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_075_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_A,self).__init__(fa=75.0,fb=72.9, R1=41.3, R2=-34.0, R3=-137.1, 
                                    tc1=2.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=125',
                                    label="AC127-075-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_030_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_A,self).__init__(fa=30.0,fb=22.9, R1=20.9, R2=-16.7, R3=-79.8, 
                                    tc1=12.0, tc2=2.0, te=8.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=126',
                                    label="AC254-030-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_035_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_A,self).__init__(fa=35.2,fb=27.3, R1=24.0, R2=-19.1, R3=-102.1, 
                                    tc1=12.0, tc2=2.0, te=9.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=127',
                                    label="AC254-035-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_040_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_A,self).__init__(fa=40.1,fb=33.4, R1=23.7, R2=-20.1, R3=-57.7, 
                                    tc1=10.0, tc2=2.5, te=7.4, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=128',
                                    label="AC254-040-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_045_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_A,self).__init__(fa=45.0,fb=40.2, R1=31.2, R2=-25.9, R3=-130.6, 
                                    tc1=7.0, tc2=2.0, te=5.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=129',
                                    label="AC254-045-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_050_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_A,self).__init__(fa=50.2,fb=43.4, R1=33.3, R2=-22.3, R3=-291.1, 
                                    tc1=9.0, tc2=2.5, te=8.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=130',
                                    label="AC254-050-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_050_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_050_A,self).__init__(fa=50.0,fb=44.3, R1=34.0, R2=-29.4, R3=-161.5, 
                                    tc1=8.5, tc2=2.0, te=6.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=131',
                                    label="AC300-050-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_080_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_080_A,self).__init__(fa=80.0,fb=74.3, R1=56.0, R2=-44.2, R3=-219.8, 
                                    tc1=8.5, tc2=2.0, te=7.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=132',
                                    label="AC300-080-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_100_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_100_A,self).__init__(fa=100.0,fb=96.4, R1=70.0, R2=-57.0, R3=-284.4, 
                                    tc1=5.0, tc2=2.0, te=5.0, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=133',
                                    label="AC300-100-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_075_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_A,self).__init__(fa=74.9,fb=61.8, R1=50.8, R2=-41.7, R3=-247.7, 
                                    tc1=20.0, tc2=3.0, te=14.9, n1=None, mat1=E_BAF11, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=134',
                                    label="AC508-075-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_080_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_A,self).__init__(fa=80.0,fb=69.9, R1=54.9, R2=-46.4, R3=-247.2, 
                                    tc1=16.0, tc2=2.0, te=10.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=135',
                                    label="AC508-080-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_100_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_A,self).__init__(fa=100.0,fb=89.0, R1=71.1, R2=-44.2, R3=-363.1, 
                                    tc1=16.0, tc2=4.0, te=14.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=136',
                                    label="AC508-100-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_150_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_A,self).__init__(fa=150.0,fb=140.4, R1=83.2, R2=-72.1, R3=-247.7, 
                                    tc1=12.0, tc2=3.0, te=9.7, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=137',
                                    label="AC508-150-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_180_Ag(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_180_Ag,self).__init__(fa=180.0,fb=172.7, R1=109.7, R2=-80.7, R3=-238.5, 
                                    tc1=12.0, tc2=2.0, te=9.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=138',
                                    label="AC508-180-Ag", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_020_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_020_A,self).__init__(fa=-20.0,fb=-22.3, R1=-13.5, R2=14.3, R3=87.9, 
                                    tc1=1.5, tc2=3.0, te=6.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=139',
                                    label="ACN127-020-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_025_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_025_A,self).__init__(fa=-25.0,fb=-27.0, R1=-16.9, R2=16.5, R3=97.7, 
                                    tc1=1.5, tc2=2.5, te=5.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=140',
                                    label="ACN127-025-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_030_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_030_A,self).__init__(fa=-30.0,fb=-32.2, R1=-16.2, R2=16.5, R3=154.2, 
                                    tc1=1.5, tc2=2.3, te=5.2, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=141',
                                    label="ACN127-030-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_050_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_050_A,self).__init__(fa=-50.0,fb=-52.3, R1=-25.6, R2=25.6, R3=372.7, 
                                    tc1=1.5, tc2=2.2, te=4.6, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=142',
                                    label="ACN127-050-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_040_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_040_A,self).__init__(fa=-40.1,fb=-43.6, R1=-27.1, R2=27.1, R3=189.2, 
                                    tc1=2.0, tc2=5.0, te=10.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF11, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=143',
                                    label="ACN254-040-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_050_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_050_A,self).__init__(fa=-50.0,fb=-53.2, R1=-34.0, R2=32.5, R3=189.2, 
                                    tc1=2.0, tc2=4.5, te=9.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=144',
                                    label="ACN254-050-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_075_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_075_A,self).__init__(fa=-75.1,fb=-78.8, R1=-39.0, R2=39.2, R3=489.8, 
                                    tc1=2.0, tc2=4.3, te=8.6, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=145',
                                    label="ACN254-075-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_100_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_100_A,self).__init__(fa=-100.1,fb=-103.6, R1=-52.0, R2=49.9, R3=600.0, 
                                    tc1=2.0, tc2=4.0, te=7.7, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=146',
                                    label="ACN254-100-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_200_Ag(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_200_Ag,self).__init__(fa=200.0,fb=190.6, R1=106.2, R2=-92.1, R3=-409.4, 
                                    tc1=10.6, tc2=6.0, te=12.8, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=147',
                                    label="ACT508-200-Ag", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_250_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_A,self).__init__(fa=250.0,fb=241.4, R1=131.2, R2=-116.0, R3=-538.1, 
                                    tc1=9.3, tc2=6.0, te=12.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=148',
                                    label="ACT508-250-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_300_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_A,self).__init__(fa=300.0,fb=291.3, R1=153.7, R2=-139.9, R3=-706.8, 
                                    tc1=8.4, tc2=7.0, te=12.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=149',
                                    label="ACT508-300-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_400_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_A,self).__init__(fa=400.0,fb=394.6, R1=292.3, R2=-148.9, R3=-398.5, 
                                    tc1=8.0, tc2=8.0, te=14.1, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=149',
                                    label="ACT508-400-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_500_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_500_A,self).__init__(fa=500.0,fb=496.3, R1=382.5, R2=-182.1, R3=-471.2, 
                                    tc1=6.0, tc2=6.0, te=10.5, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=149',
                                    label="ACT508-500-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_750_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_750_A,self).__init__(fa=750.0,fb=743.9, R1=398.6, R2=-343.7, R3=-1544.5, 
                                    tc1=6.0, tc2=6.0, te=11.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=149',
                                    label="ACT508-750-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_1000_A(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_1000_A,self).__init__(fa=1000.0,fb=996.4, R1=757.9, R2=-364.7, R3=-954.2, 
                                    tc1=6.0, tc2=6.0, te=11.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=149',
                                    label="ACT508-1000-A", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_019_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_AB,self).__init__(fa=19.0,fb=16.29, R1=14.3, R2=-13.8, R3=-68.5, 
                                    tc1=4.0, tc2=1.0, te=3.2, n1=None, mat1=N_LAK10 , n2=None, mat2= N_SF57, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12767',
                                    label="AC127-019-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_025_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_AB,self).__init__(fa=25.0,fb=21.89, R1=19.1, R2=-17.8, R3=-82.3, 
                                    tc1=4.0, tc2=2.0, te=4.6, n1=None, mat1=N_LAK10 , n2=None, mat2= N_SF57, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12768',
                                    label="AC127-025-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_030_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_AB,self).__init__(fa=30.0,fb=27.16, R1=16.7, R2=-13.8, R3=-52.1, 
                                    tc1=4.0, tc2=1.0, te=3.3, n1=None, mat1=N_BK7 , n2=None, mat2= N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12769',
                                    label="AC127-030-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_050_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_AB,self).__init__(fa=50.0,fb=46.56, R1=26.3, R2=-22.6, R3=-102.4, 
                                    tc1=4.0, tc2=2.0, te=5.0, n1=None, mat1=N_BK7 , n2=None, mat2= N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12770',
                                    label="AC127-050-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_075_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_AB,self).__init__(fa=75.0,fb=72.67, R1=38.4, R2=-35.0, R3=-177.3, 
                                    tc1=2.5, tc2=1.5, te=3.3, n1=None, mat1=N_BK7 , n2=None, mat2= N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12771',
                                    label="AC127-075-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_030_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_AB,self).__init__(fa=30.0,fb=21.22, R1=20.0, R2=-17.4, R3=-93.1, 
                                    tc1=12.0, tc2=3.0, te=9.5, n1=None, mat1=S_BAH11 , n2=None, mat2= S_TIH6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12772',
                                    label="AC254-030-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_050_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_AB,self).__init__(fa=50.0,fb=43.39, R1=34.9, R2=-28.8, R3=-137.5, 
                                    tc1=9.0, tc2=3.5, te=9.5, n1=None, mat1=N_BAF10 , n2=None, mat2= N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12773',
                                    label="AC254-050-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_075_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_AB,self).__init__(fa=75.0,fb=68.72, R1=52.0, R2=-43.4, R3=-217.4, 
                                    tc1=8.0, tc2=4.0, te=10.0, n1=None, mat1=N_BAF10 , n2=None, mat2= N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12774',
                                    label="AC254-075-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_100_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_AB,self).__init__(fa=100.0,fb=95.03, R1=92.4, R2=-48.2, R3=-152.8, 
                                    tc1=8.0, tc2=4.0, te=10.5, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12775',
                                    label="AC254-100-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_150_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_AB,self).__init__(fa=150.0,fb=143.68, R1=87.9, R2=-105.6, R3=float("+inf"),
                                    tc1=6.0, tc2=3.0, te=8.0, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12776',
                                    label="AC254-150-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_200_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_AB,self).__init__(fa=200.0,fb=194.15, R1=117.1, R2=-142.1, R3=float("+inf"),
                                    tc1=5.0, tc2=3.0, te=7.3, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12777',
                                    label="AC254-200-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_080_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_AB,self).__init__(fa=80.0,fb=72.73, R1=63.6, R2=-80.6, R3=-181.7, 
                                    tc1=12.0, tc2=3.0, te=7.8, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12778',
                                    label="AC508-080-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_180_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_180_AB,self).__init__(fa=180.0,fb=173.52, R1=144.4, R2=-115.4, R3=-328.2, 
                                    tc1=9.5, tc2=4.0, te=10.2, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12779',
                                    label="AC508-180-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_300_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_300_AB,self).__init__(fa=300.0,fb=289.81, R1=167.7, R2=-285.8, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.0, n1=None, mat1=N_LAK22 , n2=None, mat2= N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12780',
                                    label="AC508-300-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_400_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_400_AB,self).__init__(fa=400.0,fb=388.56, R1=184.3, R2=-274.0, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.2, n1=None, mat1=N_BAK4 , n2=None, mat2= N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12781',
                                    label="AC508-400-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_500_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_500_AB,self).__init__(fa=500.0,fb=488.04, R1=230.3, R2=-343.9, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.5, n1=None, mat1=N_BAK4 , n2=None, mat2= N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12782',
                                    label="AC508-500-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_600_AB(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_600_AB,self).__init__(fa=600.0,fb=590.52, R1=276.4, R2=-413.9, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.8, n1=None, mat1=N_BAK4 , n2=None, mat2= N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12783',
                                    label="AC508-600-AB", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC020_004_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC020_004_B,self).__init__(fa=4.0,fb=3.12, R1=3.19, R2=-1.77, R3=-5.23, 
                                    tc1=1.24, tc2=0.95, te=1.93, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=2.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC020-004-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_008_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_B,self).__init__(fa=7.5,fb=4.8, R1=4.6, R2=-3.9, R3=-36.0, 
                                    tc1=2.8, tc2=1.8, te=3.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=260',
                                    label="AC050-008-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_010_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_B,self).__init__(fa=10.0,fb=8.0, R1=6.6, R2=-5.3, R3=-24.9, 
                                    tc1=2.2, tc2=1.6, te=3.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=261',
                                    label="AC050-010-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_015_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_B,self).__init__(fa=15.0,fb=13.0, R1=10.3, R2=-7.6, R3=-32.1, 
                                    tc1=2.3, tc2=1.7, te=3.6, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=262',
                                    label="AC050-015-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC060_010_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_B,self).__init__(fa=10.0,fb=8.1, R1=7.1, R2=-5.3, R3=-19.5, 
                                    tc1=2.5, tc2=1.5, te=2.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=263',
                                    label="AC060-010-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_013_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_B,self).__init__(fa=12.7,fb=10.7, R1=8.6, R2=-6.7, R3=-29.0, 
                                    tc1=2.5, tc2=1.4, te=3.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=264',
                                    label="AC064-013-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_015_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_B,self).__init__(fa=15.0,fb=13.1, R1=10.3, R2=-7.8, R3=-32.9, 
                                    tc1=2.4, tc2=1.5, te=3.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=265',
                                    label="AC064-015-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_010_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_B,self).__init__(fa=10.0,fb=7.0, R1=7.6, R2=-4.6, R3=-30.6, 
                                    tc1=4.5, tc2=1.3, te=4.4, n1=None, mat1=N_LAK10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=266',
                                    label="AC080-010-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_016_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_B,self).__init__(fa=16.0,fb=14.0, R1=11.0, R2=-8.6, R3=-35.8, 
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=267',
                                    label="AC080-016-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_020_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_B,self).__init__(fa=20.0,fb=18.2, R1=13.5, R2=-10.6, R3=-47.8, 
                                    tc1=2.3, tc2=1.3, te=2.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=268',
                                    label="AC080-020-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_030_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_B,self).__init__(fa=30.0,fb=27.7, R1=18.5, R2=-16.2, R3=-106.0, 
                                    tc1=2.5, tc2=1.5, te=3.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=269',
                                    label="AC080-030-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_020_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_020_B,self).__init__(fa=-20.0,fb=-22.5, R1=-12.3, R2=14.0, R3=152.8, 
                                    tc1=1.5, tc2=3.0, te=6.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=270',
                                    label="ACN127-020-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_025_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_025_B,self).__init__(fa=-25.0,fb=-27.7, R1=-13.6, R2=17.1, R3=-859.0, 
                                    tc1=1.5, tc2=2.8, te=5.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=271',
                                    label="ACN127-025-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_030_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_030_B,self).__init__(fa=-30.0,fb=-32.0, R1=-19.3, R2=18.4, R3=106.4, 
                                    tc1=1.5, tc2=2.5, te=5.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=272',
                                    label="ACN127-030-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN127_050_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN127_050_B,self).__init__(fa=-50.0,fb=-52.5, R1=-24.4, R2=30.4, R3=-291.1, 
                                    tc1=1.5, tc2=2.0, te=4.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=273',
                                    label="ACN127-050-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_019_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_B,self).__init__(fa=19.0,fb=15.5, R1=12.2, R2=-10.6, R3=-77.4, 
                                    tc1=4.5, tc2=1.5, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=274',
                                    label="AC127-019-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_025_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_B,self).__init__(fa=25.0,fb=21.1, R1=16.2, R2=-13.3, R3=-68.5, 
                                    tc1=5.0, tc2=2.0, te=5.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=275',
                                    label="AC127-025-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_030_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_B,self).__init__(fa=30.0,fb=27.3, R1=19.8, R2=-16.2, R3=-79.1, 
                                    tc1=3.5, tc2=1.5, te=3.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=276',
                                    label="AC127-030-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_050_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_B,self).__init__(fa=50.0,fb=46.2, R1=24.2, R2=-26.8, R3=250.0, 
                                    tc1=3.5, tc2=1.5, te=4.2, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=277',
                                    label="AC127-050-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_075_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_B,self).__init__(fa=75.0,fb=72.0, R1=36.2, R2=-40.4, R3=398.1, 
                                    tc1=2.5, tc2=1.5, te=3.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=278',
                                    label="AC127-075-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_040_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_040_B,self).__init__(fa=-40.0,fb=-43.4, R1=-24.43, R2=27.86, R3=332.30, 
                                    tc1=2.0, tc2=4.0, te=9.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=279',
                                    label="ACN254-040-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_050_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_050_B,self).__init__(fa=-50.0,fb=-53.8, R1=-27.05, R2=33.91, R3=-1330.50, 
                                    tc1=2.0, tc2=4.0, te=9.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=280',
                                    label="ACN254-050-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_075_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_075_B,self).__init__(fa=-75.0,fb=-78.9, R1=-37.14, R2=46.39, R3=-494.3, 
                                    tc1=2.0, tc2=3.8, te=7.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=281',
                                    label="ACN254-075-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACN254_100_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACN254_100_B,self).__init__(fa=-100.1,fb=-103.9, R1=-48.8, R2=59.0, R3=-580.8, 
                                    tc1=2.0, tc2=3.4, te=6.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=282',
                                    label="ACN254-100-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_030_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_B,self).__init__(fa=30.0,fb=23.0, R1=21.09, R2=-16.18, R3=-79.08, 
                                    tc1=12.0, tc2=1.5, te=8.2, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=283',
                                    label="AC254-030-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_035_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_B,self).__init__(fa=35.0,fb=28.4, R1=23.99, R2=-18.62, R3=-97.27, 
                                    tc1=10.5, tc2=1.5, te=7.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=284',
                                    label="AC254-035-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_040_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_B,self).__init__(fa=40.0,fb=32.8, R1=26.12, R2=-21.28, R3=-137.09, 
                                    tc1=10.0, tc2=2.5, te=8.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=285',
                                    label="AC254-040-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_045_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_B,self).__init__(fa=45.0,fb=39.6, R1=29.38, R2=-25.05, R3=-127.06, 
                                    tc1=7.8, tc2=1.6, te=5.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=286',
                                    label="AC254-045-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_050_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_B,self).__init__(fa=50.0,fb=45.0, R1=33.55, R2=-27.05, R3=-125.60, 
                                    tc1=7.5, tc2=1.8, te=6.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=287',
                                    label="AC254-050-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_060_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_060_B,self).__init__(fa=60.0,fb=55.8, R1=39.48, R2=-33.0, R3=-165.20, 
                                    tc1=6.0, tc2=1.7, te=5.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=288',
                                    label="AC254-060-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_075_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_B,self).__init__(fa=75.0,fb=69.9, R1=36.9, R2=-42.17, R3=417.8, 
                                    tc1=5.0, tc2=1.6, te=4.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=289',
                                    label="AC254-075-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_080_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_080_B,self).__init__(fa=80.3,fb=73.5, R1=38.7, R2=-43.2, R3=374.0, 
                                    tc1=6.6, tc2=2.0, te=6.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=290',
                                    label="AC254-080-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_100_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_B,self).__init__(fa=100.0,fb=97.1, R1=66.68, R2=-53.7, R3=-259.41, 
                                    tc1=4.0, tc2=1.5, te=4.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=291',
                                    label="AC254-100-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_125_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_125_B,self).__init__(fa=125.0,fb=115.4, R1=44.5, R2=-55.3, R3=930.5, 
                                    tc1=6.0, tc2=6.0, te=10.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF8, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=292',
                                    label="AC254-125-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_150_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_B,self).__init__(fa=150.0,fb=144.6, R1=83.6, R2=-89.33, R3=-1330.50, 
                                    tc1=4.0, tc2=3.5, te=6.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=293',
                                    label="AC254-150-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_200_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_B,self).__init__(fa=200.0,fb=194.8, R1=106.4, R2=-96.6, R3=2000.0, 
                                    tc1=4.0, tc2=4.0, te=7.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=294',
                                    label="AC254-200-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_250_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_250_B,self).__init__(fa=250.0,fb=237.5, R1=52.0, R2=-65.31, R3=111.51, 
                                    tc1=4.0, tc2=1.5, te=4.7, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=295',
                                    label="AC254-250-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_300_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_300_B,self).__init__(fa=300.0,fb=290.0, R1=62.4, R2=-77.4, R3=134.00, 
                                    tc1=4.0, tc2=2.0, te=5.3, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=296',
                                    label="AC254-300-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_400_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_400_B,self).__init__(fa=400.0,fb=391.1, R1=83.6, R2=-106.41, R3=181.55, 
                                    tc1=3.5, tc2=1.8, te=4.8, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=297',
                                    label="AC254-400-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_500_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_500_B,self).__init__(fa=500.0,fb=480.8, R1=60.6, R2=-62.75, R3=87.57, 
                                    tc1=4.0, tc2=2.0, te=5.6, n1=None, mat1=N_SF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=298',
                                    label="AC254-500-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_050_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_050_B,self).__init__(fa=50.0,fb=42.9, R1=30.8, R2=-27.9, R3=-272.9, 
                                    tc1=9.5, tc2=2.0, te=7.2, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=299',
                                    label="AC300-050-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_080_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_080_B,self).__init__(fa=80.0,fb=75.3, R1=52.5, R2=-42.7, R3=-216.3, 
                                    tc1=6.5, tc2=2.0, te=5.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=300',
                                    label="AC300-080-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_100_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_100_B,self).__init__(fa=100.0,fb=94.0, R1=49.1, R2=-55.3, R3=557.4, 
                                    tc1=6.0, tc2=2.0, te=5.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=301',
                                    label="AC300-100-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_075_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_B,self).__init__(fa=75.0,fb=65.7, R1=51.8, R2=-93.1, R3=-291.1, 
                                    tc1=12.0, tc2=5.0, te=9.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=302',
                                    label="AC508-075-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_080_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_B,self).__init__(fa=80.0,fb=69.5, R1=51.8, R2=-44.6, R3=-312.6, 
                                    tc1=16.0, tc2=2.0, te=10.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=303',
                                    label="AC508-080-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_100_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_B,self).__init__(fa=100.0,fb=91.5, R1=65.8, R2=-56.0, R3=-280.6, 
                                    tc1=13.0, tc2=2.0, te=8.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=304',
                                    label="AC508-100-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_150_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_B,self).__init__(fa=150.0,fb=145.3, R1=112.2, R2=-95.9, R3=-325.1, 
                                    tc1=8.2, tc2=5.0, te=9.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=305',
                                    label="AC508-150-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_200_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_200_B,self).__init__(fa=200.0,fb=193.2, R1=121.0, R2=-118.7, R3=-422.2, 
                                    tc1=8.2, tc2=5.0, te=9.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF57, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=306',
                                    label="ACT508-200-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_250_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_B,self).__init__(fa=250.0,fb=241.8, R1=137.7, R2=-137.7, R3=-930.4, 
                                    tc1=8.1, tc2=6.0, te=11.4, n1=None, mat1=N_SK2, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=307',
                                    label="ACT508-250-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_300_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_B,self).__init__(fa=300.0,fb=291.4, R1=158.1, R2=-171.1, R3=-1529.9, 
                                    tc1=8.0, tc2=6.0, te=11.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=308',
                                    label="ACT508-300-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_400_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_B,self).__init__(fa=400.0,fb=389.5, R1=189.8, R2=-152.8, R3=-2290.9, 
                                    tc1=8.0, tc2=6.0, te=12.5, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=309',
                                    label="ACT508-400-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_500_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_500_B,self).__init__(fa=500.0,fb=491.1, R1=233.8, R2=-192.8, R3=-2471.1, 
                                    tc1=6.0, tc2=6.0, te=10.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=310',
                                    label="ACT508-500-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_750_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_750_B,self).__init__(fa=750.0,fb=742.4, R1=386.7, R2=-269.6, R3=float("+inf"),
                                    tc1=6.0, tc2=5.0, te=10.2, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=311',
                                    label="ACT508-750-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_1000_B(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_1000_B,self).__init__(fa=1000.0,fb=991.1, R1=465.2, R2=-388.7, R3=-4726.2, 
                                    tc1=6.0, tc2=6.0, te=11.4, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=312',
                                    label="ACT508-1000-B", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC020_004_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC020_004_C,self).__init__(fa=3.99,fb=2.45, R1=1.89, R2=-2.0, R3=-19.71, 
                                    tc1=1.35, tc2=1.0, te=2.04, n1=None, mat1=S_PHM52, n2=None, mat2=S_NPH2, diameter=2.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=899',
                                    label="AC020-004-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_008_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_C,self).__init__(fa=7.5,fb=5.2, R1=4.6, R2=-3.9, R3=-23.9, 
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=900',
                                    label="AC050-008-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_010_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_C,self).__init__(fa=10.0,fb=6.9, R1=4.6, R2=-4.6, R3=36.0, 
                                    tc1=2.5, tc2=1.5, te=3.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=901',
                                    label="AC050-010-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC050_015_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_C,self).__init__(fa=15.0,fb=11.6, R1=5.3, R2=-5.5, R3=15.2, 
                                    tc1=2.0, tc2=1.3, te=2.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=902',
                                    label="AC050-015-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC060_010_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_C,self).__init__(fa=10.0,fb=8.5, R1=10.4, R2=-3.6, R3=-9.2, 
                                    tc1=3.5, tc2=1.3, te=3.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=903',
                                    label="AC060-010-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_013_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_C,self).__init__(fa=12.7,fb=11.4, R1=13.2, R2=-4.9, R3=-12.4, 
                                    tc1=2.8, tc2=1.3, te=3.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=904',
                                    label="AC064-013-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC064_015_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_C,self).__init__(fa=15.0,fb=14.4, R1=22.7, R2=-4.9, R3=-11.3, 
                                    tc1=2.3, tc2=1.3, te=2.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=905',
                                    label="AC064-015-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_010_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_C,self).__init__(fa=10.0,fb=7.2, R1=7.1, R2=-4.9, R3=-20.9, 
                                    tc1=4.2, tc2=1.3, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=906',
                                    label="AC080-010-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_016_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_C,self).__init__(fa=16.0,fb=12.3, R1=7.5, R2=-7.8, R3=68.5, 
                                    tc1=3.5, tc2=1.3, te=3.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=907',
                                    label="AC080-016-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_020_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_C,self).__init__(fa=20.0,fb=15.7, R1=7.8, R2=-8.6, R3=31.9, 
                                    tc1=3.3, tc2=1.3, te=3.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=908',
                                    label="AC080-020-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC080_030_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_C,self).__init__(fa=30.0,fb=27.3, R1=12.3, R2=-16.0, R3=-70.4, 
                                    tc1=2.3, tc2=2.3, te=3.7, n1=None, mat1=N_PK52A, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=909',
                                    label="AC080-030-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_019_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_C,self).__init__(fa=19.0,fb=15.4, R1=12.4, R2=-10.0, R3=-48.8, 
                                    tc1=5.0, tc2=1.5, te=4.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=910',
                                    label="AC127-019-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_025_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_C,self).__init__(fa=25.0,fb=20.3, R1=12.0, R2=-12.9, R3=151.7, 
                                    tc1=4.7, tc2=1.5, te=4.6, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=911',
                                    label="AC127-025-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_030_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_C,self).__init__(fa=30.0,fb=24.5, R1=12.4, R2=-14.0, R3=65.3, 
                                    tc1=4.7, tc2=1.5, te=4.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=912',
                                    label="AC127-030-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_050_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_C,self).__init__(fa=49.9,fb=43.5, R1=16.0, R2=-18.4, R3=44.6, 
                                    tc1=4.0, tc2=1.5, te=4.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=913',
                                    label="AC127-050-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC127_075_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_C,self).__init__(fa=75.1,fb=69.8, R1=23.2, R2=-27.9, R3=66.7, 
                                    tc1=3.0, tc2=1.5, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=914',
                                    label="AC127-075-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_030_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_C,self).__init__(fa=30.4,fb=22.2, R1=21.1, R2=-15.2, R3=-71.1, 
                                    tc1=13.0, tc2=1.8, te=9.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=915',
                                    label="AC254-030-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_035_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_C,self).__init__(fa=35.1,fb=27.4, R1=23.2, R2=-17.9, R3=-105.2, 
                                    tc1=11.5, tc2=1.8, te=8.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=916',
                                    label="AC254-035-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_040_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_C,self).__init__(fa=40.0,fb=32.8, R1=24.4, R2=-21.1, R3=-143.9, 
                                    tc1=10.0, tc2=1.8, te=7.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=917',
                                    label="AC254-040-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_045_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_C,self).__init__(fa=45.0,fb=36.7, R1=22.9, R2=-23.7, R3=900.0, 
                                    tc1=9.6, tc2=1.8, te=7.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=918',
                                    label="AC254-045-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_050_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_C,self).__init__(fa=50.0,fb=41.2, R1=22.9, R2=-25.9, R3=194.5, 
                                    tc1=9.0, tc2=1.8, te=7.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=919',
                                    label="AC254-050-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_060_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_060_C,self).__init__(fa=60.0,fb=50.5, R1=23.9, R2=-28.1, R3=112.1, 
                                    tc1=8.3, tc2=1.8, te=7.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=920',
                                    label="AC254-060-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_075_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_C,self).__init__(fa=75.1,fb=65.0, R1=26.4, R2=-29.4, R3=84.9, 
                                    tc1=7.6, tc2=1.8, te=7.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=921',
                                    label="AC254-075-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_100_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_C,self).__init__(fa=100.1,fb=90.4, R1=32.1, R2=-38.0, R3=93.5, 
                                    tc1=6.5, tc2=1.8, te=6.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=922',
                                    label="AC254-100-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_125_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_125_C,self).__init__(fa=125.0,fb=115.35, R1=36.9, R2=-47.5, R3=108.6, 
                                    tc1=5.0, tc2=3.0, te=6.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=923',
                                    label="AC254-125-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_150_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_C,self).__init__(fa=150.5,fb=140.8, R1=42.7, R2=-52.0, R3=111.5, 
                                    tc1=5.0, tc2=2.5, te=6.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=924',
                                    label="AC254-150-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_200_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_C,self).__init__(fa=200.1,fb=193.1, R1=70.0, R2=-95.9, R3=274.3, 
                                    tc1=4.0, tc2=3.0, te=6.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=925',
                                    label="AC254-200-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_250_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_250_C,self).__init__(fa=249.2,fb=235.2, R1=44.0, R2=-57.7, R3=93.1, 
                                    tc1=4.5, tc2=2.5, te=6.0, n1=None, mat1=N_SF2, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=926',
                                    label="AC254-250-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_300_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_300_C,self).__init__(fa=299.9,fb=285.8, R1=52.5, R2=-68.5, R3=112.2, 
                                    tc1=4.5, tc2=2.5, te=6.2, n1=None, mat1=N_SF2, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=927',
                                    label="AC254-300-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_400_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_400_C,self).__init__(fa=400.1,fb=386.7, R1=70.0, R2=-93.1, R3=151.4, 
                                    tc1=4.2, tc2=2.5, te=6.1, n1=None, mat1=N_SF2, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=928',
                                    label="AC254-400-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC254_500_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_500_C,self).__init__(fa=497.6,fb=486.7, R1=87.9, R2=-115.5, R3=194.5, 
                                    tc1=3.5, tc2=2.0, te=5.0, n1=None, mat1=N_SF2, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=929',
                                    label="AC254-500-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_050_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_050_C,self).__init__(fa=50.1,fb=44.7, R1=41.7, R2=-22.7, R3=-75.7, 
                                    tc1=10.0, tc2=2.0, te=7.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=930',
                                    label="AC300-050-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_080_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_080_C,self).__init__(fa=80.5,fb=68.5, R1=29.4, R2=-33.9, R3=97.7, 
                                    tc1=9.5, tc2=2.0, te=8.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=931',
                                    label="AC300-080-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC300_100_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC300_100_C,self).__init__(fa=99.9,fb=87.8, R1=33.5, R2=-39.2, R3=100.7, 
                                    tc1=8.5, tc2=2.2, te=8.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=30.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=932',
                                    label="AC300-100-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_075_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_C,self).__init__(fa=75.4,fb=63.0, R1=49.9, R2=-39.1, R3=-230.7, 
                                    tc1=19.0, tc2=2.5, te=13.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=933',
                                    label="AC508-075-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_080_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_C,self).__init__(fa=80.3,fb=66.9, R1=47.2, R2=-43.2, R3=-640.7, 
                                    tc1=18.0, tc2=2.5, te=12.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=934',
                                    label="AC508-080-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_100_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_C,self).__init__(fa=99.7,fb=83.0, R1=44.7, R2=-48.3, R3=259.4, 
                                    tc1=17.0, tc2=2.5, te=12.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=935',
                                    label="AC508-100-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_150_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_C,self).__init__(fa=150.2,fb=117.7, R1=39.5, R2=-49.9, R3=83.6, 
                                    tc1=18.0, tc2=5.0, te=17.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=936',
                                    label="AC508-150-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class AC508_200_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_200_C,self).__init__(fa=199.2,fb=182.7, R1=67.1, R2=-87.6, R3=234.3, 
                                    tc1=12.0, tc2=3.0, te=11.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=937',
                                    label="AC508-200-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_250_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_C,self).__init__(fa=250.0,fb=235.7, R1=104.7, R2=-110.1, R3=349.5, 
                                    tc1=10.0, tc2=5.0, te=12.8, n1=None, mat1=H_LAF3B, n2=None, mat2=H_ZF52GT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=938',
                                    label="ACT508-250-C", wavelength=wavelength, wavelengthRef=0.5876)
    
class ACT508_300_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_C,self).__init__(fa=300.0,fb=290.8, R1=199.7, R2=-91.4, R3=float("+inf"),
                                    tc1=10.0, tc2=5.0, te=13.4, n1=None, mat1=H_LAF3B, n2=None, mat2=H_ZF13, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=939',
                                    label="ACT508-300-C", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_400_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_C,self).__init__(fa=400.0,fb=389.7, R1=228.7, R2=-64.9, R3=float("+inf"),
                                    tc1=10.0, tc2=6.0, te=14.6, n1=None, mat1=H_ZK50, n2=None, mat2=H_F4, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=940',
                                    label="ACT508-400-C", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_500_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_500_C,self).__init__(fa=499.7,fb=474.3, R1=86.1, R2=-103.2, R3=166.0,
                                    tc1=8.8, tc2=3.0, te=9.9, n1=None, mat1=N_SF5, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=941',
                                    label="AC508-500-C", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_750_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_750_C,self).__init__(fa=748.9,fb=710.6, R1=91.6, R2=-95.9, R3=130.6,
                                    tc1=8.8, tc2=3.0, te=10.7, n1=None, mat1=N_SF10, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=942',
                                    label="AC508-750-C", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_1000_C(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_1000_C,self).__init__(fa=1010.0,fb=990.3, R1=173.0, R2=-234.3, R3=336.0,
                                    tc1=6.0, tc2=3.0, te=8.1, n1=None, mat1=N_SF5, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=943',
                                    label="AC508-1000-C", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_008_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_A_ML,self).__init__(fa=7.5,fb=5.2, R1=5.3, R2=-3.9, R3=-17.1,
                                    tc1=2.8, tc2=1.7, te=3.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2696',
                                    label="AC050-008-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_010_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_A_ML,self).__init__(fa=10.0,fb=7.9, R1=6.6, R2=-4.3, R3=-15.4,
                                    tc1=2.5, tc2=1.9, te=3.7, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2697',
                                    label="AC050-010-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_015_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_A_ML,self).__init__(fa=15.0,fb=13.6, R1=12.5, R2=-5.3, R3=-12.1,
                                    tc1=2.7, tc2=2.1, te=4.3, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2698',
                                    label="AC050-015-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC060_010_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_A_ML,self).__init__(fa=10.0,fb=7.9, R1=6.2, R2=-4.6, R3=-19.6,
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2699',
                                    label="AC060-010-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_013_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_A_ML,self).__init__(fa=12.7,fb=10.3, R1=7.1, R2=-5.9, R3=-40.4,
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_BAK4, n2=None, mat2=SF5, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2700',
                                    label="AC064-013-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_015_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_A_ML,self).__init__(fa=15.0,fb=13.0, R1=8.8, R2=-6.6, R3=-21.7,
                                    tc1=2.5, tc2=1.5, te=3.2, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2701',
                                    label="AC064-015-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_010_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_A_ML,self).__init__(fa=10.0,fb=6.7, R1=7.1, R2=-5.3, R3=-22.7,
                                    tc1=4.5, tc2=2.0, te=4.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2702',
                                    label="AC080-010-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_016_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_A_ML,self).__init__(fa=16.0,fb=13.9, R1=11.0, R2=-9.2, R3=-46.8,
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2703',
                                    label="AC080-016-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_020_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_A_ML,self).__init__(fa=20.0,fb=17.8, R1=11.1, R2=-9.2, R3=-34.8,
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2704',
                                    label="AC080-020-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_030_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_A_ML,self).__init__(fa=30.0,fb=27.8, R1=16.0, R2=-13.5, R3=-59.4,
                                    tc1=2.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2705',
                                    label="AC080-030-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_019_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_A_ML,self).__init__(fa=19.0,fb=15.7, R1=12.9, R2=-11.0, R3=-59.3,
                                    tc1=4.5, tc2=1.5, te=4.0, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2706',
                                    label="AC127-019-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_025_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_A_ML,self).__init__(fa=25.0,fb=21.5, R1=18.8, R2=-10.6, R3=-68.1,
                                    tc1=5.0, tc2=2.0, te=5.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2707',
                                    label="AC127-025-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_030_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_A_ML,self).__init__(fa=30.0,fb=27.5, R1=17.9, R2=-13.5, R3=-44.2,
                                    tc1=3.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2708',
                                    label="AC127-030-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_050_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_A_ML,self).__init__(fa=50.0,fb=47.2, R1=27.4, R2=-22.5, R3=-91.8,
                                    tc1=3.5, tc2=1.5, te=4.0, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2709',
                                    label="AC127-050-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_075_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_A_ML,self).__init__(fa=75.0,fb=72.9, R1=41.3, R2=-34.0, R3=-137.1,
                                    tc1=2.5, tc2=1.5, te=3.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2710',
                                    label="AC127-075-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_030_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_A_ML,self).__init__(fa=30.0,fb=22.9, R1=20.9, R2=-16.7, R3=-79.8,
                                    tc1=12.0, tc2=2.0, te=8.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2711',
                                    label="AC254-030-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_035_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_A_ML,self).__init__(fa=35.0,fb=27.3, R1=24.0, R2=-19.1, R3=-102.1,
                                    tc1=12.0, tc2=2.0, te=9.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2712',
                                    label="AC254-035-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_040_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_A_ML,self).__init__(fa=40.0,fb=33.4, R1=23.7, R2=-20.1, R3=-57.7,
                                    tc1=10.0, tc2=2.5, te=7.4, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2713',
                                    label="AC254-040-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_045_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_A_ML,self).__init__(fa=45.0,fb=40.2, R1=31.2, R2=-25.9, R3=-130.6,
                                    tc1=7.0, tc2=2.0, te=5.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2714',
                                    label="AC254-045-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_050_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_A_ML,self).__init__(fa=50.0,fb=43.4, R1=33.3, R2=-22.3, R3=-291.1,
                                    tc1=9.0, tc2=2.5, te=8.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2715',
                                    label="AC254-050-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

# class AC254_060_A_ML(AchromatDoubletLens):
#     def __init__(self, wavelength=None):
#         super(AC254_060_A_ML,self).__init__(fa=60.0,fb=54.3, R1=41.7, R2=-25.9, R3=-230.7,
#                                     tc1=8.0, tc2=2.5, te=8.2, n1=None, mat1=E_BAF11, n2=None, mat2=FD10, diameter=25.4,
#                                     url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2716',
#                                     label="AC254-060-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_075_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_A_ML,self).__init__(fa=75.0,fb=70.3, R1=46.5, R2=-33.9, R3=-95.5,
                                    tc1=7.0, tc2=2.5, te=6.9, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2717',
                                    label="AC254-075-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_080_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_080_A_ML,self).__init__(fa=80.0,fb=75.3, R1=49.6, R2=-35.5, R3=-101.2,
                                    tc1=7.0, tc2=3.0, te=7.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2718',
                                    label="AC254-080-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_100_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_A_ML,self).__init__(fa=100.0,fb=97.1, R1=62.8, R2=-45.7, R3=-128.2,
                                    tc1=4.0, tc2=2.5, te=4.7, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2719',
                                    label="AC254-100-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_125_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_125_A_ML,self).__init__(fa=125.0,fb=122.0, R1=77.6, R2=-55.9, R3=-160.8,
                                    tc1=4.0, tc2=2.8, te=5.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2720',
                                    label="AC254-125-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_A_ML,self).__init__(fa=150.0,fb=146.1, R1=91.6, R2=-66.7, R3=-197.7,
                                    tc1=5.7, tc2=2.2, te=6.6, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2721',
                                    label="AC254-150-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_200_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_A_ML,self).__init__(fa=200.0,fb=194.0, R1=77.4, R2=-87.6, R3=291.1,
                                    tc1=4.0, tc2=2.5, te=5.7, n1=None, mat1=N_SSK5, n2=None, mat2=LAFN7, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2722',
                                    label="AC254-200-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_250_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_250_A_ML,self).__init__(fa=250.0,fb=246.7, R1=137.1, R2=-111.5, R3=-459.2,
                                    tc1=4.0, tc2=2.0, te=5.2, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2723',
                                    label="AC254-250-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_300_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_300_A_ML,self).__init__(fa=300.0,fb=297.0, R1=165.2, R2=-137.1, R3=-557.4,
                                    tc1=4.0, tc2=2.0, te=5.4, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2724',
                                    label="AC254-300-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_400_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_400_A_ML,self).__init__(fa=400.0,fb=396.0, R1=219.8, R2=-181.6, R3=-738.5,
                                    tc1=4.0, tc2=2.0, te=5.5, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2725',
                                    label="AC254-400-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_500_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_500_A_ML,self).__init__(fa=500.0,fb=499.9, R1=337.3, R2=-186.8, R3=-557.4,
                                    tc1=4.0, tc2=2.0, te=5.6, n1=None, mat1=N_BK7, n2=None, mat2=SF2, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2726',
                                    label="AC254-500-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_075_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_A_ML,self).__init__(fa=75.0,fb=61.7, R1=50.8, R2=-41.7, R3=-247.7,
                                    tc1=20.0, tc2=3.0, te=14.9, n1=None, mat1=E_BAF11, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2727',
                                    label="AC508-075-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_080_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_A_ML,self).__init__(fa=80.0,fb=69.9, R1=54.9, R2=-46.4, R3=-247.2,
                                    tc1=16.0, tc2=2.0, te=10.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2728',
                                    label="AC508-080-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_100_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_A_ML,self).__init__(fa=100.0,fb=89.0, R1=71.1, R2=-44.2, R3=-363.1,
                                    tc1=16.0, tc2=4.0, te=14.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2729',
                                    label="AC508-100-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_150_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_A_ML,self).__init__(fa=150.0,fb=140.4, R1=83.2, R2=-72.1, R3=-247.7,
                                    tc1=12.0, tc2=3.0, te=9.7, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2730',
                                    label="AC508-150-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_180_A_MLd(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_180_A_MLd,self).__init__(fa=180.0,fb=172.7, R1=109.7, R2=-80.7, R3=-238.5,
                                    tc1=12.0, tc2=2.0, te=9.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2731',
                                    label="AC508-180-A-MLd", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_200_A_MLd(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_200_A_MLd,self).__init__(fa=200.0,fb=190.6, R1=106.2, R2=-92.1, R3=-409.4,
                                    tc1=10.6, tc2=6.0, te=12.8, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2732',
                                    label="ACT508-200-A-MLd", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_250_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_A_ML,self).__init__(fa=250.0,fb=241.4, R1=131.2, R2=-116.0, R3=-538.1,
                                    tc1=9.3, tc2=6.0, te=12.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2733',
                                    label="ACT508-250-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_300_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_A_ML,self).__init__(fa=300.0,fb=291.3, R1=153.7, R2=-139.9, R3=-706.8,
                                    tc1=8.4, tc2=7.0, te=12.4, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2734',
                                    label="ACT508-300-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_400_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_A_ML,self).__init__(fa=400.0,fb=394.6, R1=292.3, R2=-148.9, R3=-398.5,
                                    tc1=8.0, tc2=8.0, te=14.1, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2735',
                                    label="ACT508-400-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_500_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_500_A_ML,self).__init__(fa=500.0,fb=496.3, R1=382.5, R2=-182.1, R3=-471.2,
                                    tc1=6.0, tc2=6.0, te=10.5, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2736',
                                    label="ACT508-500-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_750_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_750_A_ML,self).__init__(fa=750.0,fb=743.9, R1=398.6, R2=-343.7, R3=-1544.5,
                                    tc1=6.0, tc2=6.0, te=11.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2737',
                                    label="ACT508-750-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_1000_A_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_1000_A_ML,self).__init__(fa=1000.0,fb=996.4, R1=757.9, R2=-364.7, R3=-954.2,
                                    tc1=6.0, tc2=6.0, te=11.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2738',
                                    label="ACT508-1000-A-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_019_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_AB_ML,self).__init__(fa=19.0,fb=16.29, R1=14.3, R2=-13.8, R3=-68.5,
                                    tc1=4.0, tc2=1.0, te=3.2, n1=None, mat1=N_LAK10, n2=None, mat2=N_SF57, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12804',
                                    label="AC127-019-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_025_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_AB_ML,self).__init__(fa=25.0,fb=21.89, R1=19.1, R2=-17.8, R3=-82.3,
                                    tc1=4.0, tc2=2.0, te=4.6, n1=None, mat1=N_LAK10, n2=None, mat2=N_SF57, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12805',
                                    label="AC127-025-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_030_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_AB_ML,self).__init__(fa=30.0,fb=27.16, R1=16.7, R2=-13.8, R3=-52.1,
                                    tc1=4.0, tc2=1.0, te=3.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12806',
                                    label="AC127-030-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_050_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_AB_ML,self).__init__(fa=50.0,fb=46.56, R1=23.3, R2=-22.6, R3=-102.4,
                                    tc1=4.0, tc2=2.0, te=5.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12807',
                                    label="AC127-050-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_075_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_AB_ML,self).__init__(fa=75.0,fb=72.67, R1=38.4, R2=-35.0, R3=-1773,
                                    tc1=2.5, tc2=1.5, te=3.3, n1=None, mat1=N_BK7, n2=None, mat2=N_SF2, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12808',
                                    label="AC127-075-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_030_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_AB_ML,self).__init__(fa=30.0,fb=21.22, R1=20.0, R2=-17.4, R3=-93.1,
                                    tc1=12.0, tc2=3.0, te=9.5, n1=None, mat1=S_BAH11, n2=None, mat2=S_TIH6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12809',
                                    label="AC254-030-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_050_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_AB_ML,self).__init__(fa=50.0,fb=43.39, R1=34.9, R2=-28.8, R3=-137.5,
                                    tc1=9.0, tc2=3.5, te=9.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12810',
                                    label="AC254-050-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_075_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_AB_ML,self).__init__(fa=75.0,fb=68.72, R1=52.0, R2=-43.4, R3=-217.4,
                                    tc1=8.0, tc2=4.0, te=10.0, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12811',
                                    label="AC254-075-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_100_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_AB_ML,self).__init__(fa=100.0,fb=95.03, R1=92.4, R2=-48.2, R3=-152.8,
                                    tc1=8.0, tc2=4.0, te=10.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12812',
                                    label="AC254-100-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_AB_ML,self).__init__(fa=150.0,fb=143.68, R1=87.9, R2=-105.6, R3=float("+inf"),
                                    tc1=6.0, tc2=3.0, te=8.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12813',
                                    label="AC254-150-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_200_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_AB_ML,self).__init__(fa=200.0,fb=194.15, R1=117.1, R2=-142.1, R3=float("+inf"),
                                    tc1=5.0, tc2=3.0, te=7.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12814',
                                    label="AC254-200-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_080_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_AB_ML,self).__init__(fa=80.0,fb=72.73, R1=63.6, R2=-80.6, R3=-181.7,
                                    tc1=12.0, tc2=3.0, te=7.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12815',
                                    label="AC508-080-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_180_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_180_AB_ML,self).__init__(fa=180.0,fb=173.52, R1=144.4, R2=-115.4, R3=-328.2,
                                    tc1=9.5, tc2=4.0, te=10.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12816',
                                    label="AC508-180-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_300_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_300_AB_ML,self).__init__(fa=300.0,fb=289.81, R1=167.7, R2=-285.8, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12817',
                                    label="AC508-300-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_400_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_400_AB_ML,self).__init__(fa=400.0,fb=388.56, R1=184.3, R2=-274.0, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.2, n1=None, mat1=N_BAK4, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12818',
                                    label="AC508-400-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_500_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_500_AB_ML,self).__init__(fa=500.0,fb=488.04, R1=230.3, R2=-343.9, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.5, n1=None, mat1=N_BAK4, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12819',
                                    label="AC508-500-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_600_AB_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_600_AB_ML,self).__init__(fa=600.0,fb=590.52, R1=276.4, R2=-413.9, R3=float("+inf"),
                                    tc1=9.0, tc2=4.0, te=11.8, n1=None, mat1=N_BAK4, n2=None, mat2=N_SF10, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12820',
                                    label="AC508-600-AB-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_008_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_B_ML,self).__init__(fa=7.5,fb=4.8, R1=4.6, R2=-3.9, R3=-36.0,
                                    tc1=2.8, tc2=1.8, te=3.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3647',
                                    label="AC050-008-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_010_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_B_ML,self).__init__(fa=10.0,fb=8.0, R1=6.6, R2=-5.3, R3=-24.9,
                                    tc1=2.2, tc2=1.6, te=3.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3648',
                                    label="AC050-010-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_015_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_B_ML,self).__init__(fa=15.0,fb=13.0, R1=10.3, R2=-7.6, R3=-32.1,
                                    tc1=2.3, tc2=1.7, te=3.6, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3649',
                                    label="AC050-015-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC060_010_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_B_ML,self).__init__(fa=10.0,fb=8.1, R1=7.1, R2=-5.3, R3=-19.5,
                                    tc1=2.5, tc2=1.5, te=2.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3650',
                                    label="AC060-010-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_013_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_B_ML,self).__init__(fa=12.7,fb=10.7, R1=8.6, R2=-6.7, R3=-29.0,
                                    tc1=2.5, tc2=1.4, te=3.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3651',
                                    label="AC064-013-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_015_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_B_ML,self).__init__(fa=15.0,fb=13.1, R1=10.3, R2=-7.8, R3=-32.9,
                                    tc1=2.4, tc2=1.5, te=3.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3652',
                                    label="AC064-015-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_010_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_B_ML,self).__init__(fa=10.0,fb=7.0, R1=7.6, R2=-4.6, R3=-30.6,
                                    tc1=4.5, tc2=1.3, te=4.4, n1=None, mat1=N_LAK10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3653',
                                    label="AC080-010-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_016_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_B_ML,self).__init__(fa=16.0,fb=14.0, R1=11.0, R2=-8.6, R3=-35.8,
                                    tc1=2.5, tc2=1.5, te=3.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3654',
                                    label="AC080-016-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_020_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_B_ML,self).__init__(fa=20.0,fb=18.2, R1=13.5, R2=-10.6, R3=-47.8,
                                    tc1=2.3, tc2=1.3, te=2.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3655',
                                    label="AC080-020-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_030_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_B_ML,self).__init__(fa=30.0,fb=27.7, R1=18.5, R2=-16.2, R3=-106.0,
                                    tc1=2.5, tc2=1.5, te=3.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3656',
                                    label="AC080-030-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_019_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_B_ML,self).__init__(fa=19.0,fb=15.5, R1=12.2, R2=-10.6, R3=-77.4,
                                    tc1=4.5, tc2=1.5, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3657',
                                    label="AC127-019-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_025_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_B_ML,self).__init__(fa=25.0,fb=21.1, R1=16.2, R2=-13.3, R3=-68.5,
                                    tc1=5.0, tc2=2.0, te=5.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3658',
                                    label="AC127-025-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_030_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_B_ML,self).__init__(fa=30.0,fb=27.3, R1=19.8, R2=-16.2, R3=-79.8,
                                    tc1=3.5, tc2=1.5, te=3.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3659',
                                    label="AC127-030-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_050_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_B_ML,self).__init__(fa=50.0,fb=46.2, R1=24.2, R2=-26.8, R3=250.0,
                                    tc1=3.5, tc2=1.5, te=4.2, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3660',
                                    label="AC127-050-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_075_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_B_ML,self).__init__(fa=75.0,fb=72.0, R1=36.2, R2=-40.4, R3=398.1,
                                    tc1=2.5, tc2=1.5, te=3.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3661',
                                    label="AC127-075-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_030_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_B_ML,self).__init__(fa=30.0,fb=23.0, R1=21.09, R2=-16.18, R3=-79.08,
                                    tc1=12.0, tc2=1.5, te=8.2, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3662',
                                    label="AC254-030-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_035_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_B_ML,self).__init__(fa=35.0,fb=28.4, R1=23.99, R2=-18.62, R3=-97.27,
                                    tc1=10.5, tc2=1.5, te=7.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3663',
                                    label="AC254-035-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_040_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_B_ML,self).__init__(fa=40.0,fb=32.8, R1=26.12, R2=-21.28, R3=-137.09,
                                    tc1=10.0, tc2=2.5, te=8.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3664',
                                    label="AC254-040-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_045_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_B_ML,self).__init__(fa=45.0,fb=39.6, R1=29.38, R2=-25.05, R3=-127.06,
                                    tc1=7.8, tc2=1.6, te=5.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3665',
                                    label="AC254-045-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_050_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_B_ML,self).__init__(fa=50.0,fb=45.0, R1=33.55, R2=-27.05, R3=-125.60,
                                    tc1=7.5, tc2=1.8, te=6.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3666',
                                    label="AC254-050-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_060_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_060_B_ML,self).__init__(fa=60.0,fb=55.8, R1=39.48, R2=-33.0, R3=-165.20,
                                    tc1=6.0, tc2=1.7, te=5.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3667',
                                    label="AC254-060-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_075_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_B_ML,self).__init__(fa=75.0,fb=69.9, R1=36.9, R2=-42.17, R3=417.8,
                                    tc1=5.0, tc2=1.6, te=4.5, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3668',
                                    label="AC254-075-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_080_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_080_B_ML,self).__init__(fa=80.3,fb=73.5, R1=38.7, R2=-43.2, R3=374.0,
                                    tc1=6.6, tc2=2.0, te=6.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3669',
                                    label="AC254-080-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_100_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_B_ML,self).__init__(fa=100.0,fb=97.1, R1=66.68, R2=-53.7, R3=-259.41,
                                    tc1=4.0, tc2=1.5, te=4.0, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3670',
                                    label="AC254-100-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_125_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_125_B_ML,self).__init__(fa=125.0,fb=115.4, R1=44.5, R2=-55.3, R3=930.5,
                                    tc1=6.0, tc2=6.0, te=10.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF8, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3671',
                                    label="AC254-125-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_B_ML,self).__init__(fa=150.0,fb=144.6, R1=83.6, R2=-89.33, R3=-1330.5,
                                    tc1=4.0, tc2=3.5, te=6.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3672',
                                    label="AC254-150-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_200_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_B_ML,self).__init__(fa=200.0,fb=194.8, R1=106.4, R2=-96.6, R3=2000.0,
                                    tc1=4.0, tc2=4.0, te=7.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF10, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3673',
                                    label="AC254-200-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_250_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_250_B_ML,self).__init__(fa=250.0,fb=237.5, R1=52.0, R2=-65.31, R3=111.51,
                                    tc1=4.0, tc2=1.5, te=4.7, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3674',
                                    label="AC254-250-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_300_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_300_B_ML,self).__init__(fa=300.0,fb=290.0, R1=62.4, R2=-77.4, R3=134.00,
                                    tc1=4.0, tc2=2.0, te=5.3, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3675',
                                    label="AC254-300-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_400_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_400_B_ML,self).__init__(fa=400.0,fb=391.1, R1=83.6, R2=-106.41, R3=181.55,
                                    tc1=3.5, tc2=1.8, te=4.8, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3676',
                                    label="AC254-400-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_500_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_500_B_ML,self).__init__(fa=500.0,fb=480.8, R1=60.6, R2=-62.75, R3=87.57,
                                    tc1=4.0, tc2=2.0, te=5.6, n1=None, mat1=N_SF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3677',
                                    label="AC254-500-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_075_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_B_ML,self).__init__(fa=75.0,fb=65.7, R1=51.8, R2=-93.1, R3=-291.1,
                                    tc1=12.0, tc2=5.0, te=9.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3678',
                                    label="AC508-075-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_080_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_B_ML,self).__init__(fa=80.0,fb=69.5, R1=51.8, R2=-44.6, R3=-312.6,
                                    tc1=16.0, tc2=2.0, te=10.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3679',
                                    label="AC508-080-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_100_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_B_ML,self).__init__(fa=100.0,fb=91.5, R1=65.8, R2=-56.0, R3=-280.6,
                                    tc1=13.0, tc2=2.0, te=8.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3680',
                                    label="AC508-100-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_150_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_B_ML,self).__init__(fa=150.0,fb=145.3, R1=112.2, R2=-95.9, R3=-325.1,
                                    tc1=8.2, tc2=5.0, te=9.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3681',
                                    label="AC508-150-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_200_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_200_B_ML,self).__init__(fa=200.0,fb=193.2, R1=121.0, R2=-118.7, R3=-422.4,
                                    tc1=8.2, tc2=5.0, te=9.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF57, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3682',
                                    label="ACT508-200-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_250_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_B_ML,self).__init__(fa=250.0,fb=241.8, R1=137.7, R2=-137.7, R3=-930.4,
                                    tc1=8.1, tc2=6.0, te=11.4, n1=None, mat1=N_SK2, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3683',
                                    label="ACT508-250-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_300_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_B_ML,self).__init__(fa=300.0,fb=291.4, R1=158.1, R2=-171.1, R3=-1529.9,
                                    tc1=8.0, tc2=6.0, te=11.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF11, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3684',
                                    label="ACT508-300-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_400_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_B_ML,self).__init__(fa=400.0,fb=389.5, R1=189.8, R2=-152.8, R3=-2290.9,
                                    tc1=8.0, tc2=6.0, te=12.5, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3685',
                                    label="ACT508-400-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_500_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_500_B_ML,self).__init__(fa=500.0,fb=491.1, R1=233.8, R2=-192.8, R3=-2471.1,
                                    tc1=6.0, tc2=6.0, te=10.8, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3686',
                                    label="ACT508-500-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_750_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_750_B_ML,self).__init__(fa=750.0,fb=742.4, R1=386.7, R2=-269.6, R3=float("+inf"),
                                    tc1=6.0, tc2=5.0, te=10.2, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3687',
                                    label="ACT508-750-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_1000_B_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_1000_B_ML,self).__init__(fa=1000.0,fb=991.1, R1=465.2, R2=-388.7, R3=-4726.2,
                                    tc1=6.0, tc2=6.0, te=11.4, n1=None, mat1=N_SK2, n2=None, mat2=N_SF5, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3688',
                                    label="ACT508-1000-B-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_008_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_008_C_ML,self).__init__(fa=7.5,fb=5.2, R1=4.6, R2=-3.9, R3=-23.9,
                                    tc1=2.5, tc2=1.5, te=3.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4066',
                                    label="AC050-008-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_010_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_010_C_ML,self).__init__(fa=10.0,fb=6.9, R1=4.6, R2=-4.6, R3=36.0,
                                    tc1=2.5, tc2=1.5, te=3.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4067',
                                    label="AC050-010-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC050_015_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC050_015_C_ML,self).__init__(fa=15.0,fb=11.6, R1=5.3, R2=-5.5, R3=15.2,
                                    tc1=2.0, tc2=1.3, te=2.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=5.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4068',
                                    label="AC050-015-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC060_010_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC060_010_C_ML,self).__init__(fa=10.0,fb=8.5, R1=10.4, R2=-3.6, R3=-9.2,
                                    tc1=3.5, tc2=1.3, te=3.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4069',
                                    label="AC060-010-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_013_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_013_C_ML,self).__init__(fa=12.7,fb=11.4, R1=13.2, R2=-4.9, R3=-12.4,
                                    tc1=2.8, tc2=1.3, te=3.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4070',
                                    label="AC064-013-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC064_015_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC064_015_C_ML,self).__init__(fa=15.0,fb=14.4, R1=22.7, R2=-4.9, R3=-11.3,
                                    tc1=2.3, tc2=1.3, te=2.9, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=6.35,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4071',
                                    label="AC064-015-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_010_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_010_C_ML,self).__init__(fa=10.0,fb=7.2, R1=7.1, R2=-4.9, R3=-20.0,
                                    tc1=4.2, tc2=1.3, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4072',
                                    label="AC080-010-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_016_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_016_C_ML,self).__init__(fa=16.0,fb=12.3, R1=7.5, R2=-7.8, R3=68.5,
                                    tc1=3.5, tc2=1.3, te=3.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4073',
                                    label="AC080-016-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_020_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_020_C_ML,self).__init__(fa=20.0,fb=15.7, R1=7.8, R2=-8.6, R3=31.9,
                                    tc1=3.3, tc2=1.3, te=3.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4074',
                                    label="AC080-020-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC080_030_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC080_030_C_ML,self).__init__(fa=30.0,fb=27.3, R1=12.3, R2=-16.0, R3=-70.4,
                                    tc1=2.3, tc2=2.3, te=3.7, n1=None, mat1=N_PK52A, n2=None, mat2=N_SF6, diameter=8.0,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4075',
                                    label="AC080-030-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_019_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_019_C_ML,self).__init__(fa=19.0,fb=15.4, R1=12.4, R2=-10.0, R3=-48.8,
                                    tc1=5.0, tc2=1.5, te=4.3, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4076',
                                    label="AC127-019-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_025_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_025_C_ML,self).__init__(fa=25.0,fb=20.3, R1=12.0, R2=-12.9, R3=151.7,
                                    tc1=4.7, tc2=1.5, te=4.5, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4077',
                                    label="AC127-025-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_030_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_030_C_ML,self).__init__(fa=30.0,fb=24.5, R1=12.4, R2=-14.0, R3=65.3,
                                    tc1=4.7, tc2=1.5, te=4.8, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4078',
                                    label="AC127-030-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_050_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_050_C_ML,self).__init__(fa=50.0,fb=43.5, R1=16.0, R2=-18.4, R3=44.6,
                                    tc1=4.0, tc2=1.5, te=4.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4079',
                                    label="AC127-050-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC127_075_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC127_075_C_ML,self).__init__(fa=75.0,fb=69.8, R1=23.2, R2=-27.9, R3=66.7,
                                    tc1=3.0, tc2=1.5, te=3.9, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=12.7,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4080',
                                    label="AC127-075-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_030_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_030_C_ML,self).__init__(fa=30.0,fb=22.2, R1=21.1, R2=-15.2, R3=-71.1,
                                    tc1=13.0, tc2=1.8, te=9.4, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4081',
                                    label="AC254-030-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_035_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_035_C_ML,self).__init__(fa=35.0,fb=27.4, R1=23.2, R2=-17.9, R3=-105.2,
                                    tc1=11.5, tc2=1.8, te=8.7, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4082',
                                    label="AC254-035-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_040_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_040_C_ML,self).__init__(fa=40.0,fb=32.8, R1=24.4, R2=-21.1, R3=-143.9,
                                    tc1=10.0, tc2=1.8, te=7.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4083',
                                    label="AC254-040-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_045_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_045_C_ML,self).__init__(fa=45.0,fb=36.7, R1=22.9, R2=-23.7, R3=900.0,
                                    tc1=9.6, tc2=1.8, te=7.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4084',
                                    label="AC254-045-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_050_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_050_C_ML,self).__init__(fa=50.0,fb=41.2, R1=22.9, R2=-25.9, R3=194.5,
                                    tc1=9.0, tc2=1.8, te=7.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4085',
                                    label="AC254-050-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_060_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_060_C_ML,self).__init__(fa=60.0,fb=50.5, R1=23.9, R2=-28.1, R3=112.1,
                                    tc1=8.3, tc2=1.8, te=7.2, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4086',
                                    label="AC254-060-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_075_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_075_C_ML,self).__init__(fa=75.0,fb=64.9, R1=26.4, R2=-29.4, R3=84.9,
                                    tc1=7.6, tc2=1.8, te=7.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4087',
                                    label="AC254-075-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_100_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_100_C_ML,self).__init__(fa=100.0,fb=90.3, R1=32.1, R2=-38.0, R3=93.5,
                                    tc1=6.5, tc2=1.8, te=6.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4088',
                                    label="AC254-100-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_150_C_ML,self).__init__(fa=150.0,fb=140.8, R1=42.7, R2=-52.0, R3=111.5,
                                    tc1=5.0, tc2=2.5, te=6.3, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4089',
                                    label="AC254-150-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_200_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_200_C_ML,self).__init__(fa=200.0,fb=193.1, R1=70.0, R2=-95.9, R3=274.3,
                                    tc1=4.0, tc2=3.0, te=6.1, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4090',
                                    label="AC254-200-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_250_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_250_C_ML,self).__init__(fa=250.0,fb=235.2, R1=44.0, R2=-57.7, R3=93.1,
                                    tc1=4.5, tc2=2.5, te=6.0, n1=None, mat1=SF2, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4091',
                                    label="AC254-250-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_300_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_300_C_ML,self).__init__(fa=300.0,fb=285.8, R1=52.5, R2=-68.5, R3=112.2,
                                    tc1=4.5, tc2=2.5, te=6.2, n1=None, mat1=SF2, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4092',
                                    label="AC254-300-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_400_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_400_C_ML,self).__init__(fa=400.0,fb=386.8, R1=70.0, R2=-93.1, R3=151.4,
                                    tc1=4.2, tc2=2.5, te=6.1, n1=None, mat1=SF2, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4093',
                                    label="AC254-400-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_500_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC254_500_C_ML,self).__init__(fa=500.0,fb=486.7, R1=87.9, R2=-115.5, R3=194.5,
                                    tc1=3.5, tc2=2.0, te=5.0, n1=None, mat1=SF2, n2=None, mat2=N_SF6HT, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4094',
                                    label="AC254-500-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_075_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_075_C_ML,self).__init__(fa=75.0,fb=63.0, R1=49.9, R2=-39.1, R3=-230.7,
                                    tc1=19.0, tc2=2.5, te=13.1, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4095',
                                    label="AC508-075-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_080_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_080_C_ML,self).__init__(fa=80.0,fb=66.9, R1=47.2, R2=-43.2, R3=-640.7,
                                    tc1=18.0, tc2=2.5, te=12.6, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4096',
                                    label="AC508-080-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_100_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_100_C_ML,self).__init__(fa=100.0,fb=83.0, R1=44.7, R2=-48.3, R3=259.4,
                                    tc1=17.0, tc2=2.5, te=12.8, n1=None, mat1=N_BAF10, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4097',
                                    label="AC508-100-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_150_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_150_C_ML,self).__init__(fa=150.0,fb=117.7, R1=39.5, R2=-49.9, R3=83.6,
                                    tc1=18.0, tc2=5.0, te=17.7, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4098',
                                    label="AC508-150-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_200_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_200_C_ML,self).__init__(fa=200.0,fb=182.7, R1=67.1, R2=-87.6, R3=234.3,
                                    tc1=12.0, tc2=3.0, te=11.4, n1=None, mat1=N_LAK22, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4099',
                                    label="AC508-200-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_250_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_250_C_ML,self).__init__(fa=250.0,fb=235.7, R1=104.7, R2=-110.1, R3=349.5,
                                    tc1=10.0, tc2=5.0, te=12.8, n1=None, mat1=H_LAF3B, n2=None, mat2=H_ZF52GT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4100',
                                    label="ACT508-250-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_300_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_300_C_ML,self).__init__(fa=300.0,fb=290.8, R1=199.7, R2=-91.4, R3=float("+inf"),
                                    tc1=10.0, tc2=5.0, te=13.4, n1=None, mat1=H_LAF3B, n2=None, mat2=H_ZF13, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4101',
                                    label="ACT508-300-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class ACT508_400_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(ACT508_400_C_ML,self).__init__(fa=400.0,fb=389.7, R1=228.7, R2=-64.9, R3=float("+inf"),
                                    tc1=10.0, tc2=6.0, te=14.6, n1=None, mat1=H_ZK50, n2=None, mat2=H_F4, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4102',
                                    label="ACT508-400-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_500_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_500_C_ML,self).__init__(fa=500.0,fb=474.3, R1=86.1, R2=-103.2, R3=166.0,
                                    tc1=8.8, tc2=3.0, te=9.9, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4103',
                                    label="AC508-500-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

# class AC508_750_C_ML(AchromatDoubletLens):
#     def __init__(self, wavelength=None):
#         super(AC508_750_C_ML,self).__init__(fa=750.0,fb=710.6, R1=91.6, R2=-95.9, R3=130.6,
#                                     tc1=8.8, tc2=3.0, te=10.7, n1=None, mat1=SF10, n2=None, mat2=N_SF6HT, diameter=50.8,
#                                     url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4104',
#                                     label="AC508-750-C-ML", wavelength=wavelength, wavelengthRef=0.5876)

class AC508_1000_C_ML(AchromatDoubletLens):
    def __init__(self, wavelength=None):
        super(AC508_1000_C_ML,self).__init__(fa=1000.0,fb=990.3, R1=173.0, R2=-234.3, R3=336.0,
                                    tc1=6.0, tc2=3.0, te=8.1, n1=None, mat1=SF5, n2=None, mat2=N_SF6HT, diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4105',
                                    label="AC508-1000-C-ML", wavelength=wavelength, wavelengthRef=0.5876)
