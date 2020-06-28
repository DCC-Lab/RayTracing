import envtest
import sys
import subprocess


class TestCallScript(envtest.RaytracingTestCase):
    def setUp(self):
        self.exec = sys.executable
        self.encoding = sys.stdout.encoding
        self.emptyFile = self.tempFilePath('script.py')
        open(self.emptyFile, "w").close()
        self.printHelloWorld = self.tempFilePath('helloWorld.py')
        with open(self.printHelloWorld, "w") as helloWorld:
            helloWorld.write('''print("hello world")''')

    def testCallFileNotFound(self):
        file = " fileDoesNotExist.py"  # Leading space important
        sts = subprocess.call(self.exec + file)
        self.assertEqual(sts, 2)

    def testCallScript(self):
        sts = subprocess.call(self.exec + " " + self.emptyFile)
        self.assertEqual(sts, 0)

    def testGetWhatIsPrinted(self):
        printed = subprocess.check_output(self.exec + " " + self.printHelloWorld)
        printed = printed.decode(self.encoding)
        self.assertEqual(printed.strip(), "hello world")

    def testGetWhatIsPrintedWithChildProcesses(self):
        code = """
import multiprocessing

def printHelloName(name):
    print(f"Hello {name}")

if __name__ == "__main__":
    inputNames = ["Toto", "Toto Jr."]
    processes = 4
    with multiprocessing.Pool(processes=processes) as pool:
        outputValues = pool.map(printHelloName, inputNames)
""".strip()
        with open(self.printHelloWorld, "w") as f:
            f.write(code)
        printed = subprocess.check_output(self.exec + " " + self.printHelloWorld, universal_newlines=True)
        self.assertEqual(printed.strip(), "Hello Toto\nHello Toto Jr.")


if __name__ == '__main__':
    envtest.main()
