# Ref. https://mathworld.wolfram.com/HeartSurface.html

import numpy as np


def evaluate_heart_implicit_function(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    Implicit: f(x, y, z) = term_1 - term_2 - term_3.

    f > 0 => outside the heart
    f = 0 => surface of the heart
    f < 0 => inside the heart
    """

    x_square = x * x
    y_square = y * y
    z_square = z * z
    z_cube = z_square * z

    term_1 = (x_square + (9 / 4) * y_square + z_square - 1) ** 3
    term_2 = x_square * z_cube
    term_3 = (9 / 80) * y_square * z_cube

    return term_1 - term_2 - term_3
