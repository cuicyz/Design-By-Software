#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#U32336445 
#HWK1
#!/usr/bin/python
#Define the earth mass and proton mass found online
earth_mass = 5.972e24;
proton_mass = 1.6726e-27;
#Find the ration in earth
i = earth_mass/proton_mass;
#Find the number of electrons
e1 = i/2;
#Convert to TB
e2 = e1/(8e12);
#Find the lower and upper bound by using +/-10%
e3 = e2*0.1;
lower = e2-e3;
upper = e2+e3;
#Print the results
print(e2)
print(lower)
print(upper)