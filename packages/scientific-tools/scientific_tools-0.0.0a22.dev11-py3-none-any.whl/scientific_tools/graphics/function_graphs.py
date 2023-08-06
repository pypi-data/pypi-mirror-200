"""This module trace function graphs."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_2Dfunction(function,
min_x: float, max_x: float, values_number: int,
args_before_x: list=[], args_after_x: list=[],
title: str="", xlabel: str="", ylabel: str="", function_label: str="", color="blue", linestyle ="-", **kwargs) :
    """Trace the 2D graphic of the function "function"
    
    function is a function with at least one argument x
    args_before_x is the list of positional arguments before the variable argument's position
    args_after_x is the list of positional arguments after the variable argument's position
    The value of the variable argument x varies from min_x to max_variable by taking values_number values
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    function_label is the label of the function. (Doesn't show it if you doesn't call plt.legend() after this plot_2Dfunction.)
    color is the line color
    linestyle is the line style (cf Matplotlib docs for futher information)
    You can add after keywords arguments for the function "function"
    """
    variable_list = np.linspace(min_x, max_x, values_number)
    results_list = []
    for variable in variable_list :
        results_list.append(function(*args_before_x, variable, *args_after_x, **kwargs))
    
    #displaying
    plt.plot(variable_list, results_list, color=color, linestyle=linestyle, label=function_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot_3Dfunction(function,
min_x: float, max_x: float, values_x: int,
min_y: float, max_y: float, values_y: int,
args_before_variables: list=[], args_between_variables: list=[], args_after_variables: list=[], x_before_y: bool=True,
ax=None,
title: str="", xlabel: str="", ylabel: str="", zlabel: str="",
colormap=cm.RdYlGn, **kwargs) :
    """Trace the 3D graphic of the function "function"
    
    function is a function with at least two arguments
    args_before_variable is the list of positional arguments before the first variable argument's position
    args_between_variables is the list of positional arguments between positions of the first and the second variable
    args_after_variables is the list of positional arguments after the second variable argument's position
    x_before_x is true if x variable is the first variable (in the function arguments order)
    The value of the "x" variable varies from min_x to max_x by taking values_x values
    Idem for "y" variable
    ax a Ax object (a class of matplotplib.pyplot). ax is use to plot the function curve (if you doesn't give an ax, this function creates one)
    title is the graph title
    xlabel, ylabel and zlabel are texts to put on the axes
    colormap is the colormap used for displaying
    You can add after keywords arguments for the function "function"
    """
    line = np.linspace(min_x, max_x, values_x)
    array_x = np.array([line for i in range(values_y) ], dtype=float)
    #create an array with x values
    column = np.linspace(min_y, max_y, values_y)
    array_y = np.array([[column[j]]*values_x for j in range(values_y)], dtype=float)
    #create an array with y values
    results = []#a array like object with values of function
    for i in range(values_y) :
        results_line = []
        for j in range(values_x) :
            variable1 = array_x[i][j]
            variable2 = array_y[i][j]
            if x_before_y is False :
                variable1, variable2 = variable2, variable1
            results_line.append(function(*args_before_variables, variable1, *args_between_variables, variable2, *args_after_variables, **kwargs))
        results.append(results_line)
    array_z = np.array(results, dtype=float)

    linewidth = (max_x - min_x+ max_y - min_y)/20#to trace around 10 lines 

    #displaying
    if ax is None :
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(array_x, array_y, array_z, cmap=colormap, linewidth=linewidth)#linewidth : distance between two lines
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
