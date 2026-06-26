import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

def check_martingale(simulated_packs, rho=5/38, initial_money=50):
    theoretical = rho * initial_money
    deviations = simulated_packs - theoretical
    # t-test
    t_stat, p_val = stats.ttest_1samp(deviations, 0)
    # Ljung-Box test
    lb_result = acorr_ljungbox(deviations, lags=[10], return_df=True)
    lb_stat = lb_result['lb_stat'].iloc[0]
    lb_pvalue = lb_result['lb_pvalue'].iloc[0]
    return {
        't_statistic': t_stat,
        't_pvalue': p_val,
        'lb_statistic': lb_stat,
        'lb_pvalue': lb_pvalue
    }