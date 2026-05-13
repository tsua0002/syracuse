from __future__ import annotations

from collections import Counter
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

from syracuse.core import SequenceStats, odd_compressed_trajectory


@dataclass(frozen=True)
class DensityGrid:
    counts: np.ndarray
    step_edges: np.ndarray
    log_value_edges: np.ndarray
    total_points: int


@dataclass(frozen=True)
class MetricGrid:
    means: np.ndarray
    counts: np.ndarray
    step_edges: np.ndarray
    log_value_edges: np.ndarray
    metric_name: str


@dataclass(frozen=True)
class ParityStats:
    start: int
    steps: int
    maximum: int
    parity_word: str
    odd_count: int
    even_count: int
    odd_transition_count: int
    zero_run_count: int
    max_zero_run: int
    mean_zero_run: float


@dataclass(frozen=True)
class OddCompressionStats:
    start: int
    odd_start: int
    compressed_length: int
    exponent_word: tuple[int, ...]
    exponent_sum: int
    exponent_mean: float
    exponent_one_count: int
    exponent_one_ratio: float
    net_log2_factor: float
    max_odd_value: int


def build_density_grid(
    stats: tuple[SequenceStats, ...],
    *,
    step_bins: int | None = None,
    log_value_bins: int = 240,
) -> DensityGrid:
    if not stats:
        raise ValueError("stats must not be empty")
    if log_value_bins < 1:
        raise ValueError("log_value_bins must be greater than or equal to 1")

    max_step = max(item.steps for item in stats)
    max_value = max(item.maximum for item in stats)
    resolved_step_bins = step_bins or max_step + 1

    steps = []
    log_values = []
    for item in stats:
        steps.extend(range(len(item.sequence)))
        log_values.extend(np.log10(item.sequence))

    counts, step_edges, log_value_edges = np.histogram2d(
        steps,
        log_values,
        bins=[resolved_step_bins, log_value_bins],
        range=[[0, max_step + 1], [0, np.log10(max_value)]],
    )

    return DensityGrid(
        counts=counts,
        step_edges=step_edges,
        log_value_edges=log_value_edges,
        total_points=len(steps),
    )


def build_normalized_density_grid(
    stats: tuple[SequenceStats, ...],
    *,
    bins: int = 1000,
) -> DensityGrid:
    if not stats:
        raise ValueError("stats must not be empty")
    if bins < 1:
        raise ValueError("bins must be greater than or equal to 1")

    max_step = max(item.steps for item in stats)
    max_value = max(item.maximum for item in stats)
    max_log_value = np.log10(max_value)

    normalized_steps = []
    normalized_log_values = []
    for item in stats:
        normalized_steps.extend(step / max_step for step in range(len(item.sequence)))
        normalized_log_values.extend(np.log10(item.sequence) / max_log_value)

    counts, step_edges, log_value_edges = np.histogram2d(
        normalized_steps,
        normalized_log_values,
        bins=[bins, bins],
        range=[[0, 1], [0, 1]],
    )

    return DensityGrid(
        counts=counts,
        step_edges=step_edges,
        log_value_edges=log_value_edges,
        total_points=len(normalized_steps),
    )


def build_parity_stats(stats: tuple[SequenceStats, ...]) -> tuple[ParityStats, ...]:
    if not stats:
        raise ValueError("stats must not be empty")

    return tuple(_parity_stats_for(item) for item in stats)


def build_odd_compression_stats(stats: tuple[SequenceStats, ...]) -> tuple[OddCompressionStats, ...]:
    if not stats:
        raise ValueError("stats must not be empty")

    return tuple(_odd_compression_stats_for(item) for item in stats)


