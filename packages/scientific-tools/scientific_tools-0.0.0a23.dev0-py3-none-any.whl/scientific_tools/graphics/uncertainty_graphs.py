"""This module trace graphs to show uncertainties."""

import matplotlib.pyplot as plt
import numpy as np

from scientific_tools.graphics.function_graphs import plot_2Dfunction
import scientific_tools.physics.uncertainty as uncertainty

def plot_uncertainty_function(f, u_f, min_x, max_x, values_number, args_before_x=[], args_after_x=[], title="", xlabel="", ylabel="", function_label="f(x)", uncertainty_label="f(x)±u(f(x))", function_color='red', uncertainty_color='blue', function_linestyle="-", uncertainty_linestyle="-",  **kwargs) :
    """Draw a graph with f, f + u_f and f - u_f
    
    Draw an uncertainty graph with the function f, the function plus its uncertainty (f + u_f) and the fonction minus its uncertainty (f - u_f).
    f is a function that take at least one argument x that varies from min_x to max_x by taking values_number values. 
    u_f calculate the uncertainty of f. It take at least one argument : x. (To add other arguments, see plot_2Dfunction documentation. N.B. f and u_f must have the same arguments)
    
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    function_label is the text display in the legend about function curve
    uncertainty_label is the text display in the legend about curves that represent f ± u_f
    function_color is color of function curve
    uncertainty_color is the color of curves that represent f ± u_f
    function_linestyle & uncertainty_linestyle are the line style of each curve (cf Matplotlib docs for futher information)
    """
    f_plus_u = lambda *args, **kwargs : f(*args, **kwargs) + u_f(*args, **kwargs)
    plot_2Dfunction(f_plus_u, min_x, max_x, values_number, args_before_x, args_after_x, color=uncertainty_color, linestyle =uncertainty_linestyle, function_label=uncertainty_label, **kwargs)#draw f+u_f

    f_minus_u = lambda *args, **kwargs : f(*args, **kwargs) - u_f(*args, **kwargs)
    plot_2Dfunction(f_minus_u, min_x, max_x, values_number, args_before_x, args_after_x, color=uncertainty_color, linestyle =uncertainty_linestyle, **kwargs)#draw f-u_f

    plot_2Dfunction(f, min_x, max_x, values_number, args_before_x, args_after_x, title=title, xlabel=xlabel, ylabel=ylabel, function_label=function_label, color=function_color, linestyle =function_linestyle,  **kwargs)#draw f (this is the last function drawing else title and axes labels haven't been displayed)
    
    plt.legend()#show function & uncertainty labels

def plot_uncertainty_points(x, y, u_x, u_y, title="Experimental values with error bar", xlabel="", ylabel="") :
    """Draw experimental values with error bar
    
    x is the list of x coordinates, y is the list of y coordinates
    u_x is the list of x uncertainties, u_y is the list of y uncertainties
    xlabel is the text to display with the x ax
    ylabel is the text to display with the y ax
    """
    plt.errorbar(x, y, xerr=u_x, yerr=u_y, fmt='bo', label='Mesures')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def null_function(*args, **kwargs) :
    """Return 0 for all value of 'value'.
    
    It's can use as an uncertainty calculator when the function is a reference function. (see the documentation of plot_z_score_graph).
    """
    return 0

