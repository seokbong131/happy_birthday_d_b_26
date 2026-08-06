from enum import Enum, auto


class RenderMode(Enum):
    """
    How to draw a point grid.
    """

    FILL = auto()
    WIREFRAME = auto()
