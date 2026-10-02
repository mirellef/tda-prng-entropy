import numpy as np


def delay_embedding(series, m=3, tau=1, max_points=600, seed=42):
    """
    Constrói uma nuvem de pontos usando delay embedding.

    Cada ponto tem a forma:

        (x_t, x_{t+tau}, ..., x_{t+(m-1)tau})
    """

    n = len(series)
    max_idx = n - (m - 1) * tau

    sub_vectors = [
        series[i:i + max_idx:tau]
        for i in range(m)
    ]

    cloud = np.column_stack(sub_vectors)

    # Subamostragem para reduzir custo computacional
    if len(cloud) > max_points:
        rng = np.random.default_rng(seed)

        indices = rng.choice(
            len(cloud),
            size=max_points,
            replace=False
        )

        cloud = cloud[indices]

    return cloud