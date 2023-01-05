#!/usr/bin/env python
from __future__ import annotations

from numpy import array
from numpy.linalg import norm
from numpy.random import normal

from pybary import bary_batch, bary_recursive


# Oracle function
def oracle(x):
    return norm(x)


# Initial point
x0 = array([1, 1])

# Batch points for batch barycenter version
mu_x = 0
sigma_x = 1
size_x = [1000, 2]

xs = normal(mu_x, sigma_x, size_x)

# Hyperparameters
nu = 5
sigma = 0.5
zeta = 0
lambda_ = 1
iterations = 1000

# Recursive run
xhat_recursive = bary_recursive(oracle, x0, nu, sigma, zeta, lambda_, iterations)

# Batch run
xhat_batch = bary_batch(oracle, xs, nu)

# Results
print("Batch result     : " + str(xhat_batch))
print("Recursive result : " + str(xhat_recursive))
