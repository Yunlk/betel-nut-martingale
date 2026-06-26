import numpy as np

from src.core_recursion import exact_distribution


def tail_probability_at_least(B, threshold):
    """Exact P(N(B) >= threshold) from the recursive distribution."""
    dist = exact_distribution(B)
    return sum(prob for packs, prob in dist.items() if packs >= threshold)


def probability_above_threshold(k, B):
    """Exact P(N(B) > k*B)."""
    threshold = int(np.floor(k * B)) + 1
    return tail_probability_at_least(B, threshold)


def compute_rate_for_grid(B=50):
    """
    Backward-compatible name used by run_all.py.
    Returns integer thresholds and exact tail probabilities, not a Cramer
    large-deviation approximation.
    """
    dist = exact_distribution(B)
    thresholds = np.array(sorted(dist.keys()))
    probabilities = np.array([tail_probability_at_least(B, t) for t in thresholds])
    return thresholds, probabilities


def distribution_table(B=50):
    """Exact distribution rows: packs, probability, tail probability."""
    dist = exact_distribution(B)
    return [(n, dist[n], tail_probability_at_least(B, n)) for n in sorted(dist)]


if __name__ == '__main__':
    for row in distribution_table(50):
        print(row)
