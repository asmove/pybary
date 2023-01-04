[![Version](https://img.shields.io/pypi/v/pybary.svg)](https://pypi.python.org/pypi/pybary)
[![python](https://img.shields.io/pypi/pyversions/pybary.svg)](https://pypi.org/project/pybary/)
[![downloads](https://img.shields.io/pypi/dm/pybary)](https://pypi.org/project/pybary/)

Pybary
========

![A sniffer optimizer](https://github.com/asmove/pybary/blob/main/images/pybary-tiny.png?raw=true)

Barycenter method in python. Take a look at original article: https://arxiv.org/abs/1801.10533

How to install
----------------

We run the command on desired installation environment:

``` {.bash}
pip install pybary
```

Minimal example
----------------

We run command `python example.py` on the folder with file `example.py` and following content:

``` {.python}
#!/usr/bin/env python
from pybary import bary_batch, bary_recursive
from numpy import power, array
from numpy.random import normal

# Oracle function
oracle = lambda x: power(x, 2)

# Initial point
x0 = array([0, 0])

# Batch points for batch barycenter version
mu_x = 0
sigma_x = 1
size_x = [100, 2]

xs = normal(mu_x, sigma_x, size_x)

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
xhat_batch = bary_batch(
        oracle, xs, nu, sigma
    )

# Results
print(xhat_batch)
print(xhat_recursive)
```
