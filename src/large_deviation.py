import numpy as np
from scipy.optimize import minimize_scalar

p = 0.3
rho = 5/38


def cumulant_generating_function(theta):
    """
    一个完整"购买周期"的对数矩母函数。
    每周期：先强制买一包 (ΔN=1, ΔC=10)，
    然后以概率 p=0.3 反复换购 (ΔN=1, ΔC=2)，直至失败。
    期望包数 = 1/(1-p) = 10/7，期望花费 = 10 + 2p/(1-p) = 76/7。
    """
    purchase_term = theta * (1 - rho * 10)
    # 几何分布的换购阶段 MGF
    exchange_mgf = (1 - p) / (1 - p * np.exp(theta * (1 - rho * 2)))
    return purchase_term + np.log(exchange_mgf)


def rate_function(x):
    """
    I(x) = sup_θ [θx − Λ(θ)]
    其中 x = (超额包数) / (周期数)，即每周期超出均值的包数。
    """
    def obj(theta):
        return -(theta * x - cumulant_generating_function(theta))
    res = minimize_scalar(obj, bounds=(-5, 5), method='bounded')
    return -res.fun


def compute_rate_for_grid():
    """计算速率函数在 x ∈ [0.01, 0.03] 上的值（每周期超额包数）。"""
    xs = np.linspace(0.01, 0.03, 50)
    rates = [rate_function(x) for x in xs]
    return xs, rates


def probability_above_threshold(k, B):
    """
    估计获得超过 k·B 包的概率（大偏差估计）。
    k > ρ 时概率指数衰减，速率 ≈ B · I(k − ρ)。
    其中 B 为初始资金，周期数约 N = B / (76/7)。
    """
    avg_cost_per_cycle = 10 + 2 * p / (1 - p)  # = 76/7
    N_cycles = B / avg_cost_per_cycle
    excess_per_cycle = (k - rho) * avg_cost_per_cycle
    # I(x) 的 x 定义为每周期超额
    # 总超额 = N·x，k·B − ρ·B = B·(k−ρ) = N·x
    # x = B·(k−ρ)/N = (k−ρ)·avg_cost_per_cycle
    I_val = rate_function(excess_per_cycle) if excess_per_cycle > 0 else 0.0
    return np.exp(-N_cycles * I_val)


if __name__ == '__main__':
    xs, rates = compute_rate_for_grid()
    print(f"Rate function computed for {len(xs)} points.")
    print(f"Example: P(excess 10% packs | B=50) ≈ {probability_above_threshold(rho*1.10, 50):.4f}")
