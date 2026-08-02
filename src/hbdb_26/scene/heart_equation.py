from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from hbdb_26.equation import julia, taubin

type HeartEquation = ParametricCurve2D | ImplicitSurface3D


@dataclass(frozen=True)
class ParametricCurve2D:
    """
    `t` in [0, 2 * pi] -> `(x, z)` (a closed curve on the XZ plane)
    """

    formula: Callable[[np.ndarray], tuple[np.ndarray, np.ndarray]]


@dataclass(frozen=True)
class ImplicitSurface3D:
    """
    `(x, y, z)` -> `f` (f = 0 => surface, f < 0 => inside)
    """

    formula: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]


JULIA_CURVE = ParametricCurve2D(julia.compute_heart_curve)
TAUBIN_SURFACE = ImplicitSurface3D(taubin.evaluate_heart_implicit_function)
