# A fifth heart curve
# Ref. https://mathworld.wolfram.com/HeartCurve.html

import numpy as np


def compute_heart_curve(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Heart curve on the XZ plane: `t` -> `(x, z)`

    - `t`: float array of angular parameters in [0, 2 * pi]
    """

    x = 16 * np.sin(t) ** 3
    z = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    return x, z
