from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

from syracuse.analysis import DensityGrid


CONNECTIVITY_8 = np.ones((3, 3), dtype=bool)


@dataclass(frozen=True)
class DenseSupportStats:
    threshold: int
    epsilon: int
    occupied_cells: int
    dilated_cells: int
    beta0_before: int
    beta0_after: int
    beta1_before: int
    beta1_after: int
    largest_component_before: int
    largest_component_after: int
    largest_inscribed_radius: float
    radius_step_center: float
    radius_log_value_center: float


@dataclass(frozen=True)
class EpsilonSweepStats:
    limit: int
    bins: int
    threshold: int
    epsilon_cells: int
    epsilon_normalized: float
    largest_inscribed_radius_cells: float
    largest_inscribed_radius_normalized: float
    occupied_cells: int
    beta0_before: int
    beta1_after: int


@dataclass(frozen=True)
class BlockAttachmentStats:
    start: int
    stop: int
    bins: int
    added_cells: int
    previous_cells: int
    min_distance_cells: float
    min_distance_normalized: float
    max_distance_cells: float
    max_distance_normalized: float
    mean_distance_cells: float
    mean_distance_normalized: float


@dataclass(frozen=True)
class AlphaAttachmentStats:
    start: int
    stop: int
    bins: int
    alpha: float
    added_cells: int
    min_distance: float
    mean_distance: float
    max_distance: float


def analyze_dense_supports(
    grid: DensityGrid,
    *,
    thresholds: tuple[int, ...] = (1, 2, 5, 10, 20, 50, 100),
) -> tuple[DenseSupportStats, ...]:
    return tuple(analyze_dense_support(grid, threshold=threshold) for threshold in thresholds)


def summarize_epsilon_sweep_item(
    *,
    limit: int,
    bins: int,
    threshold: int,
    stats: DenseSupportStats,
) -> EpsilonSweepStats:
    return EpsilonSweepStats(
        limit=limit,
        bins=bins,
        threshold=threshold,
        epsilon_cells=stats.epsilon,
        epsilon_normalized=stats.epsilon / bins,
        largest_inscribed_radius_cells=stats.largest_inscribed_radius,
        largest_inscribed_radius_normalized=stats.largest_inscribed_radius / bins,
        occupied_cells=stats.occupied_cells,
        beta0_before=stats.beta0_before,
        beta1_after=stats.beta1_after,
    )


def analyze_dense_support(grid: DensityGrid, *, threshold: int) -> DenseSupportStats:
    if threshold < 1:
        raise ValueError("threshold must be greater than or equal to 1")

    mask = dense_support_mask(grid, threshold=threshold)
    beta0_before, largest_before = component_summary(mask)
    beta1_before = count_holes(mask)
    epsilon = minimal_connection_epsilon(mask)
    dilated_mask = dilate_mask(mask, epsilon=epsilon)
    beta0_after, largest_after = component_summary(dilated_mask)
    beta1_after = count_holes(dilated_mask)
    radius, radius_indices = largest_inscribed_radius(dilated_mask)
    radius_step_center, radius_log_value_center = cell_center(grid, radius_indices)

    return DenseSupportStats(
        threshold=threshold,
        epsilon=epsilon,
        occupied_cells=int(mask.sum()),
        dilated_cells=int(dilated_mask.sum()),
        beta0_before=beta0_before,
        beta0_after=beta0_after,
        beta1_before=beta1_before,
        beta1_after=beta1_after,
        largest_component_before=largest_before,
        largest_component_after=largest_after,
        largest_inscribed_radius=radius,
        radius_step_center=radius_step_center,
        radius_log_value_center=radius_log_value_center,
    )


def dense_support_mask(grid: DensityGrid, *, threshold: int) -> np.ndarray:
    return grid.counts >= threshold


def component_summary(mask: np.ndarray) -> tuple[int, int]:
    labels, component_count = ndimage.label(mask, structure=CONNECTIVITY_8)
    if component_count == 0:
        return 0, 0

    component_sizes = np.bincount(labels.ravel())[1:]
    return int(component_count), int(component_sizes.max())


