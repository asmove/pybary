from __future__ import annotations

import pytest
from numpy import array, zeros
from numpy.linalg import norm
from numpy.testing import assert_allclose

from pybary.pybary import bary_batch, bary_recursive


def test_bary_batch_raise(batch_inputs_raise):
    """
    Must raise on multiple input oracle function
    """

    xs = batch_inputs_raise.xs
    nu = batch_inputs_raise.nu
    fake_oracle = batch_inputs_raise.oracle

    match_str = "Oracle function must evaluate as a scalar value."

    with pytest.raises(ValueError, match=match_str):
        bary_batch(fake_oracle, xs, nu)


def test_bary_batch(batch_inputs):
    """
    Must return deterministic barycenter evaluation
    """
    xs = batch_inputs.xs
    nu = batch_inputs.nu
    oracle = batch_inputs.oracle

    result = bary_batch(oracle, xs, nu)
    expected = array([0.19557032, 0.19557032])

    assert_allclose(result, expected)


def test_bary_recur_raise(recur_inputs_raise):
    """
    Must raise on multiple input oracle function
    """

    # Hyperparameters
    fake_oracle = recur_inputs_raise.oracle
    x0 = recur_inputs_raise.x0
    nu = recur_inputs_raise.nu
    sigma = recur_inputs_raise.sigma
    zeta = recur_inputs_raise.zeta
    lambda_ = recur_inputs_raise.lambda_
    n_iters = recur_inputs_raise.iters

    match_str = "Oracle function must evaluate as a scalar value."

    with pytest.raises(ValueError, match=match_str):
        bary_recursive(fake_oracle, x0, nu, sigma, zeta, lambda_, n_iters)


def test_bary_recursive(recur_inputs):
    """
    Must return stochastic barycenter evaluation within standard deviation
    """

    # Recursive setup
    oracle = recur_inputs.oracle
    x0 = recur_inputs.x0
    nu = recur_inputs.nu
    sigma = recur_inputs.sigma
    zeta = recur_inputs.zeta
    lambda_ = recur_inputs.lambda_
    n_iters = recur_inputs.iters

    # Recursive run
    _, xhat = bary_recursive(oracle, x0, nu, sigma, zeta, lambda_, n_iters)

    n = len(x0)
    size_x = (n, 1)
    solution = zeros(size_x)

    assert norm(solution - xhat) < sigma
