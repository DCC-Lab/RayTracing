import csv
from raytracing import *

"""
This is just for experimenting with building lenses from prescriptions.
We use an Olympus patent as a test, since everything is there

"""
class PrescriptionFile:
    def __init__(self, filepath, columnId=None):
        self.filepath = filepath
        self.headers = []
        self.rows = self.readRows(self.filepath)

    def readRows(self, filepath):
        rows = []
        with open(filepath) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            if csv.Sniffer().has_header(csvfile.read(1024)):
                csvfile.seek(0)
                self.headers = csvfile.readline().split(dialect.delimiter)
            else:
                csvfile.seek(0)
            fileReader = csv.reader(csvfile, dialect,
                                    quoting=csv.QUOTE_NONNUMERIC)

            for row in fileReader:
                rows.append(row)
        return rows


file = PrescriptionFile("olympus-table3.csv")

n1 = 1.33 # water immersion
olympus20xPrescription = MatrixGroup(label="OlympusTest")
for row in file.rows:
    i, R, d, n2, eta = row

    try: 
        n2 = float(n2)
    except:
        n2 = 1.0

    element1 = DielectricInterface(n1=n1, n2=n2, R=R, diameter=20, label="#int{0}".format(i))
    element2 = Space(n=n2, d=float(d), label="space-{0}".format(i))

    olympus20xPrescription.append(element1)
    olympus20xPrescription.append(element2)
    n1 = n2

print("--------------")
print("From Raytracing calculations")
print("f  = {0:0.3f} mm".format(olympus20xPrescription.effectiveFocalLengths().f1))
print("WD = {0:.3f} mm".format(olympus20xPrescription.frontFocalLength()))
print("--------------")
print("From Olympus patent, Table 3, at https://patents.google.com/patent/US6501603B2/en")
print("f = 9.006 mm")
print("WD = 2.04 mm")
