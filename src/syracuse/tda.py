from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import gudhi as gd
import matplotlib.pyplot as plt
import numpy as np

from syracuse.analysis import DensityGrid


@dataclass(frozen=True)
class PersistenceFeature:
    dimension: int
    birth: float
    death: float
    persistence: float


@dataclass(frozen=True)
class AlphaWindowSummary:
    point_count: int
    h0_count: int
    h1_count: int
    max_h1_persistence: float


def density_filtration_values(grid: DensityGrid) -> np.ndarray:
    """Dense cells appear first in the sublevel filtration."""
    return -np.log1p(grid.counts)


def compute_density_persistence(grid: DensityGrid) -> tuple[PersistenceFeature, ...]:
    filtration_values = density_filtration_values(grid)
    complex_ = gd.CubicalComplex(
        dimensions=filtration_values.shape,
        top_dimensional_cells=filtration_values.ravel(order="F"),
    )
    persistence = complex_.persistence()

    features = []
    for dimension, (birth, death) in persistence:
        persistence_value = np.inf if death == np.inf else death - birth
        features.append(
            PersistenceFeature(
                dimension=dimension,
                birth=float(birth),
                death=float(death),
                persistence=float(persistence_value),
            )
        )

    return tuple(features)


def points_from_mask_window(
    mask: np.ndarray,
    *,
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    max_points: int = 5000,
) -> np.ndarray:
    if max_points < 1:
        raise ValueError("max_points must be greater than or equal to 1")

    bins_x, bins_y = mask.shape
    x_centers = (np.arange(bins_x) + 0.5) / bins_x
    y_centers = (np.arange(bins_y) + 0.5) / bins_y
    x_indices, y_indices = np.nonzero(mask)
    points = np.array(
        [
            (x_centers[x_index], y_centers[y_index])
            for x_index, y_index in zip(x_indices, y_indices, strict=True)
            if x_range[0] <= x_centers[x_index] <= x_range[1]
            and y_range[0] <= y_centers[y_index] <= y_range[1]
        ],
        dtype=float,
    )

    if len(points) > max_points:
        indices = np.linspace(0, len(points) - 1, max_points, dtype=int)
        points = points[indices]

    return points


def compute_alpha_persistence(points: np.ndarray) -> tuple[PersistenceFeature, ...]:
    if len(points) == 0:
        raise ValueError("points must not be empty")

    alpha_complex = gd.AlphaComplex(points=points)
    simplex_tree = alpha_complex.create_simplex_tree()
    persistence = simplex_tree.persistence()

    features = []
    for dimension, (birth, death) in persistence:
        persistence_value = np.inf if death == np.inf else death - birth
        features.append(
            PersistenceFeature(
                dimension=dimension,
                birth=float(birth),
                death=float(death),
                persistence=float(persistence_value),
            )
        )
    return tuple(features)


def summarize_alpha_window(points: np.ndarray, features: tuple[PersistenceFeature, ...]) -> AlphaWindowSummary:
    h0 = [feature for feature in features if feature.dimension == 0]
    h1 = [feature for feature in features if feature.dimension == 1]
    finite_h1 = [feature for feature in h1 if np.isfinite(feature.persistence)]
    return AlphaWindowSummary(
        point_count=len(points),
        h0_count=len(h0),
        h1_count=len(h1),
        max_h1_persistence=max((feature.persistence for feature in finite_h1), default=0.0),
    )


