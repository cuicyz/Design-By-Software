#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#U32336445 
#HWK3
#!/usr/bin/python
import  numpy

#Ask user for inputs and get rid of the spaces
#Put the inputs into arrays
in1 = input().split(' ')
arr1 = [float(num1) for num1 in in1]
in2 = input().split(' ')
arr2 = [float(num2) for num2 in in2]

#Use numpy.convolve to do the polynomial multiplications
arr3 = numpy.convolve(arr1, arr2)

#Print out the array
print(*arr3)
