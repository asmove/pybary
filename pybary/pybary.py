"""Main module."""
from functools import reduce
from numpy import exp, zeros
from numpy.random import normal

DEFAULT_NU = 1
DEFAULT_LAMBDA = 1
DEFAULT_SIGMA = 0.1
DEFAULT_ZETA = 0
DEFAULT_ITERANTION_COUNT = 0

def bary_batch(oracle, xs, nu = DEFAULT_NU):
    ''' 
     Batch barycenter algorithm for direct optimization
     
     In:
       - oracle     [function]   : Oracle function e.g. lambda x: numpy.norm(x)
       - xs         [list[list]] : list with coordinates
       - nu         [double]     : positive value (Caution on its value due overflow)
       - lambda     [double]     : Forgetting factor between 0 and 1
     Out:
        - xhat      [np.array]   : barycenter position
    '''
    
    n = len(xs[0])
    size_x = (n, 1)

    bexp_fun = lambda x: exp(-nu*oracle(x))

    prod_func = lambda elems: elems[0]*elems[1]
    sum_func = lambda acc, a: acc + a

    num = reduce(
        sum_func, 
        map(prod_func, zip(map(bexp_fun, xs), xs)), 
        zeros(size_x).T
    )

    den = reduce(sum_func, map(bexp_fun, xs), 0)

    return num/den

def bary_recursive(
    oracle, x0, 
    nu = DEFAULT_NU, 
    sigma = DEFAULT_SIGMA, 
    zeta = DEFAULT_ZETA, 
    lambda_ = DEFAULT_LAMBDA, 
    iterations = DEFAULT_ITERANTION_COUNT
  ):
    '''
     Recursive barycenter algorithm for direct optimization
     
     In:
       - oracle     [function]  : Oracle function e.g. lambda x: numpy.power(x, 2)
       - x0         [np.array]  : Initial query values
       - nu         [double]    : positive value (Caution on its value due overflow)
       - sigma      [double]    : Std deviation of normal distribution
       - zeta       [double]    : Proportional value for mean of normal distribution
       - lambda     [double]    : Forgetting factor between 0 and 1
       - iterations [integer]   : Maximum number of iterations
     
     Out:
        - xhat      [np.array]  : barycenter position
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
        m_1 = m
        xhat_1 = xhat
        
        i = i + 1
    
    return xhat