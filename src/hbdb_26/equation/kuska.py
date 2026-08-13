# Ref. https://forums.wolfram.com/mathgroup/archive/2004/Feb/msg00303.html

import numpy as np


def evaluate_heart_implicit_function(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    Heart implicit function: `(x, y, z)` -> `f`

    - `x`: float array of x coordinates
    - `y`: float array of y coordinates
    - `z`: float array of z coordinates
    """

    x_square = x * x
    y_square = y * y
    z_square = z * z

    z_cube = z_square * z

    term_1 = (x_square + 2 * y_square + z_square - 1) ** 3
    term_2 = x_square * z_cube
    term_3 = (1 / 10) * y_square * z_cube

    return term_1 - term_2 - term_3
