from dataclasses import dataclass

import numpy as np

type HeartGeometry = (
    HeartPointCloud | HeartPointGrid | HeartPolyhedron | HeartTriangleMesh | HeartVoxelGrid
)


@dataclass(frozen=True)
class HeartPointCloud:
    """
    Point cloud sampled from the interior or the boundary of a heart.

    - `points`: (#points, 3) float array of positions
    """

    points: np.ndarray


@dataclass(frozen=True, kw_only=True)
class HeartPointGrid:
    """
    Point grid sampled from a parametric surface equation.

    - `x`: 2D float array of x coordinates over the (u, v) grid
    - `y`: 2D float array of y coordinates over the (u, v) grid
    - `z`: 2D float array of z coordinates over the (u, v) grid
    """

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray


@dataclass(frozen=True)
class HeartPolyhedron:
    """
    Polyhedron extruded from a parametric curve equation.

    - `faces`: (#vertices, 3) float array of vertex positions, one per face; #vertices varies
    """

    faces: tuple[np.ndarray, ...]


@dataclass(frozen=True, kw_only=True)
class HeartTriangleMesh:
    """
    Triangle mesh extracted from an implicit surface equation.

    - `vertices`: (#vertices, 3) float array of vertex positions
    - `faces`: (#faces, 3) int array of vertex indices defining triangular faces
    """

    vertices: np.ndarray
    faces: np.ndarray


@dataclass(frozen=True, kw_only=True)
class HeartVoxelGrid:
    """
    Voxel grid extracted from an implicit surface equation.

    - `filled`: 3D bool array, indicator function of the strict sublevel set (f < 0)
    - `origin`: (3,) float array, lower corner of the grid
    - `spacing`: edge length of one cubic voxel
    """

    filled: np.ndarray
    origin: np.ndarray
    spacing: float
