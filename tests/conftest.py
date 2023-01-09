from collections import namedtuple

import pytest
from numpy import array
from numpy.linalg import norm

BatchInputs = namedtuple("baryBatchInputs", ["oracle", "xs", "nu"])

RecurInputs = namedtuple(
    "baryRecurInputs", ["oracle", "x0", "nu", "sigma", "zeta", "lambda_", "n_iters"]
)


# Oracle function
def oracle(x):
    return norm(x)


# Oracle function
def fake_oracle(x):
    return [norm(x), norm(x)]


# Recursive bary hyperparameters
def recursive_hyperparameters():
    # Hyperparameters
    nu, sigma, zeta, lambda_ = 5, 0.5, 0, 1

    return nu, sigma, zeta, lambda_


# Recursive bary hyperparameters
def batch_hyperparameters():
    # Hyperparameters
    nu = 1

    return nu


@pytest.fixture
def recur_inputs():
    # Initial point
    x0 = array([1, 1])

    # Hyperparameters
    nu, sigma, zeta, lambda_ = recursive_hyperparameters()

    # Iteration cardinality
    n_iters = 1000

    return RecurInputs(oracle, x0, nu, sigma, zeta, lambda_, n_iters)


@pytest.fixture
def recur_inputs_raise():
    # Initial point
    x0 = array([1, 1])

    # Hyperparameters
    nu, sigma, zeta, lambda_ = recursive_hyperparameters()

    # Iteration cardinality
    n_iters = 1000

    return RecurInputs(fake_oracle, x0, nu, sigma, zeta, lambda_, n_iters)


@pytest.fixture
def batch_inputs():
    # Test points
    xs = array([[0, 0], [1, 1]])

    nu = batch_hyperparameters()

    return BatchInputs(oracle, xs, nu)


@pytest.fixture
def batch_inputs_raise():
    # Test points
    xs = array([[0, 0], [1, 1]])

    nu = batch_hyperparameters()

    return BatchInputs(fake_oracle, xs, nu)
