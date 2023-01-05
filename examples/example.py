#!/usr/bin/env python
from pybary import bary_batch, bary_recursive
from numpy import array
from numpy.random import normal
from numpy.linalg import norm

# Oracle function
def oracle(x):
    return norm(x)

# Initial point
x0 = array([0, 0])

# Batch points for batch barycenter version
mu_x = 0
sigma_x = 1
size_x = [1000, 2]

xs = normal(mu_x, sigma_x, size_x)

# Hyperparameters
nu = 1
sigma = 0.1
zeta = 0
lambda_ = 1
iterations = 1000

# Recursive run
xhat_recursive = bary_recursive(oracle, x0, nu, sigma, zeta, lambda_, iterations)

# Batch run
xhat_batch = bary_batch(oracle, xs, nu)

# Results
print('Batch result     : '+str(xhat_batch))
print('Recursive result : '+str(xhat_recursive))