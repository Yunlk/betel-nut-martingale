import numpy as np

# 求解递推特征方程 r^11 - r^10 - 0.3r^9 + 0.3r^8 - 0.7r + 0.7 = 0
# 该方程可因式分解为 (r-1)^2 (r+1) (r^8 + 0.7r^6 + 0.7r^4 + 0.7r^2 + 0.7) = 0
# 其中 r=1 (二重) 给出线性项 αm+β，r=-1 给出 (-1)^m 交替项
# 八次因子给出 4 对共轭复根，按模分为两组

def compute_eigenvalues():
    """计算递推特征方程的全部 11 个根（不含 r=1 二重和 r=-1 时显示 8 个非单位复根）。"""
    # 八次因子: r^8 + 0.7r^6 + 0.7r^4 + 0.7r^2 + 0.7 = 0
    coeffs = [1.0, 0, 0.7, 0, 0.7, 0, 0.7, 0, 0.7]
    r_roots = np.roots(coeffs)  # 8 个复根

    # 加上三个单位根
    unit_roots = np.array([1.0, 1.0, -1.0])  # r=1 (double), r=-1
    all_roots = np.concatenate([unit_roots, r_roots])

    return r_roots  # 返回非单位复根（展开式中实际衰减的项）


def print_eigenvalue_table():
    r_roots = compute_eigenvalues()

    print("=" * 70)
    print("Appendix B: Recurrence characteristic roots (8 non-unit complex roots)")
    print("=" * 70)
    print(f"{'Index':<6} {'Real':<20} {'Imag':<20} {'Magnitude':<15}")
    print("-" * 70)

    # 按模降序排列
    sorted_roots = sorted(r_roots, key=lambda r: abs(r), reverse=True)
    for i, r in enumerate(sorted_roots, 1):
        mag = abs(r)
        print(f"{i:<6} {r.real:<20.15f} {r.imag:<20.15f} {mag:<15.10f}")

    print("-" * 70)
    print(f"Dominant non-unit |r| = {abs(sorted_roots[0]):.10f}  (decay half-life ≈ {np.log(0.5)/np.log(abs(sorted_roots[0])):.1f} yuan)")
    print(f"Secondary     |r| = {abs(sorted_roots[4]):.10f}  (decay half-life ≈ {np.log(0.5)/np.log(abs(sorted_roots[4])):.1f} yuan)")
    print("r = 1 (double) gives linear term  αm + β")
    print("r = -1        gives alternating  (-1)^m  (coefficient ≈ 0.067, negligible)")
    print("=" * 70)

    # 返回全 11 个根用于绘图（含单位根，使复平面图完整）
    coeffs = [1.0, 0, 0.7, 0, 0.7, 0, 0.7, 0, 0.7]
    r_roots = np.roots(coeffs)
    unit_roots = np.array([1.0, 1.0, -1.0])
    all_roots = np.concatenate([unit_roots, r_roots])
    return all_roots