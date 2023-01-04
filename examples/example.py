#!/usr/bin/env python
from pybary import bary_batch, bary_recursive
from numpy import power, array
from numpy.random import normal

# Oracle function
oracle = lambda x: power(x, 2)

# Initial point
x0 = array([0, 0])

# Batch points for batch barycenter version
xs = normal(0, 1, [100, 2])

# Hyperparameters
nu = 10
sigma = 0.1
zeta = 0
lambda_ = 1
iterations = 100

# Recursive run
xhat_recursive = bary_recursive(
        oracle, x0, nu, sigma, zeta, lambda_, iterations
    )

# Batch run
xhat_batch = bary_batch(oracle, xs, nu, sigma)

# Results
print(xhat_batch)
print(xhat_recursive)