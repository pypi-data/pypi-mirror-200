import numpy as np


def normal_distribution_pdf(
    x: float, mu: float, sigma: float, c: float, a: float
) -> float:
    return a * np.exp(-((x - mu) ** 2) / (2 * sigma**2)) - c