def plot_alpha_window(points: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 7), constrained_layout=True)
    ax.scatter(points[:, 0], points[:, 1], s=2, alpha=0.55)
    ax.set_title("Alpha complex input points")
    ax.set_xlabel("normalized step")
    ax.set_ylabel("normalized log-value")
    ax.set_aspect("equal", adjustable="box")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_alpha_window_report(
    summary: AlphaWindowSummary,
    features: tuple[PersistenceFeature, ...],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    finite_h1 = sorted(
        [feature for feature in features if feature.dimension == 1 and np.isfinite(feature.persistence)],
        key=lambda feature: feature.persistence,
        reverse=True,
    )[:10]

    lines = [
        "# Alpha Complex Local Report",
        "",
        f"- Points: `{summary.point_count}`",
        f"- H0 features: `{summary.h0_count}`",
        f"- H1 features: `{summary.h1_count}`",
        f"- Max H1 persistence: `{summary.max_h1_persistence:.8f}`",
        "",
        "## Top H1 Features",
        "",
        "| birth | death | persistence |",
        "|---:|---:|---:|",
    ]

    for feature in finite_h1:
        lines.append(f"| {feature.birth:.8f} | {feature.death:.8f} | {feature.persistence:.8f} |")

    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            (
                "This alpha complex is a local validation tool. It is closer to a continuous union-of-balls model "
                "than the global cubical grid, but it is computed only on a sampled local window."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def export_persistence(features: tuple[PersistenceFeature, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["dimension", "birth", "death", "persistence"])
        writer.writeheader()
        for feature in features:
            writer.writerow(
                {
                    "dimension": feature.dimension,
                    "birth": feature.birth,
                    "death": feature.death,
                    "persistence": feature.persistence,
                }
            )


def plot_persistence_barcode(features: tuple[PersistenceFeature, ...], path: Path, *, max_features: int = 80) -> None:
    finite_features = [feature for feature in features if np.isfinite(feature.death)]
    selected = sorted(finite_features, key=lambda feature: feature.persistence, reverse=True)[:max_features]

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 7), constrained_layout=True)

    colors = {0: "#377eb8", 1: "#e41a1c"}
    labels_seen = set()
    for index, feature in enumerate(reversed(selected)):
        label = f"H{feature.dimension}" if feature.dimension not in labels_seen else None
        labels_seen.add(feature.dimension)
        ax.hlines(
            y=index,
            xmin=feature.birth,
            xmax=feature.death,
            color=colors.get(feature.dimension, "#4daf4a"),
            linewidth=1.8,
            label=label,
        )

    ax.set_title("Persistent homology barcode for density filtration")
    ax.set_xlabel("Filtration value")
    ax.set_ylabel("Feature")
    ax.legend(loc="best")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_persistence_diagram(features: tuple[PersistenceFeature, ...], path: Path) -> None:
    finite_features = [feature for feature in features if np.isfinite(feature.death)]

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)

    for dimension, color in ((0, "#377eb8"), (1, "#e41a1c")):
        points = [feature for feature in finite_features if feature.dimension == dimension]
        if not points:
            continue
        ax.scatter(
            [feature.birth for feature in points],
            [feature.death for feature in points],
            s=12,
            alpha=0.65,
            color=color,
            label=f"H{dimension}",
        )

    if finite_features:
        values = [value for feature in finite_features for value in (feature.birth, feature.death)]
        min_value = min(values)
        max_value = max(values)
        ax.plot([min_value, max_value], [min_value, max_value], color="black", linestyle="--", linewidth=1)

    ax.set_title("Persistence diagram for density filtration")
    ax.set_xlabel("Birth")
    ax.set_ylabel("Death")
    ax.legend(loc="best")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_tda_report(features: tuple[PersistenceFeature, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    h0 = [feature for feature in features if feature.dimension == 0]
    h1 = [feature for feature in features if feature.dimension == 1]
    finite_h0 = [feature for feature in h0 if np.isfinite(feature.persistence)]
    finite_h1 = [feature for feature in h1 if np.isfinite(feature.persistence)]
    top_h1 = sorted(finite_h1, key=lambda feature: feature.persistence, reverse=True)[:10]

    lines = [
        "# TDA Density Report",
        "",
        "The filtration is defined by:",
        "",
        "$$F=-\\log(1+\\mu_N).$$",
        "",
        "Dense cells therefore appear earlier in the sublevel filtration.",
        "",
        f"- H0 features: `{len(h0)}`",
        f"- finite H0 features: `{len(finite_h0)}`",
        f"- H1 features: `{len(h1)}`",
        f"- finite H1 features: `{len(finite_h1)}`",
    ]

    if finite_h0:
        lines.append(f"- max finite H0 persistence: `{max(feature.persistence for feature in finite_h0):.6f}`")
    if finite_h1:
        lines.append(f"- max H1 persistence: `{max(feature.persistence for feature in finite_h1):.6f}`")

    lines.extend(
        [
            "",
            "## Top H1 Features",
            "",
            "| birth | death | persistence |",
            "|---:|---:|---:|",
        ]
    )

    for feature in top_h1:
        lines.append(f"| {feature.birth:.6f} | {feature.death:.6f} | {feature.persistence:.6f} |")

    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            (
                "Persistent H0 classes indicate robust dense components. Persistent H1 classes indicate holes or "
                "lacunae in the density support, but their interpretation must be checked against resolution changes."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_tda_resolution_report(features_by_bins: dict[int, tuple[PersistenceFeature, ...]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# TDA Resolution Comparison",
        "",
        "| vertical bins | H0 | finite H0 | H1 | max H1 persistence |",
        "|---:|---:|---:|---:|---:|",
    ]

    for bins, features in sorted(features_by_bins.items()):
        h0 = [feature for feature in features if feature.dimension == 0]
        finite_h0 = [feature for feature in h0 if np.isfinite(feature.persistence)]
        h1 = [feature for feature in features if feature.dimension == 1]
        finite_h1 = [feature for feature in h1 if np.isfinite(feature.persistence)]
        max_h1 = max((feature.persistence for feature in finite_h1), default=0.0)
        lines.append(f"| {bins} | {len(h0)} | {len(finite_h0)} | {len(h1)} | {max_h1:.6f} |")

    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            (
                "Stable H1 persistence across resolutions suggests robust holes in the density support. "
                "Large variation suggests discretization artifacts."
            ),
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
