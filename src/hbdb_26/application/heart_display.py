import matplotlib.pyplot as plt

from hbdb_26.application.heart_registry import HEART_REGISTRY
from hbdb_26.application.subplot_grid import compute_subplot_grid_shape
from hbdb_26.visualizer import visualize_heart


def i_love_d_b() -> None:
    # layout
    heart_count = len(HEART_REGISTRY)
    rows, cols = compute_subplot_grid_shape(heart_count)
    figure = plt.figure(figsize=(3 * cols, 3 * rows))  # 3 inches (hard coding)

    # scene (discretization) & visualization (composition)
    for index, heart_object in enumerate(HEART_REGISTRY, start=1):
        axes_3d = figure.add_subplot(rows, cols, index, projection="3d")

        heart_geometry = heart_object.make()
        visualize_heart(axes_3d=axes_3d, heart_geometry=heart_geometry)

    # display
    figure.tight_layout()  # one-time adjustment
    plt.show()
