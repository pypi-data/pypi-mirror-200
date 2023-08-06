"""This module calculate spectrum, Fourier transform, ..."""

import numpy as np

def DFT_frequencies(function, f: float, fs: float,
anti_aliasing: bool = True,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->list[complex] :
    """Return frequencies corresponding to the coefficients list of DFT
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, delete aliased coefficients.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=1/fs)]
    N = len(signal_values)#caution : not opmised process
    assert N==fs//f
    #N = fs//f

    if anti_aliasing :
        frequencies = [f*i for i in range(N//2)]
    else :
        frequencies = [f*i for i in range(N + 1)]#+1 because end is excluded
    return frequencies

def DFT_complex(function, f: float, fs: float, nb_period:int = 1,
anti_aliasing: bool = True,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->tuple(list[complex]) :
    """Return complex coefficients list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, delete aliased coefficients.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    signal_values = [function(*args_before_t, t, *args_after_t, **kwargs) for t in np.arange(start=0, stop=1/f, step=nb_period/fs)]
    N = len(signal_values)

    DFT_coefficients = np.fft.fft(signal_values)/N#values of Discrete Fourier Transform
    if anti_aliasing :
        DFT_coefficients = DFT_coefficients[:N//2]#remove aliased frenquencies
    return DFT_coefficients

def DFT_amplitudes(function, f: float, fs: float,
anti_aliasing: bool = True,
args_before_t: list=[], args_after_t: list=[],
**kwargs)->tuple(list[complex]) :
    """Return amplitudes list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, delete aliased coefficients.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    DFT_coefficients = DFT_complex(function, f, fs, anti_aliasing, args_before_t, args_after_t, **kwargs)

    return np.abs(2*DFT_coefficients)#calculate the modulus of DFT_coefficients

def DFT_phases(function, f: float, fs: float,
anti_aliasing: bool = True, unit: float = "deg",
args_before_t: list=[], args_after_t: list=[],
**kwargs)->tuple(list[complex]) :
    """Return amplitudes list of Discrete Fourier Transform
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If anti_aliasing is True, delete aliased coefficients.
    unit in the unit of phases (must be a string in this list : "deg" for degrees, "rad" for radians)
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    """
    DFT_coefficients = DFT_complex(function, f, fs, anti_aliasing, args_before_t, args_after_t, **kwargs)

    phases = 2*np.angle(DFT_coefficients)#calculate the arguments of DFT in radians
    if unit != "rad" :
        phases *= 180/np.pi#transform radian into degrees
    phases.insert(0, 0)
    return phases