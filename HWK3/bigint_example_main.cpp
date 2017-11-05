#include <iostream>
#include <vector>

using namespace std;

#include "bigint.cpp"

int main()
{ 

  BigInt A,B;

  cin >> A >> B;

  cout << multiply_int(A,B) << endl;

}