import numpy as np


def generate_mt(n_samples=10000, seed=None):
    bitgen = np.random.MT19937(seed)
    rng = np.random.Generator(bitgen)
    return rng.uniform(0, 1, size=n_samples)

def generate_lcg_bad(n_samples=10000, seed=42):
    """LCG fraco baseado no RANDU, com padrões lineares."""
    a, c, m = 65539, 0, 2 ** 31
    state = seed

    seq = np.zeros(n_samples)

    for i in range(n_samples):
        state = (a * state + c) % m
        seq[i] = state / m

    return seq