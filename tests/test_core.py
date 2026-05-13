import pytest

from syracuse.core import (
    odd_compressed_next,
    odd_compressed_trajectory,
    stats_for,
    stats_for_range,
    syracuse_next,
    syracuse_sequence,
    two_adic_valuation,
)


def test_syracuse_next_even_number() -> None:
    assert syracuse_next(20) == 10


def test_syracuse_next_odd_number() -> None:
    assert syracuse_next(11) == 34


def test_syracuse_sequence_for_11_matches_reference() -> None:
    assert syracuse_sequence(11) == (
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


def test_two_adic_valuation() -> None:
    assert two_adic_valuation(1) == 0
    assert two_adic_valuation(16) == 4
    assert two_adic_valuation(40) == 3


def test_odd_compressed_next() -> None:
    step = odd_compressed_next(13)

    assert step.source == 13
    assert step.exponent == 3
    assert step.target == 5


def test_odd_compressed_trajectory_for_11() -> None:
    steps = odd_compressed_trajectory(11)

    assert [(step.source, step.exponent, step.target) for step in steps] == [
        (11, 1, 17),
        (17, 2, 13),
        (13, 3, 5),
        (5, 4, 1),
    ]


def test_stats_for_11() -> None:
    stats = stats_for(11)

    assert stats.start == 11
    assert stats.steps == 14
    assert stats.maximum == 52


def test_stats_for_range_is_inclusive() -> None:
    assert [item.start for item in stats_for_range(3)] == [1, 2, 3]


@pytest.mark.parametrize("value", [0, -1])
def test_start_values_must_be_positive(value: int) -> None:
    with pytest.raises(ValueError):
        syracuse_sequence(value)
