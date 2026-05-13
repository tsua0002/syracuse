from syracuse.arithmetic import analyze_block_arithmetic, suffix_arithmetic_metrics
from syracuse.cache import SequenceCache


def test_analyze_block_arithmetic(tmp_path) -> None:
    cache = SequenceCache(tmp_path / "syracuse.sqlite")
    try:
        stats = analyze_block_arithmetic(cache, start=1, stop=20)
    finally:
        cache.close()

    assert stats.root_count == 20
    assert stats.max_steps >= stats.mean_steps
    assert stats.mean_exponent >= 0


def test_suffix_arithmetic_metrics_reuses_cache(tmp_path) -> None:
    cache = SequenceCache(tmp_path / "syracuse.sqlite")
    metrics_cache = {}
    try:
        cache.ensure_range(11)
        metrics = suffix_arithmetic_metrics(cache, 11, metrics_cache)
    finally:
        cache.close()

    assert metrics.odd_count == 5
    assert metrics.odd_transition_count == 4
    assert metrics.exponent_sum == 10
    assert 13 in metrics_cache
