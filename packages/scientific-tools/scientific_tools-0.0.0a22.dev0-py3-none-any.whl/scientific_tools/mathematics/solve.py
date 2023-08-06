"""This file contains functions to solve equations."""

import numpy as np
import numpy.linalg as la#import functions about "linear algebra"

def dichotomy(f, x_min, x_max, args_before_x=[], args_after_x=[], accuracy=-3):
    """Search the x value to obtain f(x)=0 with an accuracy of 10^(accuracy).
    
    This function is based on the dichotomous algorithm.

    function is a function with at least one argument x. f must be a continuous function (in the mathematical sense) and must be strictly monotone. f(x_min) and f(x_max) must have different signs (one positive and one negative).
    args_before_x is the list of positional arguments before the variable argument's position
    args_after_x is the list of positional arguments after the variable argument's position
    The value of the variable argument x varies from min_x to max_variable
    """
    a = x_min
    f_a = f(*args_before_x, a, *args_after_x)
    b = x_max
    f_b = f(*args_before_x, b, *args_after_x)

    if f_a*f_b  > 0 :
        #f=0 can have no solution (under the hypothesis of continuous function and strictly monotone function)
        x = None
    #because f is strictly monotone, f_a != f_b, in particular f_a = f_b = 0 is not possible
    elif f_a == 0 :
        x = a
    elif f_b == 0 :
        x = b
    else :
        while b-a > 10**accuracy :
            m = a + (b-a)/2
            f_a = f(*args_before_x, a, *args_after_x)
            f_m = f(*args_before_x, m, *args_after_x)
            if f_m == 0 :
                break
            elif f_a*f_m > 0 :
                a = m
            else :
                b = m
        x = a + (b-a)/2
    return x

def explicit_finite_difference_solver(Ctt:float, Ctx:float, Cxx:float,
        Ct:float, Cx:float, Cu:float, Cc:float,
        min_t:float, max_t:float, T:int, min_x:float, max_x:float, X:int,
        U_t0 : list, U_t1 : list, U_min_x : list, U_max_x : list):
    """Solve a partial differential equation with the finite difference method.
    
    The partial differential equation must have two variables (called t and x).
    It must be linear with constant coefficients.
    Its shape must be : Ctt Utt + Ctx Uxt + Cxx Uxx + Cx Ux + Ct Ut + Cu U = Cc
    This function use explicit method with finite difference to solve this equation.
    
    Solving limits and accuracy:
    min_t is the minimal value for t
    max_t is the maxiamal value for t
    T is the number of t values
    min_x is the minimal value for x
    max_x is the maxiamal value for x
    X is the number of x values
        
    Initial conditions:
    U_t0 is the list of U values when t = min_t. len(U_t0) must be X.
    U_t1 is the list of U values when t = min_t + 1*step_t. len(U_t1) must be X.
    
    Limit conditions:
    U_min_x is the list of U values when x=min_x. len(U_min_x) must be T-2.
    U_max_x is the list of U values when x=max_x. len(U_max_x) must be T-2.

    Return a matrix where line index represent t and column index represent x. 
    
    Warning ! To ensure solution stability, it's heavily recommend to check if 
    r = Cxx * T * (max_x-min_x)**2/((max_t-min_t)*(X**2)) < 0.5
    To avoid stability problems, please use implicit_finite_difference_solver function.
    """
    step_t = (max_t-min_t)/(T-1)
    step_x = (max_x-min_x)/(X-1)
    
    #check if the solution will be stable
    r = Cxx * step_t/(step_x**2)
    if r <= 0.5 :
        raise UserWarning("The solving of the partial differential equation may be not stable. To avoid unstability change T & X.")

    Ktt = Ctt/(step_t**2)
    Ktx = Ctx/(4 * step_t *step_x)
    Kxx = Cxx/(step_x**2)
    Kt = Ct/step_t
    Kx = Cx/(2*step_x)
    
    #constants for the differential equation
    C1 = Ktx
    C2 = Ktt + Kt + 3*Cu/2
    C3 = - Ktx
    C4 = Kxx + Kx
    C5 = -2*Ktt - 2*Kxx - Kt - Cu
    C6 = Kxx - Kx
    C7 = -Ktx
    C8 = Ktt + Cu/2
    C9 = Ktx

    #U will contains values of U, the searched function
    U = np.zeros[[T, X]]

    #initial conditions
    U[0] = U_t0
    U[1] = U_t1

    #resolve an linear system to have U value at the time n+1
    for n in range(2, T) :
        #C is the second hand matrix
        C = np.zeros(X)
        for i in range(X) :
            if i == 0 :
                C[i] = U_min_x[n-2]
            if i == X-1 :
                C[i] = U_max_x[n-2]
            else :
                C[i] = Cc - C4*U[n-1, i+1] - C5*U[n-1, i] - C6*U[n-1, i-1] - C7*U[n-2, i+1], -C8*U[n-2, i] - C9*U[n-2, i-1]
        
        M = np.zeros([X, X])
        for i in range(X) :
            if i in (0, X-1) :
                M[i, i]=1
            else :
                M[i+1] = C1
                M[i] = C2
                M[i-1] = C3

        U[n] = la.solve(M, C)

    return U

