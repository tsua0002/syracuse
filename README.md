# Syracuse

Outils Python pour explorer les suites de Syracuse (conjecture de Collatz) : trajectoires compressées sur les impairs, grilles de densité normalisées, support dense et son épaississement, analyse par blocs, métriques de raccordement ($\varepsilon$, $\delta$, balayages), persistance topologique (TDA) sur heatmaps, et rapports reproductibles.

**English.** This repository provides reproducible experiments on Syracuse/Collatz dynamics: odd-compressed dynamics, normalized density heatmaps, dense supports and discrete thickening, block-wise attachment distances, robustness notes around monotonicity, persistence summaries via Gudhi, CSV/Markdown artefacts under `outputs/`, and research notes under `plans/syracuse/`.

## État du dépôt

Le code correspond à l’implémentation testée décrite dans [`plans/syracuse/synthese-programme-recherche.md`](plans/syracuse/synthese-programme-recherche.md). Les sorties versionnées sous `outputs/` couvrent notamment \(N \leq 10^4\) et les rapports « blocs » jusqu’à \(10^7\) lorsque le cache SQLite est utilisé.

### Publication (recherche collective)

Document de synthèse unique pour diffusion (GitHub, séminaires, réseaux professionnels) : [`plans/syracuse/RAPPORT_PUBLICATION_COLLECTIF.md`](plans/syracuse/RAPPORT_PUBLICATION_COLLECTIF.md). Il rappelle le cadre non démonstratif, liste les livrables, et donne les commandes de reproduction — dont le script [`scripts/reproduce_collective_block_pipeline.sh`](scripts/reproduce_collective_block_pipeline.sh).

## Installation

Requires Python 3.11+ and [Gudhi](https://gudhi.inria.fr/) (declared in `pyproject.toml`).

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Minimal install:

```bash
pip install -e .
```

Developers can mirror the bundled Pipenv setup:

```bash
pipenv install --dev
pipenv run pytest
```

## Utilisation

Entry point (see `src/syracuse/cli.py` for all subcommands):

```bash
syracuse-generate --help
python generate_outputs.py --help
```

Typical workflow: pick a subcommand (density maps, dense support, TDA, epsilon sweeps, parity diagnostics, and more), write artefacts under `outputs/`, and consult matching `.md` reports.

## Structure

| Path | Role |
|------|------|
| `src/syracuse/` | Library: `core`, `analysis`, `support`, `tda`, `cache`, `cli`, … |
| `tests/` | Pytest suite |
| `outputs/` | CSV/Markdown ; quelques **figures PNG** versionnées (liste ci-dessous) ; autres `.png`, `.mp4`, `.npy` ignorés par défaut |

Les PNG suivants sont suivis dans Git comme **bandeau visuel** pour la lecture sur GitHub : chaîne « blocs » (`block_attachment_*`, `alpha_attachment_*`, `block_arithmetic`, cartes de localisation), heatmaps et supports denses pour \(N=10000\) (`heatmap_*`, `dense_support_*`, `normalized_*`), TDA (`tda_*`), fenêtre alpha complex (`alpha_window_*`). Pour élargir la liste, ajouter une ligne `!outputs/…` dans `.gitignore` puis `git add` le fichier.
| `plans/syracuse/` | Notes de recherche ; rapport de publication collective |
| `scripts/` | Scripts de reproduction du pipeline « blocs » |
| `generate_outputs.py` | Thin wrapper around `syracuse.cli:main` |

## Licence

MIT — voir [LICENSE](LICENSE).

## Citation

Si vous réutilisez ce dépôt dans un travail académique, citez l’URL du dépôt et la version (tag ou commit) utilisée.
