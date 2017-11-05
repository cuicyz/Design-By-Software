//Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
//U32336445 
//HWK1
#include <iostream>
using namespace std;

int main(int argc, char const *argv[])
{
	//Loop through the arguments
	for (int i=1; i<argc; i++){
		//If less than five arguments, print to standard out
		if(i<5){
			cout << argv[i] << endl;
		}
		//If more than four arguments, print those to standard error
		if(i>4){
			cerr << argv[i] << endl;
		}
	}
	return 0;
}