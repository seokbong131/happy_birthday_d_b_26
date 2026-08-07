import numpy as np
from skimage import measure

from hbdb_26.scene.heart import HeartTriangleMesh
from hbdb_26.scene.heart_equation import HeartEquation, ImplicitSurface3D
from hbdb_26.scene.parameter import MarchingCubesParameter


def extract_isosurface(
    heart_equation: HeartEquation, marching_cubes_parameter: MarchingCubesParameter
) -> HeartTriangleMesh:
    """
    Zero set of a 3D implicit function taken as it is: `f = 0` -> `(vertices, faces)`

    - `heart_equation`: implicit function evaluated at every sample of the voxel grid
    - `marching_cubes_parameter`: grid bound, iso level, and resolution of the voxel grid
    """

    # heart equation is-a 3D implicit surface
    if not isinstance(heart_equation, ImplicitSurface3D):
        raise TypeError(
            f"Marching cubes needs a 3D implicit surface. "
            f"(equation: {type(heart_equation).__name__})"
        )

    grid_bound = marching_cubes_parameter.grid_bound
    resolution = marching_cubes_parameter.resolution

    # [start, stop] -> evenly spaced samples for each axis
    axis = np.linspace(-grid_bound, grid_bound, resolution)

    # index [i, j, k] aligned with (x, y, z); default: "xy" indexing
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    scalar_field_volume = heart_equation.evaluate(x, y, z)

    # actual distance between adjacent samples
    voxel_size = 2 * grid_bound / (resolution - 1)

    # Extract a 2D surface mesh from a 3D volume.
    vertices, faces, _, _ = measure.marching_cubes(
        volume=scalar_field_volume,
        level=marching_cubes_parameter.iso_level,
        spacing=(voxel_size, voxel_size, voxel_size),
        allow_degenerate=False,
    )

    # [0, 2 * grid_bound] -> [-grid_bound, grid_bound]
    grid_origin = np.array([axis[0], axis[0], axis[0]])
    vertices += grid_origin

    return HeartTriangleMesh(vertices=vertices, faces=faces)
