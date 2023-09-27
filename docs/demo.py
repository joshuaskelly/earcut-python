import matplotlib.pylab as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from seaborn import color_palette

from earcut import earcut
from earcut.utils_3d import project3d_to_2d

colors = color_palette("pastel")


def load_polygons2() -> list[list[np.ndarray]]:
    polygons = [
        [
            np.array(
                [
                    [0, 0, 0],
                    [0, 4, 0],
                    [4, 4, 0],
                    [4, 0, 0],
                ]
            ),
            np.array(
                [
                    [1, 1, 0],
                    [1, 2, 0],
                    [2, 2, 0],
                    [2, 1, 0],
                ]
            ),
            np.array(
                [
                    [2, 2, 0],
                    [2, 3, 0],
                    [3, 3, 0],
                    [3, 2, 0],
                ]
            ),
        ],
        [
            np.array(
                [
                    [0, 0, 0],
                    [0, 0, 4],
                    [0, 4, 4],
                    [0, 4, 0],
                ]
            ),
            np.array(
                [
                    [0, 1, 1],
                    [0, 1, 3],
                    [0, 3, 3],
                    [0, 3, 1],
                ]
            ),
        ],
        [
            np.array(
                [
                    [0, 4, 0],
                    [0, 4, 4],
                    [4, 4, 4],
                    [4, 4, 0],
                ]
            ),
            np.array(
                [
                    [3, 4, 2],
                    [2, 4, 3],
                    [1, 4, 2],
                    [2, 4, 1],
                ]
            ),
        ],
        [
            np.array(
                [
                    [0, 4, 0],
                    [0, 4, 4],
                    [4, 4, 4],
                    [4, 4, 0],
                ]
            ),
            np.array(
                [
                    [3, 4, 2],
                    [2, 4, 3],
                    [1, 4, 2],
                    [2, 4, 1],
                ]
            ),
        ],
        [
            np.array(
                [
                    [4, 0, 0],
                    [4, 4, 0],
                    [7, 4, -3],
                    [7, 0, -3],
                ],
            ),
            np.array(
                [
                    [5, 1, -1],
                    [5, 3, -1],
                    [6, 3, -2],
                    [6, 1, -2],
                ],
            ),
        ],
    ]

    ix = np.linspace(0, 2 * np.pi, 150)
    u = 4 + 0.5 * np.sin(ix * 17)
    x = 4 + u * np.cos(ix)
    z = u * np.sin(ix)
    y = 6 * np.ones(150)
    ix = np.linspace(0, 2 * np.pi, 13)
    in_x = 4 + 2 * np.cos(ix)
    in_z = 2 * np.sin(ix)
    in_y = 6 * np.ones(13)

    polygons.append(
        [
            np.vstack((x, y, z)).T,
            np.vstack((in_x, in_y, in_z)).T,
        ]
    )

    return polygons


def triangulate(polygon: list[np.ndarray]) -> np.ndarray:
    # Flatten
    holeIndices = []
    if len(polygon) > 1:
        hi = polygon[0].shape[0]
        for ring in polygon[1:]:
            holeIndices.append(hi)
            hi += ring.shape[0]
    vertices = np.vstack(polygon)
    flatten_vertices = vertices.flatten()

    # Earcut
    flatten_vertices = project3d_to_2d(flatten_vertices, len(polygon[0]))
    if flatten_vertices is not None:
        if cut := earcut(flatten_vertices, holeIndices, dim=2):
            cut = np.asarray(cut).reshape(-1, 3)
            return vertices[cut]

    return np.empty((0, 3, 3))


# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
# ax.view_init(90, -90, 0)
ax.set_xlim(0, 7)
ax.set_ylim(0, 7)
ax.set_zlim(-3, 4)
ax.set_box_aspect((1, 1, 1))

ci = 0
polygons = load_polygons2()
for poly in polygons:
    triangles = triangulate(poly)
    print(triangles)
    poly = Poly3DCollection(
        triangles,
        alpha=0.8,
        edgecolor="k",
        zsort="max",
        facecolor=colors[ci],
        linewidth=1,
    )
    ax.add_collection3d(poly)
    ci += 1

fig.tight_layout()
plt.savefig("demo.png", transparent=True, dpi=300)
