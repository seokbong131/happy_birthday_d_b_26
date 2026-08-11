# Ref. https://www.cs.bilkent.edu.tr/~gudukbay/cs465/super_quadrics.pdf

import numpy as np

from hbdb_26.scene.parameter import HalfEllipse


def compute_half_ellipse(half_ellipse: HalfEllipse, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Generatrix of a spherical product: `v` -> `(cross_section_curve_scale, depth)`

    - `half_ellipse`: two semi-axes of the generatrix
    - `v`: float array of angular parameters in [0, pi] (like colatitude)
    """

    cross_section_curve_scale = half_ellipse.cross_section_curve_scale * np.sin(v)
    depth = half_ellipse.half_depth * np.cos(v)

    return cross_section_curve_scale, depth
