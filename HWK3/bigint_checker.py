import ec602lib
import unittest
import random
import subprocess
import os
import numpy as np

progname = "bigint.cpp"

valid_includes = set(['vector','string'])

TIMEALLOWED = 1
COMPILEALLOWED = 3

P={"stdout":subprocess.PIPE,"timeout":TIMEALLOWED,"stderr":subprocess.PIPE}

CP={"stdout":subprocess.PIPE,"timeout":COMPILEALLOWED,"stderr":subprocess.PIPE}

refcode={'lines':36,'words':165}

cppmain="""
#include <iostream>
#include <vector>

using namespace std;

#include "PROGNAME"

int main()
{ 

  BigInt A,B;

  cin >> A >> B;

  cout << multiply_int(A,B) << endl;

}"""

SmallIntTests=[(8,9),(4,5),(999,1001)]

BigIntTests=[(123456,123456),(10000100060043,34444234234),(10**19-1,10**19-1),
(100000001,9900000099)]

ZeroTests=[(12340,0),(0,23342342)]

def compile(cpp,executable):
  return ['g++','-std=c++14',cpp, '-o', executable]
          
        
def check_mult(self,a,b,atimesb):
    with self.subTest(CASE=" {} * {} = {}".format(a,b,atimesb)):
      intext="{} {}".format(a,b).encode()
      T = subprocess.run([self.executable],input=intext,**P)
      res = T.stdout.decode().strip()
      if res != str(atimesb):
        self.fail("your multiply: {}\ncorrect answer: {}\n".format(res,atimesb))


class bigintTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseprogname = 'bigmain'+str(random.randint(1000,100000))
        mainprogname = baseprogname+'.cpp'
        with open(mainprogname,'w') as f:
            f.write(cppmain.replace('PROGNAME',progname))

        try:
          C = subprocess.run(compile(mainprogname,baseprogname),**CP)
        except Exception as e:
          raise unittest.SkipTest("Compile failed.\n"+str(e))
        finally:
          os.remove(mainprogname)

        if C.returncode:
            raise unittest.SkipTest("Compile failed.\n"+str(C.stderr.decode()))

        cls.executable = baseprogname

    @classmethod
    def tearDownClass(cls):
       os.remove(cls.executable)


    def test_includes(self):
        "a. check the included libraries are allowed"
        f=open(progname)
        file_contents=f.read()
        f.close() 
        includes = ec602lib.get_includes(file_contents)
        invalid_includes = includes - valid_includes
        if invalid_includes:
          self.fail('Invalid includes: {}'.format(" ".join(x for x in invalid_includes)))

    def test_mult(self):
       "b. test small numbers"
       for (a,b) in SmallIntTests:
           check_mult(self,a,b,a*b)

    def test_big_mult(self):
       "c. test big numbers"
       for (a,b) in BigIntTests:
           check_mult(self,a,b,a*b)

    def test_zero_mult(self):
       "d. test mult by zero"
       for (a,b) in ZeroTests:
           check_mult(self,a,b,a*b)

if __name__=="__main__":
    _, results, _ = ec602lib.overallcpp(progname,bigintTestCase,refcode,compile=False)
    #unittest.main()
    print(results)