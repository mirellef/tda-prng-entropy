import sys
from pathlib import Path
import numpy as np
from scipy.stats import mannwhitneyu

# Adiciona a raiz do projeto ao PATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

from prng.generators import generate_mt19937, generate_lcg_bad
from embedding.delay import delay_embedding
from topology.persistence import compute_persistence_diagrams
from topology.entropy import calculate_persistent_entropy


def run_reproducible_poc(n_seqs: int = 100, n_samples: int = 10000, m: int = 3, tau: int = 1, max_points: int = 600):
    print(f"--- Executando PoC Modular ({n_seqs} amostras MT19937 vs LCG/RANDU) ---")

    mt_h0, mt_h1 = [], []
    lcg_h0, lcg_h1 = [], []

    for seed in range(n_seqs):
        # 1. Gerar e Embedding MT19937
        seq_mt = generate_mt19937(n_samples=n_samples, seed=seed)
        cloud_mt = delay_embedding(seq_mt, m=m, tau=tau, max_points=max_points, seed=seed)

        # 2. Topologia MT19937
        dgms_mt = compute_persistence_diagrams(cloud_mt, maxdim=1)
        mt_h0.append(calculate_persistent_entropy(dgms_mt[0]))
        mt_h1.append(calculate_persistent_entropy(dgms_mt[1]))

        # 3. Gerar e Embedding LCG RANDU
        seq_lcg = generate_lcg_bad(n_samples=n_samples, seed=seed + 1000)
        cloud_lcg = delay_embedding(seq_lcg, m=m, tau=tau, max_points=max_points, seed=seed)

        # 4. Topologia LCG
        dgms_lcg = compute_persistence_diagrams(cloud_lcg, maxdim=1)
        lcg_h0.append(calculate_persistent_entropy(dgms_lcg[0]))
        lcg_h1.append(calculate_persistent_entropy(dgms_lcg[1]))

    # 5. Avaliação Estatística (Mann-Whitney U)
    _, p_val_h0 = mannwhitneyu(mt_h0, lcg_h0)
    _, p_val_h1 = mannwhitneyu(mt_h1, lcg_h1)

    print("\n=== RESULTADOS DA POC MODULAR ===")
    print(f"Média H0 | MT19937: {np.mean(mt_h0):.4f} | LCG: {np.mean(lcg_h0):.4f}")
    print(f"Média H1 | MT19937: {np.mean(mt_h1):.4f} | LCG: {np.mean(lcg_h1):.4f}")
    print(f"Mann-Whitney H0 p-value: {p_val_h0:.2e}")
    print(f"Mann-Whitney H1 p-value: {p_val_h1:.2e}")

    if p_val_h0 < 0.05 or p_val_h1 < 0.05:
        print("\nSINAL DETECTADO: Separação estatística confirmada no código modular.")
    else:
        print("\nSINAL NÃO DETECTADO: Verificar parâmetros de entrada.")


if __name__ == "__main__":
    run_reproducible_poc()