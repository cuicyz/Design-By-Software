import ec602lib
import unittest
import random
import subprocess
import os
import numpy as np

progname = "system.py"

valid_imports = set(['numpy'])

TIMEALLOWED = 2

P = {
    "stdout": subprocess.PIPE,
    "timeout": TIMEALLOWED,
    "stderr": subprocess.PIPE
}

refcode = {'lines': 3, 'words': 14}

Output_Same_Tests = [
    [(1.2, 0, 5), (3, 2, 1), (3.6, 2.4, 16.2, 10, 5)],
    [(1, 2, 3), (4, 5, 6), (4, 13, 28, 27, 18)],
    [(0, 0, 4), (0, 0, 0.1), (0, 0, 0, 0, 0.4)],
]

Output_Diff_Tests = [
    [(1.2, 0, 0, 5), (3, 2, 1), (3.6, 2.4, 1.2, 15, 10, 5)],
    [(1, 6, 3), (4, ), (4, 24, 12)],
    [(1, 1, -1), (1, 1, 1), (1, 2, 1, 0.0, -1)],
    [(0, 0, 0, 0, 5), (0, 0, 1, 4), (0, 0, 0, 0, 0, 0, 5, 20)],
]


def fin(x, h):
    "format the input for system"
    xstr = " ".join(str(f) for f in x)
    hstr = " ".join(str(f) for f in h)
    input_str = "{x}\n{h}\n".format(x=xstr, h=hstr)
    return input_str.encode()


def check_output(self, x, h, yans):
    with self.subTest(CASE=" x[n] = {}, h[n] = {} y[n] = {}".format(
            x, h, yans)):
        T = subprocess.run(['python', progname], input=fin(x, h), **P)
        if T.returncode:
           self.fail('program terminated with error:\n'+T.stderr.decode()+"\n")
        res = [float(x) for x in T.stdout.decode().strip().split()]
        if len(res) != len(yans) or not np.allclose(res, yans, atol=0):
            self.fail(
                "your output: {}\ncorrect answer: {}\n".format(res, yans))


class systemTestCase(unittest.TestCase):
    def test_includes(self):
        "d. check the included modules are allowed"
        f=open(progname)
        file_contents=f.read()
        f.close() 
        imports = ec602lib.get_python_imports(file_contents)
        invalid_imports = imports - valid_imports
        if invalid_imports:
          self.fail('Invalid imports: {}'.format(" ".join(x for x in invalid_imports)))

    def test_same_system(self):
        "a. h and x same size"
        for (x, h, y) in Output_Same_Tests:
            check_output(self, x, h, y)

    def test_diff_system(self):
        "b. h and x different size"
        for (x, h, y) in Output_Diff_Tests:
            check_output(self, x, h, y)



if __name__ == "__main__":
    _, results, _ = ec602lib.overallpy(progname, systemTestCase, refcode)
    # unittest.main()
    print(results)
