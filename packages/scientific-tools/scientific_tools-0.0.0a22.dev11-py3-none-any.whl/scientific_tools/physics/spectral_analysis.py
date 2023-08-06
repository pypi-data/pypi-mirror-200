"""This module calculate spectrum, Fourier transform, ..."""

import numpy as np

def DFT_frequencies(function, f: float, fs: float,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[complex] :
    """Return frequencies corresponding to the coefficients list of DFT
    
    function is a function with at least one argument (the time). This function must return real values.
    f is the signal frequency
    fs is the sampling frequency. fs must be twice superior to the maximal frequence component in the original signal. 
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    if fs < 2*f :
        raise ValueError("Sampling frequency must be twice superior to the maximal frequence component in the original signal.""")
    
    #N is the number of values in signal values
    #signal_values = [0 for t in np.arange(start=0, stop=1/f, step=1/fs)]
    #N = len(signal_values)

    #To optimise this function, we calculate N with an other calculus
    if fs//f == fs/f :
        N = fs//f
    else :
        N = int(fs//f) + 1
    return [f*i for i in range(N//2+1)]

def DFT(function, f: float, fs: float,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[complex] :
    """Return complex coefficients list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time). This function must return real values.
    f is the signal frequency
    fs is the sampling frequency
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    if fs < 2*f :
        raise ValueError("Sampling frequency must be twice superior to the maximal frequence component in the original signal.""")
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=1/fs)]
    N = len(signal_values)

    DFT_coefficients = np.fft.rfft(signal_values)/N#values of Discrete Fourier Transform
    return list(DFT_coefficients)

def DFT_amplitudes(function, f: float, fs: float,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[float] :
    """Return amplitudes list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time). This function must return real values.
    f is the signal frequency
    fs is the sampling frequency
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    DFT_coefficients = DFT(function, f, fs, args_before_t, args_after_t, **kwargs)

    amplitudes = 2*np.abs(DFT_coefficients)#calculate the modulus of DFT_coefficients
    amplitudes[0] /= 2
    return list(amplitudes)

def DFT_phases(function, f: float, fs: float, unit: float = "deg",
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[float] :
    """Return amplitudes list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time). This function must return real values.
    f is the signal frequency
    fs is the sampling frequency
    unit in the unit of phases (must be a string in this list : "deg" for degrees, "rad" for radians)
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    DFT_coefficients = DFT(function, f, fs, args_before_t, args_after_t, **kwargs)

    phases = 2*np.angle(DFT_coefficients)#calculate the arguments of DFT in radians
    if unit != "rad" :
        phases *= 180/np.pi#transform radian into degrees
    return list(phases)