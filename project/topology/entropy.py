import numpy as np


def calculate_persistent_entropy(dgm: np.ndarray) -> float:
    """
    Calcula a Entropia Persistente H_pers para um diagrama de homologia H_k.

    H_pers = - sum(p_i * log(p_i)), onde p_i = l_i / L
    """
    # Filtra barras infinitas se existirem (ex: componente conexa principal em H0)
    finite_dgm = dgm[np.isfinite(dgm[:, 1])]
    if len(finite_dgm) == 0:
        return 0.0

    lengths = finite_dgm[:, 1] - finite_dgm[:, 0]
    total_length = np.sum(lengths)

    if total_length == 0:
        return 0.0

    p = lengths / total_length
    p = p[p > 0]  # Remove zeros para evitar log(0)
    return -float(np.sum(p * np.log(p)))