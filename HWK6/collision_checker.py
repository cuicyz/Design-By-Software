#!/usr/bin/env python
# Copyright 2017 J Carruthers jbc@bu.edu

# Tester for collision program. 
# also, solution to collision_tester assignment

import unittest
import subprocess
import random
import math
import numpy


refcode_cpp={'lines':151, 'words':608}
refcode_py={'lines':117, 'words':439}

PROGRAM_TO_TEST = "collision.py" # or "collision"

TIMEOUT = 3.2

BAD_ARGS_RC = 2
BAD_INPUT_RC = 1

runners = [("for",100, -100, 100,100), ('back',0,0,-100,100)]

random_twenty = [(1000, -1663, -1068, 4, 3), (1001, 1771, 1241, 4, -9), (1002, 531, -1842, 5, -7), (1003, -1999, 576, 9, 7), (1004, 282, -338, 0, -5), (1005, 1432, 1146, -3, -10), (1006, 1818, 1972, 9, 10), (1007, -1819, 365, -6, 6), (1008, 1896, 1553, 4, -8), (1009, 1561, 952, 5, 4), (1010, -1937, -1948, -2, -6), (1011, 110, 1424, 1, 7), (1012, 1754, 1794, -2, -7), (1013, 1042, -193, 5, -4), (1014, 563, 1074, 8, -9), (1015, 243, 62, 5, 10), (1016, 1749, 923, -10, -5), (1017, -1365, -346, -5, 7), (1018, 495, -769, -10, -1), (1019, -548, -841, 5, -2)]

bad_args=[('-4',"-5"),("one","two"),("one","4","5"),("4","5","alpha")]

bad_inputs =["""a
b 0 0 1 1
c 20 20 1 1
""",
"""a 0 0 0 0
b 10 10 10 10 10
""",
"""a b c 0 0 
d 10 10 10 10
e 30 30 30 30
""",
"""a 10 10 1 1


"""
]


