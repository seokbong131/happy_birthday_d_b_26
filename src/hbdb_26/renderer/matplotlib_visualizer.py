import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from hbdb_26.scene.heart import HeartPointGrid, HeartTriangleMesh


def visualize_point_grid(heart_point_grid: HeartPointGrid) -> Figure:
    """
    Plot a 3D surface of the heart shape using parametric point grid.
    """

    figure = plt.figure()

    axes = figure.add_subplot(projection="3d")

    axes.plot_surface(
        heart_point_grid.x,
        heart_point_grid.y,
        heart_point_grid.z,
        color="crimson",
    )
    axes.set_aspect("equal")

    return figure


def visualize_triangle_mesh(heart_triangle_mesh: HeartTriangleMesh) -> Figure:
    """
    Plot a 3D triangle mesh of the heart shape using extracted vertices and faces.
    """

    figure = plt.figure()

    axes = figure.add_subplot(projection="3d")

    axes.plot_trisurf(
        heart_triangle_mesh.vertices[:, 0],
        heart_triangle_mesh.vertices[:, 1],
        heart_triangle_mesh.vertices[:, 2],
        triangles=heart_triangle_mesh.faces,
        color="crimson",
    )
    axes.set_aspect("equal")

    return figure
