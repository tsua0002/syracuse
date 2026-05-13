import numpy as np

from syracuse.analysis import DensityGrid
from syracuse.support import (
    analyze_block_attachment,
    analyze_alpha_attachment,
    analyze_dense_support,
    component_summary,
    count_holes,
    dense_support_mask,
    dilate_mask,
    largest_inscribed_radius,
    minimal_connection_epsilon,
    summarize_epsilon_sweep_item,
)


def test_minimal_connection_epsilon_connects_two_components() -> None:
    mask = np.zeros((5, 5), dtype=bool)
    mask[2, 1] = True
    mask[2, 3] = True

    assert component_summary(mask)[0] == 2
    assert minimal_connection_epsilon(mask) == 1
    assert component_summary(dilate_mask(mask, epsilon=1))[0] == 1


def test_count_holes_detects_square_hole() -> None:
    mask = np.ones((5, 5), dtype=bool)
    mask[2, 2] = False

    assert count_holes(mask) == 1


def test_largest_inscribed_radius_on_square() -> None:
    mask = np.ones((5, 5), dtype=bool)

    radius, center = largest_inscribed_radius(mask)

    assert radius == 3
    assert center == (2, 2)


def test_analyze_dense_support_from_density_grid() -> None:
    counts = np.zeros((5, 5), dtype=float)
    counts[1:4, 1:4] = 2
    counts[2, 2] = 0
    grid = DensityGrid(
        counts=counts,
        step_edges=np.arange(6),
        log_value_edges=np.arange(6),
        total_points=int(counts.sum()),
    )

    mask = dense_support_mask(grid, threshold=1)
    stats = analyze_dense_support(grid, threshold=1)

    assert mask.sum() == 8
    assert stats.beta1_before == 1
    assert stats.occupied_cells == 8


def test_summarize_epsilon_sweep_item_normalizes_values() -> None:
    counts = np.ones((5, 5), dtype=float)
    grid = DensityGrid(
        counts=counts,
        step_edges=np.arange(6),
        log_value_edges=np.arange(6),
        total_points=int(counts.sum()),
    )
    support_stats = analyze_dense_support(grid, threshold=1)

    summary = summarize_epsilon_sweep_item(limit=10, bins=5, threshold=1, stats=support_stats)

    assert summary.limit == 10
    assert summary.epsilon_normalized == support_stats.epsilon / 5
    assert summary.largest_inscribed_radius_normalized == support_stats.largest_inscribed_radius / 5


def test_analyze_block_attachment_distances() -> None:
    previous = np.zeros((5, 5), dtype=bool)
    previous[2, 2] = True
    block = np.zeros((5, 5), dtype=bool)
    block[2, 3] = True
    block[4, 4] = True

    stats = analyze_block_attachment(previous_mask=previous, block_mask=block, start=2, stop=3)

    assert stats.added_cells == 2
    assert stats.min_distance_cells == 1
    assert stats.max_distance_cells > stats.min_distance_cells


def test_analyze_alpha_attachment_respects_axis_weight() -> None:
    previous = np.zeros((5, 5), dtype=bool)
    previous[2, 2] = True
    block = np.zeros((5, 5), dtype=bool)
    block[3, 2] = True

    low_alpha = analyze_alpha_attachment(previous_mask=previous, block_mask=block, start=2, stop=3, alpha=0.5)
    high_alpha = analyze_alpha_attachment(previous_mask=previous, block_mask=block, start=2, stop=3, alpha=2.0)

    assert low_alpha.min_distance < high_alpha.min_distance
    assert low_alpha.added_cells == 1
