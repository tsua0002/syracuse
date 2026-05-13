from syracuse.core import stats_for_range
from syracuse.reporting import evaluate_hypotheses


def test_hypotheses_return_expected_sections() -> None:
    results = evaluate_hypotheses(stats_for_range(16))

    assert [result.title for result in results] == [
        "Termination on the tested range",
        "Powers of two",
        "Longest sequence versus highest peak",
        "Odd starts versus even starts",
    ]
    assert results[1].result == "confirmed on this finite range"
