import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from prng.generators import (
    generate_mt,
    generate_lcg_bad
)

from embedding.delay import delay_embedding

from analysis.visualization import (
    plot_embedding_2d,
    plot_point_cloud_3d
)


def main():

    N_SAMPLES = 10000
    SEED = 42

    print("Gerando Mersenne Twister...")
    seq_mt = generate_mt(
        n_samples=N_SAMPLES,
        seed=SEED
    )

    print("Gerando LCG...")
    seq_lcg = generate_lcg_bad(
        n_samples=N_SAMPLES,
        seed=SEED
    )

    # --------------------------------------------------
    # 1. Visualização 2D
    # --------------------------------------------------

    plot_embedding_2d(
        seq_mt,
        "Mersenne Twister — x(t) × x(t+1)"
    )

    plot_embedding_2d(
        seq_lcg,
        "LCG — x(t) × x(t+1)"
    )

    # --------------------------------------------------
    # 2. Delay Embedding
    # --------------------------------------------------

    cloud_mt = delay_embedding(
        seq_mt,
        m=3,
        tau=1,
        max_points=600,
        seed=SEED
    )

    cloud_lcg = delay_embedding(
        seq_lcg,
        m=3,
        tau=1,
        max_points=600,
        seed=SEED
    )

    print(f"MT cloud shape: {cloud_mt.shape}")
    print(f"LCG cloud shape: {cloud_lcg.shape}")

    # --------------------------------------------------
    # 3. Visualização 3D
    # --------------------------------------------------

    plot_point_cloud_3d(
        cloud_mt,
        "Mersenne Twister — Delay Embedding"
    )

    plot_point_cloud_3d(
        cloud_lcg,
        "LCG — Delay Embedding"
    )


if __name__ == "__main__":
    main()