from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from syracuse.core import SequenceStats


@dataclass(frozen=True)
class HypothesisResult:
    title: str
    hypothesis: str
    result: str
    evidence: str


def export_summary_csv(stats: tuple[SequenceStats, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["start", "steps_to_1", "maximum"])
        writer.writeheader()
        for item in stats:
            writer.writerow(
                {
                    "start": item.start,
                    "steps_to_1": item.steps,
                    "maximum": item.maximum,
                }
            )


def evaluate_hypotheses(stats: tuple[SequenceStats, ...]) -> tuple[HypothesisResult, ...]:
    if not stats:
        raise ValueError("stats must not be empty")

    by_steps = max(stats, key=lambda item: item.steps)
    by_maximum = max(stats, key=lambda item: item.maximum)
    powers_of_two = [item for item in stats if item.start & (item.start - 1) == 0]
    even_steps = [item.steps for item in stats if item.start % 2 == 0]
    odd_steps = [item.steps for item in stats if item.start % 2 == 1]
    all_reach_one = all(item.sequence[-1] == 1 for item in stats)

    powers_result = all(
        item.steps == item.start.bit_length() - 1 and item.maximum == item.start
        for item in powers_of_two
    )
    odd_mean = mean(odd_steps)
    even_mean = mean(even_steps)

    return (
        HypothesisResult(
            title="Termination on the tested range",
            hypothesis="Every start value in the tested range reaches 1.",
            result="confirmed on this finite range" if all_reach_one else "rejected",
            evidence=f"Checked {len(stats)} sequences; all final values are 1: {all_reach_one}.",
        ),
        HypothesisResult(
            title="Powers of two",
            hypothesis="A power of two reaches 1 in log2(n) steps and never exceeds its start.",
            result="confirmed on this finite range" if powers_result else "rejected",
            evidence=f"Checked powers of two up to {stats[-1].start}: {[item.start for item in powers_of_two]}.",
        ),
        HypothesisResult(
            title="Longest sequence versus highest peak",
            hypothesis="The start value with the longest sequence is also the one with the highest peak.",
            result="rejected" if by_steps.start != by_maximum.start else "confirmed on this finite range",
            evidence=(
                f"Longest sequence: start={by_steps.start}, steps={by_steps.steps}, max={by_steps.maximum}. "
                f"Highest peak: start={by_maximum.start}, steps={by_maximum.steps}, max={by_maximum.maximum}."
            ),
        ),
        HypothesisResult(
            title="Odd starts versus even starts",
            hypothesis="Odd start values have a higher average stopping time than even start values.",
            result="confirmed on this finite range" if odd_mean > even_mean else "rejected",
            evidence=f"Odd average steps={odd_mean:.2f}; even average steps={even_mean:.2f}.",
        ),
    )


def write_hypothesis_report(results: tuple[HypothesisResult, ...], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Syracuse Hypotheses", ""]

    for result in results:
        lines.extend(
            [
                f"## {result.title}",
                "",
                f"- Hypothesis: {result.hypothesis}",
                f"- Result: {result.result}",
                f"- Evidence: {result.evidence}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
