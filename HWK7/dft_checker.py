from numpy import zeros,exp,array,pi
import numpy
import unittest

from random import uniform

progname = "dft.py"

refcode={'lines':15,'words':60}

try:
    import ec602lib
    if ec602lib.VERSION < (1,0):
        print("Please update ec602lib.")
        quit()
except AttributeError:  
    print("Please update ec602lib.")
    quit()
except ImportError:
    print("Please install ec602lib in this directory or in your PYTHONPATH.")
    quit()


class MyList(list):
    pass

dft_notclose_msg="""
Your DFT did not match the results of fft.
For x = {}
DFT(x) returned {}
but
numpy.fft.fft(x) returned {}
"""

class DFTTestCase(unittest.TestCase):
    def test_import_valid(self):
        "e. test valid import statement"
        valid_import_str = "from numpy import zeros, exp, array, pi"
        file_contents=open(progname).read()
        imports = ec602lib.get_python_imports(file_contents)
        if imports != {'numpy'}:
            self.fail('Invalid imports detected.')
        if file_contents.count('import') > 1:
            self.fail('Too many import statements.')

        if  valid_import_str not in file_contents:
            self.fail('Invalid import statement.\n Please use:\n{}\n'.format(valid_import_str))

    def test_good_input_sequences(self):
        "a. test that DFT accepts sequences as input and returns ndarray"
        for tc in [ (4,5), [3,4],range(2),MyList([5,6])]:
            with self.subTest(input_val=tc):
                X = dft_under_test(tc)
                self.assertIsInstance(X,numpy.ndarray)

    def test_bad_inputs(self):
        "b. test invalid inputs"
        for tc in [8,"abc",dft_under_test,(4,5,"B"),{6:7,1:4}]:
            with self.subTest(input_val=tc):
                with self.assertRaises(ValueError,msg="DFT({}) did not raise exception".format(repr(tc))):
                    dft_under_test(tc)

    def test_shape(self):
        "c. test output of correct type"
        for N in [1,2,9,10,30]:
            X = dft_under_test(range(N))
            self.assertEqual(X.shape, (N,))
        
    def test_results(self):
        "d. check accuracy of calculation"
        for N in range(2,21):
            with self.subTest(N=N):
                for t in range(10):            
                    x =[uniform(-1,1)+uniform(-1,1)*1j for i in range(N)]
                    Xdft = dft_under_test(x)
                    Xfft = numpy.fft.fft(x)
                    self.assertEqual(Xdft.shape,Xfft.shape)

                    if not numpy.allclose(Xdft,Xfft):
                        self.fail(dft_notclose_msg.format(x,Xdft,Xfft))


if __name__=="__main__":
    from dft import DFT as dft_under_test
    _,results,_ = ec602lib.overallpy(progname,DFTTestCase,refcode)
    #unittest.main()
    print(results)
