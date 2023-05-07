#iJ

import pyaudio
from pyaudio import PyAudio, paFloat32, paInt16
import numpy as np
import time
import noisereduce as nr
import math

np.seterr(invalid='ignore')

def check_frequency(recording, volume_division, noise_reduction):
    try:


        CHUNK = 4096
        RATE = 44100
        DEVICE = 0


        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=RATE,
                        input_device_index=DEVICE,
                        frames_per_buffer=CHUNK,
                        input=True)

        def lower_volume(data):
            data = np.array((data//int(volume_division)))
            return data

        while (recording == "on"):
            indata = nr.reduce_noise(y=(np.frombuffer(stream.read(CHUNK),dtype=np.int16)), sr=RATE)
            indata = lower_volume(indata)
            
            for i in range(int(noise_reduction)):
                indata = nr.reduce_noise(y=indata, sr=RATE)
                
            fftData=abs(np.fft.rfft(indata))**2
            which = fftData[1:].argmax() + 1
            
            if which != len(fftData)-1:
                current_frequency = which*RATE/CHUNK
                current_frequency = int(current_frequency)
                return current_frequency

        stream.close()
        p.terminate()

    except:
        current_frequency = "0"
        return current_frequency