//Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
#include <iostream>
#include <vector>
#include <sstream>
#include <iterator>
#include <string>  
#include <math.h>

using namespace std;

int main(int argc, char ** argv) {

vector<string> init;
vector<string> name;
vector<vector<double> > state;
string line;
float e;
string d = "1";

for (int i = 1; i < argc; i++) //check if arguments input have any character
{
	stringstream(argv[i]) >> d;
	for (int j = 0; j < d.size(); j++)
	{
		e = d[j];
		if (e < 48 || e > 57)
			if( e != 46)
		{
			cout << "arguments have alpha!" << endl;
            return 2;
			goto end;
		}
	}
}
if(argc < 2)      //no input of time arguments
{
	cout << "no time input!" << endl;
    return 2;
	goto end;
}

while(getline(cin,line))
{
	if (!line.size())
	{
		return 1;
		goto end;
	}
 init.push_back(line);
}

state.resize(init.size());
//input

for (int i=0;i<init.size();i++)
{
 istringstream iss(init[i]);
 vector<string> temp{istream_iterator<string>{iss},istream_iterator<string>{}};
 name.push_back(temp[0]);
 
 if (temp.size() != 5)   //check the number of the input 
 {
 	cout << "error! wrong input size" << endl;
     return 1;
 	goto end;
 }

 for(int j=1;j<5;j++){
 	stringstream(temp[j]) >> d;
 	for (int j = 0; j < d.size(); j++)
	{
		e = d[j];
		if (e < 48 || e > 57)
		{
			if( e != 46)
			{
				if (e != 45)
				{
					cout << "input alpha!" << endl;
                    return 1;
					goto end;
				}				
			}
		}
	}
  	state[i].push_back(stod(temp[j]));
 }
	
}
//put data in vector
double a,b,c,g,f,delta,result1,result2,collision_time,detect_time,current_time;
current_time= 0;
for(int k = 1;k < argc;k++){
	stringstream(argv[k]) >> detect_time;
	while(current_time < detect_time){
		stringstream(argv[k]) >> collision_time;
		int ctimes=0;
		for(int i = 0;i < init.size();i++){
			for(int j = i+1;j < init.size();j++){
				a = pow((state[i][2] - state[j][2]),2) + pow((state[i][3] - state[j][3]),2);
				b = 2*((state[j][0] - state[i][0])*(state[j][2] - state[i][2]) + (state[j][1] - state[i][1])*(state[j][3] - state[i][3]));
				c = (pow((state[j][0] - state[i][0]),2) + pow((state[j][1] - state[i][1]),2)-100);
				delta = double((pow(b,2) - 4*a*c));
				if(delta > 0){
					result1 = (-b - sqrt(delta))/(2*a);
					result2 = (-b + sqrt(delta))/(2*a);				
					if(result1 >= 0){
						if(detect_time > (current_time+result1)){
							if (collision_time >= result1){
							collision_time = result1;
							ctimes++;
						}
						else{
							collision_time = collision_time;
						}
						}
					}				
				}
				else{
					collision_time = collision_time;
				}
			}
		}
	//get the collision time
		if((current_time+collision_time) < detect_time){
			for(int i = 0;i < init.size();i++){
				state[i][0] = state[i][0] + state[i][2]*collision_time;
				state[i][1] = state[i][1] + state[i][3]*collision_time;
			}
	//get the new position
			for(int t=0;t<=ctimes;t++){
				for(int i = 0;i < init.size();i++){
					for(int j = i+1;j < init.size();j++){
						double instance; 
						double instance1;
						double deltat=0.0000001;
						instance = pow((state[i][0]-state[j][0]),2)+pow((state[i][1]-state[j][1]),2);
						instance = pow((state[i][0]-state[j][0])+(state[i][2]-state[j][2])*deltat,2)+pow((state[i][1]-state[j][1])+(state[i][3]-state[j][3])*deltat,2);	
						if (instance <= 100 && instance1<100){
								double temp1 = ((state[i][2] - state[j][2])*(state[i][0] - state[j][0]) + (state[i][3] - state[j][3])*(state[i][1] - state[j][1]))/(pow((state[i][0] - state[j][0]),2)+pow((state[i][1] - state[j][1]),2));
								double temp2 = ((state[j][2] - state[i][2])*(state[j][0] - state[i][0]) + (state[j][3] - state[i][3])*(state[j][1] - state[i][1]))/(pow((state[i][0] - state[j][0]),2)+pow((state[i][1] - state[j][1]),2));
								state[i][2] = state[i][2] - temp1*(state[i][0] - state[j][0]);
								state[i][3] = state[i][3] - temp1*(state[i][1] - state[j][1]);
								state[j][2] = state[j][2] - temp2*(state[j][0] - state[i][0]);
								state[j][3] = state[j][3] - temp2*(state[j][1] - state[i][1]);
//							}
						}
					}
				}
			}
			current_time = current_time + collision_time;
		}
		else{		
			for(int i = 0;i < init.size();i++){
				state[i][0] = state[i][0] + state[i][2]*(detect_time - current_time);
				state[i][1] = state[i][1] + state[i][3]*(detect_time - current_time);
			}
			cout<<detect_time<<endl;
			for(int i = 0;i < init.size();i++){	
				cout.precision(8);		
				cout<<name[i]<<" ";
				for(int j = 0;j < 4;j++){
					cout<<state[i][j]<<" ";
				}
				cout<<endl;
				current_time = detect_time;
			}
		}
	}
}
return 0;
end: cout << "end" << endl;
}