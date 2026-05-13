# Rapport de publication — piste « support géométrique normalisé » (recherche collective)

**English abstract.** This document closes the first *publishable* cycle of a collaborative exploratory line on Syracuse (Collatz) dynamics: we summarize goals, implemented tooling, fixed artefacts under `outputs/`, reproduction commands, and what remains genuinely open. Nothing here constitutes a proof of the Collatz conjecture; all claims are empirical and conditional on chosen grids and ranges.

---

## 1. Propos et cadre honnête

Le projet vise à **décrire quantitativement** comment les orbites de Syracuse remplissent une fenêtre normalisée (temps de parcours vs logarithme de la valeur) et comment ce remplissage **évolue** lorsque l’on élargit progressivement l’ensemble des entiers de départ \(1,\ldots,N\).

Les outils combinent :

- géométrie discrète sur grilles (supports denses, dilatation minimale de connexion) ;
- mesures de **raccordement** entre étapes successives (nouvelles cellules vs support précédent) ;
- sensibilité à une métrique anisotrope \(d_\alpha\) ;
- indices topologiques via **persistance** (cubique sur masques ; alpha complex en fenêtre locale) ;
- agrégats **arithmétiques par blocs** sur les trajectoires compressées sur les impairs.

## 2. Livrables « figés » dans ce dépôt

### 2.1 Cœur \(N \leq 10^4\) (sans cache lourd)

Les rapports et CSV versionnés sous `outputs/` pour `limit = 1000` et `10000` décrivent :

- densités et heatmaps (`density_*`, rapports associés) ;
- diagnostics parité / compression impaire ;
- supports denses et comparaisons de résolution (`dense_support_*`, `normalized_dense_support_*`) ;
- TDA cubique sur heatmaps (`tda_*`) ;
- bilans d’hypothèses (`hypotheses_*`, `summary_*`).

Ils permettent une lecture **autonome** du comportement à petite échelle.

### 2.2 Chaîne « blocs » jusqu’à \(N = 10^7\) (via cache SQLite)

Les fichiers suivants correspondent au pipeline décrit en section 3 et ont été produits avec une grille **1000 × 1000** et des coupures :

`10000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000`.

| Thème | Fichiers types |
|------|----------------|
| Raccordement euclidien sur grille fixe | `block_attachment_bins_1000.{csv,md}` |
| Sensibilité \(d_\alpha\) | `alpha_attachment_bins_1000.{csv,md}` |
| Agrégats arithmétiques par bloc | `block_arithmetic.{csv,md}` |
| Balayage \(\varepsilon_*\) normalisé (extrait / consolidation) | `epsilon_sweep_*`, `epsilon_fit_report.md`, notes robustesse |

**Figures.** Une sélection de PNG illustratifs est **versionnée** (liste dans [`README.md`](../../README.md), exceptions dans [`.gitignore`](../../.gitignore)). Les autres images, animations `*.mp4` et grilles `*.npy` restent régénérables localement pour limiter la taille du dépôt.

### 2.3 Fenêtre locale alpha complex

Résultats et données persistées pour la fenêtre standard :

- `alpha_window_report.md`
- `alpha_window_persistence.csv`

Les figures associées se régénèrent avec `--alpha-window` (voir section 3).

### 2.4 Notes formelles et méthodologie

Les intentions, objections et raffinements conceptuels sont dans `plans/syracuse/` — en particulier :

- `synthese-programme-recherche.md` (feuille de route mise à jour) ;
- `note-formelle-epsilon-monotonie.md` (pourquoi \(\varepsilon_*\) seul est trompeur ; rôle de \(\delta\)) ;
- notes TDA, compression impaire, propriétés, etc.

## 3. Reproduction minimale

### 3.1 Environnement

```bash
pip install -e ".[dev]"
# ou : pipenv install --dev
```

### 3.2 Pipeline bloc \(10^7\) + \(d_\alpha\) + arithmétique

Créer un cache SQLite (répertoire créé automatiquement si besoin) :

