#!/usr/bin/env python
#Copyright 2017 Jiaxin Tang jxtang@bu.edu
#Copyright 2017 Ziran Li zrli@bu.edu
import sys

inputstr = sys.stdin.read()

def main():
    global s
    global time
    global time1
    s = inputstr.splitlines(True)
    time = sys.argv
    del time[0]
    if len(time) == 0:
        exit(2)
    for i in range(0, len(time)):
        try:
            time[i] = float(sys.argv[i])
        except:
            exit(2)
    for i in range(0, len(s)):
        s[i] = s[i].split()
        if len(s[i]) != 5:
            exit(1)
        for j in range(1, 5):
            try:
                s[i][j] = float(s[i][j])
            except:
                exit(1)
    time.append(0)
    time=sorted(time)
    for i in range(0,len(time)):
        if time[0]<0:
            del time[0]
    if len(time)==1:
        exit(2)
    time1=[0]*(len(time)-1)
    for i in range(0,len(time)-1):
        time1[i]=time[i+1]-time[i]
    output()            

def swap_v(i1,i2):
    delta_x = s[i1][1]-s[i2][1]
    delta_y = s[i1][2]-s[i2][2]
    delta_vx = s[i1][3]-s[i2][3]
    delta_vy = s[i1][4]-s[i2][4]
    dot = (delta_x*delta_vx+delta_y*delta_vy)/(delta_x*delta_x+delta_y*delta_y)
    s[i1][3]=s[i1][3]-dot*delta_x
    s[i1][4]=s[i1][4]-dot*delta_y
    s[i2][3]=s[i2][3]+dot*delta_x
    s[i2][4]=s[i2][4]+dot*delta_y

def collidetime(i1,i2):
    tt=0
    a = (s[i1][3]-s[i2][3])**2 + (s[i1][4]-s[i2][4])**2
    if(a==0):
        return 0
    b = 2*(s[i1][1]-s[i2][1])*(s[i1][3]-s[i2][3])+ 2*(s[i1][2]-s[i2][2])*(s[i1][4]-s[i2][4])
    c = (s[i1][1]-s[i2][1])**2 +(s[i1][2]-s[i2][2])**2-100
    if(a!=0):
        if((b**2-4*a*c)>=0):
            delta=(b**2-4*a*c)**0.5
            if(-b-delta)/(2*a)>=0:
                tt=(-b-delta)/(2*a)
            elif(-b+delta)/(2*a)>=0:
                tt=(-b+delta)/(2*a)
    if tt>0.00000000000001:
        return tt
    else:
        return 0


def collisioncase(time_index):
    tij=[[]]
    row=0
    tmin=time1[time_index]
    '''for i in range(len(s)-1):
        for j in range (i+1,len(s)):
            t0=collidetime(i,j)
            if type(t0)==float:
                if t0<=tmin:
                    tmin=t0
                    i2=i
                    j2=j'''
    for i in range(len(s)-1):
        for j in range (i+1,len(s)):
            t0=collidetime(i,j)
            if type(t0)==float:
                if t0<=tmin:
                    tmin=t0
                    tij.append([])
                    tij[row].append(t0)
                    tij[row].append(i)
                    tij[row].append(j)
                    row+=1
    ti=[v for v in tij if v and v[0]<=tmin]
    if tmin>=time1[time_index]:
        for i in range(len(s)):
            s[i][1]+=s[i][3]*time1[time_index]
            s[i][2]+=s[i][4]*time1[time_index]        
        printout(s)
    else:
        for i in range(len(s)):
            s[i][1]+=s[i][3]*tmin
            s[i][2]+=s[i][4]*tmin
        for i in range(len(ti)):
            swap_v(ti[i][1],ti[i][2])
        #swap_v(i2,j2)
        time1[time_index]-=tmin
        return(collisioncase(time_index))
        
def printout(list1):
    for i in range(len(list1)):
        for j in range(5):
            print((list1[i][j]), end=' ')
        print()

def output():
    for i in range(len(time1)):
        print(time[i+1])
        collisioncase(i)

if __name__ == '__main__':
    main()
