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
        super(AC254_100_A,self).__init__(fa=100.1,fb=97.1, R1=62.8,R2=-45.7, R3=-128.2, 
                                    tc1=4.0, tc2=2.5, te=4.7, n1=None, mat1=N_BK7, n2=None, mat2=SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-100-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_125_A(AchromatDoubletLens):
    """ AC254_125_A

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
    """

    def __init__(self, wavelength= None):
        """
        Notes
        -----
        As of May 31 2020, the calculated edge thickness does not match
        the product page. There does not seem to be another place where 
        the information can be validated (the PDF doesn't show the edge thickness).
        https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120
        """
        super(AC254_125_A,self).__init__(fa=125.0,fb=122.0, R1=77.6,R2=-55.9, R3=-160.8, 
                                    tc1=4.0, tc2=2.8, te=5.0, n1=None, mat1=N_BK7, n2=None, mat2=N_SF5, diameter=25.4,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120',
                                    label="AC254-125-A", wavelength=wavelength, wavelengthRef=0.5876)

class AC254_150_A(AchromatDoubletLens):
    """ AC254_150_A

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
    """ AC254_200_A

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
    """ AC254_250_A

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
    """ AC254_300_A

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
    """ AC254_400_A

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
    """ AC254_500_A

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
    """ AC254_050_B

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
    """ AC508_075_B

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
    """ AC508_080_B

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
    """ AC508_100_B

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
                                    tc1=13.0, tc2=2.0, te=8.7, n1=N_LAK22.n(0.855), n2=N_SF6HT.n(0.855), diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-100-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_150_B(AchromatDoubletLens):
    """ AC508_150_B

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
                                    tc1=8.2, tc2=5.0, te=9.3, n1=N_LAK22.n(0.855), n2=N_SF6HT.n(0.855), diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-150-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_200_B(AchromatDoubletLens):
    """ AC508_200_B

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
                                    tc1=8.2, tc2=5.0, te=10.1, n1=N_LAK22.n(0.855), n2=N_SF6HT.n(0.855), diameter=50.8,
                                    url='https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=259',
                                    label="AC508-200-B", wavelength=wavelength, wavelengthRef=0.855)

class AC508_250_B(AchromatDoubletLens):
    """ AC508_250_B

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
    """ AC508_300_B

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
    """ AC508_400_B

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
    """ AC508_500_B

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
    """ AC508_750_B

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
    """ AC508_1000_B

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
    """ LA1608_A

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
    """ LA1134_A

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
    """ LA1131_A

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
    """ LA1422_A

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
    """ LA1805_A

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
    """ LA1274_A

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