def explicit_finite_difference_solver_2(Ctt:float, Cxx:float,
        Ct:float, Cx:float, Cu:float, Cc:float,
        min_t:float, max_t:float, T:int, min_x:float, max_x:float, X:int,
        U_t0 : list, U_t1 : list, U_min_x : list, U_max_x : list):
    """Solve a partial differential equation with the finite difference method.
    
    The partial differential equation must have two variables (called t and x).
    It must be linear with constant coefficients.
    Its shape must be : Ctt Utt + Cxx Uxx + Cx Ux + Ct Ut + Cu U = Cc
    This function use explicit method with finite difference to solve this equation.
    
    Solving limits and accuracy:
    min_t is the minimal value for t
    max_t is the maxiamal value for t
    T is the number of t values
    min_x is the minimal value for x
    max_x is the maxiamal value for x
    X is the number of x values
        
    Initial conditions:
    U_t0 is the list of U values when t = min_t. len(U_t0) must be X.
    U_t1 is the list of U values when t = min_t + 1*step_t. len(U_t1) must be X.
    
    Limit conditions:
    U_min_x is the list of U values when x=min_x. len(U_min_x) must be T-2.
    U_max_x is the list of U values when x=max_x. len(U_max_x) must be T-2.

    Return a matrix where line index represent t and column index represent x. 
    
    Warning ! To ensure solution stability, it's heavily recommend to check if 
    r = Cxx * T * (max_x-min_x)**2/((max_t-min_t)*(X**2)) < 0.5
    To avoid stability problems, please use implicit_finite_difference_solver function.
    """
    step_t = np.linspace(min_t, max_t, T, retstep=True)[1]
    #step_t =(max_t-min_t)/(T-1)
    step_x = np.linspace(min_x, max_x, X, retstep=True)[1]
    #step_x = (max_x-min_x)/(X-1)

    Ktt = Ctt/(step_t**2)
    Kxx = Cxx/(step_x**2)
    Kt = Ct/step_t
    Kx = Cx/(2*step_x)
    
    #constants for the differential equation
    C2 = Ktt + Kt + 3*Cu/2
    C4 = Kxx + Kx
    C5 = -2*Ktt - 2*Kxx - Kt - Cu
    C6 = Kxx - Kx
    C8 = Ktt + Cu/2

    #U will contains values of U, the searched function
    U = np.zeros([T, X])

    #initial conditions
    assert len(U_t0) == X
    assert len(U_t1) == X
    U[0] = U_t0
    U[1] = U_t1

    #resolve an linear system to have U value at the time n+1
    for n in range(1, T-1) :
        for i in range(X) :
            if i == 0 :
                U[n+1, 0] = U_min_x[n-1]
            elif i == X-1 :
                U[n+1, X-1] = U_max_x[n-1]
            else :
                U[n+1, i] = (Cc -C2*U[n-1, i] - C4*U[n, i-1] - C5*U[n, i] - C6*U[n, i+1])/C8
    return U

