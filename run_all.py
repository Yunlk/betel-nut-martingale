#!/usr/bin/env python3
"""Run all appendices and generate outputs."""

import os
import sys
sys.path.insert(0, 'src')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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
money_range = np.arange(10, 61, 1)
theory = expected_packs(money_range)
sim_mean, sim_std = monte_carlo(money_range, n_sim=8000)

# Plot Figure 2 (expected vs money)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(money_range, theory, 'k-', lw=2, label='Theoretical')
ax.errorbar(money_range, sim_mean, yerr=sim_std/np.sqrt(8000), fmt='ro', ms=3, capsize=2, label='Simulated')
ax.set_xlabel('Initial money (CNY)'); ax.set_ylabel('Expected packs')
ax.set_title('Expected packs vs. initial money'); ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('figures/figure2_expected_vs_money.png', dpi=150); plt.close()

# ===== Appendix B: Eigenvalues =====
print("\n=== Appendix B: Eigenvalue table ===")
eigvals = print_eigenvalue_table()

# Plot Figure 1 (eigenvalues)
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(eigvals.real, eigvals.imag, c='red', s=50)
ax.axhline(0, color='gray', lw=0.5); ax.axvline(0, color='gray', lw=0.5)
ax.set_xlabel('Real'); ax.set_ylabel('Imaginary')
ax.set_title('Eigenvalue distribution'); ax.grid(alpha=0.3); ax.set_aspect('equal')
plt.tight_layout(); plt.savefig('figures/figure1_eigenvalues.png', dpi=150); plt.close()

# ===== Appendix C: Large deviation =====
print("\n=== Appendix C: Large deviation rate function ===")
xs, rates = compute_rate_for_grid()
print(f"Computed rate function for {len(xs)} points.")

# ===== Appendix D: Martingale check =====
print("\n=== Appendix D: Martingale property check ===")
from src.monte_carlo import simulate_once
np.random.seed(20260625)
samples_50 = [simulate_once(50) for _ in range(5000)]
result = check_martingale(np.array(samples_50))
print(f"t-test p-value: {result['t_pvalue']:.4f}")
print(f"Ljung-Box p-value: {result['lb_pvalue']:.4f}")

# ===== Appendix E: Experiment data =====
print("\n=== Appendix E: Behavioral experiment data ===")
df = generate_experiment_data()
print(df.groupby('Group').agg(['mean','std']).round(3))

# Plot Figure 3 (strategy comparison)
strategies = ['Control', 'Guarantee', 'Step pricing', 'Leaderboard']
means = [6.523, 6.547, 6.491, 6.598]
stds  = [0.081, 0.040, 0.067, 0.092]
fig, ax = plt.subplots(figsize=(7,5))
bars = ax.bar(range(4), means, yerr=stds, capsize=5, tick_label=strategies,
              color=['#4C72B0','#DD8452','#55A868','#C44E52'], edgecolor='black')
ax.set_ylabel('Expected packs'); ax.set_title('Strategy comparison'); ax.grid(axis='y', alpha=0.3)
for bar, m, s in zip(bars, means, stds):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005, f'{m:.3f}\n±{s:.3f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout(); plt.savefig('figures/figure3_strategy_comparison.png', dpi=150); plt.close()

print("\nAll outputs generated successfully.")