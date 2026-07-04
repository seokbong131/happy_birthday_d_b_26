# Ref. https://community.wolfram.com/groups/-/m/t/2142619

import numpy as np


def compute_heart_coordinates(
    u: np.ndarray, v: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    u: float array of angular parameters in [0, 2 * pi] (like longitude),
    v: float array of angular parameters in [0, pi] (like latitude)
    """

    sin_v = np.sin(v)

    x = sin_v * (15 * np.sin(u) - 4 * np.sin(3 * u))
    y = 8 * np.cos(v)
    z = sin_v * (15 * np.cos(u) - 5 * np.cos(2 * u) - 2 * np.cos(3 * u) - np.cos(4 * u))

    return x, y, z
