import numpy as np
from src.core_recursion import p


def simulate_once(start_money):
    money = start_money
    packs = 0
    while money >= 10:
        money -= 10
        packs += 1
        while money >= 2 and np.random.rand() < p:
            money -= 2
            packs += 1
    return packs


def monte_carlo(money_values, n_sim=10000, seed=20260625):
    np.random.seed(seed)
    means, stds = [], []
    for m in money_values:
        samples = [simulate_once(m) for _ in range(n_sim)]
        means.append(np.mean(samples))
        stds.append(np.std(samples))
    return np.array(means), np.array(stds)