def count_holes(mask: np.ndarray) -> int:
    padded_mask = np.pad(mask, pad_width=1, mode="constant", constant_values=False)
    background_labels, background_count = ndimage.label(~padded_mask, structure=CONNECTIVITY_8)
    if background_count == 0:
        return 0

    border_labels = set(background_labels[0, :])
    border_labels.update(background_labels[-1, :])
    border_labels.update(background_labels[:, 0])
    border_labels.update(background_labels[:, -1])
    hole_labels = set(range(1, background_count + 1)) - border_labels
    return len(hole_labels)


def dilate_mask(mask: np.ndarray, *, epsilon: int) -> np.ndarray:
    if epsilon < 0:
        raise ValueError("epsilon must be greater than or equal to 0")
    if epsilon == 0:
        return mask.copy()
    return ndimage.binary_dilation(mask, structure=CONNECTIVITY_8, iterations=epsilon)


def minimal_connection_epsilon(mask: np.ndarray, *, max_epsilon: int | None = None) -> int:
    component_count, _ = component_summary(mask)
    if component_count <= 1:
        return 0

    resolved_max_epsilon = max_epsilon or max(mask.shape)
    for epsilon in range(1, resolved_max_epsilon + 1):
        dilated = dilate_mask(mask, epsilon=epsilon)
        dilated_component_count, _ = component_summary(dilated)
        if dilated_component_count <= 1:
            return epsilon

    return resolved_max_epsilon


def largest_inscribed_radius(mask: np.ndarray) -> tuple[float, tuple[int, int]]:
    if not mask.any():
        return 0.0, (0, 0)

    padded_mask = np.pad(mask, pad_width=1, mode="constant", constant_values=False)
    distances = ndimage.distance_transform_edt(padded_mask)[1:-1, 1:-1]
    flat_index = int(np.argmax(distances))
    indices = np.unravel_index(flat_index, distances.shape)
    return float(distances[indices]), (int(indices[0]), int(indices[1]))


def cell_center(grid: DensityGrid, indices: tuple[int, int]) -> tuple[float, float]:
    step_index, log_value_index = indices
    step_center = (grid.step_edges[step_index] + grid.step_edges[step_index + 1]) / 2
    log_value_center = (grid.log_value_edges[log_value_index] + grid.log_value_edges[log_value_index + 1]) / 2
    return float(step_center), float(log_value_center)


