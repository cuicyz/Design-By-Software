#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#U32336445 
#HWK1
#!/usr/bin/python
import sys
#Loop through the arguments
for index in range(1,len(sys.argv)):
	#Print the first 4 arguments to standard out
    if index < 5:
    	sys.stdout.write(sys.argv[index] + '\n')
    #Print the arguments after the 4th argument to standard error
    if index > 4:
        sys.stderr.write(sys.argv[index] + '\n') 