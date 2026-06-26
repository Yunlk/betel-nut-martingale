#!/usr/bin/env python3
"""Run all appendices and generate outputs."""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.core_recursion import E, expected_packs, parity_asymptotic
from src.monte_carlo import monte_carlo
from src.eigenvalues import print_eigenvalue_table
from src.large_deviation import compute_rate_for_grid, distribution_table, tail_probability_at_least
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

print("\nTABLE I. Expected number of packs for selected initial money values.")
print(f"{'Money':<12} {'Exact':<20} {'Asymptotic approx':<20}")
print("-" * 52)
for m in [10, 20, 30, 40, 50, 70, 100]:
    approx = parity_asymptotic(m)
    print(f"{m:<12} {E(m):<20.10f} {approx:<20.10f}")

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

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(eigvals.real, eigvals.imag, c='red', s=50, zorder=3)
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

# ===== Appendix C: Exact tail probabilities =====
print("\n=== Appendix C: Exact tail probabilities for B=50 ===")
thresholds, probabilities = compute_rate_for_grid(B=50)
print(f"Computed exact distribution tail probabilities for {len(thresholds)} thresholds.")
for threshold in [7, 8, 9]:
    print(f"P(N(50) >= {threshold}): {tail_probability_at_least(50, threshold):.6f}")
print("Distribution rows (packs, probability, tail probability):")
for row in distribution_table(50):
    print(f"{row[0]:<3} {row[1]:.8f} {row[2]:.8f}")

# ===== Appendix D: Martingale check =====
print("\n=== Appendix D: Martingale property check ===")
from src.monte_carlo import simulate_once
np.random.seed(20260625)
samples_50 = np.array([simulate_once(50) for _ in range(5000)])
result = check_martingale(samples_50)
print(f"Corrected martingale difference t-test p-value: {result['t_pvalue']:.4f}")
print(f"Corrected martingale difference Ljung-Box p-value: {result['lb_pvalue']:.4f}")
print(f"Terminal E[R_tau] for B=50:       {result['terminal_remainder']:.6f}")
print(f"P(X_tau=1) for B=50:              {result['terminal_coupon_probability']:.6f}")
print(f"Martingale stopping formula:      {result['martingale_formula']:.6f}")
print(f"Exact E[N(50)] from recursion:     {result['exact_expectation']:.6f}")
print(f"Simulated mean E[N(50)] (5k runs):  {result['simulated_mean']:.6f}")
print(f"Parity asymptotic approximation:    {result['asymptotic_approx']:.6f}")

# ===== Appendix E: Hypothetical mechanism data =====
print("\n=== Appendix E: Hypothetical behavioral mechanism data ===")
df = generate_experiment_data()
group_stats = df.groupby('Group').agg(['mean', 'std']).round(3)
print(group_stats)

fig, ax = plt.subplots(figsize=(7, 5))
groups = ['Control', 'Guarantee', 'Step pricing', 'Leaderboard']
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
means_vals, stds_vals = [], []
for g in groups:
    gdata = df[df['Group'] == g]['Packs']
    means_vals.append(gdata.mean())
    stds_vals.append(gdata.std())
bars = ax.bar(range(4), means_vals, yerr=stds_vals, capsize=5,
              tick_label=groups, color=colors, edgecolor='black')
ax.set_ylabel('Illustrative packs')
ax.set_title('Hypothetical mechanism comparison (not empirical)')
ax.grid(axis='y', alpha=0.3)
for bar, m, s in zip(bars, means_vals, stds_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f'{m:.3f}\n±{s:.3f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('figures/figure3_strategy_comparison.png', dpi=150)
plt.close()

# ===== Monte Carlo for conclusion =====
n_conclusion = int(os.environ.get('N_MC_CONCLUSION', '100000'))
print(f"\n=== Monte Carlo for B=50 (n={n_conclusion:,}) ===")
np.random.seed(20260625)
samples_conclusion = np.array([simulate_once(50) for _ in range(n_conclusion)])
mean_conclusion = np.mean(samples_conclusion)
std_conclusion = np.std(samples_conclusion)
se_conclusion = std_conclusion / np.sqrt(n_conclusion)
exact_50 = E(50)
print(f"Exact E[N(50)]:              {exact_50:.6f}")
print(f"MC mean:                     {mean_conclusion:.6f}")
print(f"MC std error:                {se_conclusion:.6f}")
print(f"Difference:                  {abs(mean_conclusion - exact_50):.6f}")
print(f"Agreement within {max(3 * se_conclusion, abs(mean_conclusion - exact_50)):.6f}")

print("\nAll outputs generated successfully.")
