from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SequenceStats:
    start: int
    steps: int
    maximum: int
    sequence: tuple[int, ...]


@dataclass(frozen=True)
class OddCompressedStep:
    source: int
    exponent: int
    target: int


def _validate_positive_integer(value: int, *, name: str = "value") -> None:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 1:
        raise ValueError(f"{name} must be greater than or equal to 1")


def syracuse_next(n: int) -> int:
    """Return the next value of the Syracuse/Collatz function."""
    _validate_positive_integer(n, name="n")
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def two_adic_valuation(n: int) -> int:
    """Return v2(n), the exponent of the largest power of 2 dividing n."""
    _validate_positive_integer(n, name="n")
    exponent = 0
    current = n
    while current % 2 == 0:
        exponent += 1
        current //= 2
    return exponent


def odd_compressed_next(odd_n: int) -> OddCompressedStep:
    """Return the next odd-to-odd compressed Syracuse step."""
    _validate_positive_integer(odd_n, name="odd_n")
    if odd_n % 2 == 0:
        raise ValueError("odd_n must be odd")

    expanded = 3 * odd_n + 1
    exponent = two_adic_valuation(expanded)
    return OddCompressedStep(
        source=odd_n,
        exponent=exponent,
        target=expanded // (2**exponent),
    )


def odd_compressed_trajectory(start: int) -> tuple[OddCompressedStep, ...]:
    """Return odd-to-odd compressed steps until 1 is reached."""
    _validate_positive_integer(start, name="start")
    current = start
    while current % 2 == 0:
        current //= 2

    steps = []
    while current != 1:
        step = odd_compressed_next(current)
        steps.append(step)
        current = step.target

    return tuple(steps)


def syracuse_sequence(start: int) -> tuple[int, ...]:
    """Return the complete sequence from start until 1 is reached."""
    _validate_positive_integer(start, name="start")
    values = [start]

    while values[-1] != 1:
        values.append(syracuse_next(values[-1]))

    return tuple(values)


def stats_for(start: int) -> SequenceStats:
    sequence = syracuse_sequence(start)
    return _stats_from_sequence(start, sequence)


def stats_for_range(limit: int) -> tuple[SequenceStats, ...]:
    _validate_positive_integer(limit, name="limit")
    sequences = _memoized_sequences_for_range(limit)
    return tuple(_stats_from_sequence(start, sequences[start]) for start in range(1, limit + 1))


def _memoized_sequences_for_range(limit: int) -> dict[int, tuple[int, ...]]:
    sequences = {1: (1,)}

    for start in range(1, limit + 1):
        if start in sequences:
            continue

        path = []
        current = start
        while current not in sequences:
            path.append(current)
            current = syracuse_next(current)

        known_suffix = sequences[current]
        full_path = tuple(path) + known_suffix
        for index, value in enumerate(path):
            sequences[value] = full_path[index:]

    return sequences


def _stats_from_sequence(start: int, sequence: tuple[int, ...]) -> SequenceStats:
    return SequenceStats(
        start=start,
        steps=len(sequence) - 1,
        maximum=max(sequence),
        sequence=sequence,
    )
