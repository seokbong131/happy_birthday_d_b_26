import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D

from hbdb_26.scene import HeartGeometry, HeartPointGrid, HeartTriangleMesh, HeartVoxelGrid
from hbdb_26.visualizer.render_mode import RenderMode


def visualize_heart(
    *, axes_3d: Axes3D, heart_geometry: HeartGeometry, render_mode: RenderMode | None
) -> None:
    """
    Plot a heart geometry onto the 3D axes.
    """

    match heart_geometry, render_mode:
        case HeartPointGrid(), RenderMode():
            _visualize_point_grid(axes_3d, heart_geometry, render_mode)

        case HeartTriangleMesh(), None:
            _visualize_triangle_mesh(axes_3d, heart_geometry)

        case HeartVoxelGrid(), None:
            _visualize_voxel_grid(axes_3d, heart_geometry)

        case _:
            raise TypeError(
                f"Unsupported pair of heart geometry and render mode. "
                f"(geometry: {type(heart_geometry).__name__} & render mode: {render_mode})"
            )


def _visualize_point_grid(
    axes_3d: Axes3D, heart_point_grid: HeartPointGrid, render_mode: RenderMode
) -> None:
    """
    Plot a 3D surface or wireframe of the heart shape using parametric point grid.
    """

    x, y, z = heart_point_grid.x, heart_point_grid.y, heart_point_grid.z

    match render_mode:
        case RenderMode.FILL:
            axes_3d.plot_surface(x, y, z, color="crimson")

        case RenderMode.WIREFRAME:
            axes_3d.plot_wireframe(x, y, z, color="crimson")

        case _:
            raise NotImplementedError(f"Unsupported render mode. (render mode: {render_mode})")

    axes_3d.set_aspect("equal")


def _visualize_triangle_mesh(axes_3d: Axes3D, heart_triangle_mesh: HeartTriangleMesh) -> None:
    """
    Plot a 3D triangle mesh of the heart shape using extracted vertices and faces.
    """

    vertices, faces = heart_triangle_mesh.vertices, heart_triangle_mesh.faces

    axes_3d.plot_trisurf(
        vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=faces, color="crimson"
    )

    axes_3d.set_aspect("equal")


def _visualize_voxel_grid(axes_3d: Axes3D, heart_voxel_grid: HeartVoxelGrid) -> None:
    """
    Plot a 3D voxel grid of the heart shape using filled cells.
    """

    filled = heart_voxel_grid.filled
    origin = heart_voxel_grid.origin
    spacing = heart_voxel_grid.spacing

    # corners of the voxels (one larger in every dimension)
    x, y, z = np.meshgrid(
        origin[0] + np.arange(filled.shape[0] + 1) * spacing,
        origin[1] + np.arange(filled.shape[1] + 1) * spacing,
        origin[2] + np.arange(filled.shape[2] + 1) * spacing,
        indexing="ij",
    )

    axes_3d.voxels(x, y, z, filled, facecolors="crimson")

    axes_3d.set_aspect("equal")
