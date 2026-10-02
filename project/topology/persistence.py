import numpy as np
from ripser import ripser


def compute_persistence_diagrams(cloud: np.ndarray, maxdim: int = 1) -> list[np.ndarray]:
    """
    Executa a filtração de Vietoris-Rips sobre a nuvem de pontos.

    Retorna uma lista de diagramas de persistência [dgm_H0, dgm_H1, ...].
    Cada diagrama é uma matriz (N, 2) com pares (birth, death).
    """
    result = ripser(cloud, maxdim=maxdim)
    return result['dgms']