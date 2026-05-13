from syracuse.analysis import build_normalized_density_grid
from syracuse.cache import (
    SequenceCache,
    build_fixed_normalized_support_mask_from_cache,
    build_normalized_density_grid_from_cache,
)
from syracuse.core import stats_for_range


def test_sequence_cache_reconstructs_known_sequence(tmp_path) -> None:
    cache = SequenceCache(tmp_path / "syracuse.sqlite")
    try:
        cache.ensure_range(11)

        assert tuple(cache.sequence(11)) == (
            11,
            34,
            17,
            52,
            26,
            13,
            40,
            20,
            10,
            5,
            16,
            8,
            4,
            2,
            1,
        )
        assert cache.nodes[40].steps == 8
        assert cache.nodes[11].next_value == 34
    finally:
        cache.close()


def test_cached_normalized_density_matches_in_memory_grid(tmp_path) -> None:
    limit = 20
    bins = 32
    cache = SequenceCache(tmp_path / "syracuse.sqlite")
    try:
        cached_grid = build_normalized_density_grid_from_cache(cache, limit=limit, bins=bins)
    finally:
        cache.close()

    memory_grid = build_normalized_density_grid(stats_for_range(limit), bins=bins)

    assert cached_grid.total_points == memory_grid.total_points
    assert (cached_grid.counts == memory_grid.counts).all()


def test_fixed_normalized_support_mask_from_cache(tmp_path) -> None:
    cache = SequenceCache(tmp_path / "syracuse.sqlite")
    try:
        cache.ensure_range(20)
        max_step = max(cache.nodes[start].steps for start in range(1, 21))
        max_value = max(cache.nodes[start].maximum for start in range(1, 21))
        mask = build_fixed_normalized_support_mask_from_cache(
            cache,
            start=1,
            stop=20,
            bins=32,
            max_step=max_step,
            max_value=max_value,
        )
    finally:
        cache.close()

    assert mask.shape == (32, 32)
    assert mask.any()
