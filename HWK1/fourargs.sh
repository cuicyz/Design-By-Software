#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#U32336445 
#HWK1
#!/bin/bash
#compiles the C++ program to an executable called "fourargs"
g++ fourargs.cpp -o fourargs
#runs the python program with 6 args
python fourargs.py one two 3 four five six 
#runs the python program with 3 args
python fourargs.py one two 3
#runs the C++ program with 6 args
fourargs one two 3 four five six 
#runs the C++ program with 3 args
fourargs one two 3