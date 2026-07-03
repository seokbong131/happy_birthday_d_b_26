from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class HeartPointGrid:
    """
    Point grid sampled from a parametric surface equation.

    x: 2D float array of x coordinates over the (u, v) grid
    y: 2D float array of y coordinates over the (u, v) grid
    z: 2D float array of z coordinates over the (u, v) grid
    """

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray


@dataclass(frozen=True)
class HeartTriangleMesh:
    """
    Triangle mesh extracted from an implicit surface equation.

    vertices: (#vertices, 3) float array of vertex positions
    faces: (#faces, 3) int array of vertex indices defining triangular faces
    """

    vertices: np.ndarray
    faces: np.ndarray
