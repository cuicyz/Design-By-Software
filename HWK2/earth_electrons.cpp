//Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
//U32336445 
//HWK2
#include <iostream>
#include <cstdint>
#include <cfloat>
#include <cmath>
using namespace std;

int main(int argc, char const *argv[])
{
	//Define the earth mass and proton mass found online
	double earth_mass = 5.972e24;
	double proton_mass = 1.6726e-27;
	//Find the ration in earth
	double i = earth_mass/proton_mass;
	//Find the number of electrons
	double e1 = i/2;
	//Convert to TB
	double e2 = e1/(8e12);
	//Find the lower and upper bound by using +/-10%
	double e3 = e2*0.1;
	double lower = e2-e3;
	double upper = e2+e3;
	//Print the results
	cout << e2 << endl;
	cout << lower << endl;
	cout << upper << endl;

	return 0;
}