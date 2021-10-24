import pyopencl as pycl
import pyopencl as cl
import numpy as np
import unittest
import time
import pyopencl.cltypes
from pyopencl.array import Array as clArray
import pyopencl.clmath
import matplotlib.pyplot as plt

class TestOpenCL(unittest.TestCase):
    context = None

    def test01Import(self):
        """
        Is it installed?
        """
        self.assertIsNotNone(pycl)

    def test02AtLeast1(self):
        """
        Let's get the platform so we can get the devices.
        There should be at least one.
        """
        self.assertTrue(len(pycl.get_platforms()) > 0)

    def test03AtLeast1Device(self):
        """
        Let's get the devices (graphics card?).  There could be a few.
        """
        platform = pycl.get_platforms()[0]
        devices = platform.get_devices()
        self.assertTrue(len(devices) > 0)

    def test031AtLeastGPUorCPU(self):
        devices = pycl.get_platforms()[0].get_devices()
        for device in devices:
            self.assertTrue(device.type == pycl.device_type.GPU or device.type == pycl.device_type.CPU)

    def test04Context(self):
        """ Finally, we need the context for computation context.
        """
        devices = pycl.get_platforms()[0].get_devices(pycl.device_type.GPU)
        context = pycl.Context(devices=devices)
        self.assertIsNotNone(context)

    def test05GPUDevice(self):
        gpuDevices = pycl.get_platforms()[0].get_devices(pycl.device_type.GPU)
        self.assertTrue(len(gpuDevices) >= 1)
        gpuDevice = [ device for device in gpuDevices if device.vendor == 'AMD']
        if gpuDevice is None:
            gpuDevice = [ device for device in gpuDevices if device.vendor == 'Intel']
        self.assertIsNotNone(gpuDevice)

    def test06ProgramSource(self):
        gpuDevices = pycl.get_platforms()[0].get_devices(pycl.device_type.GPU)
        context = pycl.Context(devices=gpuDevices)
        queue = pycl.CommandQueue(context)

        program_source = """
        kernel void sum(global float *a, 
                      global float *b,
                      global float *c)
                      {
                      int gid = get_global_id(0);
                      c[gid] = a[gid] + b[gid];
                      }

        kernel void multiply(global float *a, 
                      global float *b,
                      global float *c)
                      {
                      int gid = get_global_id(0);
                      c[gid] = a[gid] * b[gid];
                      }
        """
        program = pycl.Program(context, program_source).build()

    def test07CopyingBuffersFromHostToGPU(self):
        """
        If I run this several times, I sometimes get 1 ms or 1000 ms.
        I suspect there is some stsartup time for PyOpenCL.
        I will write a setup function for the test

        I did, it is now much more stable at 1-2 ms.
        """

        # gpuDevices = pycl.get_platforms()[0].get_devices(pycl.device_type.GPU)
        context = TestOpenCL.context

        N = 10000000
        a_np = np.random.rand(N).astype(np.float32)
        b_np = np.random.rand(N).astype(np.float32)
        self.assertIsNotNone(a_np)
        self.assertIsNotNone(b_np)
        mf = pycl.mem_flags
        a_g = pycl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
        b_g = pycl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)
        self.assertIsNotNone(a_g)
        self.assertIsNotNone(b_g)
        res_g = pycl.Buffer(context, mf.WRITE_ONLY, a_np.nbytes)


        queue = pycl.CommandQueue(context)

        program_source = """
        kernel void sum(global float *a, 
                      global float *b,
                      global float *c)
                      {
                      int gid = get_global_id(0);
                      c[gid] = a[gid] + b[gid];
                      }

        kernel void multiply(global float *a, 
                      global float *b,
                      global float *c)
                      {
                      int gid = get_global_id(0);
                      c[gid] = a[gid] * b[gid];
                      }
        """
        program = pycl.Program(context, program_source).build()


        knlSum = program.sum  # Use this Kernel object for repeated calls
        knlProd = program.multiply  # Use this Kernel object for repeated calls

        for i in range(10):
            startTime = time.time()
            knlSum(queue, a_np.shape, None, a_g, b_g, res_g)
            knlProd(queue, a_np.shape, None, res_g, b_g, res_g)
            calcTime = time.time()-startTime
            res_np = np.empty_like(a_np)
            pycl.enqueue_copy(queue, res_np, res_g)
            copyTime = time.time()-startTime
            #print("\nCalculation time {0:.1f} ms, with copy {1:.1f} ms".format( 1000*calcTime, 1000*copyTime))

        # Check on CPU with Numpy:
        startTime = time.time()
        answer = (a_np + b_np)*b_np
        npTime = time.time() - startTime
        # print("Numpy {0:0.1f} ms".format(1000*npTime))
        assert np.allclose(res_np, answer)
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        devices = pycl.get_platforms()[0].get_devices(device_type=pycl.device_type.GPU)
        TestOpenCL.context = pycl.Context(devices=devices)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def testNumpyVectorsWithOpenCLLayout(self):
        vectors = np.empty((128,), dtype=pycl.cltypes.float3) # array of float16
        self.assertIsNotNone(vectors)

    def testCreateOpenCLArray(self):
        queue = pycl.CommandQueue(TestOpenCL.context)

        a = clArray(cq=queue, shape=(1024,), dtype=pycl.cltypes.float)
        self.assertIsNotNone(a)
        self.assertIsNotNone(a.data)

    def testCreateOpenCLArray(self):
        queue = pycl.CommandQueue(TestOpenCL.context)

        a = clArray(cq=queue, shape=(1024,), dtype=pycl.cltypes.float)
        self.assertIsNotNone(a)
        self.assertIsNotNone(a.data)
        for i in range(a.size):
            a[i] = i

        for i, e in enumerate(a):
            self.assertEqual(e, i)

    def testScalarMultiplicationOfOpenCLArrays(self):
        queue = pycl.CommandQueue(TestOpenCL.context)

        a = clArray(cq=queue, shape=(1024,), dtype=pycl.cltypes.float)
        self.assertIsNotNone(a)
        self.assertIsNotNone(a.data)

        for i in range(a.size):
            a[i] = i

        b = 2*a
        for i, e in enumerate(b):
            self.assertEqual(e, 2*i)

    @unittest.skip("Skipping for now")
    def test001ScalarMultiplicationOfOpenCLArrays(self):
        queue = pycl.CommandQueue(TestOpenCL.context)
        a = clArray(cq=queue, shape=(2<<12,), dtype=pycl.cltypes.float)
        for i in range(a.size):
            a[i] = i

        startTime = time.time()        
        b = a+a
        calcTime = (time.time()-startTime)*1000
        print("\nOpenCL 1 scalar: {0:.1f} ms ".format(calcTime))

        a = np.array(object=[0]*(2<<14), dtype=pycl.cltypes.float)
        for i in range(a.size):
            a[i] = i

        startTime = time.time()        
        b = a+a
        calcTime = (time.time()-startTime)*1000
        print("\nnumpy: {0:.1f} ms ".format(calcTime))

        a = clArray(cq=queue, shape=(2<<14,), dtype=pycl.cltypes.float)
        for i in range(a.size):
            a[i] = i

        startTime = time.time()        
        b = a+a
        calcTime = (time.time()-startTime)*1000
        print("\nOpenCL 2 scalar: {0:.1f} ms ".format(calcTime))

    @unittest.skip("Skipping for now")
    def test002ArraysWithAllocator(self):
        """
        I really expected this to work.  Performance is more complicate than I expected.
        The OpenCL calculation is much slower than the numpy version regardless of parameters 
        I used.

        The plan was simple: manipulate arrays in numpy and opencl, show it is much faster in Opencl.
        Well, it is not.

        UPDATE: yes it is, with VERY large arrays (2^18 or more). See next test.

        """

        # Set up basic OpenCl things
        queue = pycl.CommandQueue(TestOpenCL.context)
        allocator = pycl.tools.ImmediateAllocator(queue)
        mempool = pycl.tools.MemoryPool(allocator)

        N = 1<<10
        M = 1000

        # Pre-allocate all arrays
        a_n = np.random.rand(N).astype(np.float32)
        b_n = np.random.rand(N).astype(np.float32)

        # Pre-allocate opencl arrays with MemoryPool to reuse memory
        a = pycl.array.to_device(queue=queue, ary=a_n, allocator=mempool)
        b = pycl.array.to_device(queue=queue, ary=b_n, allocator=mempool)

        startTime = time.time()        
        for i in range(M):
            c = i*a + b + a + b + a + a + a
        calcTimeOpenCL1 = (time.time()-startTime)*1000

        startTime = time.time()        
        for i in range(M):
            c = i*a_n + b_n + a_n + b_n + a_n + a_n + a_n 
        calcTimeNumpy = (time.time()-startTime)*1000

        # Often, OpenCL is faster on the second attempt.
        startTime = time.time()        
        for i in range(M):
            c = i*a + b + a + b + a + a + a
        calcTimeOpenCL2 = (time.time()-startTime)*1000

        self.assertTrue(calcTimeOpenCL2 < calcTimeNumpy,msg="\nNumpy is faster than OpenCL: CL1 {0:.1f} ms NP {1:.1f} ms CL2 {2:.1f} ms".format(calcTimeOpenCL1, calcTimeNumpy, calcTimeOpenCL2))
        print("\nCL1 {0:.1f} ms NP {1:.1f} ms".format(calcTimeOpenCL2, calcTimeNumpy))

    @unittest.skip("Skipping for now")
    def test003PerformanceVsSize(self):
        """
        I really expected this to work.  Performance is more complicated than I expected.
        The OpenCL calculation is much slower than the numpy version regardless of parameters 
        I used.

        The plan was simple: manipulate arrays in numpy and opencl, show it is much faster in Opencl.
        Well, it is not.

        UPDATE: yes it is, with VERY large arrays (2^20 or more)
        """

        # Set up basic OpenCl things
        queue = pycl.CommandQueue(TestOpenCL.context)
        allocator = pycl.tools.ImmediateAllocator(queue)
        mempool = pycl.tools.MemoryPool(allocator)

        N = 1
        M = 10
        P = 27
        nptimes = []
        cltimes = []
        for j in range(P):
            # Pre-allocate all arrays
            N = 1 << j
            a_n = np.random.rand(N).astype(np.float32)
            b_n = np.random.rand(N).astype(np.float32)

            # Pre-allocate opencl arrays, with MemoryPool to reuse memory
            a = pycl.array.to_device(queue=queue, ary=a_n, allocator=mempool)
            b = pycl.array.to_device(queue=queue, ary=b_n, allocator=mempool)

            startTime = time.time()        
            calcTimeOpenCL1 = []
            for i in range(M):
                c = i*a + b + a + b + a + a * a
            calcTimeOpenCL1.append((time.time()-startTime)*1000)
            cltimes.append(np.mean(calcTimeOpenCL1))

            startTime = time.time()        
            calcTimeOpenNP = []
            for i in range(M):
                c = i*a_n + b_n + a_n + b_n + a_n + a_n * a_n
            calcTimeOpenNP.append((time.time()-startTime)*1000)
            nptimes.append(np.mean(calcTimeOpenNP))

        plt.plot(range(P), cltimes, label="OpenCL")
        plt.plot(range(P), nptimes, label="Numpy")
        plt.xlabel("Size of array 2^x")
        plt.ylabel("Computation time [ms]")
        plt.legend()
        plt.show()

    def test004_2x2Matrix_and_Vectors(self):
        """
        Here I am getting excited about the possiblities for RayTracing and I want to
        see it in action multiplying 2x2 matrices and vectors.

        """

        context = TestOpenCL.context
        queue = pycl.CommandQueue(context)

        program_source = """
        kernel void product(global const float *mat, int M, 
                            global float *vec,
                            global float *res)
                      {
                      int i    = get_global_id(0); // the vector index
                      int j;                       // the matrix index

                      for (j = 0; j < M; j++) {
                          res[i + 2*j]     = vec[i];
                          res[i + 2*j + 1] = vec[i+1];

                          vec[i]     = mat[i+4*j]   * vec[i] + mat[i+4*j+1] * vec[i+1];
                          vec[i + 1] = mat[i+4*j+2] * vec[i] + mat[i+4*j+3] * vec[i+1];
                          }
                      }

        """
        program_source_floats = """
        kernel void product(global const float4 *mat, int M, 
                            global float2 *vec,
                            global float2 *res)
                      {
                      int i    = get_global_id(0); // the vector index
                      int j;                       // the matrix index
                      int N    = get_global_size(0);
                      float2 v = vec[i];
                      res[i] = v;
                      for (j = 0; j < M; j++) {
                          float4 m = mat[j];

                          v.x = m.x * v.x + m.y * v.y;
                          v.y = m.z * v.x + m.w * v.y;
                          res[i+N*(j+1)] = v;
                          }
                      }

        """
        program = pycl.Program(context, program_source_floats).build()
        knl = program.product  # Use this Kernel object for repeated calls


        startTime = time.time()        
        M = np.int32(40)     # M 2x2 matrices in path
        N = np.int32(2^24)  # N 2x1 rays to propagate  
        # Pre-allocate opencl arrays, with MemoryPool to reuse memory
        matrix_n = np.random.rand(M,2,2).astype(np.float32)
        vector_n = np.random.rand(N,2).astype(np.float32)
        result_n = np.zeros((M+1,N,2)).astype(np.float32)

        matrix = pycl.array.to_device(queue=queue, ary=matrix_n)
        vector = pycl.array.to_device(queue=queue, ary=vector_n)
        result = pycl.array.to_device(queue=queue, ary=result_n)

        knl(queue, (N,), None, matrix.data, M, vector.data, result.data)


        print(result.shape)
        # print(vector.get())
        print(result.get())
        print("\n{0:0.1f} ms".format((time.time()-startTime)*1000))
        # print(result.shape)
        # print(vector.get())
        # print(result.get())
        # print(result.get().reshape(2*(M+1)*N,1,1))


if __name__ == "__main__":
    unittest.main()
