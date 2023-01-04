#!/usr/bin/env python
from pybary import bary_batch, bary_recursive
from numpy import power, array
from numpy.random import normal

oracle = lambda x: power(x, 2)
x0 = array([0, 0])

xhat_recursive = bary_recursive(oracle, x0, 10, 0.1, 0, 1, 100)

xs = normal(0, 1, [100, 2])

xhat_batch = bary_recursive(oracle, xs, 10, 0.1)

print(xhat_batch)
print(xhat_recursive)