Pybary
========

[![Version](https://img.shields.io/pypi/v/pybary.svg)](https://pypi.python.org/pypi/pybary)
[![python](https://img.shields.io/pypi/pyversions/pybary.svg)](https://pypi.org/project/pybary/)
[![downloads](https://img.shields.io/pypi/dm/pybary)](https://pypi.org/project/pybary/)

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

oracle = lambda x: power(x, 2)
x0 = array([0, 0])

xhat_recursive = bary_recursive(oracle, x0, 10, 0.1, 0, 1, 100)

xs = normal(0, 1, [100, 2])

xhat_batch = bary_recursive(oracle, xs, 10, 0.1)

print(xhat_batch)
print(xhat_recursive)
```