```bash
export SYRACUSE_CACHE="$(pwd)/outputs/cache/syracuse.sqlite"
```

Puis (équivalent au script `scripts/reproduce_collective_block_pipeline.sh`) :

```bash
syracuse-generate \
  --output-dir outputs \
  --sequence-cache "$SYRACUSE_CACHE" \
  --block-attachment-limits \
      10000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 \
  --block-attachment-bins 1000 \
  --alpha-attachment \
  --alpha-values 0.25 0.5 1 2 4 \
  --block-arithmetic
```

**Temps de calcul.** Le premier passage remplit le cache jusqu’à \(10^7\) ; selon la machine, compter un ordre de grandeur de **plusieurs minutes à quelques dizaines de minutes**.

### 3.3 Fenêtre alpha complex (exemple par défaut du CLI)

```bash
syracuse-generate \
  --output-dir outputs \
  --sequence-cache "$SYRACUSE_CACHE" \
  --alpha-window
```

### 3.4 Jeu complet \(N \leq 10^4\) sans cache

```bash
syracuse-generate --limit 10000 --output-dir outputs \
  --dense-support --normalized-support --normalized-bins 1000 2000 \
  --tda --compare-heatmap-resolutions
```

(Ajuster les options selon les rapports que vous voulez régénérer.)

## 4. Lecture synthétique des résultats obtenus

Les rapports Markdown sous `outputs/` sont la source primaire ; on résume ici **sans sur-interprétation**.

1. **Supports denses et épaississement.** Pour les grilles testées, la procédure de dilatation minimale reliant les composantes du support \(\{\mu \geq \lambda\}\) est entièrement reproductible ; les rapports comparent aussi les résolutions de binning.

2. **Raccordement par blocs.** Les distances minimales observées dans `block_attachment_bins_1000.md` sont compatibles avec une dynamique où **chaque nouveau bloc intersecte le support précédent à l’échelle d’une cellule** de la grille fixe (après normalisation choisie).

3. **Métrique \(d_\alpha\).** Le fichier `alpha_attachment_bins_1000.md` montre comment min / mean / max évoluent sous plusieurs \(\alpha\). Les petites distances minimales sur une plage de \(\alpha\) milite contre un artefact purement « vertical » ou purement « horizontal » au sens où une métrique anisotrope extreme changerait radicalement le fait de toucher ou non ; la qualification demeure **locale au choix de grille et de plage de \(N\)**.

4. **Arithmétique par bloc.** `block_arithmetic.md` agrège longueurs, bornes sur les maxima, exposants \(v_2\) moyens sur la dynamique impaire compressée, fréquence des \(a_i=1\), et une grandeur liée au budget \(\sum (\log_2(3) - a_i)\). C’est une **première passerelle** entre géométrie macro par bloc et statistiques orbitales ; une carte fine « cellule \(\rightarrow\) régime arithmétique » reste ouverte.

5. **Alpha complex local.** `alpha_window_report.md` documente une validation locale : beaucoup de cycles courts dans le complexe, persistance \(H_1\) maximale faible dans la fenêtre testée — indicatif de **micro-lacunarité** plutôt que d’un trou géométrique massif stable dans ce zoom.

## 5. Ce qui reste ouvert (hors prétention de ce dépôt)

- Cartographie **fine** : quelles orbites / quels invariants arithmétiques dominent **quelles régions** du plan normalisé (au-delà d’agrégats par blocs).
- Extensions systématiques à d’autres coupures de blocs, autres \(N\) maximaux, autres résolutions \(B\), autres fenêtres pour l’alpha complex.
- Toute affirmation asymptotique sur \(N \to \infty\) : non démontrée ici.

## 6. Utilisation pour communication externe

Pour GitHub / LinkedIn / séminaires internes : présenter ce dépôt comme **code et données d’exploration reproductibles** attachés à une **question de recherche précise** (géométrie du support agrégé), avec la clause explicite qu’il **ne résout pas** la conjecture de Syracuse.

---

*Document préparé pour clôturer une première livraison collective cohérente entre implémentation, artefacts et lecture scientifique prudente.*
