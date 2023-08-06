"""This module calculate spectrum, Fourier transform, ..."""

import numpy as np

def maximal_range(f: float, fs: float)->int :
    """Return the maximal range frequency of DFT without aliasing.
    
    f is the signal frequency
    fs is the sampling frequency. fs must be twice superior to the maximal frequence component in the original signal. 
    """
    if fs <= 2*f :
        raise ValueError("Sampling frequency must be twice superior to the maximal frequence component in the original signal.""")
    #f*n is the maximal frequency
    #According to Nyquist-Shannon theorem, fs > 2*n*f
    # So fs/(2*f) > n
    n = np.floor(fs/(2*f))
    if n == fs/(2*f) : #last frequence is aliased
        n -= 1
    return int(n)

def maximal_frequency(f: float, fs: float)->float :
    """Return the maximal frequency of DFT without aliasing.
    
    f is the signal frequency
    fs is the sampling frequency. fs must be twice superior to the maximal frequence component in the original signal. 
    """
    return f*maximal_range(f, fs)

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
    n = maximal_range(f, fs)
    return [f*i for i in range(n+1)]

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
    n = maximal_range(f, fs)
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=1/fs)]
    N = len(signal_values)

    DFT_coefficients = np.fft.rfft(signal_values)/N#values of Discrete Fourier Transform
    DFT_coefficients = DFT_coefficients[:n+1]#remove aliasing frequencies
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

def DFT_phases(function, f: float, fs: float, deg: bool = True,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[float] :
    """Return amplitudes list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time). This function must return real values.
    f is the signal frequency
    fs is the sampling frequency
    If deg is True phases are in degree, else they are in radians.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    DFT_coefficients = DFT(function, f, fs, args_before_t, args_after_t, **kwargs)

    phases = np.angle(DFT_coefficients, deg)#calculate the arguments of DFT in radians
    return list(phases)