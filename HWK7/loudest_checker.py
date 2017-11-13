""" loudest checker


"""

import ec602lib
import unittest
from numpy import pi,cos,sin,linspace,ones_like,zeros_like
import scipy.io.wavfile as wavfile
import time

debug = False

testing_time={}

def read_wave(fname,debug=False):
    frame_rate,music = wavfile.read(fname)
    if debug:
        print(frame_rate,type(music),music.shape,music.ndim)
    if music.ndim>1:
        nframes,nchannels = music.shape
    else:
        nchannels = 1
        nframes = music.shape[0]    
    return music,frame_rate,nframes,nchannels

music,frame_rate,nframes,nchannels = read_wave("bach10sec.wav")
if nchannels > 1:
    music = music.sum(axis=1)

refcode={'lines':22,'words':80}

progname = "loudest.py"

def match_signals(w,ref):
    "return the relative similarity of w and ref"
    energy = (abs(ref)**2).sum()
    error = (abs(w-ref)**2).sum() 
    return error/energy

class loudestTestCase(unittest.TestCase):
    def test_find_band(self):
        "a. sine wave at 100 Hz, 1 kHz frame rate"
        frame_rate,T,ftest,bandwidth = 1000,1,100,10
        m = sin(2*pi*ftest * linspace(0,T,T*frame_rate,endpoint=False))
        low,high,filtered = loudest_band(m,frame_rate,bandwidth)
        self.assertEqual(m.shape,filtered.shape)
        self.assertLess(low,ftest,msg="low of band incorrect")
        self.assertLess(ftest,high,msg="high of band incorrect")
        self.assertEqual(bandwidth,high-low,msg="high-low must match bandwidth")
        self.assertLess(match_signals(filtered,m),0.1,msg="filtered signal incorrect")

    def test_find_energy(self):
        "b. cosines at 10 11 12 and 30"
        frame_rate,T,ftest,bandwidth = 10000,1,100,10
        t = linspace(0,T,T*frame_rate,endpoint=False)
        m = zeros_like(t)
        for a,f in [(1,10),(1,11),(1,12),(2,30)]:
            m += a*cos(2*pi*f*t)
        low,high,filtered = loudest_band(m,frame_rate,bandwidth)
        self.assertEqual(m.shape,filtered.shape)
        self.assertLessEqual(low,30,msg="low of band incorrect")
        self.assertLessEqual(30,high,msg="high of band incorrect")
        self.assertEqual(bandwidth,high-low)

    def test_find_band_split(self):
        "d. two sines 80% of bw apart"
        frame_rate,T,ftest,bandwidth = 10000,1,100,10
        t = linspace(0,T,T*frame_rate,endpoint=False)
        m = sin(2*pi*ftest*t)+sin(2*pi*(ftest+0.8*bandwidth)*t)
        low,high,filtered = loudest_band(m,frame_rate,bandwidth)
        self.assertEqual(m.shape,filtered.shape)
        self.assertLessEqual(low,ftest,msg="low of band incorrect")
        self.assertLessEqual(ftest+.8*bandwidth,high,msg="high of band incorrect")
        self.assertEqual(bandwidth,high-low)
        self.assertLess(match_signals(filtered,m),0.1,msg="filtered signal incorrect")

    def test_find_band_dc(self):
        "c. DC is the loudest"
        frame_rate,T,ftest,bandwidth = 1000,1,100,20
        t = linspace(0,T,T*frame_rate,endpoint=False)
        m = ones_like(t) + sin(2*pi*bandwidth//2*t)
        low,high,filtered = loudest_band(m,frame_rate,bandwidth)
        self.assertEqual(m.shape,filtered.shape)
        self.assertEqual(high,bandwidth)
        self.assertEqual(low,0)
        self.assertLess(match_signals(filtered,m),0.1,msg="filtered signal incorrect")

    def test_bach(self):
        "e. what is the loudest 75 Hz of Bach 10 seconds?"
        start = time.time()
        low,high,filtered = loudest_band(music,frame_rate,75)
        duration = time.time() - start
        testing_time['bach']=duration
        self.assertEqual(music.shape,filtered.shape)        
        self.assertAlmostEqual(low/823.5,1.0,2)
        self.assertAlmostEqual(high/898.3,1.0,2)
    

if __name__ == '__main__':
    from loudest import loudest_band
    _,results,_ = ec602lib.overallpy(progname,loudestTestCase,refcode)
    print(results)
    print()
    print('processing bach10sec took {:.2f} seconds'.format(testing_time['bach']))
    if testing_time['bach'] > 1.0:
            print("WARNING: my analysis of bach10sec takes 0.13 s, yours took {:.3f} s".format(testing_time['bach']))
            print('the actual checker will fail you on this test. Passing this is extra credit.')
      #unittest.main() # alternative testing suite from unittest
