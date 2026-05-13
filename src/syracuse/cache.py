from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sqlite3
from typing import Iterator

import numpy as np

from syracuse.analysis import DensityGrid
from syracuse.core import syracuse_next


@dataclass(frozen=True)
class CachedNode:
    next_value: int | None
    steps: int
    maximum: int


class SequenceCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                value INTEGER PRIMARY KEY,
                next_value INTEGER,
                steps INTEGER NOT NULL,
                maximum INTEGER NOT NULL
            )
            """
        )
        self.connection.commit()
        self.nodes = self._load_nodes()
        if 1 not in self.nodes:
            self.nodes[1] = CachedNode(next_value=None, steps=0, maximum=1)
            self._insert_nodes([(1, None, 0, 1)])

    def close(self) -> None:
        self.connection.close()

    def ensure_range(self, limit: int, *, batch_size: int = 50_000) -> None:
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        pending: list[tuple[int, int | None, int, int]] = []
        for start in range(1, limit + 1):
            if start in self.nodes:
                continue

            path = []
            current = start
            while current not in self.nodes:
                next_value = syracuse_next(current)
                path.append((current, next_value))
                current = next_value

            suffix = self.nodes[current]
            suffix_steps = suffix.steps
            suffix_maximum = suffix.maximum

            for value, next_value in reversed(path):
                steps = suffix_steps + 1
                maximum = max(value, suffix_maximum)
                self.nodes[value] = CachedNode(next_value=next_value, steps=steps, maximum=maximum)
                pending.append((value, next_value, steps, maximum))
                suffix_steps = steps
                suffix_maximum = maximum

            if len(pending) >= batch_size:
                self._insert_nodes(pending)
                pending.clear()

        if pending:
            self._insert_nodes(pending)

    def sequence(self, start: int) -> Iterator[int]:
        if start not in self.nodes:
            self.ensure_range(start)

        current: int | None = start
        while current is not None:
            yield current
            current = self.nodes[current].next_value

    def _load_nodes(self) -> dict[int, CachedNode]:
        rows = self.connection.execute("SELECT value, next_value, steps, maximum FROM nodes").fetchall()
        return {
            int(value): CachedNode(
                next_value=None if next_value is None else int(next_value),
                steps=int(steps),
                maximum=int(maximum),
            )
            for value, next_value, steps, maximum in rows
        }

    def _insert_nodes(self, rows: list[tuple[int, int | None, int, int]]) -> None:
        self.connection.executemany(
            "INSERT OR IGNORE INTO nodes(value, next_value, steps, maximum) VALUES (?, ?, ?, ?)",
            rows,
        )
        self.connection.commit()


def build_normalized_density_grid_from_cache(cache: SequenceCache, *, limit: int, bins: int) -> DensityGrid:
    if limit < 1:
        raise ValueError("limit must be greater than or equal to 1")
    if bins < 1:
        raise ValueError("bins must be greater than or equal to 1")

    cache.ensure_range(limit)
    max_step = max(cache.nodes[start].steps for start in range(1, limit + 1))
    max_value = max(cache.nodes[start].maximum for start in range(1, limit + 1))
    max_log_value = math.log10(max_value)
    counts = np.zeros((bins, bins), dtype=np.float64)
    total_points = 0

    for start in range(1, limit + 1):
        for step, value in enumerate(cache.sequence(start)):
            step_bin = min(int((step / max_step) * bins), bins - 1)
            log_value_bin = min(int((math.log10(value) / max_log_value) * bins), bins - 1)
            counts[step_bin, log_value_bin] += 1
            total_points += 1

    return DensityGrid(
        counts=counts,
        step_edges=np.linspace(0, 1, bins + 1),
        log_value_edges=np.linspace(0, 1, bins + 1),
        total_points=total_points,
    )


def build_fixed_normalized_support_mask_from_cache(
    cache: SequenceCache,
    *,
    start: int,
    stop: int,
    bins: int,
    max_step: int,
    max_value: int,
) -> np.ndarray:
    if start < 1:
        raise ValueError("start must be greater than or equal to 1")
    if stop < start:
        raise ValueError("stop must be greater than or equal to start")
    if bins < 1:
        raise ValueError("bins must be greater than or equal to 1")
    if max_step < 1:
        raise ValueError("max_step must be greater than or equal to 1")
    if max_value < 2:
        raise ValueError("max_value must be greater than or equal to 2")

    cache.ensure_range(stop)
    max_log_value = math.log10(max_value)
    mask = np.zeros((bins, bins), dtype=bool)

    for root in range(start, stop + 1):
        for step, value in enumerate(cache.sequence(root)):
            step_bin = min(int((step / max_step) * bins), bins - 1)
            log_value_bin = min(int((math.log10(value) / max_log_value) * bins), bins - 1)
            mask[step_bin, log_value_bin] = True

    return mask
