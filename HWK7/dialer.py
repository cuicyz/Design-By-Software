#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu

#!/usr/bin/python
import scipy.io.wavfile as wavfile
import numpy as np

def dialer(file_name, frame_rate, phone, tone_time):

    output=[]
    
    for n in phone:
        if(n=="0"):
            LF = 941.0
            HF = 1336.0
        elif(n=="1"):
            LF = 697.0
            HF = 1209.0
        elif(n=="2"):
            LF = 697.0
            HF = 1336.0
        elif(n=="3"):
            LF = 697.0
            HF = 1477.0
        elif(n=="4"):
            LF = 770.0
            HF = 1209.0
        elif(n=="5"):
            LF = 770.0
            HF = 1336.0
        elif(n=="6"):
            LF = 770.0
            HF = 1477.0
        elif(n=="7"):
            LF = 852.0
            HF = 1209.0
        elif(n=="8"):
            LF = 852.0
            HF = 1336.0
        elif(n=="9"):
            LF = 852.0
            HF = 1477.0
        elif(n=="A"):
            LF = 697.0
            HF = 1633.0
        elif(n=="B"):
            LF = 770.0
            HF = 1633.0
        elif(n=="C"):
            LF = 852.0
            HF = 1633.0
        elif(n=="D"):
            LF = 941.0
            HF = 1633.0
        elif(n=="*"):
            LF = 941.0
            HF = 1209.0
        elif(n=="#"):
            LF = 941.0
            HF = 1477.0
        else:
            LF = 0.0
            HF = 0.0
            
        period = np.linspace(0, tone_time, tone_time*frame_rate,endpoint=False)
        #print(period)
        LF_sinewave = np.sin(2*np.pi*LF*period)
        #print(LF_sinewave)
        HF_sinewave = np.sin(2*np.pi*HF*period)
        #print(HF_sinewave)
        tone_wave = LF_sinewave + HF_sinewave
        output = np.concatenate([output, tone_wave])
        #print(output)
        
    output = np.array(output)
    #print (output)
    wavfile.write(file_name, frame_rate, output)  

dialer("test1",4000,"321",0.2)