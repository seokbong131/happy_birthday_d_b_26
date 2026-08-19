# Ref. https://www.cs.bilkent.edu.tr/~gudukbay/cs465/super_quadrics.pdf

import numpy as np

from hbdb_26.scene.generatrix import compute_half_ellipse
from hbdb_26.scene.heart import HeartPointGrid
from hbdb_26.scene.heart_equation import HeartEquation, ParametricCurve2D
from hbdb_26.scene.parameter import SphericalProductParameter
from hbdb_26.scene.taper import taper_depth


def form_spherical_product(
    heart_equation: HeartEquation, spherical_product_parameter: SphericalProductParameter
) -> HeartPointGrid:
    """
    Spherical product of a cross-section curve and a generatrix: `(u, v)` -> `(x, y, z)`

    - `heart_equation`: cross-section curve scaled by the generatrix into each parallel
    - `spherical_product_parameter`: generatrix, taper, and the number of samples along u and v
    """

    # heart equation is-a 2D parametric curve
    if not isinstance(heart_equation, ParametricCurve2D):
        raise TypeError(
            f"Spherical product needs a 2D parametric curve. "
            f"(equation: {type(heart_equation).__name__})"
        )

    # [start, stop] -> evenly spaced samples
    u = np.linspace(0, 2 * np.pi, spherical_product_parameter.u_samples)
    v = np.linspace(0, np.pi, spherical_product_parameter.v_samples)

    # u -> cross-section curve, v -> generatrix (1D each, no grid yet)
    cross_section_curve_x, cross_section_curve_z = heart_equation.compute(u)
    cross_section_curve_scale, depth = compute_half_ellipse(
        spherical_product_parameter.generatrix, v
    )

    # each u sample paired with every v sample -> [i, j] grid aligned with (u, v)
    x = cross_section_curve_x[:, np.newaxis] * cross_section_curve_scale
    z = cross_section_curve_z[:, np.newaxis] * cross_section_curve_scale
    y = np.broadcast_to(depth, x.shape).copy()  # one generatrix depth per parallel

    heart_point_grid = HeartPointGrid(x=x, y=y, z=z)
    taper = spherical_product_parameter.taper

    return heart_point_grid if taper is None else taper_depth(heart_point_grid, taper)
