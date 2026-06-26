import numpy as np
import pandas as pd


def generate_experiment_data(seed=20260625):
    """
    Generate hypothetical mechanism data for a satirical figure.
    These are not empirical human-subject results.
    """
    np.random.seed(seed)
    groups = ['Control', 'Guarantee', 'Step pricing', 'Leaderboard']
    params = {
        'Control':      {'mean_packs': 5.918, 'std_packs': 1.224, 'mean_time': 45.2, 'std_time': 12.3, 'mean_sat': 3.1, 'std_sat': 0.93},
        'Guarantee':    {'mean_packs': 6.100, 'std_packs': 1.050, 'mean_time': 42.1, 'std_time': 10.8, 'mean_sat': 4.2, 'std_sat': 0.73},
        'Step pricing': {'mean_packs': 6.000, 'std_packs': 1.150, 'mean_time': 44.6, 'std_time': 11.5, 'mean_sat': 4.0, 'std_sat': 0.81},
        'Leaderboard':  {'mean_packs': 5.950, 'std_packs': 1.300, 'mean_time': 51.3, 'std_time': 15.2, 'mean_sat': 3.8, 'std_sat': 1.01},
    }
    rows = []
    for group, par in params.items():
        for _ in range(30):
            packs = max(0.0, np.random.normal(par['mean_packs'], par['std_packs']))
            time = np.random.normal(par['mean_time'], par['std_time'])
            sat = np.clip(np.random.normal(par['mean_sat'], par['std_sat']), 1, 5)
            rows.append({'Group': group, 'Packs': packs, 'Time_s': time, 'Satisfaction': round(sat)})
    df = pd.DataFrame(rows)
    df.to_csv('data/experiment_raw.csv', index=False)
    return df