in_out_tests=[
("random10",(20,60),
"""2MU133 -34.94 -69.13 0.468 -0.900
0WI913 -43.08 92.12 -0.811 -0.958
6UP738  2.97 -66.25 -0.077 0.074
1IA244 72.94 -86.02 -0.665 -0.283
8RT773 -32.25 -2.63 -0.797 0.628
0HV350 -73.97 24.21 0.960 -0.870
0DU118 -82.09 44.95 0.661 -0.343
4FA522 -18.20 72.32 0.734 -0.990
1WR684 31.71 68.89 -0.509 -0.706
7SW673 41.29 42.68 0.549 -0.012
""",
"""20.0
2MU133 -25.58 -87.13 0.468 -0.9
0WI913 -59.3 72.96 -0.811 -0.958
6UP738 1.43 -64.77 -0.077 0.074
1IA244 59.64 -91.68 -0.665 -0.283
8RT773 -44.8335733812 9.9991408741 0.928409713 0.6635426617
0HV350 -58.1264266188 6.7408591259 -0.765409713 -0.9055426617
0DU118 -68.87 38.09 0.661 -0.343
4FA522 -3.52 52.52 0.734 -0.99
1WR684 21.53 54.77 -0.509 -0.706
7SW673 52.27 42.44 0.549 -0.012
60.0
2MU133 -6.86 -123.13 0.468 -0.9
0WI913 -91.74 34.64 -0.811 -0.958
6UP738 -1.65 -61.81 -0.077 0.074
1IA244 33.04 -103.0 -0.665 -0.283
8RT773 -7.6971848605 36.5408473413 0.928409713 0.6635426617
0HV350 -88.7428151395 -29.4808473413 -0.765409713 -0.9055426617
0DU118 -42.43 24.37 0.661 -0.343
4FA522 9.3281000698 -0.0479229456 0.1031531012 -1.4854471629
1WR684 17.6818999302 39.4979229456 0.1218468988 -0.2105528371
7SW673 74.23 41.96 0.549 -0.012
"""),
('basic',(1,2,3),
"""a 10 20 -1.5 2
b 90 90 -3 -3
c 100 100 1 1
"""
,
"""1
a 8.5 22 -1.5 2
b 87 87 -3 -3
c 101 101 1 1
2
a 7 24 -1.5 2
b 84 84 -3 -3
c 102 102 1 1
3
a 5.5 26 -1.5 2
b 81 81 -3 -3
c 103 103 1 1
"""),
('one',(12,),
"""one -10 -10 2 2
two 10 10 -1 -1
"""
,
"""12
one -9.0710678 -9.0710678 -1 -1
two 21.071068 21.071068 2 2
"""),
('large time',(1000,100000),"a 0 0 0 0\n",
    """1000
a 0 0 0 0
100000
a 0 0 0 0
"""),
('big locations',(9999,),
"""one 1000000 1000000 -100 -100
two -1000000 1000000 100 -100
three 1000000 -1000000 -100 100
four -1000000 -1000000 100 100
""",
"""9999
one 100 100 -100 -100
two -100 100 100 -100
three 100 -100 -100 100
four -100 -100 100 100
"""),
('dup names',(1,2),
"""one 0 0 1 1
one 10 10 10 10
two 20 20 20 20
""",
"""1
one 1 1 1 1
one 20 20 10 10
two 40 40 20 20
2
one 2 2 1 1
one 30 30 10 10
two 60 60 20 20
"""),
('many colliders',(2450,),
'mover 0 0 0 1\nmover0 0 20 0 0\nmover1 0 60 0 0\nmover2 0 100 0 0\nmover3 0 140 0 0\nmover4 0 180 0 0\nmover5 0 220 0 0\nmover6 0 260 0 0\nmover7 0 300 0 0\nmover8 0 340 0 0\nmover9 0 380 0 0\nmover10 0 420 0 0\nmover11 0 460 0 0\nmover12 0 500 0 0\nmover13 0 540 0 0\nmover14 0 580 0 0\nmover15 0 620 0 0\nmover16 0 660 0 0\nmover17 0 700 0 0\nmover18 0 740 0 0\nmover19 0 780 0 0\nmover20 0 820 0 0\nmover21 0 860 0 0\nmover22 0 900 0 0\nmover23 0 940 0 0\nmover24 0 980 0 0\nmover25 0 1020 0 0\nmover26 0 1060 0 0\nmover27 0 1100 0 0\nmover28 0 1140 0 0\nmover29 0 1180 0 0\nmover30 0 1220 0 0\nmover31 0 1260 0 0\nmover32 0 1300 0 0\nmover33 0 1340 0 0\nmover34 0 1380 0 0\nmover35 0 1420 0 0\nmover36 0 1460 0 0\nmover37 0 1500 0 0\nmover38 0 1540 0 0\nmover39 0 1580 0 0\nmover40 0 1620 0 0\nmover41 0 1660 0 0\nmover42 0 1700 0 0\nmover43 0 1740 0 0\nmover44 0 1780 0 0\nmover45 0 1820 0 0\nmover46 0 1860 0 0\nmover47 0 1900 0 0\nmover48 0 1940 0 0\nmover49 0 1980 0 0\nmover50 0 2020 0 0\nmover51 0 2060 0 0\nmover52 0 2100 0 0\nmover53 0 2140 0 0\nmover54 0 2180 0 0\nmover55 0 2220 0 0\nmover56 0 2260 0 0\nmover57 0 2300 0 0\nmover58 0 2340 0 0\nmover59 0 2380 0 0\nmover60 0 2420 0 0\nmover61 0 2460 0 0\nmover62 0 2500 0 0\nmover63 0 2540 0 0\nmover64 0 2580 0 0\nmover65 0 2620 0 0\nmover66 0 2660 0 0\nmover67 0 2700 0 0\nmover68 0 2740 0 0\nmover69 0 2780 0 0\nmover70 0 2820 0 0\nmover71 0 2860 0 0\nmover72 0 2900 0 0\nmover73 0 2940 0 0\nmover74 0 2980 0 0\n',
'2450\nmover 0 10 0 0\nmover0 0 50 0 0\nmover1 0 90 0 0\nmover2 0 130 0 0\nmover3 0 170 0 0\nmover4 0 210 0 0\nmover5 0 250 0 0\nmover6 0 290 0 0\nmover7 0 330 0 0\nmover8 0 370 0 0\nmover9 0 410 0 0\nmover10 0 450 0 0\nmover11 0 490 0 0\nmover12 0 530 0 0\nmover13 0 570 0 0\nmover14 0 610 0 0\nmover15 0 650 0 0\nmover16 0 690 0 0\nmover17 0 730 0 0\nmover18 0 770 0 0\nmover19 0 810 0 0\nmover20 0 850 0 0\nmover21 0 890 0 0\nmover22 0 930 0 0\nmover23 0 970 0 0\nmover24 0 1010 0 0\nmover25 0 1050 0 0\nmover26 0 1090 0 0\nmover27 0 1130 0 0\nmover28 0 1170 0 0\nmover29 0 1210 0 0\nmover30 0 1250 0 0\nmover31 0 1290 0 0\nmover32 0 1330 0 0\nmover33 0 1370 0 0\nmover34 0 1410 0 0\nmover35 0 1450 0 0\nmover36 0 1490 0 0\nmover37 0 1530 0 0\nmover38 0 1570 0 0\nmover39 0 1610 0 0\nmover40 0 1650 0 0\nmover41 0 1690 0 0\nmover42 0 1730 0 0\nmover43 0 1770 0 0\nmover44 0 1810 0 0\nmover45 0 1850 0 0\nmover46 0 1890 0 0\nmover47 0 1930 0 0\nmover48 0 1970 0 0\nmover49 0 2010 0 0\nmover50 0 2050 0 0\nmover51 0 2090 0 0\nmover52 0 2130 0 0\nmover53 0 2170 0 0\nmover54 0 2210 0 0\nmover55 0 2250 0 0\nmover56 0 2290 0 0\nmover57 0 2330 0 0\nmover58 0 2370 0 0\nmover59 0 2410 0 0\nmover60 0 2450 0 0\nmover61 0 2490 0 0\nmover62 0 2530 0 0\nmover63 0 2570 0 0\nmover64 0 2610 0 0\nmover65 0 2650 0 0\nmover66 0 2690 0 0\nmover67 0 2730 0 0\nmover68 0 2770 0 0\nmover69 0 2810 0 0\nmover70 0 2850 0 0\nmover71 0 2890 0 0\nmover72 0 2930 0 0\nmover73 0 2970 0 0\nmover74 0 3200.0 0 1\n'),

('three way',(5,9,11,15),
"""down    0  20  0 -1
right -20   0  1  0
left   10   0 -1  0
""",
"""5.0
down 0.0 15.0 0.0 -1.0
right -15.0 0.0 1.0 0.0
left 5.0 0.0 -1.0 0.0
9.0
down 0.0 11.0 0.0 -1.0
right -11.0 0.0 1.0 0.0
left 1.0 0.0 -1.0 0.0
11.0
down 0.0 10.0 0.0 0.0
right -11.0 0.0 -1.0 0.0
left 1.0 -1.0 1.0 -1.0
15.0
down 0.0 10.0 0.0 0.0
right -15.0 0.0 -1.0 0.0
left 5.0 -5.0 1.0 -1.0"""),
('twelve all at once',(5,9.9,10.1,15),
"""pone -15 0 1 0
pfive -65 0 5 0
pten -125 0 10 0
none 15 0 -1 0
nfive 65 0 -5 0
nten 125 0 -10 0
dpone -15 50 1 -4
dpfive -65 50 5 -4
dpten -125 50 10 -4
dnone 15 50 -1 -4
dnfive 65 50 -5 -4
dnten 125 50 -10 -4
""",
"""5.0
pone -10.0 0.0 1.0 0.0
pfive -40.0 0.0 5.0 0.0
pten -75.0 0.0 10.0 0.0
none 10.0 0.0 -1.0 0.0
nfive 40.0 0.0 -5.0 0.0
nten 75.0 0.0 -10.0 0.0
dpone -10.0 30.0 1.0 -4.0
dpfive -40.0 30.0 5.0 -4.0
dpten -75.0 30.0 10.0 -4.0
dnone 10.0 30.0 -1.0 -4.0
dnfive 40.0 30.0 -5.0 -4.0
dnten 75.0 30.0 -10.0 -4.0
9.9
pone -5.1 0.0 1.0 0.0
pfive -15.5 0.0 5.0 0.0
pten -26.0 0.0 10.0 0.0
none 5.1 0.0 -1.0 0.0
nfive 15.5 0.0 -5.0 0.0
nten 26.0 0.0 -10.0 0.0
dpone -5.1 10.4 1.0 -4.0
dpfive -15.5 10.4 5.0 -4.0
dpten -26.0 10.4 10.0 -4.0
dnone 5.1 10.4 -1.0 -4.0
dnfive 15.5 10.4 -5.0 -4.0
dnten 26.0 10.4 -10.0 -4.0
10.1
pone -5.1 -0.4 -1.0 -4.0
pfive -15.5 -0.4 -5.0 -4.0
pten -26.0 -0.4 -10.0 -4.0
none 5.1 -0.4 1.0 -4.0
nfive 15.5 -0.4 5.0 -4.0
nten 26.0 -0.4 10.0 -4.0
dpone -5.1 10.0 -1.0 0.0
dpfive -15.5 10.0 -5.0 0.0
dpten -26.0 10.0 -10.0 0.0
dnone 5.1 10.0 1.0 0.0
dnfive 15.5 10.0 5.0 0.0
dnten 26.0 10.0 10.0 0.0
15.0
pone -10.0 -20.0 -1.0 -4.0
pfive -40.0 -20.0 -5.0 -4.0
pten -75.0 -20.0 -10.0 -4.0
none 10.0 -20.0 1.0 -4.0
nfive 40.0 -20.0 5.0 -4.0
nten 75.0 -20.0 10.0 -4.0
dpone -10.0 10.0 -1.0 0.0
dpfive -40.0 10.0 -5.0 0.0
dpten -75.0 10.0 -10.0 0.0
dnone 10.0 10.0 1.0 0.0
dnfive 40.0 10.0 5.0 0.0
dnten 75.0 10.0 10.0 0.0"""),
('three vertical',(1,3.9,3.99,4.01,4.1,9),
"""one 0 50 0 -10
two 0 10  0 -2.5
thr 0 -20 0 2.5
""",
"""1.0
one 0.0 40.0 0.0 -10.0
two 0.0 7.5 0.0 -2.5
thr 0.0 -17.5 0.0 2.5
3.9
one 0.0 11.0 0.0 -10.0
two 0.0 0.25 0.0 -2.5
thr 0.0 -10.25 0.0 2.5
3.99
one 0.0 10.1 0.0 -10.0
two 0.0 0.025 0.0 -2.5
thr 0.0 -10.025 0.0 2.5
4.01
one 0.0 10.025 0.0 2.5
two 0.0 -0.025 0.0 -2.5
thr 0.0 -10.1 0.0 -10.0
4.1
one 0.0 10.25 0.0 2.5
two 0.0 -0.25 0.0 -2.5
thr 0.0 -11.0 0.0 -10.0
9.0
one 0.0 22.5 0.0 2.5
two 0.0 -12.5 0.0 -2.5
thr 0.0 -60.0 0.0 -10.0
""")
]