def implicit_finite_difference_solver(Ctt:float, Ctx:float, Cxx:float,
        Ct:float, Cx:float, Cu:float, Cc:float,
        min_t:float, max_t:float, T:int, min_x:float, max_x:float, X:int,
        U_t0 : list, U_t1 : list, U_min_x : list, U_max_x : list):
    """Solve a partial differential equation with the finite difference method.
    
    The partial differential equation must have two variables (called t and x).
    It must be linear with constant coefficients.
    Its shape must be : Ctt Utt + Ctx Uxt + Cxx Uxx + Cx Ux + Ct Ut + Cu U = Cc
    This function use implicit method with finite difference to solve this equation.
    
    Solving limits and accuracy:
    min_t is the minimal value for t
    max_t is the maximal value for t
    T is the number of t values
    min_x is the minimal value for x
    max_x is the maxiamal value for x
    X is the number of x values
        
    Initial conditions:
    U_t0 is the list of U values when t = min_t. len(U_t0) must be X.
    U_t1 is the list of U values when t = min_t + 1*step_t. len(U_t1) must be X.
    
    Limit conditions:
    U_min_x is the list of U values when x=min_x. len(U_min_x) must be T-2.
    U_max_x is the list of U values when x=max_x. len(U_max_x) must be T-2.

    Return a matrix where line index represent t and column index represent x. 
    """
    #define some constants
    step_t = (max_t-min_t)/(T-1)
    step_x = (max_x-min_x)/(X-1)

    Ktt = Ctt/(step_t**2)
    Ktx = Ctx/(4 * step_t *step_x)
    Kxx = Cxx/(step_x**2)
    Kt = Ct/step_t
    Kx = Cx/(2*step_x)
    
    #constants for the differential equation
    C1 = Ktx
    C2 = Ktt + 0.5*Cu
    C3 = -Ktx
    C4 = Kxx - Kx
    C5 = -2*Ktt - 2*Kxx - Kt - Cu
    C6 = Kxx + Kx
    C7 = - Ktx
    C8 = Ktt + Kt + 1.5*Cu
    C9 = Ktx

    M = np.zeros([X*T, X*T])
    for n in range(T) :
        for i in range(X) :
            if n == 0 :
                M[i, i] = 1
            elif n == 1 :
                M[X+i, X+i] = 1
            elif i == 0 :
                M[n*X, n*X] = 1
            elif i == X-1 :
                M[n*X + i, n*X + i] = 1
            if n<T-1 and n>0 and i<X-1 and i>0 :
                k = (n+1)*X+i#line index of the current equation
                M[k, (n-1)*X + i-1] = C1#constant for U(n-1, i-1) of the differential equation in (n, i)
                M[k, (n-1)*X + i] = C2#constant for U(n-1, i) of the differential equation in (n, i)
                M[k, (n-1)*X + i+1] = C3#constant for U(n-1, i+1) of the differential equation in (n, i)
                M[k, n*X + i-1] = C4#constant for U(n, i-1) of the differential equation in (n, i)
                M[k, n*X + i] = C5#constant for U(n, i) of the differential equation in (n, i)
                M[k, n*X + i+1] = C6#constant for U(n, i+1) of the differential equation in (n, i)
                M[k, (n+1)*X + i-1] = C7#constant for U(n+1, i-1) of the differential equation in (n, i)
                M[k, (n+1)*X + i] = C8#constant for U(n+1, i) of the differential equation in (n, i)
                M[k, (n+1)*X + i+1] = C9#constant for U(n+1, i+1) of the differential equation in (n, i)

    #C is the second hand matrix
    C = U_t0 + U_t1
    for n in range(2, T) : 
        C.append(U_min_x[n-2])
        C += [Cc]*(X-2)
        C.append(U_max_x[n-2])
    C = np.array(C)#trasfort C into an numpy array

    #V will contains values of U, the searched function (but V is a single column matrix)
    V = la.solve(M, C)

    #transform X matrix into U matrix where line index represent t and column index represent x. 
    #n is the line index and i the column index
    U = np.zeros([T, X])
    for n in range(T) :
        U[n] = V[n*X : (n+1)*X]
    return U

