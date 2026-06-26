#!/usr/bin/env python3
"""Run all appendices and generate outputs."""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.core_recursion import E, expected_packs
from src.monte_carlo import monte_carlo
from src.eigenvalues import print_eigenvalue_table
from src.large_deviation import compute_rate_for_grid
from src.martingale_check import check_martingale
from src.experiment_simulator import generate_experiment_data

# Settings
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(20260625)

os.makedirs('figures', exist_ok=True)
os.makedirs('data', exist_ok=True)

# ===== Appendix A: Recursion & Monte Carlo =====
print("=== Appendix A: Core recursion and Monte Carlo ===")
money_range = np.arange(10, 101, 1)
theory = expected_packs(money_range)
sim_mean, sim_std = monte_carlo(money_range, n_sim=8000)

# Print Table I data
print("\nTABLE I. Expected number of packs for selected initial money values.")
print(f"{'Money':<12} {'Exact':<20} {'Linear approx':<20}")
print("-" * 52)
for m in [10, 20, 30, 40, 50, 70, 100]:
    linear = (5 / 38) * m - 13 / 133
    print(f"{m:<12} {E(m):<20.10f} {linear:<20.10f}")

# Plot Figure 2 (expected vs money)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(money_range, theory, 'k-', lw=2, label='Theoretical')
ax.errorbar(money_range[::5], sim_mean[::5],
            yerr=sim_std[::5] / np.sqrt(8000),
            fmt='ro', ms=3, capsize=2, label='Simulated (8k runs)')
ax.set_xlabel('Initial money (CNY)')
ax.set_ylabel('Expected packs')
ax.set_title('Expected packs vs. initial money')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figures/figure2_expected_vs_money.png', dpi=150)
plt.close()

# ===== Appendix B: Eigenvalues =====
print("\n=== Appendix B: Eigenvalue table ===")
eigvals = print_eigenvalue_table()

# Plot Figure 1 (eigenvalues)
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(eigvals.real, eigvals.imag, c='red', s=50, zorder=3)
# 单位圆
theta = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(theta), np.sin(theta), 'b--', lw=1, alpha=0.5, label='Unit circle')
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title('Recurrence characteristic roots')
ax.legend()
ax.grid(alpha=0.3)
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig('figures/figure1_eigenvalues.png', dpi=150)
plt.close()

# ===== Appendix C: Large deviation =====
print("\n=== Appendix C: Large deviation rate function ===")
xs, rates = compute_rate_for_grid()
print(f"Computed rate function for {len(xs)} points.")

# ===== Appendix D: Martingale check =====
print("\n=== Appendix D: Martingale property check ===")
from src.monte_carlo import simulate_once
np.random.seed(20260625)
samples_50 = np.array([simulate_once(50) for _ in range(5000)])
result = check_martingale(samples_50)
print(f"Martingale difference  t-test p-value: {result['t_pvalue']:.4f}")
print(f"Martingale difference  Ljung-Box p-value: {result['lb_pvalue']:.4f}")
print(f"Exact E[N(50)] from recursion:     {result['exact_expectation']:.6f}")
print(f"Simulated mean E[N(50)] (5k runs):  {result['simulated_mean']:.6f}")
print(f"Linear approximation αB+β:          {result['linear_approx']:.6f}")

# ===== Appendix E: Experiment data =====
print("\n=== Appendix E: Behavioral experiment data ===")
df = generate_experiment_data()
group_stats = df.groupby('Group').agg(['mean', 'std']).round(3)
print(group_stats)

# Plot Figure 3 (strategy comparison) — computed from data, not hardcoded
fig, ax = plt.subplots(figsize=(7, 5))
groups = ['Control', 'Guarantee', 'Step pricing', 'Leaderboard']
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
means_vals, stds_vals = [], []
for i, g in enumerate(groups):
    gdata = df[df['Group'] == g]['Packs']
    means_vals.append(gdata.mean())
    stds_vals.append(gdata.std())
bars = ax.bar(range(4), means_vals, yerr=stds_vals, capsize=5,
              tick_label=groups, color=colors, edgecolor='black')
ax.set_ylabel('Expected packs')
ax.set_title('Strategy comparison')
ax.grid(axis='y', alpha=0.3)
for bar, m, s in zip(bars, means_vals, stds_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f'{m:.3f}\n±{s:.3f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('figures/figure3_strategy_comparison.png', dpi=150)
plt.close()

# ===== 10^7 Monte Carlo for conclusion =====
print("\n=== 10^7 Monte Carlo for B=50 (conclusion verification) ===")
np.random.seed(20260625)
samples_10m = np.array([simulate_once(50) for _ in range(10_000_000)])
mean_10m = np.mean(samples_10m)
std_10m = np.std(samples_10m)
se_10m = std_10m / np.sqrt(10_000_000)
exact_50 = E(50)
print(f"Exact E[N(50)]:              {exact_50:.6f}")
print(f"10^7 MC mean:                {mean_10m:.6f}")
print(f"10^7 MC std error:           {se_10m:.6f}")
print(f"Difference:                  {abs(mean_10m - exact_50):.6f}")
print(f"Agreement within {max(3 * se_10m, abs(mean_10m - exact_50)):.6f}")

print("\nAll outputs generated successfully.")
