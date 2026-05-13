import csv

from syracuse.fit import fit_log_power_law, fit_power_law, load_epsilon_sweep


def test_load_epsilon_sweep(tmp_path) -> None:
    path = tmp_path / "sweep.csv"
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["limit", "epsilon_normalized"])
        writer.writeheader()
        writer.writerow({"limit": 10, "epsilon_normalized": 0.1})
        writer.writerow({"limit": 100, "epsilon_normalized": 0.01})

    limits, epsilons = load_epsilon_sweep(path)

    assert limits.tolist() == [10.0, 100.0]
    assert epsilons.tolist() == [0.1, 0.01]


def test_fit_models_return_predictions() -> None:
    limits, epsilons = load_epsilon_sweep_fixture()

    power = fit_power_law(limits, epsilons)
    log_power = fit_log_power_law(limits, epsilons)

    assert len(power.predicted) == 4
    assert len(log_power.predicted) == 4
    assert power.alpha > 0


def load_epsilon_sweep_fixture():
    import numpy as np

    return np.array([10.0, 100.0, 1000.0, 10000.0]), np.array([0.1, 0.05, 0.025, 0.0125])