def implicit_finite_difference_solver_2(Ctt:float, Cxx:float,
        Ct:float, Cx:float, Cu:float, Cc:float,
        min_t:float, max_t:float, T:int, min_x:float, max_x:float, X:int,
        U_t0 : list, U_t1 : list, U_min_x : list, U_max_x : list):
    """Solve a partial differential equation with the finite difference method.
    
    The partial differential equation must have two variables (called t and x).
    It must be linear with constant coefficients.
    Its shape must be : Ctt Utt + Cxx Uxx + Cx Ux + Ct Ut + Cu U = Cc
    This function use implicit method with finite difference to solve this equation.
    
    Solving limits and accuracy:
    min_t is the minimal value for t
    max_t is the maximal value for t
    T is the number of t values
    min_x is the minimal value for x
    max_x is the maxiamal value for x
    X is the number of x values
        
    Initial conditions:
    U_t0 is the list of U values when t = min_t. len(U_t0) must be X.
    U_t1 is the list of U values when t = min_t + 1*step_t. len(U_t1) must be X.
    
    Limit conditions:
    U_min_x is the list of U values when x=min_x. len(U_min_x) must be T-2.
    U_max_x is the list of U values when x=max_x. len(U_max_x) must be TS-2.

    Return a matrix where line index represent t and column index represent x. 
    """
    #define some constants
    step_t = (max_t-min_t)/(T-1)
    step_x = (max_x-min_x)/(X-1)

    Ktt = Ctt/(step_t**2)
    Kxx = Cxx/(step_x**2)
    Kt = Ct/step_t
    Kx = Cx/(2*step_x)
    
    #constants for the differential equation
    C2 = Ktt + 0.5*Cu
    C4 = Kxx - Kx
    C5 = -2*Ktt - 2*Kxx - Kt - Cu
    C6 = Kxx + Kx
    C8 = Ktt + Kt + 1.5*Cu

    M = np.zeros([X*T, X*T])
    for n in range(T) :
        for i in range(X) :
            if n == 0 :
                M[i, i] = 1
            elif n == 1 :
                M[X+i, X+i] = 1
            elif i == 0 :
                M[n*X, n*X] = 1
            elif i == X-1 :
                M[n*X + i, n*X + i] = 1
            if n<T-1 and n>0 and i<X-1 and i>0 :
                k = (n+1)*X+i#line index of the current equation
                M[k, (n-1)*X + i] = C2#constant for U(n-1, i) of the differential equation in (n, i)
                M[k, n*X + i-1] = C4#constant for U(n, i-1) of the differential equation in (n, i)
                M[k, n*X + i] = C5#constant for U(n, i) of the differential equation in (n, i)
                M[k, n*X + i+1] = C6#constant for U(n, i+1) of the differential equation in (n, i)
                M[k, (n+1)*X + i] = C8#constant for U(n+1, i) of the differential equation in (n, i)

    #C is the second hand matrix
    C = U_t0 + U_t1
    for n in range(2, T) : 
        C.append(U_min_x[n-2])
        C += [Cc]*(X-2)
        C.append(U_max_x[n-2])
    C = np.array(C)#trasfort C into an numpy array

    #V will contains values of U, the searched function (but V is a single column matrix)
    V = la.solve(M, C)

    #transform X matrix into U matrix where line index represent t and column index represent x. 
    #n is the line index and i the column index
    U = np.zeros([T, X])
    for n in range(T) :
        U[n] = V[n*X : (n+1)*X]
    return U