def build_orbit_metric_grid(
    stats: tuple[SequenceStats, ...],
    metric_by_start: dict[int, float],
    *,
    metric_name: str,
    step_bins: int | None = None,
    log_value_bins: int = 240,
) -> MetricGrid:
    if not stats:
        raise ValueError("stats must not be empty")
    if log_value_bins < 1:
        raise ValueError("log_value_bins must be greater than or equal to 1")

    max_step = max(item.steps for item in stats)
    max_value = max(item.maximum for item in stats)
    resolved_step_bins = step_bins or max_step + 1

    steps = []
    log_values = []
    weights = []
    for item in stats:
        metric = metric_by_start[item.start]
        steps.extend(range(len(item.sequence)))
        log_values.extend(np.log10(item.sequence))
        weights.extend([metric] * len(item.sequence))

    counts, step_edges, log_value_edges = np.histogram2d(
        steps,
        log_values,
        bins=[resolved_step_bins, log_value_bins],
        range=[[0, max_step + 1], [0, np.log10(max_value)]],
    )
    weighted_sums, _, _ = np.histogram2d(
        steps,
        log_values,
        bins=[step_edges, log_value_edges],
        weights=weights,
    )

    means = np.divide(
        weighted_sums,
        counts,
        out=np.full_like(weighted_sums, np.nan, dtype=float),
        where=counts > 0,
    )
    return MetricGrid(
        means=means,
        counts=counts,
        step_edges=step_edges,
        log_value_edges=log_value_edges,
        metric_name=metric_name,
    )


def export_parity_summary(parity_stats: tuple[ParityStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "start",
                "steps_to_1",
                "maximum",
                "parity_word",
                "parity_length",
                "odd_count",
                "even_count",
                "odd_transition_count",
                "odd_ratio",
                "zero_run_count",
                "max_zero_run",
                "mean_zero_run",
                "first_16_bits",
                "last_16_bits",
            ],
        )
        writer.writeheader()
        for item in parity_stats:
            parity_length = len(item.parity_word)
            writer.writerow(
                {
                    "start": item.start,
                    "steps_to_1": item.steps,
                    "maximum": item.maximum,
                    "parity_word": item.parity_word,
                    "parity_length": parity_length,
                    "odd_count": item.odd_count,
                    "even_count": item.even_count,
                    "odd_transition_count": item.odd_transition_count,
                    "odd_ratio": item.odd_count / parity_length,
                    "zero_run_count": item.zero_run_count,
                    "max_zero_run": item.max_zero_run,
                    "mean_zero_run": f"{item.mean_zero_run:.4f}",
                    "first_16_bits": item.parity_word[:16],
                    "last_16_bits": item.parity_word[-16:],
                }
            )


def export_common_parity_prefixes(
    parity_stats: tuple[ParityStats, ...],
    path: Path,
    *,
    prefix_length: int = 16,
    top_count: int = 50,
) -> None:
    if prefix_length < 1:
        raise ValueError("prefix_length must be greater than or equal to 1")
    if top_count < 1:
        raise ValueError("top_count must be greater than or equal to 1")

    path.parent.mkdir(parents=True, exist_ok=True)
    prefixes = Counter(item.parity_word[:prefix_length] for item in parity_stats)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["prefix", "count", "frequency"])
        writer.writeheader()
        for prefix, count in prefixes.most_common(top_count):
            writer.writerow(
                {
                    "prefix": prefix,
                    "count": count,
                    "frequency": count / len(parity_stats),
                }
            )


def export_odd_compression_summary(compression_stats: tuple[OddCompressionStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "start",
                "odd_start",
                "compressed_length",
                "exponent_word",
                "exponent_sum",
                "exponent_mean",
                "exponent_one_count",
                "exponent_one_ratio",
                "net_log2_factor",
                "max_odd_value",
            ],
        )
        writer.writeheader()
        for item in compression_stats:
            writer.writerow(
                {
                    "start": item.start,
                    "odd_start": item.odd_start,
                    "compressed_length": item.compressed_length,
                    "exponent_word": " ".join(str(exponent) for exponent in item.exponent_word),
                    "exponent_sum": item.exponent_sum,
                    "exponent_mean": f"{item.exponent_mean:.6f}",
                    "exponent_one_count": item.exponent_one_count,
                    "exponent_one_ratio": f"{item.exponent_one_ratio:.6f}",
                    "net_log2_factor": f"{item.net_log2_factor:.6f}",
                    "max_odd_value": item.max_odd_value,
                }
            )


