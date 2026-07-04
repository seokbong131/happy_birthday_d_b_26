import matplotlib.pyplot as plt

from hbdb_26.renderer import visualize_point_grid, visualize_triangle_mesh
from hbdb_26.scene import make_julia_heart, make_taubin_heart


def i_love_d_b() -> None:
    # scene (discretization)
    julia_heart = make_julia_heart()
    taubin_heart = make_taubin_heart()

    # visualization (composition)
    visualize_point_grid(julia_heart)
    visualize_triangle_mesh(taubin_heart)

    # display
    plt.show()


if __name__ == "__main__":
    i_love_d_b()
