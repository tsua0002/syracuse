from syracuse.analysis import (
    build_density_grid,
    build_normalized_density_grid,
    build_odd_compression_stats,
    build_parity_stats,
)
from syracuse.core import stats_for_range


def test_density_grid_counts_all_orbit_points() -> None:
    stats = stats_for_range(3)
    grid = build_density_grid(stats, log_value_bins=8)

    assert int(grid.counts.sum()) == sum(len(item.sequence) for item in stats)
    assert grid.total_points == int(grid.counts.sum())


def test_density_grid_uses_step_bins_by_default() -> None:
    stats = stats_for_range(3)
    grid = build_density_grid(stats, log_value_bins=8)

    assert grid.counts.shape == (max(item.steps for item in stats) + 1, 8)


def test_normalized_density_grid_counts_all_orbit_points() -> None:
    stats = stats_for_range(3)
    grid = build_normalized_density_grid(stats, bins=10)

    assert grid.counts.shape == (10, 10)
    assert int(grid.counts.sum()) == sum(len(item.sequence) for item in stats)
    assert grid.step_edges[0] == 0
    assert grid.step_edges[-1] == 1
    assert grid.log_value_edges[0] == 0
    assert grid.log_value_edges[-1] == 1


def test_parity_stats_for_known_sequence() -> None:
    stats = stats_for_range(3)
    parity_by_start = {item.start: item for item in build_parity_stats(stats)}

    assert parity_by_start[3].parity_word == "10100001"
    assert parity_by_start[3].odd_count == 3
    assert parity_by_start[3].even_count == 5
    assert parity_by_start[3].odd_transition_count == 2
    assert parity_by_start[3].zero_run_count == 2
    assert parity_by_start[3].max_zero_run == 4


def test_odd_compression_stats_for_known_sequence() -> None:
    stats = stats_for_range(11)
    compression_by_start = {item.start: item for item in build_odd_compression_stats(stats)}

    assert compression_by_start[11].exponent_word == (1, 2, 3, 4)
    assert compression_by_start[11].compressed_length == 4
    assert compression_by_start[11].exponent_sum == 10
    assert compression_by_start[11].exponent_one_count == 1
    assert compression_by_start[11].max_odd_value == 17
