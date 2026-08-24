from dataclasses import dataclass


# marching cubes
# --------------------------------------------------------------------------------------------------
@dataclass(frozen=True, kw_only=True)
class MarchingCubesParameter:
    """
    - `grid_bound`: half of the sampling grid's edge length ([-grid_bound, grid_bound]^3)
    - `iso_value`: scalar value of the isosurface (0.0 => zero set)
    - `resolution`: number of samples along each axis
    """

    grid_bound: float
    iso_value: float
    resolution: int

    def __post_init__(self) -> None:
        if self.grid_bound <= 0:
            raise ValueError(f"grid_bound must be positive. (grid_bound: {self.grid_bound})")

        if self.resolution < 2:
            raise ValueError(
                f"resolution must be at least 2 per axis. (resolution: {self.resolution})"
            )


# spherical product
# --------------------------------------------------------------------------------------------------
@dataclass(frozen=True, kw_only=True)
class HalfEllipse:
    """
    - `cross_section_curve_scale`: semi-axis scaling the cross-section curve (dimensionless)
    - `half_depth`: semi-axis along the Y-axis (length)
    """

    cross_section_curve_scale: float
    half_depth: float

    def __post_init__(self) -> None:
        if self.cross_section_curve_scale <= 0:
            raise ValueError(
                f"cross_section_curve_scale must be positive. "
                f"(cross_section_curve_scale: {self.cross_section_curve_scale})"
            )

        if self.half_depth <= 0:
            raise ValueError(f"half_depth must be positive. (half_depth: {self.half_depth})")


_MINIMUM_HALF_ANGLE = 15.0
_MAXIMUM_HALF_ANGLE = 56.3  # arctan(3 / 2) in degrees, rounded down


@dataclass(frozen=True)
class Teardrop:
    """
    - `half_angle`: half of the angle at the lower vertex (degrees)
    """

    half_angle: float

    def __post_init__(self) -> None:
        if self.half_angle < _MINIMUM_HALF_ANGLE:
            raise ValueError(
                f"half_angle must be at least {_MINIMUM_HALF_ANGLE} degrees. "
                f"(half_angle: {self.half_angle})"
            )

        if self.half_angle > _MAXIMUM_HALF_ANGLE:
            raise ValueError(
                f"half_angle must be at most {_MAXIMUM_HALF_ANGLE} degrees. "
                f"(half_angle: {self.half_angle})"
            )


@dataclass(frozen=True, kw_only=True)
class SphericalProductParameter:
    """
    - `generatrix`: curve giving the cross-section curve its scale and depth at each v
    - `taper`: teardrop scaling the depth (`None` for an untapered spherical product)
    - `u_samples`: number of samples along u in [0, 2 * pi]
    - `v_samples`: number of samples along v in [0, pi]
    """

    generatrix: HalfEllipse
    taper: Teardrop | None
    u_samples: int
    v_samples: int

    def __post_init__(self) -> None:
        if self.u_samples < 5:
            raise ValueError(f"u_samples must be at least 5. (u_samples: {self.u_samples})")

        if self.u_samples % 2 == 0:
            raise ValueError(f"u_samples must be odd. (u_samples: {self.u_samples})")

        if self.v_samples < 3:
            raise ValueError(f"v_samples must be at least 3. (v_samples: {self.v_samples})")

        if self.v_samples % 2 == 0:
            raise ValueError(f"v_samples must be odd. (v_samples: {self.v_samples})")


# voxelization
# --------------------------------------------------------------------------------------------------
@dataclass(frozen=True, kw_only=True)
class VoxelizationParameter:
    """
    - `grid_bound`: half of the voxel grid's edge length ([-grid_bound, grid_bound]^3)
    - `resolution`: number of voxels along each axis
    """

    grid_bound: float
    resolution: int

    def __post_init__(self) -> None:
        if self.grid_bound <= 0:
            raise ValueError(f"grid_bound must be positive. (grid_bound: {self.grid_bound})")

        if self.resolution < 2:
            raise ValueError(
                f"resolution must be at least 2 per axis. (resolution: {self.resolution})"
            )
