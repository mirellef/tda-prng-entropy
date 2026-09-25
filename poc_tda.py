import numpy as np
from scipy.stats import mannwhitneyu
from ripser import ripser


# ---------------------------------------------------------
# 1. Módulo de Geração e Embedding
# ---------------------------------------------------------
def generate_mt(n_samples=10000, seed=None):
    """Mersenne Twister (PRNG Referência)."""
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 1, size=n_samples)


def generate_lcg_bad(n_samples=10000, seed=42):
    """LCG Fraco (RANDU - Padrões Lineares em 3D)."""
    a, c, m = 65539, 0, 2 ** 31
    state = seed
    seq = np.zeros(n_samples)
    for i in range(n_samples):
        state = (a * state + c) % m
        seq[i] = state / m
    return seq


def delay_embedding(series, m=3, tau=1, max_points=600, seed=42):
    """Delay Embedding com subamostragem para eficiência computacional."""
    n = len(series)
    max_idx = n - (m - 1) * tau
    sub_vectors = [series[i: i + max_idx: tau] for i in range(m)]
    cloud = np.column_stack(sub_vectors)

    # Subamostragem aleatória para acelerar o Vietoris-Rips
    if len(cloud) > max_points:
        rng = np.random.default_rng(seed)
        indices = rng.choice(len(cloud), size=max_points, replace=False)
        cloud = cloud[indices]
    return cloud


# ---------------------------------------------------------
# 2. Módulo Topológico (Persistência e Entropia)
# ---------------------------------------------------------
def persistent_entropy(dgm):
    """Calcula a Entropia Persistente de um diagrama de homologia."""
    # Remover pontos com morte infinita se existirem
    finite_dgm = dgm[np.isfinite(dgm[:, 1])]
    if len(finite_dgm) == 0:
        return 0.0

    lengths = finite_dgm[:, 1] - finite_dgm[:, 0]
    total_length = np.sum(lengths)

    if total_length == 0:
        return 0.0

    p = lengths / total_length
    # Evitar log(0)
    p = p[p > 0]
    return -np.sum(p * np.log(p))


def run_tda_pipeline(cloud):
    """Executa Vietoris-Rips e extrai entropia para H0 e H1."""
    res = ripser(cloud, maxdim=1)
    dgms = res['dgms']

    e_h0 = persistent_entropy(dgms[0])
    e_h1 = persistent_entropy(dgms[1]) if len(dgms) > 1 else 0.0
    return e_h0, e_h1


# ---------------------------------------------------------
# 3. Execução da Prova de Conceito (100 sequências por grupo)
# ---------------------------------------------------------
if __name__ == "__main__":
    N_SEQS = 100
    N_SAMPLES = 10000
    EMBED_M, EMBED_TAU = 3, 1

    print(f"--- A iniciar PoC: {N_SEQS} sequências MT vs {N_SEQS} LCG ruim ---")

    mt_h0, mt_h1 = [], []
    lcg_h0, lcg_h1 = [], []

    for i in range(N_SEQS):
        # Mersenne Twister
        seq_mt = generate_mt(n_samples=N_SAMPLES, seed=i)
        cloud_mt = delay_embedding(seq_mt, m=EMBED_M, tau=EMBED_TAU, seed=i)
        h0, h1 = run_tda_pipeline(cloud_mt)
        mt_h0.append(h0)
        mt_h1.append(h1)

        # LCG Ruim
        seq_lcg = generate_lcg_bad(n_samples=N_SAMPLES, seed=i + 1)
        cloud_lcg = delay_embedding(seq_lcg, m=EMBED_M, tau=EMBED_TAU, seed=i)
        h0, h1 = run_tda_pipeline(cloud_lcg)
        lcg_h0.append(h0)
        lcg_h1.append(h1)

    # ---------------------------------------------------------
    # 4. Análise Estatística (Mann-Whitney U)
    # ---------------------------------------------------------
    stat_h0, p_val_h0 = mannwhitneyu(mt_h0, lcg_h0)
    stat_h1, p_val_h1 = mannwhitneyu(mt_h1, lcg_h1)

    print("\n=== RESULTADOS DA POC ===")
    print(f"Média Entropia H0 -> MT: {np.mean(mt_h0):.4f} | LCG: {np.mean(lcg_h0):.4f}")
    print(f"Média Entropia H1 -> MT: {np.mean(mt_h1):.4f} | LCG: {np.mean(lcg_h1):.4f}")
    print(f"Mann-Whitney H0 p-value: {p_val_h0:.2e}")
    print(f"Mann-Whitney H1 p-value: {p_val_h1:.2e}")

    if p_val_h0 < 0.05 or p_val_h1 < 0.05:
        print("\n SINAL DETETADO: Existe separação estatística significativa entre os geradores!")
    else:
        print("\n SINAL NÃO DETETADO: Ajustar parâmetros de embedding (m, tau) ou número de pontos.")