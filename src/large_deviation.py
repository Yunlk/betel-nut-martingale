import numpy as np
from scipy.optimize import minimize_scalar

def cumulant_generating_function(theta, p=0.3):
    """
    log MGF of single-step increment ΔN - ρΔC.
    For purchase step: ΔN=1, ΔC=10 with prob 1.
    For exchange step: ΔN=1, ΔC=2 with prob p; else ΔN=0, ΔC=0 with prob 1-p.
    But careful: the step distribution depends on state. We approximate using average.
    Here we use the simplified version for demonstration.
    """
    rho = 5/38
    # Two possible increments: (1, 10) with prob 1 (first purchase), then subsequent exchanges.
    # Simplified: treat each pack cost as random variable with mean 76/7.
    # Actually, for rate function we need the true distribution.
    # This is a placeholder – see paper for rigorous derivation.
    return np.log(0.7 * np.exp(theta*(1 - rho*10)) + 0.3 * np.exp(theta*(1 - rho*2)))

def rate_function(x):
    """I(x) = sup_θ [θx - log M(θ)]"""
    def obj(theta):
        return -(theta*x - cumulant_generating_function(theta))
    res = minimize_scalar(obj, bounds=(-10,10), method='bounded')
    return -res.fun

def compute_rate_for_grid():
    xs = np.linspace(0.1, 0.2, 50)
    rates = [rate_function(x) for x in xs]
    return xs, rates