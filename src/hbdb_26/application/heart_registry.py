from collections.abc import Callable
from dataclasses import dataclass

from hbdb_26.scene import HeartGeometry, make_julia_heart, make_taubin_heart


@dataclass(frozen=True, slots=True)
class HeartObject:
    """
    Register a heart's information.

    name: TOML section key
    make: equation -> geometry (discretization for the scene)
    """

    name: str
    make: Callable[[], HeartGeometry]


HEART_REGISTRY: tuple[HeartObject, ...] = (
    HeartObject("julia", make_julia_heart),
    HeartObject("taubin", make_taubin_heart),
)
