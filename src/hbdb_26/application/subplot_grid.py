import math


def compute_subplot_grid_shape(heart_count: int) -> tuple[int, int]:
    """
    Return an optimal grid layout for the number of hearts.

    assumption: the range of heart_count is [1, 9].
    """

    if not 1 <= heart_count <= 9:
        raise ValueError(f"heart_count must be in [1, 9]. (heart_count: {heart_count})")

    cols = math.isqrt(heart_count - 1) + 1
    rows = (heart_count + cols - 1) // cols

    return rows, cols
