import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

def simulate_with_steps(start_money, p=0.3, seed=None):
    """模拟一次，记录每一步的 (N_n, C_n)。"""
    if seed is not None:
        np.random.seed(seed)
    money = start_money
    N, C = 0, 0
    steps_N, steps_C = [], []
    while money >= 10:
        money -= 10
        N += 1
        C += 10
        steps_N.append(N)
        steps_C.append(C)
        while money >= 2 and np.random.rand() < p:
            money -= 2
            N += 1
            C += 2
            steps_N.append(N)
            steps_C.append(C)
    return np.array(steps_N), np.array(steps_C)


def check_martingale(simulated_packs, rho=5/38, initial_money=50):
    """
    鞅性质检验。
    simulated_packs: 多次独立模拟的最终包数数组。
    同时输出：
    1. 对模拟路径的步级鞅差序列检验
    2. 最终期望与理论的对比
    """
    # 步级鞅差检验：对多条路径采样
    np.random.seed(20260625)
    all_diffs = []
    for _ in range(200):  # 200 条路径足够
        steps_N, steps_C = simulate_with_steps(initial_money)
        M = steps_N - rho * steps_C
        diffs = np.diff(M, prepend=0.0)
        all_diffs.extend(diffs)

    all_diffs = np.array(all_diffs)

    # t 检验：鞅差均值为零
    t_stat, t_pval = stats.ttest_1samp(all_diffs, 0)

    # Ljung-Box 检验：鞅差序列无自相关
    lb_result = acorr_ljungbox(all_diffs[:2000], lags=[10], return_df=True)
    lb_stat = lb_result['lb_stat'].iloc[0]
    lb_pvalue = lb_result['lb_pvalue'].iloc[0]

    # 最终期望对比（包含边界修正）
    rho = 5/38
    beta = -13/133
    # 使用递推精确值
    from src.core_recursion import E
    exact = E(initial_money)
    sim_mean = np.mean(simulated_packs)

    return {
        't_statistic': t_stat,
        't_pvalue': t_pval,
        'lb_statistic': lb_stat,
        'lb_pvalue': lb_pvalue,
        'exact_expectation': exact,
        'simulated_mean': sim_mean,
        'linear_approx': rho * initial_money + beta,
    }