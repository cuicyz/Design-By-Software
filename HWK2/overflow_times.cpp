//Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
//U32336445 
//HWK2
#include <iostream>
#include <cstdint>
#include <ctime>
#include <cmath>
using namespace std;

int main(int argc, char const *argv[])
{

	uint16_t b=1;

	uint8_t int8=pow(2,8)-1;
	uint16_t int16=pow(2,16)-1;
	uint32_t int32=pow(2,32)-1;
	long long int64=pow(2,64)-1;
	
	double x = (double)int8/int16;
	double y = (double)int16/int32;
	double z = (double)int16/int64;

	clock_t start_clock, end_clock;

	start_clock = clock();

	while (b>0) {b++;}

	end_clock = clock();

	double seconds = static_cast<double>(end_clock - start_clock) / CLOCKS_PER_SEC;
	double microsec = seconds * 1000000;

	double nanosec = (microsec*1000)/x;
	double sec = seconds/y;
	long double years = (microsec*3.171*(pow(10,-14)))/z;

	cout << "estimated int8 time (nanoseconds): " << nanosec << endl;
	
	cout << "measured int16 time (microseconds): " << microsec << endl;

	cout << "estimated int32 time (seconds): " << sec << endl;

	cout << "estimated int64 time (years): " << years << endl;

	return 0;
}