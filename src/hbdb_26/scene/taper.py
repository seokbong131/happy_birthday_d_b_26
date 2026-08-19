# Ref. https://en.wikipedia.org/wiki/Cubic_Hermite_spline
# Ref. https://en.wikipedia.org/wiki/Tapering_(mathematics)

import numpy as np

from hbdb_26.scene.heart import HeartPointGrid
from hbdb_26.scene.parameter import Teardrop


def taper_depth(heart_point_grid: HeartPointGrid, teardrop: Teardrop) -> HeartPointGrid:
    """
    Spherical product tapered into a teardrop: `(x, y, z)` -> `(x, y * depth_scale, z)`

    - `heart_point_grid`: spherical product rescaled along the Y-axis at every height
    - `teardrop`: depth profile of the silhouette on the YZ plane
    """

    x, y, z = heart_point_grid.x, heart_point_grid.y, heart_point_grid.z

    z_min = z.min()
    z_max = z.max()

    # Z-axis split in three:
    # upper third -> quarter circle, lower two thirds -> cubic
    z_axis_length = z_max - z_min
    upper_quarter_circle_radius = z_axis_length / 3  # same as upper_z_axis_length
    z_joint = z_max - upper_quarter_circle_radius
    lower_z_axis_length = z_joint - z_min

    # depth at every height
    upper_quarter_circle_depth = np.sqrt(
        np.clip(upper_quarter_circle_radius**2 - (z - z_joint) ** 2, 0.0, None)
    )

    # cubic fixed by four conditions - value and tangent at each end
    # ----------------------------------------------------------------------------------------------
    # tangent scaled by the interval length (per z -> per t)
    t = (z - z_min) / lower_z_axis_length  # unit interval parameter
    m_0 = np.tan(np.radians(teardrop.half_angle)) * lower_z_axis_length  # same as start_tangent

    t_square = t * t
    t_cube = t_square * t

    # p_0 = 0 (start_value) and m_1 = 0 (end_tangent) -> two basis functions dropped
    lower_cubic_depth = m_0 * (t_cube - 2 * t_square + t) + upper_quarter_circle_radius * (
        -2 * t_cube + 3 * t_square
    )
    # ----------------------------------------------------------------------------------------------

    # two pieces joined at z_joint
    teardrop_depth = np.where(z > z_joint, upper_quarter_circle_depth, lower_cubic_depth)

    # assumption: half-elliptical generatrix - the deepest depth at every height
    half_depth = np.abs(y).max()
    z_extremum = np.where(z > 0, z_max, z_min)
    formed_depth = half_depth * np.sqrt(np.clip(1 - (z / z_extremum) ** 2, 0.0, None))

    # guard: 0 / 0 at both ends of the axis -> scale 0
    depth_scale = np.divide(
        teardrop_depth, formed_depth, out=np.zeros_like(y), where=formed_depth > 0
    )

    # deformed spherical product (only depth)
    return HeartPointGrid(x=x, y=y * depth_scale, z=z)
