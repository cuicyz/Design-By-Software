// Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
// Copyright 2017
// Copyright 2017

#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <regex>
#include <cmath>
#include <typeinfo>


using namespace std;

struct Ball {
    string name;
    double xin, yin;
    double vxin, vyin;
};

///////////////////////////////////////////////////////////////////////////////

// Ascending sort function for time
bool wayToSort(double i, double j) { return i < j; }

bool isNumber(char number[])
{
    int i = 0;
    //checking for negative numbers
    if (number[0] == '-'){
        i = 1;
        return false;
    }
    else {
        for (; number[i] != 0; i++)
        {
            if (!isdigit(number[i]))
                return false;
        }
        return true;
    }
}

bool regexmatch(string s){
    regex e ("[-+]?([0-9]*\\.[0-9]+|[0-9]+)");
    if (regex_match (s,e))
        return true;
    return false;
}

bool regexmatch2(string s){
    regex e ("[+]?([0-9]*\\.[0-9]+|[0-9]+)");
    if (regex_match (s,e))
        return true;
    return false;
}

//////////////////////////////////////////////////////////////////////////////

void swap_v(double& ball1_x, double& ball1_y, double& ball2_x, double& ball2_y,
    double& ball1_vx, double& ball1_vy, double& ball2_vx, double& ball2_vy) {

    double delta_x = ball1_x - ball2_x;
    double delta_y = ball1_y - ball2_y;
    double delta_vx = ball1_vx - ball2_vx;
    double delta_vy = ball1_vy - ball2_vy;
    double dot = (delta_x*delta_vx+delta_y*delta_vy)/(delta_x*delta_x+delta_y*delta_y);

    ball1_vx -= dot*delta_x;
    ball1_vy -= dot*delta_y;
    ball2_vx += dot*delta_x;
    ball2_vy += dot*delta_y;
}

double collidetime(double ball1_x, double ball1_y, double ball2_x, double ball2_y,
    double ball1_vx, double ball1_vy, double ball2_vx, double ball2_vy) {

    double tt = 0;
    double a = pow((ball1_vx-ball2_vx),2) + pow((ball1_vy-ball2_vy),2);
    if(a==0){
        return 0;
    }
    double b = 2*(ball1_x-ball2_x)*(ball1_vx-ball2_vx)+2*(ball1_y-ball2_y)*(ball1_vy-ball2_vy);
    double c = pow((ball1_x-ball2_x),2)+pow((ball1_y-ball2_y),2) - 100;
    if(a!=0)
    {
        if((b*b-4*a*c)>=0)
        {
            double delta = sqrt(b*b-4*a*c);
            if((-b-delta)/(2*a)>=0)
            {
                tt = (-b-delta)/(2*a);
                //collide = true;
            }
            else if((-b+delta)/(2*a)>=0){
                tt = (-b+delta)/(2*a);
                //collide = true;
            }
        }
    }
    return tt;
/*    if(tt > 0.00000000000001) {
        return tt;
    } else {
        return 0;
    }*/
}

void printout(vector<Ball> v){
    for (int i = 0; i < sizeof(v); i++)
    {
        cout.precision(8);
        cout << v[i].name << " " << v[i].xin <<" "<<v[i].yin<<" "<<v[i].vxin<<" "<<v[i].vyin <<endl;
    }

}

void CollisionResponse(int time_label, vector<double>& v, vector<Ball>& BB){
    
    vector <double> tc,ic,jc;
    vector <double> ti,ii,ji;
    double t0;
    //int row = 0;
    double tmin = v[time_label];
    //cout << tmin << endl;
    for(int i=0;i<BB.size();i++){
        for(int j=i+1;j<BB.size();j++){
            t0 = collidetime(BB[i].xin, BB[i].yin, BB[j].xin, BB[j].yin,
                BB[i].vxin, BB[i].vyin, BB[j].vxin, BB[j].vyin);
            if (typeid(t0) == typeid(double)){
                if(t0<=tmin){
                    tmin = t0;
                    //cout << tmin << endl;
                    tc.push_back(t0);
                    ic.push_back(i);
                    jc.push_back(j);
                    //cout << i << " " << j << endl;
                    //row+=1;
                }
            }
        }
    }

    for(int i=0;i<tc.size();i++){
        if(tc[i]<=tmin){
            double d1 = tc[i];
            double d2 = ic[i];
            double d3 = jc[i];
            ti.push_back(d1);
            ii.push_back(d2);
            ji.push_back(d3);
            //cout << ic[i] << " " << jc[i] << endl;
        }
    }

    if(tmin>=v[time_label]){
        for(int k=0;k<BB.size();k++){
            BB[k].xin+=BB[k].vxin*v[time_label];
            BB[k].yin+=BB[k].vyin*v[time_label];
        }
        printout(BB);

    } else {
        for(int z=0;z<BB.size();z++){
            BB[z].xin+=BB[z].vxin*tmin;
            BB[z].yin+=BB[z].vyin*tmin;
        }
        for(int i=0;i<ti.size();i++){
            int num1 = ii[i];
            int num2 = ji[i];
            swap_v(BB[num1].xin,BB[num1].yin,BB[num2].xin,BB[num2].yin,
                BB[num1].vxin, BB[num1].vyin, BB[num2].vxin, BB[num2].vyin);
        }
        v[time_label]-=tmin;
        CollisionResponse(time_label, v, BB);
        //cout << v[time_label] << endl;
        //cout << tmin << endl;
         
    }
    return;
}


////////////////////////////////////////////////////////////////////////////

int main(int argc, char* argv[]){

vector<double> stime, vtime;
vector<string> checkin;
vector<Ball> balls;
string line;

// Get the time and put it in a string vector
for (int i=1; i<argc; i++){
    if (regexmatch2(argv[i]) == true) {
            double t1 = stod(argv[i]);
	        stime.push_back(t1);
    }
    else {
        return 2;
    }
}
stime.push_back(0);
// Increment the times
sort(stime.begin(), stime.end(), wayToSort);

// Read input file
while (getline(cin,line)) {
    if (!line.size()) {return 1;}

	istringstream ss(line);

    istringstream iss(line);
    do
    {
        string temp1;
        iss >> temp1;
        checkin.push_back(temp1); 
    } while(iss);
    if (checkin.size() > 6) {return 1;}
    
    for (int s=1; s<5; ++s){
        if (regexmatch(checkin[s]) == false) { return 1; }
    }
    checkin.clear();
    
	Ball ball;
	if (ss >> ball.name >> ball.xin >> ball.yin >> ball.vxin >> ball.vyin) {
		balls.push_back(ball);
	}
}

////////////////////////////////////////////////////////////////////////////

for (int t=0; t<stime.size()-1; ++t) {
    double time_diff = stime[t+1]-stime[t];
    vtime.push_back(time_diff);
}

for (int i=0; i<vtime.size(); ++i){
    //cout << stime[i+1] << endl;
    CollisionResponse(i, vtime, balls);
}

return 0;
}