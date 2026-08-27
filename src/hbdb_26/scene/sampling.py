import numpy as np

from hbdb_26.scene.heart import HeartPointCloud, HeartPointGrid
from hbdb_26.scene.heart_equation import HeartEquation, ParametricCurve2D
from hbdb_26.scene.parameter import SamplingParameter
from hbdb_26.scene.spherical_product import form_spherical_product


def sample_boundary(
    heart_equation: HeartEquation, sampling_parameter: SamplingParameter
) -> HeartPointCloud:
    """
    Point cloud sampled from the boundary of a spherical product: `area` -> `points`

    - `heart_equation`: cross-section curve forming the spherical product
    - `sampling_parameter`: point count, seed, and the spherical product beneath the points
    """

    # heart equation is-a 2D parametric curve
    if not isinstance(heart_equation, ParametricCurve2D):
        raise TypeError(
            f"Sampling needs a 2D parametric curve. (equation: {type(heart_equation).__name__})"
        )

    vertex, edge_1, edge_2 = _triangulate_point_grid(
        form_spherical_product(heart_equation, sampling_parameter.spherical_product)
    )

    # area of one triangle, half the norm of the cross product
    area = np.linalg.norm(np.cross(edge_1, edge_2), axis=1) / 2

    generator = np.random.default_rng(sampling_parameter.seed)

    return HeartPointCloud(
        _sample_on_triangles(
            vertex, edge_1, edge_2, area, sampling_parameter.point_count, generator
        )
    )


def sample_interior(
    heart_equation: HeartEquation, sampling_parameter: SamplingParameter
) -> HeartPointCloud:
    """
    Point cloud sampled from the interior of a spherical product: `volume` -> `points`

    - `heart_equation`: cross-section curve forming the spherical product
    - `sampling_parameter`: point count, seed, and the spherical product beneath the points
    """

    # heart equation is-a 2D parametric curve
    if not isinstance(heart_equation, ParametricCurve2D):
        raise TypeError(
            f"Sampling needs a 2D parametric curve. (equation: {type(heart_equation).__name__})"
        )

    vertex, edge_1, edge_2 = _triangulate_point_grid(
        form_spherical_product(heart_equation, sampling_parameter.spherical_product)
    )

    # assumption: star-shaped interior at the origin
    # volume of one tetrahedron from the origin, a sixth of the unsigned scalar triple product
    tetrahedron_volume = np.abs(np.sum(vertex * np.cross(edge_1, edge_2), axis=1)) / 6

    generator = np.random.default_rng(sampling_parameter.seed)
    point_count = sampling_parameter.point_count

    boundary_point = _sample_on_triangles(
        vertex, edge_1, edge_2, tetrahedron_volume, point_count, generator
    )

    # cube root of a uniform fraction (equal counts per equal volume)
    radial_fraction = np.cbrt(generator.random(point_count))

    return HeartPointCloud(radial_fraction[:, np.newaxis] * boundary_point)


def _triangulate_point_grid(
    heart_point_grid: HeartPointGrid,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Triangles of a point grid: `(x, y, z)` -> `(vertex, edge_1, edge_2)`

    - `heart_point_grid`: point grid with adjacent samples bounding each cell
    """

    # (u, v, 3) position of every sample
    position = np.stack([heart_point_grid.x, heart_point_grid.y, heart_point_grid.z], axis=-1)

    # one cell of the (u, v) grid -> two triangles sharing the diagonal
    cell_vertex = position[:-1, :-1]
    u_edge = position[1:, :-1] - cell_vertex
    v_edge = position[:-1, 1:] - cell_vertex
    diagonal_edge = position[1:, 1:] - cell_vertex

    return (
        np.concatenate([cell_vertex, cell_vertex]).reshape(-1, 3),
        np.concatenate([u_edge, diagonal_edge]).reshape(-1, 3),
        np.concatenate([diagonal_edge, v_edge]).reshape(-1, 3),
    )


def _sample_on_triangles(
    vertex: np.ndarray,
    edge_1: np.ndarray,
    edge_2: np.ndarray,
    weight: np.ndarray,
    point_count: int,
    generator: np.random.Generator,
) -> np.ndarray:
    """
    Points drawn on triangles in proportion to a weight: `weight` -> `points`

    - `vertex`: (#triangles, 3) float array of the first vertex per triangle
    - `edge_1`: (#triangles, 3) float array of vectors from that vertex to the second
    - `edge_2`: (#triangles, 3) float array of vectors from that vertex to the third
    - `weight`: (#triangles,) float array of relative draw frequency per triangle
    - `point_count`: number of points to draw
    - `generator`: seeded pseudorandom number generator
    """

    # one triangle per point, drawn in proportion to the weight
    triangle_index = generator.choice(len(weight), point_count, p=weight / weight.sum())

    # flat Dirichlet distribution -> barycentric coordinates uniform on the triangle
    barycentric_coordinate = generator.dirichlet(np.ones(3), point_count)

    return (
        vertex[triangle_index]
        + barycentric_coordinate[:, 1, np.newaxis] * edge_1[triangle_index]
        + barycentric_coordinate[:, 2, np.newaxis] * edge_2[triangle_index]
    )
