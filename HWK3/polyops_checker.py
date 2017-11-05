import ec602lib
import unittest
import random
import subprocess
import os
import numpy as np

progname = "polyops.cpp"

valid_includes = set(['vector'])

TIMEALLOWED = 1
COMPILEALLOWED = 2

P={"stdout":subprocess.PIPE,"timeout":TIMEALLOWED,"stderr":subprocess.PIPE}

CP={"stdout":subprocess.PIPE,"timeout":COMPILEALLOWED,"stderr":subprocess.PIPE}

refcode={'lines':29,'words':130}

cppmain="""
#include <iostream>
#include <vector>

using namespace std;

#include "PROGNAME"

int main()
{ 

  int Alen,Blen;

  cin >> Alen >> Blen;

  Poly A(Alen,0),B(Blen,0);

  for (auto& e : A)
     cin >> e;
  
  for (auto& e : B)
     cin >> e;

  for (auto e : add_poly(A,B))
     cout << e << " ";
  cout << endl;


  for (auto e : multiply_poly(A,B))
     cout << e << " ";
  cout << endl;  

}"""

Same_Add_Tests=[
[(1.2,0,5),(3,2,1),(4.2,2,6)],
[(1,2,3),(4,5,6),(5,7,9)],
[(0,0,4),(0,0,0.1),(0,0,4.1)],
]

Diff_Add_Tests=[
[(1.2,0,0, 5),(3,2,1),(4.2,2,1,5)],
[(1,6,3),(4,),(5,6,3)],
[(0,0,0,0,5),(0,0,1,4),(0,0,1,4,5)],
]

Same_Mul_Tests=[
[(1.2,0,5),(3,2,1),(3.6, 2.4, 16.2, 10, 5)],
[(1,2,3),(4,5,6),(4, 13, 28, 27, 18)],
[(0,0,4),(0,0,0.1),(0, 0, 0, 0, 0.4)],
]

Diff_Mul_Tests=[
[(1.2,0,0, 5),(3,2,1),(3.6, 2.4, 1.2, 15, 10, 5)],
[(1,6,3),(4,),(4, 24, 12)],
[(1,1,-1),(1,1,1),(1, 2, 1, 0.0, -1)],
[(0,0,0,0,5),(0,0,1,4),(0, 0, 0, 0, 0, 0, 5, 20)],
]

Tricky_Add_Tests=[
[(1,3,2),(1,6,-2),(2,9)],
[(1,1,1),(-1,-1,-1),(0,) ],
]


Tricky_Mul_Tests=[
[(1,2,1,1,1,6),(0,),(0,) ],
]

double_add_tests=[
[(1e-50,),(-0.99e-50,),(1e-52,)],
[(1e300,2e300),(0,0,3e300),(1e300,2e300,3e300)],
]

def fin(a,b):
  "format the input for polyops_example_main"
  astr = " ".join(str(x) for x in a)
  bstr = " ".join(str(x) for x in b)
  return "{} {} {} {}".format(len(a),len(b),astr,bstr).encode()

def fout(T):
  "extract the output for polyops_example_main"
  text = T.stdout.decode().splitlines()
  addition = tuple(float(x) for x in text[0].strip().split())
  multiply = tuple(float(x) for x in text[1].strip().split())
  return addition,multiply

def compile(cpp,executable):
  return ['g++','-std=c++14',cpp, '-o', executable]
          
def check_add(self,a,b,aplusb):
   with self.subTest(CASE=" {} + {} = {}".format(a,b,aplusb)):
      T = subprocess.run([self.executable],input=fin(a,b),**P)
      add_res,_ = fout(T)
      #self.assertEqual(len(add_res),len(aplusb),
      #     "your addition: {}\ncorrect answer: {}\n".format(add_res,aplusb))
      if len(add_res) != len(aplusb) or not np.allclose(add_res,aplusb,atol=0):
        self.fail("your addition: {}\ncorrect answer: {}\n".format(add_res,aplusb))


def check_mult(self,a,b,atimesb):
    with self.subTest(CASE=" {} * {} = {}".format(a,b,atimesb)):
      T = subprocess.run([self.executable],input=fin(a,b),**P)
      _,res = fout(T)
      if len(res) != len(atimesb) or not np.allclose(res,atimesb,atol=0):
        self.fail("your multiply: {}\ncorrect answer: {}\n".format(res,atimesb))


class polyopsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseprogname = 'polyopsmain'+str(random.randint(1000,100000))
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
       try:
        os.remove(cls.executable)
       except:
        pass


    def test_includes(self):
        "a. check the included libraries are allowed"
        f=open(progname)
        file_contents=f.read()
        f.close() 
        includes = ec602lib.get_includes(file_contents)
        invalid_includes = includes - valid_includes
        if invalid_includes:
          self.fail('Invalid includes: {}'.format(" ".join(x for x in invalid_includes)))


    def test_add_same_size(self):
       "b. add same size vectors"
       for (a,b,res) in Same_Add_Tests:
           check_add(self,a,b,res)


    def test_add_different_size(self):
       "c. add different size vectors"
       for (a,b,res) in Diff_Add_Tests:
           check_add(self,a,b,res)

    def test_mult_same_size(self):
       "d. multiply same size vectors"
       for (a,b,res) in Same_Mul_Tests:
           check_mult(self,a,b,res)

    def test_mult_different_size(self):
       "e. multiply different size vectors"
       for (a,b,res) in Diff_Mul_Tests:
           check_mult(self,a,b,res)

    def test_add_tricky(self):
       "f. add vectors with result smaller"
       for (a,b,res) in Tricky_Add_Tests:
           check_add(self,a,b,res)

    def test_mult_tricky(self):
       "g. multiply vectors with result smaller"
       for (a,b,res) in Tricky_Mul_Tests:
           check_mult(self,a,b,res)
    def test_double_add(self):
       "h. vector double"
       for (a,b,res) in double_add_tests:
             check_add(self,a,b,res)

if __name__=="__main__":
    _,results,_ = ec602lib.overallcpp(progname,polyopsTestCase,refcode,compile=False)
    #unittest.main()
    print(results)