#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu

#!/usr/bin/python
from numpy import zeros, exp, array, pi

def DFT(x):

	try: 
		y = array(x, dtype=complex)
		N = y.size
		n = range(N)
		n = array(n)
		k = n.reshape((N, 1))
		E = exp(-2j * pi * n * k / N)
		FT = E@y
	except:
		raise ValueError
	return FT

# def main():
# 	# array x
# 	ar = array([1,2,3])
# 	# print(DFT(x))
# 	print(DFT(ar))

# if __name__ == '__main__':
# 	main()
