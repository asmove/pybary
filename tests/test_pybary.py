from __future__ import annotations

from pybary.pybary import bary_batch, bary_recursive
from numpy import array, zeros
from numpy.testing import assert_allclose
from numpy.linalg import norm

def mean(elems): 
    return sum(array(elems)) / len(elems)

def variance(elems): 
    return sum([((x - mean(elems)) ** 2) for x in elems]) / len(elems)

def std(elems):
    return variance ** 0.5

# Oracle function
def oracle(x):
    return norm(x)

# Hyperparameters
nu = 1

def test_bary_batch():
    """
    Must return deterministic barycenter evaluation 
    """

    # Initial point
    xs_test = array([[0, 0], [1, 1]])
    
    result = bary_batch(oracle, xs_test, nu)
    expected = array([[0.19557032, 0.19557032]])
    
    assert_allclose(result, expected)

def test_bary_recursive():
    solutions = []

    # Recursive setup

    # Initial point
    x0 = array([1, 1])

    n = len(x0)
    size_x = (n, 1)

    # Hyperparameters
    nu = 5
    sigma = 0.5
    zeta = 0
    lambda_ = 1

    # Iteration cardinality
    n_iterations = 1000

    # Recursive run
    xhat_recursive = bary_recursive(
        oracle, x0, 
        nu, sigma, zeta, lambda_, 
        n_iterations
    )
    
    precision = 1e-3
    solution = zeros(size_x)
    
    assert norm(solution-xhat_recursive) < sigma