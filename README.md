# Betel Nut Martingale – Optimal Stopping Strategy for Betel Nut Consumption

This repository contains the complete reproducible research package for the paper:

"Optimal Stopping Strategy for Betel Nut Consumption Based on Martingale Theory – With a Conjoint Analysis of Gambler's Fallacy and Behavioral Economics in Promotional Design"

Authors: yunlk, otto, Tengyang Tianxia, Gunmu

## Repository Structure
```
betel-nut-martingale/
├── README.md
├── requirements.txt
├── run_all.py                      # Entry point: runs all appendices and generates figures
├── src/
│   ├── core_recursion.py           # Appendix A: Recursive solution for E(m), F(m)
│   ├── monte_carlo.py              # Appendix A: Monte Carlo simulation
│   ├── eigenvalues.py              # Appendix B: Eigenvalue table (precomputed)
│   ├── large_deviation.py          # Appendix C: Large deviation rate function
│   ├── martingale_check.py         # Appendix D: Martingale property verification
│   └── experiment_simulator.py     # Appendix E: Behavioral experiment data generator
├── data/
│   └── experiment_raw.csv          # Generated after running run_all.py
└── figures/
    ├── figure1_eigenvalues.png     # Eigenvalue distribution in complex plane
    ├── figure2_expected_vs_money.png # Expected packs vs initial money
    └── figure3_strategy_comparison.png # Marketing strategy comparison
```

## Requirements

- Python 3.9+
- Dependencies listed in requirements.txt

## Reproduction Steps

### 1. Clone the repository
```
git clone https://github.com/yunlk/betel-nut-martingale.git
cd betel-nut-martingale
```

### 2. Create a virtual environment (recommended)
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the main script
```
python run_all.py
```

### 5. Check outputs

- Figures: Three PNG files in figures/ directory.
- Experimental data: CSV file data/experiment_raw.csv.
- Console output: Tables for eigenvalues (Appendix B), large deviation (Appendix C), martingale test (Appendix D), and experiment summary (Appendix E).

## Output Description

Output: figures/figure1_eigenvalues.png
Description: Distribution of the 11 eigenvalues in the complex plane

Output: figures/figure2_expected_vs_money.png
Description: Theoretical vs simulated expected packs for initial money 10–60 CNY

Output: figures/figure3_strategy_comparison.png
Description: Bar chart comparing four marketing strategies

Output: data/experiment_raw.csv
Description: Simulated behavioral experiment data (120 subjects, 4 groups)

Output: Console (stdout)
Description: Numerical tables for Appendices B–E

## Citation

If you use this code or data in your research, please cite:

yunlk, otto, Tengyang Tianxia, Gunmu. "Optimal Stopping Strategy for Betel Nut Consumption Based on Martingale Theory." S.H.*.T. Journal of Applied Irrelevance, vol.1, no.1, pp.1-20, 2026.

## License

MIT License (or specify your preferred license)
