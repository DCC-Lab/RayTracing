import envtest
import sys
import subprocess
import os


class TestCallScript(envtest.RaytracingTestCase):
    def setUp(self):
        super().setUp()
        self.exec = sys.executable
        self.encoding = sys.stdout.encoding
        self.emptyFile = self.tempFilePath('script.py')
        open(self.emptyFile, "w").close()
        self.assertTrue(os.path.exists(self.emptyFile))

        self.printHelloWorld = self.tempFilePath('helloWorld.py')
        with open(self.printHelloWorld, "w") as helloWorld:
            helloWorld.write('''print("hello world")''')

    def testCallFileNotFound(self):
        file = " fileDoesNotExist.py"  # Leading space important

        processReturn = subprocess.run([self.exec, file], capture_output=True)
        self.assertEqual(processReturn.returncode, 2)

    def testCallScript(self):
        processReturn = subprocess.run([self.exec, self.emptyFile])
        self.assertEqual(processReturn.returncode, 0)

    def testGetWhatIsPrinted(self):
        processCompleted = subprocess.run([self.exec, self.printHelloWorld], capture_output=True)
        printed = processCompleted.stdout.decode(self.encoding)
        self.assertEqual(processCompleted.stdout.strip(), b"hello world")

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
        processCompleted = subprocess.run([self.exec, self.printHelloWorld], capture_output=True, universal_newlines=True)
        
        output = processCompleted.stdout
        possibility1 = "Hello Toto\nHello Toto Jr.\n"
        possibility2 = "Hello Toto Jr.\nHello Toto\n"
        self.assertTrue(output == possibility1 or output == possibility2)


if __name__ == '__main__':
    envtest.main()
