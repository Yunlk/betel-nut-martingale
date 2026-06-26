import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

from src.core_recursion import (
    E,
    parity_asymptotic,
    rho,
    state_potential_coupon,
    terminal_coupon_probability,
    terminal_remainder,
)


def simulate_with_steps(start_money, p=0.3, seed=None):
    """Simulate one path and record the corrected martingale after each buy."""
    if seed is not None:
        np.random.seed(seed)
    money = start_money
    x = 0  # 0=no coupon, 1=coupon
    N = 0
    C = 0
    martingale_values = [0.0]

    while True:
        price = 10 if x == 0 else 2
        if money < price:
            break
        money -= price
        N += 1
        C += price
        x = 1 if np.random.rand() < p else 0
        martingale_values.append(N - rho * C + state_potential_coupon * x)

    return np.array(martingale_values), N, C, money, x


def check_martingale(simulated_packs, rho=5/38, initial_money=50):
    """
    Diagnostics for the corrected martingale
        M_n = N_n - (5/38) C_n + (20/19) X_n.
    """
    np.random.seed(20260625)
    all_diffs = []
    for _ in range(200):
        M, *_ = simulate_with_steps(initial_money)
        all_diffs.extend(np.diff(M))

    all_diffs = np.array(all_diffs)
    t_stat, t_pval = stats.ttest_1samp(all_diffs, 0)
    lb_result = acorr_ljungbox(all_diffs[:2000], lags=[10], return_df=True)
    lb_stat = lb_result['lb_stat'].iloc[0]
    lb_pvalue = lb_result['lb_pvalue'].iloc[0]

    exact = E(initial_money)
    sim_mean = np.mean(simulated_packs)
    remainder = terminal_remainder(initial_money, 0)
    terminal_coupon = terminal_coupon_probability(initial_money, 0)
    martingale_formula = (
        rho * initial_money
        - rho * remainder
        - state_potential_coupon * terminal_coupon
    )

    return {
        't_statistic': t_stat,
        't_pvalue': t_pval,
        'lb_statistic': lb_stat,
        'lb_pvalue': lb_pvalue,
        'terminal_remainder': remainder,
        'terminal_coupon_probability': terminal_coupon,
        'martingale_formula': martingale_formula,
        'exact_expectation': exact,
        'simulated_mean': sim_mean,
        'asymptotic_approx': parity_asymptotic(initial_money),
    }