basic_input = in_out_tests[0][2]

def runprogram(program, args, inputstr):
    coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout = TIMEOUT)
    "run a program and get result: wrapper for subprocess.run"

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)


class CollisionTestCase(unittest.TestCase):
    def rc_check(self,rc_actual,rc_target):
        if rc_target == 0:
            if rc_actual !=  0:
                self.fail('bad return code of {} for valid args and inputs'.format(rc_actual))
        else:
            if rc_target != rc_actual:
                self.fail('bad return code of {}, expecting {}'.format(rc_actual,rc_target))
    
    def stderr_check(self,error_output):
        if error_output != "":
            self.fail('no output should go to stderr. You output:\n'+error_output)

    def check_collision_output(self,bad,good):
        "process and numerically compare two outputs"
        badlines = bad.splitlines()
        goodlines = good.splitlines()
        if len(badlines) != len(goodlines):

            self.fail('number of lines do not match: {} vs {}.\nGood:\n{}Bad:{}\n'.format(len(badlines),len(goodlines),
                 good,bad))
        for badline,goodline in zip(badlines,goodlines):
            goodvals = goodline.split()
            badvals = badline.split()
            if len(goodvals) != len(badvals):
                self.fail('improper line format: {}',badline)
            elif len(goodvals)==1: # time line
                if not math.isclose(float(goodvals[0]),float(badvals[0])):
                    self.fail('improper time: {} vs {}'.format(badvals[0],goodvals[0]))
            else:
                if goodvals[0] != badvals[0]:
                    self.fail('improper id: {} vs {}'.format(badvals[0],goodvals[0]))
                gv = [float(x) for x in goodvals[1:]]
                bv = [float(x) for x in badvals[1:]]
                if not numpy.allclose(gv,bv):
                    for x,y in zip(bv,gv):
                        if not math.isclose(x,y):
                            self.fail('values not close: {} vs {} on line: {}'.format(x,y,badline))
                    self.fail('values not close enough')


    def test_in_out(self):
        "a. collision events"
        for test_name,times,input_string,correct_output in in_out_tests:
            with self.subTest(CASE=test_name):
                (rc,out,errs) = runprogram(PROGRAM_TO_TEST,[str(x) for x in times], input_string)
                self.rc_check(rc,0)
                self.check_collision_output(out,correct_output)
                self.stderr_check(errs)


    def test_twenty(self):
        "b. twenty objects with random motion, no collisions"
        strin = "\n".join(" ".join(str(n) for n in x) for x in random_twenty)
        correct_out = "12\n"+"\n".join("{} {} {} {} {}".format(x[0],x[1]+12*x[3],x[2]+12*x[4],x[3],x[4]) for x in random_twenty)+"\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["12"],strin)
        self.rc_check(rc,0)

        self.check_collision_output(out,correct_out)
        self.stderr_check(errs)


    def test_bad_args(self):
        "c. bad argument examples: negative or alpha"
        for bad_arg in bad_args:
            with self.subTest(CASE=repr(bad_arg)):
                (rc,_,_) = runprogram(PROGRAM_TO_TEST,bad_arg,basic_input)
                self.rc_check(rc,BAD_ARGS_RC)


    def test_bad_inputs(self):
        "d. bad input formatting"
        for bad_in in bad_inputs:
            with self.subTest(CASE=repr(bad_in)):
                (rc,_,_) = runprogram(PROGRAM_TO_TEST,["1","2"],bad_in)
                self.rc_check(rc,BAD_INPUT_RC)


    def test_many_args(self):
        "e. handle 100+ arguments and large distances"
        many_args=list(range(1,110))
        strin = "\n".join(" ".join(str(n) for n in x) for x in runners)
        outlines=[]
        for time in many_args:
            outlines.append("{}\n".format(time))
            for name,x,y,vx,vy in runners:
                outlines.append("{} {} {} {} {}\n".format(name,x+vx*time,y+vy*time,vx,vy))
        correct_out = "".join(outlines)

        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,[str(x) for x in many_args],strin)
        self.rc_check(rc,0)
        self.check_collision_output(out,correct_out)
        self.stderr_check(errs)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

