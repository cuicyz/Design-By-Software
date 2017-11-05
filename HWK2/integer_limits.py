#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#U32336445 
#HWK1
#!/usr/bin/python

#Define the table
Table = "{:<6} {:<22} {:<22} {:<22}"
#Print the header of the table
print(Table.format('Bytes','Largest Unsigned Int','Minimum Signed Int',
                   'Maximum Signed Int'))
#Loop through byte 1 to 8
for x in range(1,9):
	#8 bits in 1 byte
    i = x*8
    #Find the largest unsigned int for the byte
    LUI = (2**i)-1
    #Find the minimum signed int for the byte
    MinSI = -(2**(i-1))
    #Find the maximum signed int for the byte
    MaxSI = (2**(i-1))-1
    #Print the values for byte 1 to 8
    print(Table.format(x,LUI,MinSI,MaxSI))