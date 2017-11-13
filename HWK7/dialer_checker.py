import unittest
import scipy.io.wavfile as wavfile
from  scipy.signal import spectrogram
import numpy as np
import random
import os
import ec602lib

# framerate * tone_time must be 800 for extract to work
refcode={'lines':18,'words':99}

progname = "dialer.py"

DialerTests = [('6', 8000, 0.1), 
('19', 8000, 0.1), 
('321', 4000, 0.2), 
('147', 8000, 0.1), 
('258', 8000, 0.1), 
('963', 8000, 0.1), 
('9123456780', 8000, 0.1), 
('8675309', 8000, 0.1), 
('6178675309', 16000, 0.05)]


DTMF = {'3': (697, 1477), '8': (852, 1336), '9': (852, 1477), '7': (852, 1209), '5': (770, 1336), '1': (697, 1209), '2': (697, 1336), '4': (770, 1209), '0': (941, 1336), '6': (770, 1477)}

def extract_digits(signal,frame_rate):
    tone_length = 200

    f,t,Sxx= spectrogram(signal,fs=frame_rate,window='boxcar',nperseg=tone_length)

    df = frame_rate//tone_length

    mapDTMF={}
    for dig in DTMF:
        mapDTMF[tuple(f[round(x/df)] for x in DTMF[dig])] = dig

    last=None

    result=[]
    i = 0 
    while i<len(t):
        count = 0        
        top_freq = tuple(sorted(f[x] for x in Sxx[:,i].argsort()[-2:]))
        next_freq = top_freq
        if next_freq not in mapDTMF:
            i += 1
            continue

        while next_freq in mapDTMF and next_freq == top_freq:
            i += 1
            count +=1
            if i==len(t): break
            next_freq = tuple(sorted(f[x] for x in Sxx[:,i].argsort()[-2:]))

        if count>1:
            result.append((mapDTMF[top_freq],count))
    return "".join(x[0] for x in result)



class DialerTestCase(unittest.TestCase):
    def test_signal(self):
        "a. extract touch tones from wave file"
        for dig,frame_rate,time_of_tone  in DialerTests:
            with self.subTest(CASE= dig):
                error = None
                try:
                  n = random.randint(10000,1000000)
                  fname='studentdialer{}.wav'.format(n)
                  dialer(fname,frame_rate,dig,time_of_tone)
                  st_frame_rate, st_signal=wavfile.read(fname)
                  os.remove(fname)
                except Exception as e:
                  error = e

                if error:
                  self.fail('Reading from the created wav file failed. Exception: {}'.format(error))

                # test rate
                if st_frame_rate != frame_rate:
                  self.fail('Frame rate mismatch: {} vs {}'.format(st_frame_rate,frame_rate))

                # test shape
                N = int(len(dig)*time_of_tone*frame_rate)
                if (N,) != st_signal.shape:
                  self.fail('Shape mismatch: {} vs {}'.format((N,),st_signal.shape))



                # test digit creation
                result_digits = extract_digits(st_signal, st_frame_rate)
                if result_digits != dig:
                    self.fail('Detect tones mismatch: {} vs {}'.format(result_digits,dig))
                



if __name__ == '__main__':
    from dialer import dialer
    _,results,_ = ec602lib.overallpy(progname,DialerTestCase,refcode)
    #unittest.main()
    print(results)

    unittest.main()