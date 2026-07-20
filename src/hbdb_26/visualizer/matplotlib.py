from mpl_toolkits.mplot3d.axes3d import Axes3D

from hbdb_26.scene import HeartGeometry, HeartPointGrid, HeartTriangleMesh


def visualize_heart(*, axes_3d: Axes3D, heart_geometry: HeartGeometry) -> None:
    """
    Plot a heart geometry onto the 3D axes.
    """

    match heart_geometry:
        case HeartPointGrid() as heart_point_grid:
            _visualize_point_grid(axes_3d, heart_point_grid)

        case HeartTriangleMesh() as heart_triangle_mesh:
            _visualize_triangle_mesh(axes_3d, heart_triangle_mesh)

        case _:
            raise TypeError(f"Unsupported heart geometry. (type: {type(heart_geometry).__name__})")


def _visualize_point_grid(axes_3d: Axes3D, heart_point_grid: HeartPointGrid) -> None:
    """
    Plot a 3D surface of the heart shape using parametric point grid.
    """

    axes_3d.plot_surface(
        heart_point_grid.x,
        heart_point_grid.y,
        heart_point_grid.z,
        color="crimson",
    )
    axes_3d.set_aspect("equal")


def _visualize_triangle_mesh(axes_3d: Axes3D, heart_triangle_mesh: HeartTriangleMesh) -> None:
    """
    Plot a 3D triangle mesh of the heart shape using extracted vertices and faces.
    """

    axes_3d.plot_trisurf(
        heart_triangle_mesh.vertices[:, 0],
        heart_triangle_mesh.vertices[:, 1],
        heart_triangle_mesh.vertices[:, 2],
        triangles=heart_triangle_mesh.faces,
        color="crimson",
    )
    axes_3d.set_aspect("equal")
