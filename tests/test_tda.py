import numpy as np

from syracuse.analysis import DensityGrid
from syracuse.tda import compute_alpha_persistence, compute_density_persistence, density_filtration_values, points_from_mask_window


def test_density_filtration_makes_dense_cells_early() -> None:
    grid = DensityGrid(
        counts=np.array([[0, 3], [10, 1]], dtype=float),
        step_edges=np.array([0, 1, 2]),
        log_value_edges=np.array([0, 1, 2]),
        total_points=14,
    )

    values = density_filtration_values(grid)

    assert values[1, 0] < values[0, 1]
    assert values[0, 0] == 0


def test_cubical_persistence_detects_toy_hole() -> None:
    counts = np.ones((5, 5), dtype=float) * 10
    counts[2, 2] = 0
    grid = DensityGrid(
        counts=counts,
        step_edges=np.arange(6),
        log_value_edges=np.arange(6),
        total_points=int(counts.sum()),
    )

    features = compute_density_persistence(grid)

    assert any(feature.dimension == 1 for feature in features)


def test_alpha_persistence_on_mask_window() -> None:
    mask = np.ones((5, 5), dtype=bool)
    points = points_from_mask_window(mask, x_range=(0, 1), y_range=(0, 1), max_points=25)
    features = compute_alpha_persistence(points)

    assert points.shape == (25, 2)
    assert any(feature.dimension == 0 for feature in features)
