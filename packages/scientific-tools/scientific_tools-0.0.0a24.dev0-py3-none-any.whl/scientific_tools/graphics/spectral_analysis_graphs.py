"""This module trace figure to analyse spectrum of signals"""

import numpy as np
import matplotlib.pyplot as plt

import scientific_tools.physics.spectral_analysis as spectral_analysis

def plot_amplitudes_spectrum(function, f: float, fs: float,
args_before_t: list=[], args_after_t: list=[],
title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Amplitudes", color="blue", **kwargs) :
    """Plot the amplitudes' spectrum of the function thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    color is lines color
    """
    frequencies = spectral_analysis.DFT_frequencies(function, f, fs, args_before_t, args_after_t, **kwargs)
    amplitudes = spectral_analysis.DFT_amplitudes(function, f, fs, args_before_t, args_after_t, **kwargs)
    
    plt.vlines(frequencies, [0], amplitudes, color)
    plt.axis([-1, 1.05*max(frequencies), 0, 1.05*max(amplitudes)])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot_phases_spectrum(function, f: float, fs: float, deg: bool = True,
args_before_t: list=[], args_after_t: list=[],
title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Phases", color="blue", **kwargs) :
    """Plot the phases' spectrum of the fiunction thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If deg is True phases are in degree, else they are in radians.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    color is lines color
    """
    frequencies = spectral_analysis.DFT_frequencies(function, f, fs, args_before_t, args_after_t, **kwargs)
    phases = spectral_analysis.DFT_phases(function, f, fs, deg, args_before_t, args_after_t, **kwargs)

    plt.vlines(frequencies, [0], phases, color)
    max_y = np.pi
    if deg :
        max_y = 360
    plt.axis([-1, 1.05*max(frequencies), -1.05*max_y, 1.05*max_y])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