def plot_odd_compression_diagnostics(compression_stats: tuple[OddCompressionStats, ...], path: Path) -> None:
    if not compression_stats:
        raise ValueError("compression_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    compressed_lengths = np.array([item.compressed_length for item in compression_stats])
    exponent_means = np.array([item.exponent_mean for item in compression_stats])
    exponent_one_ratios = np.array([item.exponent_one_ratio for item in compression_stats])
    net_log2_factors = np.array([item.net_log2_factor for item in compression_stats])

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].hist(exponent_means, bins=40, color="#377eb8")
    axes[0, 0].axvline(np.log2(3), color="black", linestyle="--", linewidth=1, label=r"$\log_2(3)$")
    axes[0, 0].set_title("Mean exponent distribution")
    axes[0, 0].set_xlabel("mean of v2(3m+1)")
    axes[0, 0].set_ylabel("Count")
    axes[0, 0].legend()

    axes[0, 1].hist(exponent_one_ratios, bins=40, color="#4daf4a")
    axes[0, 1].set_title("Frequency of exponent 1")
    axes[0, 1].set_xlabel("count(a_i = 1) / compressed_length")
    axes[0, 1].set_ylabel("Count")

    axes[1, 0].scatter(compressed_lengths, net_log2_factors, s=4, alpha=0.35, color="#984ea3")
    axes[1, 0].axhline(0, color="black", linestyle="--", linewidth=1)
    axes[1, 0].set_title("Net compressed growth budget")
    axes[1, 0].set_xlabel("compressed length")
    axes[1, 0].set_ylabel(r"$L\log_2(3)-\sum a_i$")

    axes[1, 1].scatter(compressed_lengths, exponent_means, s=4, alpha=0.35, color="#ff7f00")
    axes[1, 1].axhline(np.log2(3), color="black", linestyle="--", linewidth=1)
    axes[1, 1].set_title("Mean exponent versus compressed length")
    axes[1, 1].set_xlabel("compressed length")
    axes[1, 1].set_ylabel("mean exponent")

    fig.suptitle("Odd-to-odd compressed Syracuse diagnostics")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_odd_compression_report(compression_stats: tuple[OddCompressionStats, ...], path: Path) -> None:
    if not compression_stats:
        raise ValueError("compression_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    non_empty = [item for item in compression_stats if item.compressed_length > 0]
    longest = max(non_empty, key=lambda item: item.compressed_length)
    highest_exponent_one_ratio = max(non_empty, key=lambda item: item.exponent_one_ratio)
    largest_net_growth = max(non_empty, key=lambda item: item.net_log2_factor)
    exponent_means = np.array([item.exponent_mean for item in non_empty])
    exponent_one_ratios = np.array([item.exponent_one_ratio for item in non_empty])
    net_log2_factors = np.array([item.net_log2_factor for item in non_empty])

    path.write_text(
        "\n".join(
            [
                "# Odd-To-Odd Compression Report",
                "",
                "For each odd value $m$, define:",
                "",
                "$$a(m)=v_2(3m+1), \\qquad C(m)=\\frac{3m+1}{2^{a(m)}}.$$",
                "",
                "The compressed trajectory keeps only odd values and labels each step by $a(m)$.",
                "",
                f"- Analysed starts: `{len(compression_stats)}`",
                f"- Non-empty compressed trajectories: `{len(non_empty)}`",
                f"- Mean exponent: `{exponent_means.mean():.4f}`",
                f"- Mean frequency of exponent `1`: `{exponent_one_ratios.mean():.4f}`",
                f"- Mean net log2 growth budget: `{net_log2_factors.mean():.4f}`",
                f"- Threshold $\\log_2(3)$: `{np.log2(3):.4f}`",
                "",
                "Extremal examples:",
                "",
                (
                    f"- Longest compressed trajectory: `n={longest.start}`, "
                    f"`compressed_length={longest.compressed_length}`, "
                    f"`mean_exponent={longest.exponent_mean:.4f}`, "
                    f"`net_log2_factor={longest.net_log2_factor:.4f}`"
                ),
                (
                    f"- Highest exponent-1 ratio: `n={highest_exponent_one_ratio.start}`, "
                    f"`ratio={highest_exponent_one_ratio.exponent_one_ratio:.4f}`, "
                    f"`compressed_length={highest_exponent_one_ratio.compressed_length}`"
                ),
                (
                    f"- Largest net growth budget: `n={largest_net_growth.start}`, "
                    f"`net_log2_factor={largest_net_growth.net_log2_factor:.4f}`, "
                    f"`compressed_length={largest_net_growth.compressed_length}`"
                ),
                "",
                "Reading guide:",
                "",
                (
                    "A compressed step has approximate multiplicative factor $3/2^{a_i}$. "
                    "Values $a_i=1$ locally expand the odd subsequence, while $a_i\\geq 2$ locally contract it. "
                    "The quantity $L\\log_2(3)-\\sum_i a_i$ summarizes the net log-scale growth budget over "
                    "a compressed trajectory of length $L$."
                ),
            ]
        ),
        encoding="utf-8",
    )


def plot_parity_diagnostics(parity_stats: tuple[ParityStats, ...], path: Path) -> None:
    if not parity_stats:
        raise ValueError("parity_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    steps = np.array([item.steps for item in parity_stats])
    odd_ratios = np.array([item.odd_count / len(item.parity_word) for item in parity_stats])
    max_zero_runs = np.array([item.max_zero_run for item in parity_stats])
    odd_transitions = np.array([item.odd_transition_count for item in parity_stats])

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].hist(odd_ratios, bins=40, color="#377eb8")
    axes[0, 0].set_title("Odd-value ratio distribution")
    axes[0, 0].set_xlabel("odd_count / parity_length")
    axes[0, 0].set_ylabel("Count")

    axes[0, 1].hist(max_zero_runs, bins=range(int(max_zero_runs.max()) + 2), color="#4daf4a")
    axes[0, 1].set_title("Longest run of even values")
    axes[0, 1].set_xlabel("max zero-run length")
    axes[0, 1].set_ylabel("Count")

    axes[1, 0].scatter(steps, odd_transitions, s=4, alpha=0.35, color="#984ea3")
    axes[1, 0].set_title("Odd transitions versus stopping time")
    axes[1, 0].set_xlabel("steps to reach 1")
    axes[1, 0].set_ylabel("odd transition count")

    axes[1, 1].scatter(steps, max_zero_runs, s=4, alpha=0.35, color="#ff7f00")
    axes[1, 1].set_title("Longest even run versus stopping time")
    axes[1, 1].set_xlabel("steps to reach 1")
    axes[1, 1].set_ylabel("max zero-run length")

    fig.suptitle("Parity diagnostics for Syracuse trajectories")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_parity_metric_heatmaps(
    stats: tuple[SequenceStats, ...],
    parity_stats: tuple[ParityStats, ...],
    path: Path,
    *,
    log_value_bins: int = 240,
) -> None:
    if not stats:
        raise ValueError("stats must not be empty")
    if not parity_stats:
        raise ValueError("parity_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    parity_by_start = {item.start: item for item in parity_stats}
    metric_grids = [
        build_orbit_metric_grid(
            stats,
            {item.start: item.odd_transition_count for item in parity_stats},
            metric_name="Mean odd transition count",
            log_value_bins=log_value_bins,
        ),
        build_orbit_metric_grid(
            stats,
            {item.start: item.odd_count / len(item.parity_word) for item in parity_stats},
            metric_name="Mean odd-value ratio",
            log_value_bins=log_value_bins,
        ),
        build_orbit_metric_grid(
            stats,
            {item.start: item.max_zero_run for item in parity_stats},
            metric_name="Mean longest zero-run",
            log_value_bins=log_value_bins,
        ),
        build_orbit_metric_grid(
            stats,
            {item.start: parity_by_start[item.start].steps for item in parity_stats},
            metric_name="Mean stopping time",
            log_value_bins=log_value_bins,
        ),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(16, 10), constrained_layout=True, sharex=True, sharey=True)

    for axis, grid in zip(axes.ravel(), metric_grids, strict=True):
        masked_means = np.ma.masked_invalid(grid.means.T)
        image = axis.imshow(
            masked_means,
            origin="lower",
            aspect="auto",
            extent=[
                grid.step_edges[0],
                grid.step_edges[-1],
                grid.log_value_edges[0],
                grid.log_value_edges[-1],
            ],
            cmap="viridis",
        )
        color_bar = fig.colorbar(image, ax=axis)
        color_bar.set_label(grid.metric_name)
        axis.set_title(grid.metric_name)
        axis.set_xlabel("Step")
        axis.set_ylabel(r"$\log_{10}(u_k(n))$")

    fig.suptitle("Parity metrics projected on Syracuse orbit density support")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_parity_heatmap_report(parity_stats: tuple[ParityStats, ...], path: Path) -> None:
    if not parity_stats:
        raise ValueError("parity_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_by_steps = sorted(parity_stats, key=lambda item: item.steps, reverse=True)[:10]
    sorted_by_zero_run = sorted(parity_stats, key=lambda item: item.max_zero_run, reverse=True)[:10]

    lines = [
        "# Parity Heatmap Cross Analysis",
        "",
        "The parity metric heatmaps project trajectory-level parity metrics onto each visited point.",
        "",
        "For a cell in the plane, the displayed value is the average metric among all trajectories visiting that cell.",
        "",
        "This helps identify whether visual regions are mostly carried by trajectories with many odd transitions, high odd ratios, long even runs, or long stopping times.",
        "",
        "## Longest stopping times",
        "",
        "| start | steps | odd transitions | odd ratio | max zero-run | maximum |",
        "|---:|---:|---:|---:|---:|---:|",
    ]

    for item in sorted_by_steps:
        odd_ratio = item.odd_count / len(item.parity_word)
        lines.append(
            f"| {item.start} | {item.steps} | {item.odd_transition_count} | "
            f"{odd_ratio:.4f} | {item.max_zero_run} | {item.maximum} |"
        )

    lines.extend(
        [
            "",
            "## Longest even runs",
            "",
            "| start | max zero-run | steps | odd transitions | odd ratio | maximum |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for item in sorted_by_zero_run:
        odd_ratio = item.odd_count / len(item.parity_word)
        lines.append(
            f"| {item.start} | {item.max_zero_run} | {item.steps} | "
            f"{item.odd_transition_count} | {odd_ratio:.4f} | {item.maximum} |"
        )

    lines.extend(
        [
            "",
            "Initial reading:",
            "",
            (
                "Long stopping times are mainly associated with many odd transitions, not simply with a single long run "
                "of divisions by 2. Long zero-runs appear as sharp descent events and can occur in comparatively short trajectories."
            ),
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_parity_report(parity_stats: tuple[ParityStats, ...], path: Path) -> None:
    if not parity_stats:
        raise ValueError("parity_stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    steps = np.array([item.steps for item in parity_stats])
    odd_ratios = np.array([item.odd_count / len(item.parity_word) for item in parity_stats])
    max_zero_runs = np.array([item.max_zero_run for item in parity_stats])
    odd_transitions = np.array([item.odd_transition_count for item in parity_stats])
    longest = max(parity_stats, key=lambda item: item.steps)
    most_odd_transitions = max(parity_stats, key=lambda item: item.odd_transition_count)
    longest_zero_run = max(parity_stats, key=lambda item: item.max_zero_run)

    path.write_text(
        "\n".join(
            [
                "# Syracuse Parity Report",
                "",
                "Each trajectory is encoded by the binary word:",
                "",
                r"$$\varepsilon_k(n)=u_k(n)\bmod 2.$$",
                "",
                "A `1` marks an odd value and a `0` marks an even value.",
                "",
                f"- Analysed starts: `{len(parity_stats)}`",
                f"- Mean stopping time: `{steps.mean():.2f}`",
                f"- Mean odd-value ratio: `{odd_ratios.mean():.4f}`",
                f"- Mean odd transition count: `{odd_transitions.mean():.2f}`",
                f"- Mean longest zero-run: `{max_zero_runs.mean():.2f}`",
                "",
                "Extremal examples:",
                "",
                (
                    f"- Longest trajectory: `n={longest.start}`, "
                    f"`steps={longest.steps}`, `odd_transitions={longest.odd_transition_count}`"
                ),
                (
                    f"- Most odd transitions: `n={most_odd_transitions.start}`, "
                    f"`odd_transitions={most_odd_transitions.odd_transition_count}`, "
                    f"`steps={most_odd_transitions.steps}`"
                ),
                (
                    f"- Longest even run: `n={longest_zero_run.start}`, "
                    f"`max_zero_run={longest_zero_run.max_zero_run}`, "
                    f"`steps={longest_zero_run.steps}`"
                ),
                "",
                "Reading guide:",
                "",
                (
                    "Long runs of `0` correspond to repeated divisions by 2. "
                    "Large odd-transition counts indicate trajectories with many upward `3n+1` moves. "
                    "Comparing these metrics with the heatmap helps connect visual strata to parity patterns."
                ),
            ]
        ),
        encoding="utf-8",
    )


def _parity_stats_for(stats: SequenceStats) -> ParityStats:
    parity_word = "".join(str(value % 2) for value in stats.sequence)
    zero_runs = _zero_run_lengths(parity_word)
    odd_count = parity_word.count("1")
    even_count = parity_word.count("0")

    return ParityStats(
        start=stats.start,
        steps=stats.steps,
        maximum=stats.maximum,
        parity_word=parity_word,
        odd_count=odd_count,
        even_count=even_count,
        odd_transition_count=sum(1 for value in stats.sequence[:-1] if value % 2 == 1),
        zero_run_count=len(zero_runs),
        max_zero_run=max(zero_runs, default=0),
        mean_zero_run=sum(zero_runs) / len(zero_runs) if zero_runs else 0.0,
    )


def _zero_run_lengths(parity_word: str) -> tuple[int, ...]:
    runs = []
    current_run = 0

    for bit in parity_word:
        if bit == "0":
            current_run += 1
        elif current_run:
            runs.append(current_run)
            current_run = 0

    if current_run:
        runs.append(current_run)

    return tuple(runs)


def _odd_compression_stats_for(stats: SequenceStats) -> OddCompressionStats:
    compressed_steps = odd_compressed_trajectory(stats.start)
    exponent_word = tuple(step.exponent for step in compressed_steps)
    odd_values = tuple(value for value in stats.sequence if value % 2 == 1)
    compressed_length = len(exponent_word)
    exponent_sum = sum(exponent_word)
    exponent_one_count = exponent_word.count(1)

    return OddCompressionStats(
        start=stats.start,
        odd_start=odd_values[0],
        compressed_length=compressed_length,
        exponent_word=exponent_word,
        exponent_sum=exponent_sum,
        exponent_mean=exponent_sum / compressed_length if compressed_length else 0.0,
        exponent_one_count=exponent_one_count,
        exponent_one_ratio=exponent_one_count / compressed_length if compressed_length else 0.0,
        net_log2_factor=compressed_length * np.log2(3) - exponent_sum,
        max_odd_value=max(odd_values),
    )


def save_density_grid(grid: DensityGrid, output_prefix: Path) -> None:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_prefix.with_suffix(".npy"), grid.counts)

    with output_prefix.with_suffix(".csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["step_bin", "log_value_bin", "count"])
        non_zero_step_bins, non_zero_log_value_bins = np.nonzero(grid.counts)
        for step_bin, log_value_bin in zip(non_zero_step_bins, non_zero_log_value_bins, strict=True):
            writer.writerow([step_bin, log_value_bin, int(grid.counts[step_bin, log_value_bin])])


def plot_density_heatmap(
    grid: DensityGrid,
    path: Path,
    *,
    title: str = "Density of Syracuse orbit visits",
    x_label: str = "Step",
    y_label: str = r"$\log_{10}(u_k(n))$",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    positive_counts = grid.counts[grid.counts > 0]
    norm = LogNorm(vmin=1, vmax=max(1, positive_counts.max()))

    fig, ax = plt.subplots(figsize=(14, 8), constrained_layout=True)
    image = ax.imshow(
        grid.counts.T,
        origin="lower",
        aspect="auto",
        extent=[
            grid.step_edges[0],
            grid.step_edges[-1],
            grid.log_value_edges[0],
            grid.log_value_edges[-1],
        ],
        cmap="magma",
        norm=norm,
    )

    color_bar = fig.colorbar(image, ax=ax)
    color_bar.set_label("Number of visits per cell (log scale)")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(False)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_density_resolution_comparison(grids: dict[int, DensityGrid], path: Path) -> None:
    if not grids:
        raise ValueError("grids must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    ordered_items = sorted(grids.items())
    max_count = max(float(grid.counts.max()) for _, grid in ordered_items)
    norm = LogNorm(vmin=1, vmax=max(1, max_count))

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(16, 10),
        constrained_layout=True,
        sharex=True,
        sharey=True,
    )
    flattened_axes = axes.ravel()
    last_image = None

    for axis, (log_value_bins, grid) in zip(flattened_axes, ordered_items, strict=True):
        last_image = axis.imshow(
            grid.counts.T,
            origin="lower",
            aspect="auto",
            extent=[
                grid.step_edges[0],
                grid.step_edges[-1],
                grid.log_value_edges[0],
                grid.log_value_edges[-1],
            ],
            cmap="magma",
            norm=norm,
        )
        occupied_cells = int(np.count_nonzero(grid.counts))
        occupied_ratio = occupied_cells / grid.counts.size
        axis.set_title(f"{log_value_bins} vertical bins, occupied={occupied_ratio:.1%}")
        axis.set_xlabel("Step")
        axis.set_ylabel(r"$\log_{10}(u_k(n))$")

    for axis in flattened_axes[len(ordered_items) :]:
        axis.axis("off")

    if last_image is not None:
        color_bar = fig.colorbar(last_image, ax=flattened_axes.tolist())
        color_bar.set_label("Number of visits per cell (shared log scale)")

    fig.suptitle("Density robustness across vertical bin resolutions")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_density_resolution_report(grids: dict[int, DensityGrid], path: Path) -> None:
    if not grids:
        raise ValueError("grids must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Density Resolution Comparison",
        "",
        "This report compares the same empirical measure across several vertical bin resolutions.",
        "",
        "| vertical bins | occupied cells | total cells | occupied ratio | max visits in one cell |",
        "|---:|---:|---:|---:|---:|",
    ]

    for log_value_bins, grid in sorted(grids.items()):
        occupied_cells = int(np.count_nonzero(grid.counts))
        total_cells = int(grid.counts.size)
        occupied_ratio = occupied_cells / total_cells
        max_cell_count = int(grid.counts.max())
        lines.append(
            f"| {log_value_bins} | {occupied_cells} | {total_cells} | "
            f"{occupied_ratio:.4%} | {max_cell_count} |"
        )

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "If the same high-density regions remain visible while the occupied ratio and cell counts change, "
                "the structure is likely robust at this scale. If the regions move or disappear, the apparent "
                "continuity is mostly a binning artifact."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_density_report(grid: DensityGrid, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    non_zero_cells = int(np.count_nonzero(grid.counts))
    total_cells = int(grid.counts.size)
    max_cell_count = int(grid.counts.max())
    occupied_ratio = non_zero_cells / total_cells
    densest_step_bin, densest_log_value_bin = np.unravel_index(np.argmax(grid.counts), grid.counts.shape)

    step_start = grid.step_edges[densest_step_bin]
    step_end = grid.step_edges[densest_step_bin + 1]
    log_value_start = grid.log_value_edges[densest_log_value_bin]
    log_value_end = grid.log_value_edges[densest_log_value_bin + 1]

    path.write_text(
        "\n".join(
            [
                "# Syracuse Density Report",
                "",
                "The heatmap approximates the empirical measure:",
                "",
                r"$$\mu_N(A)=\#\{(n,k):(k,\log_{10}(u_k(n)))\in A\}.$$",
                "",
                f"- Total orbit points: `{grid.total_points}`",
                f"- Occupied cells: `{non_zero_cells}` / `{total_cells}`",
                f"- Occupied ratio: `{occupied_ratio:.4%}`",
                f"- Maximum visits in one cell: `{max_cell_count}`",
                (
                    "- Densest cell: "
                    f"step in `[{step_start:.2f}, {step_end:.2f})`, "
                    f"log-value in `[{log_value_start:.3f}, {log_value_end:.3f})`"
                ),
                "",
                "Interpretation:",
                "",
                (
                    "A low occupied ratio means the trajectories do not cover the rectangle uniformly. "
                    "The heatmap should therefore be read as a structured discrete measure rather than as a surface."
                ),
            ]
        ),
        encoding="utf-8",
    )
