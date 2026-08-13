# A seventh heart curve
# Ref. https://mathworld.wolfram.com/HeartCurve.html

import numpy as np


def compute_heart_curve(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Heart curve on the XZ plane: `t` -> `(x, z)`

    - `t`: float array of angular parameters in [0, 2 * pi]
    """

    cos_t = np.cos(t)

    x = -np.sqrt(2) * np.sin(t) ** 3
    z = 2 * cos_t - cos_t**2 - cos_t**3

    return x, z
