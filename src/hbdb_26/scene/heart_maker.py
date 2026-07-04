import numpy as np
from skimage import measure

from hbdb_26.equation import julia, taubin
from hbdb_26.scene.heart import HeartPointGrid, HeartTriangleMesh
from hbdb_26.util.configuration import JuliaConfig, TaubinConfig


def make_julia_heart(config: JuliaConfig = JuliaConfig()) -> HeartPointGrid:
    """
    Sample Julia's heart curve parametric equation over a (u, v) grid.

    The returned grid follows the Z-up rendering convention.
    """

    # [start, stop] -> evenly spaced samples
    u_steps = np.linspace(0, 2 * np.pi, config.u_samples)
    v_steps = np.linspace(0, np.pi, config.v_samples)

    # index [i, j] aligned with (u, v); default: "xy" indexing
    u, v = np.meshgrid(u_steps, v_steps, indexing="ij")
    x, y, z = julia.compute_heart_coordinates(u, v)

    # Rotate +90 degrees around the X-axis.
    # reference equation: Y-up / rendering convention: Z-up
    return HeartPointGrid(x=x, y=-z, z=y)


def make_taubin_heart(config: TaubinConfig = TaubinConfig()) -> HeartTriangleMesh:
    """
    Extract Taubin's heart-shaped surface sextic algebraic equation.

    assumption: uniform cubic bounding volume centered at the origin
    """

    grid_bound = config.grid_bound
    resolution = config.resolution

    # [start, stop] -> evenly spaced samples for each axis
    axis = np.linspace(-grid_bound, grid_bound, resolution)

    # index [i, j, k] aligned with (x, y, z); default: "xy" indexing
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    scalar_field_volume = taubin.evaluate_heart_implicit_function(x, y, z)

    # actual distance between adjacent samples
    voxel_size = 2 * grid_bound / (resolution - 1)

    # Extract a 2D surface mesh from a 3D volume.
    vertices, faces, _, _ = measure.marching_cubes(
        volume=scalar_field_volume,
        level=config.iso_level,
        spacing=(voxel_size, voxel_size, voxel_size),
        allow_degenerate=False,
    )

    # [0, 2 * grid_bound] -> [-grid_bound, grid_bound]
    grid_origin = np.array([axis[0], axis[0], axis[0]])
    vertices += grid_origin

    return HeartTriangleMesh(vertices=vertices, faces=faces)
