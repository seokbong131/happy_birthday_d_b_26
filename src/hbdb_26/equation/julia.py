# Ref. https://community.wolfram.com/groups/-/m/t/2142619

import numpy as np


def compute_heart_curve(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    - `t`: float array of angular parameters in [0, 2 * pi]
    """

    x = 15 * np.sin(t) - 4 * np.sin(3 * t)
    z = 15 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    return x, z


def compute_heart_coordinates(
    u: np.ndarray, v: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    - `u`: float array of angular parameters in [0, 2 * pi] (like longitude)
    - `v`: float array of angular parameters in [0, pi] (like latitude)
    """

    curve_x, curve_z = compute_heart_curve(u)

    sin_v = np.sin(v)

    x = sin_v * curve_x
    y = 8 * np.cos(v)
    z = sin_v * curve_z

    return x, y, z
