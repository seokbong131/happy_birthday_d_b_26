from dataclasses import dataclass


@dataclass(frozen=True)
class JuliaConfig:
    """
    u_samples: the number of samples along u in [0, 2 * pi]
    v_samples: the number of samples along v in [0, pi]
    """

    u_samples: int = 100
    v_samples: int = 100


@dataclass(frozen=True)
class TaubinConfig:
    """
    grid_bound: half-extent of voxel grid to evaluate [-bound, bound]^3
    iso_level: threshold value treated as the surface (0.0 => zero set)
    resolution: the number of voxel grid samples along each axis
    """

    grid_bound: float = 1.5  # approximately, x in [-1.2, 1.2] & y in [-0.8, 0.8] & z in [-1, 1.3]
    iso_level: float = 0.0
    resolution: int = 100
