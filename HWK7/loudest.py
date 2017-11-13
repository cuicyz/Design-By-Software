#Copyright 2017 Chuan Xing Zheng czheng78@bu.edu

#!/usr/bin/python
import scipy.io.wavfile as wavfile
import time
import timeit
import numpy as np
from scipy import signal

def loudest_band(music,frame_rate,bandwidth):
    
    band = int(bandwidth/(frame_rate/len(music))) 

    firstfft = np.fft.fft(music)
    z = np.fft.fftshift(firstfft)    
    zer = np.arange(-frame_rate/2,frame_rate,frame_rate/len(music))
    zero = abs(zer).argmin()

    musicfft = z[zero:]
    musicfft = np.array(musicfft)    
   
    signalpwr = abs(musicfft)**2

    lo = []
    hi = []
    pwr = []   

    #start = timeit.default_timer()    
    for i in np.arange(len(musicfft)-band):
        pwr += [np.sum(signalpwr[i:i+band-1])]
        lo += [i]
        hi += [i+band]
    #stop = timeit.default_timer()
    #print(stop-start)     

    maxi = np.argmax(pwr)
    if(maxi!= 0):
        bp1 = np.append(np.ones(bandwidth+1),np.zeros(maxi-1))
        bpneg = np.append(np.zeros(zero - bandwidth - maxi), bp1)

        bp2 = np.append(np.zeros(maxi-1),np.ones(bandwidth+1))
        bppos = np.append(bp2,np.zeros(zero-bandwidth-maxi))
    else:
        bpneg = np.append(np.zeros(zero - bandwidth - maxi),np.ones(bandwidth))
        bppos = np.append(np.ones(bandwidth),np.zeros(zero - bandwidth - maxi))
    
    final = np.append(bpneg,bppos)
    
    filtered = z*final
    time = np.fft.ifft(np.fft.ifftshift(filtered))
    
    result = (lo[maxi]*(frame_rate/len(music)),hi[maxi]*(frame_rate/len(music)),time.real)      
    
    return result
