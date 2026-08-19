from collections.abc import Callable
from dataclasses import dataclass

from hbdb_26.scene import (
    JULIA_CURVE,
    TAUBIN_SURFACE,
    HalfEllipse,
    HeartEquation,
    HeartGeometry,
    MarchingCubesParameter,
    SphericalProductParameter,
    extract_isosurface,
    form_spherical_product,
)
from hbdb_26.visualizer import RenderMode


@dataclass(frozen=True, kw_only=True)
class HeartObject[HeartParameter]:
    """
    Register a heart's information.

    - `name`: TOML section key
    - `equation`: heart parametric curve or heart implicit surface
    - `parameter`: settings of discretization
    - `discretize`: `{equation, parameter}` -> geometry
    - `render_mode`: how to draw a point grid (`None` for any other geometry)
    """

    name: str
    equation: HeartEquation
    parameter: HeartParameter
    discretize: Callable[[HeartEquation, HeartParameter], HeartGeometry]
    render_mode: RenderMode | None


HEART_REGISTRY: tuple[HeartObject, ...] = (
    HeartObject(
        name="julia",
        equation=JULIA_CURVE,
        parameter=SphericalProductParameter(
            generatrix=HalfEllipse(cross_section_curve_scale=1.0, half_depth=8.0),
            taper=None,
            u_samples=101,
            v_samples=101,
        ),
        discretize=form_spherical_product,
        render_mode=RenderMode.FILL,
    ),
    HeartObject(
        name="taubin",
        equation=TAUBIN_SURFACE,
        parameter=MarchingCubesParameter(
            grid_bound=1.5,  # approximately, x in [-1.2, 1.2] & y in [-0.8, 0.8] & z in [-1, 1.3]
            iso_level=0.0,
            resolution=100,
        ),
        discretize=extract_isosurface,
        render_mode=None,
    ),
)
