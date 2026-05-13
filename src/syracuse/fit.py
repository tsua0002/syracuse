from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class FitResult:
    model: str
    coefficient: float
    alpha: float
    r_squared: float
    predicted: tuple[float, ...]


def load_epsilon_sweep(path: Path) -> tuple[np.ndarray, np.ndarray]:
    limits = []
    epsilons = []

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            limits.append(float(row["limit"]))
            epsilons.append(float(row["epsilon_normalized"]))

    return np.array(limits), np.array(epsilons)


def fit_power_law(limits: np.ndarray, epsilons: np.ndarray) -> FitResult:
    x = np.log(limits)
    y = np.log(epsilons)
    slope, intercept = np.polyfit(x, y, deg=1)
    predicted = np.exp(intercept + slope * x)
    return FitResult(
        model="C * N^(-alpha)",
        coefficient=float(np.exp(intercept)),
        alpha=float(-slope),
        r_squared=_r_squared(epsilons, predicted),
        predicted=tuple(float(value) for value in predicted),
    )


def fit_log_power_law(limits: np.ndarray, epsilons: np.ndarray) -> FitResult:
    x = np.log(np.log(limits))
    y = np.log(epsilons)
    slope, intercept = np.polyfit(x, y, deg=1)
    predicted = np.exp(intercept + slope * x)
    return FitResult(
        model="C * log(N)^(-alpha)",
        coefficient=float(np.exp(intercept)),
        alpha=float(-slope),
        r_squared=_r_squared(epsilons, predicted),
        predicted=tuple(float(value) for value in predicted),
    )


def export_fit_report(limits: np.ndarray, epsilons: np.ndarray, results: tuple[FitResult, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    best = max(results, key=lambda result: result.r_squared)
    lines = [
        "# Epsilon Fit Report",
        "",
        "This report fits empirical models to the normalized connection scale:",
        "",
        "$$\\varepsilon_*(N).$$",
        "",
        "## Data",
        "",
        "| N | epsilon |",
        "|---:|---:|",
    ]

    for limit, epsilon in zip(limits, epsilons, strict=True):
        lines.append(f"| {int(limit)} | {epsilon:.6f} |")

    lines.extend(["", "## Fits", "", "| model | C | alpha | R^2 |", "|---|---:|---:|---:|"])
    for result in results:
        lines.append(
            f"| `{result.model}` | {result.coefficient:.8f} | {result.alpha:.6f} | {result.r_squared:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Reading",
            "",
            f"The best fit among these two simple models is `{best.model}` by $R^2$.",
            "",
            "This is descriptive only. The data range is still short and should not be read as an asymptotic law.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def plot_fit(limits: np.ndarray, epsilons: np.ndarray, results: tuple[FitResult, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.scatter(limits, epsilons, color="black", label="observed")

    order = np.argsort(limits)
    sorted_limits = limits[order]
    for result in results:
        predicted = np.array(result.predicted)[order]
        ax.plot(sorted_limits, predicted, marker="o", label=f"{result.model}, R^2={result.r_squared:.3f}")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Empirical fits for normalized connection scale")
    ax.set_xlabel("N")
    ax.set_ylabel(r"$\varepsilon_*(N)$")
    ax.legend()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _r_squared(observed: np.ndarray, predicted: np.ndarray) -> float:
    residual_sum = np.sum((observed - predicted) ** 2)
    total_sum = np.sum((observed - observed.mean()) ** 2)
    if total_sum == 0:
        return 1.0
    return float(1 - residual_sum / total_sum)
