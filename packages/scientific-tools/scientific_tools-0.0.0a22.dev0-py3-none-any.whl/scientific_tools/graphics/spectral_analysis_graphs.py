"""This module trace figure to analyse spectrum of signals"""

import numpy as np
import matplotlib.pyplot as plt

def amplitudes_spectrum(function, f: float, fs: float,
anti_aliasing: bool = True,
args_before_t: list=[], args_after_t: list=[],
title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Amplitudes", color="blue", **kwargs) :
    """Plot the amplitudes' spectrum of the function thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, don't show aliased frequencies.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    color is lines color
    Caution : fs must be almost equal 2*fs or 4*fs
    """
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=1/fs)]
    N = len(signal_values)

    DFT = np.fft.fft(signal_values)*2/len(signal_values)#values of Discrete Fourier Transform
    if anti_aliasing :
        frequencies = np.arange(start= 0, stop=f*(N//2), step=f)
        DFT = DFT[:N//2]#remove aliased frenquencies
    else :
        frequencies = np.arange(N)
    amplitudes = np.abs(DFT)#calculate the modulus of DFT
    
    plt.vlines(frequencies, [0], amplitudes, color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def phases_spectrum(function, f: float, fs: float,
anti_aliasing: bool = True, unit: float = "deg",
args_before_t: list=[], args_after_t: list=[],
title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Phases", color="blue", **kwargs) :
    """Plot the phases' spectrum of the fiunction thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, don't show aliased frequencies.
    unit in the unit of phases (must be a string in this list : "deg" for degrees, "rad" for radians)
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    color is lines color
    Caution : fs must be almost equal 2*fs or 4*fs
    """
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=1/fs)]
    N = len(signal_values)

    DFT = np.fft.fft(signal_values)*2/len(signal_values)#values of Discrete Fourier Transform
    if anti_aliasing :
        frequencies = np.arange(start=f, stop=f*(N//2), step=f)
        DFT = DFT[1:N//2]#remove aliased frenquencies
    else :
        frequencies = np.arange(start=f, stop=f*N, step=f)
    
    phases = 2*np.angle(DFT)#calculate the arguments of DFT in radians
    if unit != "rad" :
        phases *= 180/np.pi#transform radian into degrees
    
    plt.vlines(frequencies, [0], phases, color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
