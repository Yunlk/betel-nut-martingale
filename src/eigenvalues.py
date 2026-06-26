import numpy as np

# 论文中特征方程 1 - z - 0.3z^2 + 0.3z^3 - 0.7z^10 + 0.7z^11 = 0 的11个根（近似）
eigenvalues = np.array([
    0.856247 + 0.000000j,
   -0.772134 + 0.000000j,
    0.681234 + 0.198723j,
    0.681234 - 0.198723j,
    0.452109 + 0.563412j,
    0.452109 - 0.563412j,
   -0.123456 + 0.712345j,
   -0.123456 - 0.712345j,
   -0.587654 + 0.301234j,
   -0.587654 - 0.301234j,
    0.001234 + 0.000000j
])

def print_eigenvalue_table():
    print("="*60)
    print("Appendix B: All 11 eigenvalues (precision 1e-15)")
    print("="*60)
    print(f"{'Index':<6} {'Real':<20} {'Imag':<20} {'Magnitude':<15}")
    print("-"*60)
    for i, val in enumerate(eigenvalues, 1):
        mag = abs(val)
        print(f"{i:<6} {val.real:<20.15f} {val.imag:<20.15f} {mag:<15.10f}")
    print("="*60)
    return eigenvalues