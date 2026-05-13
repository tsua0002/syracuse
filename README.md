# Syracuse

Outils Python pour explorer les suites de Syracuse (conjecture de Collatz) : dynamique compressée sur les impairs, cartes de densité normalisées, support dense et épaississement discret, analyse par blocs, distances de raccordement ($\varepsilon$, $\delta$, balayages), persistance topologique (TDA) via Gudhi, et rapports reproductibles au format CSV/Markdown dans `outputs/` avec les notes de recherche dans `plans/syracuse/`.

## État du dépôt

Le code correspond à l’implémentation testée décrite dans [`plans/syracuse/synthese-programme-recherche.md`](plans/syracuse/synthese-programme-recherche.md). Les sorties versionnées sous `outputs/` couvrent notamment \(N \leq 10^4\) et les rapports « blocs » jusqu’à \(10^7\) lorsque le cache SQLite est utilisé.

### Publication (recherche collective)

Document de synthèse unique pour diffusion (GitHub, séminaires, réseaux professionnels) : [`plans/syracuse/RAPPORT_PUBLICATION_COLLECTIF.md`](plans/syracuse/RAPPORT_PUBLICATION_COLLECTIF.md). Il rappelle le cadre non démonstratif, liste les livrables et donne les commandes de reproduction — dont le script [`scripts/reproduce_collective_block_pipeline.sh`](scripts/reproduce_collective_block_pipeline.sh).

## Installation

Nécessite Python 3.11 ou plus et la bibliothèque [Gudhi](https://gudhi.inria.fr/) (indiquée dans `pyproject.toml`).

```bash
python -m venv .venv
source .venv/bin/activate   # sous Windows : .venv\Scripts\activate
pip install -e ".[dev]"
```

Installation minimale :

```bash
pip install -e .
```

Pour reproduire l’environnement avec Pipenv :

```bash
pipenv install --dev
pipenv run pytest
```

## Utilisation

Point d’entrée (`syracuse-generate`, défini dans `pyproject.toml`) ; la liste complète des sous-commandes est dans `src/syracuse/cli.py` :

```bash
syracuse-generate --help
python generate_outputs.py --help
```

Déroulement typique : choisir une analyse (cartes de densité, support dense, TDA, balayages de $\varepsilon_*$, diagnostics de parité, etc.), écrire les artefacts sous `outputs/`, puis consulter les rapports `.md` associés.

## Structure du dépôt

| Chemin | Rôle |
|--------|------|
| `src/syracuse/` | Bibliothèque : `core`, `analysis`, `support`, `tda`, `cache`, `cli`, … |
| `tests/` | Suite de tests Pytest |
| `outputs/` | Fichiers CSV et Markdown ; quelques **figures PNG** versionnées ; les autres `.png`, `.mp4` et `.npy` sont ignorés par Git par défaut |
| `plans/syracuse/` | Notes de recherche et rapport de publication collective |
| `scripts/` | Scripts de reproduction du pipeline « blocs » |
| `generate_outputs.py` | Script léger qui appelle `syracuse.cli:main` |

Les PNG suivants sont suivis dans Git pour illustrer le dépôt sur GitHub : chaîne « blocs » (`block_attachment_*`, `alpha_attachment_*`, `block_arithmetic`, cartes de localisation), cartes de densité et supports denses pour \(N = 10\,000\) (`heatmap_*`, `dense_support_*`, `normalized_*`), TDA (`tda_*`), fenêtre alpha complexe (`alpha_window_*`). Pour en ajouter d’autres : ajouter une ligne `!outputs/…` dans `.gitignore`, puis `git add` le fichier concerné.

## Licence

MIT — voir [LICENSE](LICENSE).

## Citation

Si vous réutilisez ce dépôt dans un travail académique, citez l’URL du dépôt et la version (étiquette ou commit) utilisée.
