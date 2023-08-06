import numpy as np 
import matplotlib.pyplot as plt 

__all__ = ['sine_wave','cosine_wave']

def sine_wave(frequency, amplitude, phase, sampling_rate, duration):
    """
    sine_wave(frequency=440, amplitude=1, phase=0, sampling_rate=44100, duration=1)
    
    """
    # Generate time values
    time = np.linspace(0, duration, int(sampling_rate * duration))
    # Generate sine wave values
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    # to plot the singal 
    plt.plot(sine_wave)
    plt.title("Sine Wave")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()



def cosine_wave(frequency, amplitude, phase, sampling_rate, duration):
    """
    cosine_wave(frequency=3, amplitude=1, phase=0, sampling_rate=44100, duration=1)
    """
    # Generate time values
    time = np.linspace(0, duration, int(sampling_rate * duration))
    # Generate cosine wave values
    cosine_wave = amplitude * np.cos(2 * np.pi * frequency * time + phase)
    # to plot the singal 
    plt.plot(cosine_wave)
    plt.title("Sine Wave")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()