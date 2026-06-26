from functools import lru_cache

p = 0.3

@lru_cache(maxsize=None)
def E(m):
    """Expected packs without exchange opportunity (initial state)."""
    if m < 10:
        return 0.0
    return 1 + p * F(m-10) + (1-p) * E(m-10)

@lru_cache(maxsize=None)
def F(m):
    """Expected packs with exchange opportunity."""
    if m < 2:
        return 0.0
    return 1 + p * F(m-2) + (1-p) * E(m-2)

def expected_packs(money_list):
    return [E(m) for m in money_list]