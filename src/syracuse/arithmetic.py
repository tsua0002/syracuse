from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from syracuse.cache import SequenceCache
from syracuse.core import two_adic_valuation


@dataclass(frozen=True)
class BlockArithmeticStats:
    start: int
    stop: int
    root_count: int
    mean_steps: float
    max_steps: int
    mean_log10_maximum: float
    max_log10_maximum: float
    mean_odd_ratio: float
    mean_odd_transition_count: float
    mean_compressed_length: float
    mean_exponent: float
    mean_exponent_one_ratio: float
    mean_net_log2_factor: float


@dataclass(frozen=True)
class SuffixArithmeticMetrics:
    odd_count: int
    odd_transition_count: int
    compressed_length: int
    exponent_sum: int
    exponent_one_count: int


def analyze_block_arithmetic(
    cache: SequenceCache,
    *,
    start: int,
    stop: int,
    metrics_cache: dict[int, SuffixArithmeticMetrics] | None = None,
) -> BlockArithmeticStats:
    if start < 1:
        raise ValueError("start must be greater than or equal to 1")
    if stop < start:
        raise ValueError("stop must be greater than or equal to start")

    cache.ensure_range(stop)
    resolved_metrics_cache = metrics_cache if metrics_cache is not None else _initial_metrics_cache()
    if 1 not in resolved_metrics_cache:
        resolved_metrics_cache.update(_initial_metrics_cache())
    root_count = stop - start + 1
    steps_values = []
    log_maxima = []
    odd_ratios = []
    odd_transition_counts = []
    compressed_lengths = []
    exponent_means = []
    exponent_one_ratios = []
    net_log2_factors = []

    for root in range(start, stop + 1):
        node = cache.nodes[root]
        metrics = suffix_arithmetic_metrics(cache, root, resolved_metrics_cache)
        parity_length = node.steps + 1

        steps_values.append(node.steps)
        log_maxima.append(np.log10(node.maximum))
        odd_ratios.append(metrics.odd_count / parity_length)
        odd_transition_counts.append(metrics.odd_transition_count)
        compressed_lengths.append(metrics.compressed_length)
        exponent_means.append(metrics.exponent_sum / metrics.compressed_length if metrics.compressed_length else 0.0)
        exponent_one_ratios.append(
            metrics.exponent_one_count / metrics.compressed_length if metrics.compressed_length else 0.0
        )
        net_log2_factors.append(metrics.compressed_length * np.log2(3) - metrics.exponent_sum)

    return BlockArithmeticStats(
        start=start,
        stop=stop,
        root_count=root_count,
        mean_steps=float(np.mean(steps_values)),
        max_steps=int(np.max(steps_values)),
        mean_log10_maximum=float(np.mean(log_maxima)),
        max_log10_maximum=float(np.max(log_maxima)),
        mean_odd_ratio=float(np.mean(odd_ratios)),
        mean_odd_transition_count=float(np.mean(odd_transition_counts)),
        mean_compressed_length=float(np.mean(compressed_lengths)),
        mean_exponent=float(np.mean(exponent_means)),
        mean_exponent_one_ratio=float(np.mean(exponent_one_ratios)),
        mean_net_log2_factor=float(np.mean(net_log2_factors)),
    )


def suffix_arithmetic_metrics(
    cache: SequenceCache,
    value: int,
    metrics_cache: dict[int, SuffixArithmeticMetrics],
) -> SuffixArithmeticMetrics:
    if 1 not in metrics_cache:
        metrics_cache.update(_initial_metrics_cache())
    if value in metrics_cache:
        return metrics_cache[value]

    path = []
    current = value
    while current not in metrics_cache:
        path.append(current)
        next_value = cache.nodes[current].next_value
        if next_value is None:
            break
        current = next_value

    suffix = metrics_cache.get(current, _initial_metrics_cache()[1])
    for current in reversed(path):
        next_value = cache.nodes[current].next_value
        has_next = next_value is not None
        is_odd = current % 2 == 1
        exponent = two_adic_valuation(3 * current + 1) if is_odd and has_next else 0

        suffix = SuffixArithmeticMetrics(
            odd_count=suffix.odd_count + (1 if is_odd else 0),
            odd_transition_count=suffix.odd_transition_count + (1 if is_odd and has_next else 0),
            compressed_length=suffix.compressed_length + (1 if is_odd and has_next else 0),
            exponent_sum=suffix.exponent_sum + exponent,
            exponent_one_count=suffix.exponent_one_count + (1 if exponent == 1 else 0),
        )
        metrics_cache[current] = suffix

    return metrics_cache[value]


def _initial_metrics_cache() -> dict[int, SuffixArithmeticMetrics]:
    return {
        1: SuffixArithmeticMetrics(
            odd_count=1,
            odd_transition_count=0,
            compressed_length=0,
            exponent_sum=0,
            exponent_one_count=0,
        )
    }


def export_block_arithmetic_stats(stats: tuple[BlockArithmeticStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(BlockArithmeticStats.__dataclass_fields__))
        writer.writeheader()
        for item in stats:
            writer.writerow(item.__dict__)


def plot_block_arithmetic(stats: tuple[BlockArithmeticStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stops = [item.stop for item in stats]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].plot(stops, [item.mean_steps for item in stats], marker="o")
    axes[0, 0].set_title("Mean stopping time by block")
    axes[0, 0].set_ylabel("mean steps")

    axes[0, 1].plot(stops, [item.mean_exponent for item in stats], marker="o", color="#4daf4a")
    axes[0, 1].axhline(np.log2(3), color="black", linestyle="--", linewidth=1)
    axes[0, 1].set_title("Mean compressed exponent")
    axes[0, 1].set_ylabel(r"mean $v_2(3m+1)$")

    axes[1, 0].plot(stops, [item.mean_exponent_one_ratio for item in stats], marker="o", color="#984ea3")
    axes[1, 0].set_title("Mean frequency of exponent 1")
    axes[1, 0].set_ylabel("mean ratio")

    axes[1, 1].plot(stops, [item.mean_net_log2_factor for item in stats], marker="o", color="#ff7f00")
    axes[1, 1].set_title("Mean net log2 growth budget")
    axes[1, 1].set_ylabel(r"mean $r\log_2(3)-\sum a_i$")

    for axis in axes.ravel():
        axis.set_xlabel("Block stop N")
        axis.set_xscale("log")

    fig.suptitle("Arithmetic diagnostics by root block")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_block_arithmetic_report(stats: tuple[BlockArithmeticStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Block Arithmetic Report",
        "",
        "This report aggregates arithmetic trajectory metrics by root block.",
        "",
        "| block | mean steps | max steps | mean exponent | freq exponent 1 | mean net log2 factor |",
        "|---:|---:|---:|---:|---:|---:|",
    ]

    for item in stats:
        lines.append(
            f"| {item.start}-{item.stop} | {item.mean_steps:.4f} | {item.max_steps} | "
            f"{item.mean_exponent:.4f} | {item.mean_exponent_one_ratio:.4f} | "
            f"{item.mean_net_log2_factor:.4f} |"
        )

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "The mean compressed exponent should be compared with log2(3). "
                "Values above log2(3) correspond to average contraction in the odd-to-odd compressed dynamics."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
