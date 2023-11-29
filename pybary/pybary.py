"""Main module."""
from __future__ import annotations

from numpy import array, average, exp, zeros
from numpy.random import normal

DEFAULT_NU = 3
DEFAULT_LAMBDA = 1
DEFAULT_SIGMA = 0.5
DEFAULT_ZETA = 0
DEFAULT_ITERATION_COUNT = 1000


def bary_batch(oracle, xs, nu=DEFAULT_NU):
    """
    Batch barycenter algorithm for direct optimization

    In:
      - oracle     [function]   : Oracle map e.g. lambda x: numpy.norm(x)
      - xs         [list[list]] : list with coordinates
      - nu         [double]     : positive value (Caution due overflow)
      - lambda     [double]     : Forgetting factor between 0 and 1
    Out:
       - xhat      [np.array]   : barycenter position
    """

    if not isinstance(oracle(xs[0]), float):
        match_str = "Oracle function must evaluate as a scalar value."
        raise ValueError(match_str)

    def bexp_fun(x):
        return exp(-nu * oracle(x))

    x_weights = [bexp_fun(x) for x in xs]
    barycenter = average(array(xs), axis=0, weights=array(x_weights))
    return barycenter


def bary_recursive(
    oracle,
    x0,
    nu=DEFAULT_NU,
    sigma=DEFAULT_SIGMA,
    zeta=DEFAULT_ZETA,
    lambda_=DEFAULT_LAMBDA,
    iterations=DEFAULT_ITERATION_COUNT,
):
    """
    Recursive barycenter algorithm for direct optimization

    In:
      - oracle     [function]  : Oracle map e.g. lambda x: numpy.norm(x, 2)
      - x0         [np.array]  : Initial query values
      - nu         [double]    : positive value (Caution due overflow)
      - sigma      [double]    : Std deviation of normal distribution
      - zeta       [double]    : scaler for mean of normal distribution
      - lambda     [double]    : Forgetting factor between 0 and 1
      - iterations [integer]   : Maximum number of iterations

    Out:
       - xhat      [np.array]  : barycenter position
    """

    if not isinstance(oracle(x0), float):
        match_str = "Oracle function must evaluate as a scalar value."
        raise ValueError(match_str)

    # Initialization
    xhat = x0
    m = 0

    solution_is_found = False

    def update(weight_total, estimate, prev_step=None):
        if prev_step is None:
            card_x = (len(estimate), 1)
            prev_step = zeros(card_x).T
        curiosity = normal(-zeta * prev_step, sigma)
        probe = estimate + curiosity
        weight = exp(-nu * oracle(probe))
        weight_total = lambda_ * weight_total + weight
        step = curiosity * weight / weight_total
        estimate = estimate + step
        return weight_total, estimate, step

    # Optimization loop
    i = 1
    step = None
    while not solution_is_found:
        m, xhat, step = update(m, xhat, step)

        solution_is_found = i >= iterations
        i = i + 1

    return m, xhat
