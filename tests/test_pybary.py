from __future__ import annotations

from pybary.pybary import bary_batch, bary_recursive
from numpy import array
from numpy.testing import assert_allclose
from numpy.linalg import norm


def test_bary_batch():
    """
    Must return deterministic barycenter evaluation 
    """

    # Oracle function
    oracle = lambda x: norm(x)

    # Initial point
    xs_test = array([[0, 0], [1, 1]])

    # Hyperparameters
    nu = 1
    
    result = bary_batch(oracle, xs_test, nu)
    expected = array([[0.19557032, 0.19557032]])
    
    print(result)
    print(expected)

    assert_allclose(result, expected)


