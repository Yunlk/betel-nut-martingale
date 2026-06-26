import numpy as np

# The ordinary generating-function denominator factors as
# D(z)=(1-z)^2(1+z)(1+0.7z^2+0.7z^4+0.7z^6+0.7z^8).
# Coefficient terms use inverse denominator roots r = z^{-1}; the eight
# non-unit recurrence roots satisfy r^8+0.7r^6+0.7r^4+0.7r^2+0.7=0.


def compute_eigenvalues():
    """Return the eight non-unit recurrence roots."""
    coeffs = [1.0, 0, 0.7, 0, 0.7, 0, 0.7, 0, 0.7]
    return np.roots(coeffs)


def print_eigenvalue_table():
    r_roots = compute_eigenvalues()

    print("=" * 70)
    print("Appendix B: Recurrence characteristic roots (8 non-unit complex roots)")
    print("=" * 70)
    print(f"{'Index':<6} {'Real':<20} {'Imag':<20} {'Magnitude':<15}")
    print("-" * 70)

    sorted_roots = sorted(r_roots, key=lambda r: abs(r), reverse=True)
    for i, r in enumerate(sorted_roots, 1):
        mag = abs(r)
        print(f"{i:<6} {r.real:<20.15f} {r.imag:<20.15f} {mag:<15.10f}")

    print("-" * 70)
    print(f"Dominant non-unit |r| = {abs(sorted_roots[0]):.10f}  (decay half-life approx {np.log(0.5)/np.log(abs(sorted_roots[0])):.1f} yuan)")
    print(f"Secondary     |r| = {abs(sorted_roots[4]):.10f}  (decay half-life approx {np.log(0.5)/np.log(abs(sorted_roots[4])):.1f} yuan)")
    print("r = 1 (double) gives linear term  (5/38)m - 915/1444")
    print("r = -1        gives alternating  (5/76)(-1)^m")
    print("Exact form: E(m)=5m/38-915/1444+(5/76)(-1)^m+sum_{j=1}^8 b_j r_j^m")
    print("=" * 70)

    unit_roots = np.array([1.0, 1.0, -1.0])
    return np.concatenate([unit_roots, r_roots])
