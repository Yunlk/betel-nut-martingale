from functools import lru_cache
from collections import defaultdict

p = 0.3
q = 1 - p

# Linear and parity-aware asymptotic constants from the ordinary generating
# function. The non-unit complex roots contribute the remaining decaying term.
rho = 5 / 38
beta = -915 / 1444
alternating_coeff = 5 / 76
state_potential_coupon = 20 / 19


@lru_cache(maxsize=None)
def E(m):
    """Expected packs without exchange opportunity (initial state)."""
    if m < 10:
        return 0.0
    return 1 + p * F(m - 10) + q * E(m - 10)


@lru_cache(maxsize=None)
def F(m):
    """Expected packs with exchange opportunity."""
    if m < 2:
        return 0.0
    return 1 + p * F(m - 2) + q * E(m - 2)


def expected_packs(money_list):
    return [E(m) for m in money_list]


def parity_asymptotic(m):
    """Asymptotic approximation retaining the non-decaying (-1)^m term."""
    return rho * m + beta + alternating_coeff * ((-1) ** m)


@lru_cache(maxsize=None)
def terminal_remainder(m, f):
    """Expected terminal leftover money under the greedy policy."""
    if f == 0:
        if m < 10:
            return float(m)
        return p * terminal_remainder(m - 10, 1) + q * terminal_remainder(m - 10, 0)
    if m < 2:
        return float(m)
    return p * terminal_remainder(m - 2, 1) + q * terminal_remainder(m - 2, 0)


@lru_cache(maxsize=None)
def terminal_coupon_probability(m, f):
    """Probability that the process stops with an unusable exchange opportunity."""
    if f == 0:
        if m < 10:
            return 0.0
        return p * terminal_coupon_probability(m - 10, 1) + q * terminal_coupon_probability(m - 10, 0)
    if m < 2:
        return 1.0
    return p * terminal_coupon_probability(m - 2, 1) + q * terminal_coupon_probability(m - 2, 0)


def corrected_martingale_expectation(m):
    """
    Exact expectation from the corrected martingale stopping identity:

        E[N(B)] = rho*B - rho*E[R_tau] - h(1)*P(X_tau=1).
    """
    return (
        rho * m
        - rho * terminal_remainder(m, 0)
        - state_potential_coupon * terminal_coupon_probability(m, 0)
    )


@lru_cache(maxsize=None)
def _distribution(m, f):
    """Cached exact distribution as tuple pairs (packs, probability)."""
    if f == 0:
        if m < 10:
            return ((0, 1.0),)
        branches = [
            (p, _distribution(m - 10, 1)),
            (q, _distribution(m - 10, 0)),
        ]
    else:
        if m < 2:
            return ((0, 1.0),)
        branches = [
            (p, _distribution(m - 2, 1)),
            (q, _distribution(m - 2, 0)),
        ]

    out = defaultdict(float)
    for weight, dist in branches:
        for packs, prob in dist:
            out[packs + 1] += weight * prob
    return tuple(sorted(out.items()))


def exact_distribution(start_money):
    """Exact distribution of total packs from the initial no-coupon state."""
    return dict(_distribution(start_money, 0))
