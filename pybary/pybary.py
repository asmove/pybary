"""Main module."""
from functools import reduce
from numpy import exp, zeros
from numpy.random import normal

def bary_batch(oracle, xs, nu = 1, lambda_ = 1):
    ''' 
     Batch barycenter algorithm for direct optimization
     
     In:
       - oracle     [function]   : Oracle function e.g. lambda x: numpy.power(x, 2)
       - xs         [list[list]] : list with coordinates
       - nu         [double]     : positive value (Caution on its value due overflow)
       - lambda     [double]     : Forgetting factor between 0 and 1
     Out:
        - x [list]: Optimum position
    '''
    
    numerator_fun = lambda lr_result, x: lambda_*lr_result + x*exp(-nu*oracle(x))
    denominator_fun = lambda lr_result, curr_x: lambda_*lr_result + exp(-nu*oracle(curr_x))

    numerator = reduce(numerator_fun, xs)
    denominator = reduce(denominator_fun, xs)
    
    return numerator/denominator

def bary_recursive(oracle, x0, nu = 1, sigma = 0.1, zeta = 0, lambda_ = 1, iterations = 1000):
    '''
     Recursive barycenter algorithm for direct optimization
     
     In:
       - oracle     [function]  : Oracle function e.g. lambda x: numpy.power(x, 2)
       - x0         [np.array]  : Initial query values
       - nu         [double]    : positive value (Caution on its value due overflow)
       - sigma      [double]    : Std deviation of normal distribution
       - zeta       [double]    : Proportional value for mean of normal distribution
       - lambda     [double]    : Forgetting factor between 0 and 1
       - iterations [int]       : Maximum number of iterations
     
     Out:
        - x [np.array]: Optimum position
    '''
    
    # Initialization
    xhat_1 = x0
    m_1 = 0

    deltax_1 = zeros((len(x0), 1))
    solution_is_found = False
    
    # Optimization loop
    i = 1
    while(not solution_is_found):    
        z = normal(zeta*deltax_1, sigma).T
        
        x = xhat_1 + z
        e_i = exp(-nu*oracle(x))
        m = lambda_*m_1 + e_i
        xhat = (1/m)*(lambda_*m_1*xhat_1 + x*e_i)
        
        solution_is_found = i >= iterations
        
        # Update previous variables
        m_1=m
        xhat_1=xhat
        
        i = i + 1
    
    return xhat