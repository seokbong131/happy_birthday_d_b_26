import numpy as np

from hbdb_26.scene.heart import HeartVoxelGrid
from hbdb_26.scene.heart_equation import HeartEquation, ImplicitSurface3D
from hbdb_26.scene.parameter import VoxelizationParameter


def extract_sublevel_set(
    heart_equation: HeartEquation, voxelization_parameter: VoxelizationParameter
) -> HeartVoxelGrid:
    """
    Strict sublevel set of a 3D implicit function: `f < 0` -> `(filled, origin, spacing)`

    - `heart_equation`: implicit function evaluated at every voxel center
    - `voxelization_parameter`: grid bound and resolution of the voxel grid
    """

    # heart equation is-a 3D implicit surface
    if not isinstance(heart_equation, ImplicitSurface3D):
        raise TypeError(
            f"Voxelization needs a 3D implicit surface. (equation: {type(heart_equation).__name__})"
        )

    grid_bound = voxelization_parameter.grid_bound
    resolution = voxelization_parameter.resolution

    origin = np.array([-grid_bound, -grid_bound, -grid_bound])

    # distance between adjacent voxel centers, the edge length of one voxel
    spacing = 2 * grid_bound / resolution

    # half a voxel inside [-grid_bound, grid_bound] (exactly mirrored about 0)
    voxel_center = (np.arange(resolution) - (resolution - 1) / 2) * spacing

    # index [i, j, k] aligned with (x, y, z); default: "xy" indexing
    x, y, z = np.meshgrid(voxel_center, voxel_center, voxel_center, indexing="ij")

    # indicator function of the strict sublevel set
    filled = heart_equation.evaluate(x, y, z) < 0

    return HeartVoxelGrid(filled=filled, origin=origin, spacing=spacing)