def plot_z_score_graph(f1, u_f1, f2, u_f2, min_x, max_x, values_nb, args_f1_before_x=[], args_f1_after_x=[], kwargs_f1={}, args_f2_before_x=[], args_f2_after_x=[], kwargs_f2={}, z_score_limit=2, title="", xlabel="", ylabel="", limit_label="Limits of z-score validity", z_score_label="Z-score", limit_color='red', z_score_color='blue', limit_linestyle="-", z_score_linestyle="-",) :
    """Trace the z-score between two functions
    
    f1 is the first function & f2 is the second one.
    u_f1 is the function that calculate the f1 uncertainty & u_f2 calculate f2 uncertainty.
    Those four functions takes at least one argument x that varies from min_x to max_x by taking values_nb values.
    f1 and u_f1 take same args and kwargs. args_f1_before_x is the list of f1 positional arguments before the x position
    args_f1_after_x is the list of f1 positional arguments after the x position
    kwargs_f1 is a dictionary with f1 kwargs
    (Idem for f2)
    If a function is a function reference, u_f must be null_function  (define in this module).

    z_score_limit is the validity limit for the z-score (usually, it's 2) 
    limit_color is color of lines that represents limits of z_score validity
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    limit_label is the text display in the legend about lines that represents limits of z_score validity
    z_score_label is the text display in the legend about the z-score curve
    z_score_color is the color of the z_score curve
    limit_linestyle & z_score_linestyle are the line style of each curve (cf Matplotlib docs for futher information)
    """
    x_values = np.linspace(min_x, max_x, values_nb)
    
    #calculate values for f1 & f2
    f1_values = []
    u_f1_values = []
    f2_values = []
    u_f2_values = []
    for x in x_values :
        f1_values.append(f1(*args_f1_before_x, x, *args_f1_after_x, **kwargs_f1))
        if u_f1 is not null_function :
            u_f1_values.append(u_f1(*args_f1_before_x, x, *args_f1_after_x, **kwargs_f1))
        f2_values.append(f2(*args_f2_before_x, x, *args_f2_after_x, **kwargs_f2))
        if u_f2 is not null_function :
            u_f2_values.append(u_f2(*args_f2_before_x, x, *args_f2_after_x, **kwargs_f2))

    z_score_values = []
    #calculate z_score
    if u_f1 is null_function :
        for i in range(values_nb) :
            z_score_values.append(uncertainty.z_score_ref(f2_values[i], f1_values[i], u_f2_values[i]))
    elif u_f2 is null_function :
        for i in range(values_nb) :
            z_score_values.append(uncertainty.z_score_ref(f1_values[i], f2_values[i], u_f1_values[i]))
    else :
        for i in range(values_nb) :
            z_score_values.append(uncertainty.z_score(f1_values[i], u_f1_values[i], f2_values[i], u_f2_values[i]))

    #displaying
    plt.plot(x_values, z_score_values, color=z_score_color, linestyle=z_score_linestyle, label=z_score_label)
    plt.plot([np.min(x_values), np.max(x_values)], [z_score_limit, z_score_limit], color=limit_color,linestyle=limit_linestyle, label=limit_label)
    plt.plot([np.min(x_values), np.max(x_values)], [-z_score_limit, -z_score_limit], color=limit_color,linestyle=limit_linestyle)
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def plot_z_score_points_graph(x, y1, u_y1, y2, u_y2, z_score_limit=2, title="", xlabel="", ylabel="", limit_label="Limits of z-score validity", z_score_label="Z-score", limit_color='red', z_score_color='blue', limit_linestyle="-", z_score_linestyle="-") :
    """Trace the z-score between two lists of points
    
    x is the list of point abscissa
    y1 is the first list of values & f2 is the second one.
    u_y1 is the list of uncertainties of y1 points & u_y2 is the list for y2 points uncertainties. If a list of points is a reference, u_y be a list of zero
    
    title is the graph title
    xlabel and ylabel are texts to put on the axes
    limit_label is the text display in the legend about lines that represents limits of z_score validity
    z_score_label is the text display in the legend about the z-score curve
    z_score_limit is the validity limit for the z-score (usually, it's 2) 
    limit_color is color of lines that represents limits of z_score validity
    z_score_color is the color of the z_score curve
    limit_linestyle & z_score_linestyle are the line style of each curve (cf Matplotlib docs for futher information)
    """
    z_score_values = []
    #calculate z_score
    for i in range(len(x)) :
        z_score_values.append(uncertainty.z_score(y1[i], u_y1[i], y2[i], u_y2[i]))

    #displaying
    plt.plot(x, z_score_values, color=z_score_color, linestyle=z_score_linestyle, label=z_score_label)
    plt.plot([np.min(x), np.max(x)], [z_score_limit, z_score_limit], color=limit_color,linestyle=limit_linestyle, label=limit_label)
    plt.plot([np.min(x), np.max(x)], [-z_score_limit, -z_score_limit], color=limit_color,linestyle=limit_linestyle)
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

