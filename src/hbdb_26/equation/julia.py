# Ref. https://community.wolfram.com/groups/-/m/t/2142619

import numpy as np


def compute_heart_curve(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Heart curve on the XZ plane: `t` -> `(x, z)`

    - `t`: float array of angular parameters in [0, 2 * pi]
    """

    x = 15 * np.sin(t) - 4 * np.sin(3 * t)
    z = 15 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    return x, z
