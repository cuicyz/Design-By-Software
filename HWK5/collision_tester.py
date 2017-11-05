"""this is the main part of the assignment"""

# Copyright 2017 Chuan Xing Zheng(Tommy) czheng78@bu.edu
# Copyright 2017 ZhiyuWang wangzy95@bu.edu
# Copyright 2017 YuxiJiang jiangyx@bu.edu

import unittest
import subprocess

#please change this to valid author emails
AUTHORS = ['czheng78@bu.edu','wangzy95@bu.edu','jiangyx@bu.edu']

PROGRAM_TO_TEST = "collision"

def runprogram(program, args, inputstr):
    coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout = 0.2)

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)

def to_int(out):
    out = out.replace(".0000","")
    return(out)

class CollisionTestCase(unittest.TestCase):  
    
    "test given"
    def test_one(self):
        strin = "one 20 10 -2 1"
        correct_out = "3\none 14 13 -2 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test one particle if not moving"
    def test_one_not_moving(self):
        strin = "one 20 10 -2 1"
        correct_out = "0\none 20 10 -2 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test the order of the output is in increasing time"
    def test_one_inc_time(self):
        strin = "one 20 10 -2 1"
        correct_out = "2\none 16 12 -2 1\n3\none 14 13 -2 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3", "2"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test the inputs (with non valid numbers) in the file and return 1"
    def test_badinput1(self):
        strin = "wo ba shi li gang"
        correct_out = "1"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1"],strin)
        out = to_int(out)
        self.assertEqual(rc,1)

    "test the inputs with too many in the file and return 1"
    def test_badinput2(self):
        strin = "three 2.97 -66.25 -0.07 0.07 8"
        correct_out = "1"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1"],strin)
        out = to_int(out)
        self.assertEqual(rc,1)

    "test the command line that consist string that's not a number and return 2"
    def test_commendlinewrong(self):
        strin = "three 2.97 -66.25 -0.07 0.07"
        correct_out = "1"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["m"],strin)
        out = to_int(out)
        self.assertEqual(rc,2)

    "test no valid values on the command line"
    def test_commendline_wrong2(self):
        strin = "three 2.97 -66.25 -0.07 0.07"
        correct_out = "2"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,[""],strin)
        out = to_int(out)
        self.assertEqual(rc,2)

    "test negative time in command line and ignore it"
    def test_negativetime(self):
        strin = "three 2.97 -66.25 -0.07 0.07"
        correct_out = "1\nthree 2.9 -66.18 -0.07 0.07\n2\nthree 2.83 -66.11 -0.07 0.07\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2","1"],strin)
        out = to_int(out)        
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"") 

    "test two particles with no collisions"
    def test_two_collide(self):
        strin = "one 20 10 5 0\ntwo 40 10 -5 0"
        correct_out = "2\none 20 10 -5 0\ntwo 40 10 5 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test two particles collision with same velocities"
    def test_two_collide2(self):
        strin = "one 0 0 5 0\ntwo 15 0 -5 0"
        correct_out = "2\none -5 0 -5 0\ntwo 20 0 5 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["2"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")       

    "test two particles collision with vary velocities"
    def test_two_differv(self):
        strin = "one -10 5 1 0\ntwo 60 5 -5 0"
        correct_out = "12\none -10 5 -5 0\ntwo 12 5 1 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["12"],strin)
        out = to_int(out)
        self.assertEqual(rc,0) 
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"") 

    "test case with more than 10 balls"
    def test_manyballs(self):
        strin = "one 0 0 5 0\ntwo 15 0 -5 0\nthree 15 0 -5 0\nfour 15 0 -5 0\nfive 15 0 -5 0\nsix 15 0 -5 0\nseven 15 0 -5 0\neight 15 0 -5 0\nnine 15 0 -5 0\nten 15 0 -5 0\nelevn 15 0 -5 0\n"
        correct_out = "0\none 0 0 5 0\ntwo 15 0 -5 0\nthree 15 0 -5 0\nfour 15 0 -5 0\nfive 15 0 -5 0\nsix 15 0 -5 0\nseven 15 0 -5 0\neight 15 0 -5 0\nnine 15 0 -5 0\nten 15 0 -5 0\nelevn 15 0 -5 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test when name same and not moving"
    def test_two_samename(self):
        strin = "one 20 10 -2 1\none 10 0 -2 1"
        correct_out = "0\none 20 10 -2 1\none 10 0 -2 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test when name same and they are moving"
    def test_two_samename1(self):
        strin = "one 0 0 1 0\none 2 2 1 0"
        correct_out = "1\none 1 0 1 0\none 3 2 1 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test when more than 2 balls collide"
    def test_manyballscollide(self):
        strin = "one -10 0 5 0\ntwo 0 0 0 0\nthree 10 0 -5 0"
        correct_out = "3\none -10 0 0 0\ntwo -5 0 -5 0\nthree 15 0 5 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test when they are not moving even when time is large"
    def test_negativespeed(self):
        strin = "one 0 0 1 0\ntwo 40 20 0 0\n"
        correct_out = "99999999\none 99999999 0 1 0\ntwo 40 20 0 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["99999999"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    "test when the velocities are floats"
    def test_four_float(self):
        strin = "BAL001 0 0 1 0\nBAL002 20 0 -1 0\nBAL003 30 15 0 -2.1111111\nBAL004 30 -15 0 3.1111111"
        correct_out = "0\nBAL001 0 0 1 0\nBAL002 20 0 -1 0\nBAL003 30 15 0 -2.1111111\nBAL004 30 -15 0 3.1111111\n2\nBAL001 2 0 1 0\nBAL002 18 0 -1 0\nBAL003 30 10.777778 0 -2.1111111\nBAL004 30 -8.7777778 0 3.1111111\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["0","2"],strin)
        out = to_int(out)
        self.assertEqual(rc,0)
        self.assertEqual(errs,"")

    def test_programname(self):
        self.assertTrue(PROGRAM_TO_TEST.startswith("cf/"),"wrong program name")

def main():
    "show how to use runprogram"

    print(runprogram('./test_program.py', ["4", "56", "test"], "my input"))
    unittest.main()

if __name__ == '__main__':
    main()