def export_dense_support_stats(stats: tuple[DenseSupportStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(DenseSupportStats.__dataclass_fields__))
        writer.writeheader()
        for item in stats:
            writer.writerow(item.__dict__)


def export_epsilon_sweep_stats(stats: tuple[EpsilonSweepStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(EpsilonSweepStats.__dataclass_fields__))
        writer.writeheader()
        for item in stats:
            writer.writerow(item.__dict__)


def analyze_block_attachment(
    *,
    previous_mask: np.ndarray,
    block_mask: np.ndarray,
    start: int,
    stop: int,
) -> BlockAttachmentStats:
    if previous_mask.shape != block_mask.shape:
        raise ValueError("previous_mask and block_mask must have the same shape")
    if not previous_mask.any():
        raise ValueError("previous_mask must not be empty")

    new_cells = block_mask & ~previous_mask
    if not new_cells.any():
        return BlockAttachmentStats(
            start=start,
            stop=stop,
            bins=previous_mask.shape[0],
            added_cells=0,
            previous_cells=int(previous_mask.sum()),
            min_distance_cells=0.0,
            min_distance_normalized=0.0,
            max_distance_cells=0.0,
            max_distance_normalized=0.0,
            mean_distance_cells=0.0,
            mean_distance_normalized=0.0,
        )

    distances = ndimage.distance_transform_edt(~previous_mask)
    new_distances = distances[new_cells]
    bins = previous_mask.shape[0]
    return BlockAttachmentStats(
        start=start,
        stop=stop,
        bins=bins,
        added_cells=int(new_cells.sum()),
        previous_cells=int(previous_mask.sum()),
        min_distance_cells=float(new_distances.min()),
        min_distance_normalized=float(new_distances.min() / bins),
        max_distance_cells=float(new_distances.max()),
        max_distance_normalized=float(new_distances.max() / bins),
        mean_distance_cells=float(new_distances.mean()),
        mean_distance_normalized=float(new_distances.mean() / bins),
    )


def analyze_alpha_attachment(
    *,
    previous_mask: np.ndarray,
    block_mask: np.ndarray,
    start: int,
    stop: int,
    alpha: float,
) -> AlphaAttachmentStats:
    if previous_mask.shape != block_mask.shape:
        raise ValueError("previous_mask and block_mask must have the same shape")
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    if not previous_mask.any():
        raise ValueError("previous_mask must not be empty")

    new_cells = block_mask & ~previous_mask
    if not new_cells.any():
        return AlphaAttachmentStats(
            start=start,
            stop=stop,
            bins=previous_mask.shape[0],
            alpha=alpha,
            added_cells=0,
            min_distance=0.0,
            mean_distance=0.0,
            max_distance=0.0,
        )

    bins = previous_mask.shape[0]
    # Axis 0 is normalized time and is weighted by alpha in d_alpha.
    distances = ndimage.distance_transform_edt(~previous_mask, sampling=(alpha / bins, 1 / bins))
    new_distances = distances[new_cells]
    return AlphaAttachmentStats(
        start=start,
        stop=stop,
        bins=bins,
        alpha=alpha,
        added_cells=int(new_cells.sum()),
        min_distance=float(new_distances.min()),
        mean_distance=float(new_distances.mean()),
        max_distance=float(new_distances.max()),
    )


def export_block_attachment_stats(stats: tuple[BlockAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(BlockAttachmentStats.__dataclass_fields__))
        writer.writeheader()
        for item in stats:
            writer.writerow(item.__dict__)


def export_alpha_attachment_stats(stats: tuple[AlphaAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(AlphaAttachmentStats.__dataclass_fields__))
        writer.writeheader()
        for item in stats:
            writer.writerow(item.__dict__)


def plot_block_attachment(stats: tuple[BlockAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stops = [item.stop for item in stats]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].plot(stops, [item.min_distance_normalized for item in stats], marker="o")
    axes[0, 0].set_title("Minimum attachment distance")
    axes[0, 0].set_xlabel("Block stop N")
    axes[0, 0].set_ylabel("normalized distance")
    axes[0, 0].set_xscale("log")

    axes[0, 1].plot(stops, [item.mean_distance_normalized for item in stats], marker="o", color="#4daf4a")
    axes[0, 1].set_title("Mean new-cell distance to previous support")
    axes[0, 1].set_xlabel("Block stop N")
    axes[0, 1].set_ylabel("normalized distance")
    axes[0, 1].set_xscale("log")

    axes[1, 0].plot(stops, [item.max_distance_normalized for item in stats], marker="o", color="#e41a1c")
    axes[1, 0].set_title("Maximum new-cell distance to previous support")
    axes[1, 0].set_xlabel("Block stop N")
    axes[1, 0].set_ylabel("normalized distance")
    axes[1, 0].set_xscale("log")

    axes[1, 1].plot(stops, [item.added_cells for item in stats], marker="o", color="#984ea3")
    axes[1, 1].set_title("New cells added by block")
    axes[1, 1].set_xlabel("Block stop N")
    axes[1, 1].set_ylabel("cells")
    axes[1, 1].set_xscale("log")

    fig.suptitle("Block attachment distances in a fixed normalized grid")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_alpha_attachment(stats: tuple[AlphaAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)
    alphas = sorted({item.alpha for item in stats})

    for alpha in alphas:
        alpha_stats = [item for item in stats if item.alpha == alpha]
        stops = [item.stop for item in alpha_stats]
        axes[0].plot(stops, [item.min_distance for item in alpha_stats], marker="o", label=f"alpha={alpha}")
        axes[1].plot(stops, [item.mean_distance for item in alpha_stats], marker="o", label=f"alpha={alpha}")
        axes[2].plot(stops, [item.max_distance for item in alpha_stats], marker="o", label=f"alpha={alpha}")

    axes[0].set_title("Minimum attachment distance")
    axes[1].set_title("Mean attachment distance")
    axes[2].set_title("Maximum attachment distance")
    for axis in axes:
        axis.set_xlabel("Block stop N")
        axis.set_ylabel(r"$d_\alpha$")
        axis.set_xscale("log")
        axis.legend()

    fig.suptitle(r"Block attachment distances under $d_\alpha$")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_block_attachment_maps(
    maps: tuple[tuple[int, int, np.ndarray, np.ndarray], ...],
    path: Path,
    *,
    max_blocks: int = 6,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    selected_maps = maps[-max_blocks:]
    fig, axes = plt.subplots(2, len(selected_maps), figsize=(4 * len(selected_maps), 8), constrained_layout=True)

    if len(selected_maps) == 1:
        axes = np.array([[axes[0]], [axes[1]]])

    max_distance = max(float(distances[new_cells].max()) for _, _, new_cells, distances in selected_maps if new_cells.any())

    for column, (start, stop, new_cells, distances) in enumerate(selected_maps):
        axes[0, column].imshow(
            new_cells.T,
            origin="lower",
            aspect="auto",
            extent=[0, 1, 0, 1],
            cmap="gray_r",
        )
        axes[0, column].set_title(f"New cells\n{start}-{stop}")
        axes[0, column].set_xlabel("normalized step")
        axes[0, column].set_ylabel("normalized log-value")

        shown_distances = np.where(new_cells, distances, np.nan).T
        image = axes[1, column].imshow(
            shown_distances,
            origin="lower",
            aspect="auto",
            extent=[0, 1, 0, 1],
            cmap="magma",
            vmin=0,
            vmax=max_distance,
        )
        axes[1, column].set_title("Distance to previous support")
        axes[1, column].set_xlabel("normalized step")
        axes[1, column].set_ylabel("normalized log-value")

    color_bar = fig.colorbar(image, ax=axes.ravel().tolist())
    color_bar.set_label("distance in cells")
    fig.suptitle("Localization of newly added support cells")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_block_attachment_report(stats: tuple[BlockAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Block Attachment Report",
        "",
        "This report measures how far newly added support cells are from the previous support in a fixed grid.",
        "",
        "| block | added cells | min distance | mean distance | max distance |",
        "|---:|---:|---:|---:|---:|",
    ]

    for item in stats:
        lines.append(
            f"| {item.start}-{item.stop} | {item.added_cells} | "
            f"{item.min_distance_normalized:.6f} | {item.mean_distance_normalized:.6f} | "
            f"{item.max_distance_normalized:.6f} |"
        )

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "The minimum distance checks whether each new block touches the previous support at grid scale. "
                "The mean and maximum distances describe how far the genuinely new cells extend away from the known support."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_alpha_attachment_report(stats: tuple[AlphaAttachmentStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Alpha Attachment Report",
        "",
        "This report measures block attachment distances under the fixed metric:",
        "",
        "$$d_\\alpha((x,y),(x',y'))=\\sqrt{\\alpha^2(x-x')^2+(y-y')^2}.$$",
        "",
        "| alpha | block | added cells | min distance | mean distance | max distance |",
        "|---:|---:|---:|---:|---:|---:|",
    ]

    for item in stats:
        lines.append(
            f"| {item.alpha:.4f} | {item.start}-{item.stop} | {item.added_cells} | "
            f"{item.min_distance:.6f} | {item.mean_distance:.6f} | {item.max_distance:.6f} |"
        )

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "Small minimum distances across alpha values indicate that each new block touches the previous support "
                "robustly, not only because of a particular axis scaling. Mean and maximum distances describe the spread "
                "of genuinely new regions under the chosen metric."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def plot_dense_support_masks(
    grid: DensityGrid,
    stats: tuple[DenseSupportStats, ...],
    path: Path,
    *,
    max_columns: int = 4,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    selected_stats = stats[:max_columns]
    fig, axes = plt.subplots(2, len(selected_stats), figsize=(4 * len(selected_stats), 8), constrained_layout=True)

    if len(selected_stats) == 1:
        axes = np.array([[axes[0]], [axes[1]]])

    for column, item in enumerate(selected_stats):
        mask = dense_support_mask(grid, threshold=item.threshold)
        dilated = dilate_mask(mask, epsilon=item.epsilon)
        for row, shown_mask in enumerate((mask, dilated)):
            axis = axes[row, column]
            axis.imshow(
                shown_mask.T,
                origin="lower",
                aspect="auto",
                extent=[
                    grid.step_edges[0],
                    grid.step_edges[-1],
                    grid.log_value_edges[0],
                    grid.log_value_edges[-1],
                ],
                cmap="gray_r",
            )
            title_prefix = "Raw" if row == 0 else f"Thickened eps={item.epsilon}"
            axis.set_title(f"{title_prefix}, threshold={item.threshold}")
            axis.set_xlabel("Step")
            axis.set_ylabel(r"$\log_{10}(u_k(n))$")

    fig.suptitle("Dense support masks before and after minimal thickening")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_epsilon_sweep(stats: tuple[EpsilonSweepStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    limits = [item.limit for item in stats]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].plot(limits, [item.epsilon_normalized for item in stats], marker="o")
    axes[0, 0].set_title(r"Normalized connection scale $\varepsilon_*(N)$")
    axes[0, 0].set_xlabel("N")
    axes[0, 0].set_ylabel("normalized epsilon")
    axes[0, 0].set_xscale("log")

    axes[0, 1].plot(limits, [item.largest_inscribed_radius_normalized for item in stats], marker="o", color="#4daf4a")
    axes[0, 1].set_title("Normalized largest inscribed radius")
    axes[0, 1].set_xlabel("N")
    axes[0, 1].set_ylabel("normalized radius")
    axes[0, 1].set_xscale("log")

    axes[1, 0].plot(limits, [item.occupied_cells for item in stats], marker="o", color="#984ea3")
    axes[1, 0].set_title("Occupied cells")
    axes[1, 0].set_xlabel("N")
    axes[1, 0].set_ylabel("cells")
    axes[1, 0].set_xscale("log")

    axes[1, 1].plot(limits, [item.beta0_before for item in stats], marker="o", color="#ff7f00")
    axes[1, 1].set_title("Raw support components before thickening")
    axes[1, 1].set_xlabel("N")
    axes[1, 1].set_ylabel(r"$\beta_0$")
    axes[1, 1].set_xscale("log")

    fig.suptitle("Normalized dense support limit sweep")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_dense_support_thickening(stats: tuple[DenseSupportStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    thresholds = [item.threshold for item in stats]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    axes[0, 0].plot(thresholds, [item.epsilon for item in stats], marker="o")
    axes[0, 0].set_title("Minimal epsilon for connectivity")
    axes[0, 0].set_xlabel("Density threshold")
    axes[0, 0].set_ylabel("epsilon in cells")
    axes[0, 0].set_xscale("log")

    axes[0, 1].plot(thresholds, [item.beta1_after for item in stats], marker="o", color="#e41a1c")
    axes[0, 1].set_title("Holes after minimal thickening")
    axes[0, 1].set_xlabel("Density threshold")
    axes[0, 1].set_ylabel("hole count")
    axes[0, 1].set_xscale("log")

    axes[1, 0].plot(thresholds, [item.largest_inscribed_radius for item in stats], marker="o", color="#4daf4a")
    axes[1, 0].set_title("Largest inscribed disk radius")
    axes[1, 0].set_xlabel("Density threshold")
    axes[1, 0].set_ylabel("radius in cells")
    axes[1, 0].set_xscale("log")

    axes[1, 1].plot(thresholds, [item.dilated_cells for item in stats], marker="o", color="#984ea3")
    axes[1, 1].set_title("Dilated support area")
    axes[1, 1].set_xlabel("Density threshold")
    axes[1, 1].set_ylabel("cells")
    axes[1, 1].set_xscale("log")

    fig.suptitle("Dense support thickening diagnostics")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_dense_support_report(stats: tuple[DenseSupportStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    thickest = max(stats, key=lambda item: item.largest_inscribed_radius)
    most_holes = max(stats, key=lambda item: item.beta1_after)

    lines = [
        "# Dense Support Thickening Report",
        "",
        "For each threshold $\\lambda$, define:",
        "",
        "$$D_\\lambda=\\{\\mu_N\\geq\\lambda\\}.$$",
        "",
        "The analysed object is the smallest 8-neighbourhood thickening that connects the support:",
        "",
        "$$D_{\\lambda,\\varepsilon}=\\operatorname{dilate}_\\varepsilon(D_\\lambda).$$",
        "",
        "| threshold | epsilon | cells | thickened cells | beta0 before | beta1 before | beta1 after | largest radius |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for item in stats:
        lines.append(
            f"| {item.threshold} | {item.epsilon} | {item.occupied_cells} | {item.dilated_cells} | "
            f"{item.beta0_before} | {item.beta1_before} | {item.beta1_after} | "
            f"{item.largest_inscribed_radius:.2f} |"
        )

    lines.extend(
        [
            "",
            "Highlights:",
            "",
            (
                f"- Largest inscribed discrete disk: threshold `{thickest.threshold}`, "
                f"epsilon `{thickest.epsilon}`, radius `{thickest.largest_inscribed_radius:.2f}` cells, "
                f"center approximately at step `{thickest.radius_step_center:.2f}`, "
                f"log-value `{thickest.radius_log_value_center:.3f}`."
            ),
            (
                f"- Most holes after minimal thickening: threshold `{most_holes.threshold}`, "
                f"holes `{most_holes.beta1_after}`."
            ),
            "",
            "Interpretation:",
            "",
            (
                "This is a cubical thickening of a density support, not a smooth manifold. "
                "A positive and stable inscribed radius indicates local two-dimensional thickness at this grid scale. "
                "Holes that survive the minimal connecting thickening are better candidates for robust lacunae."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_epsilon_sweep_report(stats: tuple[EpsilonSweepStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    first = stats[0]
    last = stats[-1]
    epsilon_direction = "decreases" if last.epsilon_normalized < first.epsilon_normalized else "does not decrease"
    radius_direction = (
        "increases"
        if last.largest_inscribed_radius_normalized > first.largest_inscribed_radius_normalized
        else "does not increase"
    )

    lines = [
        "# Normalized Epsilon Sweep Report",
        "",
        "For each limit $N$, this report analyses the normalized support:",
        "",
        "$$D_1(N)=\\{\\mu_N\\geq 1\\}.$$",
        "",
        "The main quantity is the smallest normalized thickening scale making the support connected:",
        "",
        "$$\\varepsilon_*(N)=\\frac{\\text{minimal dilation in cells}}{\\text{grid size}}.$$",
        "",
        "| N | bins | epsilon cells | epsilon normalized | radius normalized | occupied cells | beta0 before | beta1 after |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for item in stats:
        lines.append(
            f"| {item.limit} | {item.bins} | {item.epsilon_cells} | "
            f"{item.epsilon_normalized:.6f} | {item.largest_inscribed_radius_normalized:.6f} | "
            f"{item.occupied_cells} | {item.beta0_before} | {item.beta1_after} |"
        )

    lines.extend(
        [
            "",
            "Initial reading:",
            "",
            (
                f"Across this sampled range, $\\varepsilon_*(N)$ {epsilon_direction} from "
                f"`{first.epsilon_normalized:.6f}` to `{last.epsilon_normalized:.6f}`."
            ),
            (
                f"The normalized largest inscribed radius {radius_direction} from "
                f"`{first.largest_inscribed_radius_normalized:.6f}` to "
                f"`{last.largest_inscribed_radius_normalized:.6f}`."
            ),
            "",
            (
                "If $\\varepsilon_*(N)$ trends toward zero as $N$ grows, it supports the idea that the raw supports "
                "approach a connected continuum. If it stabilizes away from zero, the limiting support may retain "
                "macroscopic gaps at this normalization."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_dense_support_resolution_report(
    stats_by_bins: dict[int, tuple[DenseSupportStats, ...]],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Dense Support Resolution Comparison",
        "",
        "| vertical bins | threshold | epsilon | beta1 after | largest radius | thickened cells |",
        "|---:|---:|---:|---:|---:|---:|",
    ]

    for bins, stats in sorted(stats_by_bins.items()):
        for item in stats:
            lines.append(
                f"| {bins} | {item.threshold} | {item.epsilon} | {item.beta1_after} | "
                f"{item.largest_inscribed_radius:.2f} | {item.dilated_cells} |"
            )

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "Stable small epsilons and stable positive radii across resolutions support the interpretation "
                "of locally thick dense domains. Strong variation indicates a grid-scale artifact."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
