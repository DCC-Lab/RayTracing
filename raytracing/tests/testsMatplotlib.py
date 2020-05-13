import unittest
import envtest # modifies path
from raytracing import *
import signal
import time 
import os

inf = float("+inf")

_flag = False

def testHandler(signum, frame):
    TestSignalsAndAsynchronousTesting.flag = True

def sendCtrlCHandler(signum, frame):
    signal.signal(signal.SIGALRM, killEverything)
    signal.alarm(2)

    pid = os.getpid()
    os.kill(pid, signal.SIGINT)


def raiseKeyboardInterrupt(signum, frame):
    raise KeyboardInterrupt

def alarmAndCancelHandler(signum, frame):
    signal.signal(signal.SIGALRM, testHandler)

def killEverything(signum, frame):
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)

class TestSignalsAndAsynchronousTesting(unittest.TestCase):
    @property
    def flag(self):
        return _flag

    def testSignalAsync(self):
        TestSignalsAndAsynchronousTesting.flag = False
        signal.signal(signal.SIGALRM, testHandler)

        signal.alarm(1)

        time.sleep(1.1)
        self.assertTrue(TestSignalsAndAsynchronousTesting.flag)

    def testNoSignalAsync(self):
        TestSignalsAndAsynchronousTesting.flag = False
        signal.signal(signal.SIGALRM, testHandler)

        # do nothing

        time.sleep(0.1)
        self.assertFalse(TestSignalsAndAsynchronousTesting.flag)

    def testSendCtrlC(self):
        TestSignalsAndAsynchronousTesting.flag = False
        signal.signal(signal.SIGINT, testHandler)

        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        self.assertTrue(TestSignalsAndAsynchronousTesting.flag)

    def testMatrixDisplayCanQuit(self):
        signal.signal(signal.SIGALRM, sendCtrlCHandler)

        signal.alarm(1) # send ctrl-c in 1 second
        m = Matrix()
        m.display()

        self.assertTrue(True) # if we make it here, we succeeded



if __name__ == '__main__':
    unittest.main()