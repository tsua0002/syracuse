# Synthèse du programme de recherche

## État actuel

Le plan initial d'étude du support dense épaissi est terminé :

- support dense $D_\lambda=\{\mu_N\geq \lambda\}$ ;
- épaississement minimal par dilatation discrète ;
- composantes, trous, rayon inscrit ;
- comparaison de résolutions ;
- TDA cubique sur heatmap.

Les artefacts principaux sont :

- `outputs/dense_support_report_1_to_10000.md`
- `outputs/dense_support_resolution_comparison_1_to_10000.md`
- `outputs/tda_report_1_to_10000.md`
- `outputs/tda_resolution_comparison_1_to_10000.md`

## Extensions déjà réalisées

### Support normalisé

On a étudié le support brut normalisé :

$$
D_1(N,B)=\{(i,j):\mu_{N,B}(i,j)\geq 1\}.
$$

Cela a conduit à la quantité expérimentale :

$$
\widehat\varepsilon_*(N,B)=\frac{\varepsilon_*(N,B)}{B}.
$$

Jusqu'à $N=10^7$, les données suggèrent une décroissance de $\widehat\varepsilon_*(N,B)$.

### Cache persistant

Un cache SQLite persistant a été ajouté :

- `src/syracuse/cache.py`
- emplacement type : `outputs/cache/syracuse.sqlite` (créé localement, non versionné par défaut)

Il stocke :

- `value -> next_value`
- `value -> steps`
- `value -> maximum`

Il permet de rattacher les suffixes déjà connus et d'éviter de recalculer les mêmes suites.

### Correction conceptuelle

La quantité $\varepsilon_*(N)$ n'est pas nécessairement monotone : ajouter une nouvelle orbite éloignée peut créer une nouvelle composante.

On a donc introduit une quantité plus robuste :

$$
\delta(N_1,N_2)=d(P_{N_2}\setminus P_{N_1},P_{N_1}),
$$

qui mesure la distance de raccordement des nouvelles orbites au support précédent.

Cette correction est formalisée dans :

- `plans/syracuse/note-formelle-epsilon-monotonie.md`

### Raccordement par blocs

On a mesuré la distance de raccordement par blocs jusqu'à $N=10^7$.

Artefacts :

- `outputs/block_attachment_bins_1000.md`
- `outputs/block_attachment_bins_1000.csv`
- figures associées régénérables via le CLI (voir `RAPPORT_PUBLICATION_COLLECTIF.md`)

Observation :

> chaque nouveau bloc testé touche le support précédent à l'échelle minimale de la grille `1000x1000`.

### Sensibilité à la métrique $d_\alpha$

Implémenté dans `src/syracuse/support.py` (`analyze_alpha_attachment`) et en CLI (`--alpha-attachment`) :

$$
d_\alpha((k,y),(k',y'))
=
\sqrt{\alpha^2(k-k')^2+(y-y')^2}.
$$

Artefacts :

- `outputs/alpha_attachment_bins_1000.md`
- `outputs/alpha_attachment_bins_1000.csv`

### Localisation des raccordements

Les cartes des cellules nouvellement ajoutées et la distance au support précédent sont produites par `plot_block_attachment_maps` lors du même passage `--block-attachment-limits` (fichier image régénérable).

### Agrégats arithmétiques par blocs

Le drapeau `--block-arithmetic` agrège par segment $[n_{\mathrm{start}}, n_{\mathrm{stop}}]$ les temps d'arrêt, maxima, statistiques sur la dynamique impaire compressée et une grandeur liée au budget \(\sum_i (\log_2(3) - a_i)\).

Artefacts :

- `outputs/block_arithmetic.md`
- `outputs/block_arithmetic.csv`

### Validation locale par alpha complex

Pour une fenêtre dense ou un trou persistant : extraction des points réels, alpha complex, comparaison avec la TDA cubique sur grille.

Statut : première validation locale effectuée.

Artefacts :

- `outputs/alpha_window_report.md`
- `outputs/alpha_window_persistence.csv`
- figures `outputs/alpha_window_*.png` (régénérables)

Résultat :

> dans la fenêtre dense testée, l'alpha complex détecte beaucoup de cycles locaux, mais la persistance maximale $H_1$ reste faible (`0.00010929`). Cela suggère une micro-lacunarité locale plutôt qu'un grand trou robuste dans cette fenêtre.

## Ce qui reste ouvert

- Cartographie fine « géométrie \(\leftrightarrow\) invariants arithmétiques » au niveau des cellules ou sous-régions (pas seulement par blocs d'entiers de départ).
- Exploration systématique d'autres coupures de blocs, résolutions $B$, fenêtres alpha complexes.
- Toute affirmation sur les limites $N\to\infty$ : hors périmètre empirique actuel.

## Publication collective : synthèse unique

Un rapport de clôture de cycle (**objectifs, livrables, reproduction, limites**) est disponible :

- `plans/syracuse/RAPPORT_PUBLICATION_COLLECTIF.md`

Script bash pour le pipeline bloc jusqu'à $10^7$ :

- `scripts/reproduce_collective_block_pipeline.sh`

## Direction après cette livraison

Les chantiers logiciels « priorité 1–3 » de l'ancienne feuille de route sont **disponibles dans le dépôt** pour les analyses par blocs et la métrique $d_\alpha$. La suite côté recherche porte surtout sur l'**interprétation mathématique**, les extensions expérimentales listées dans « Ce qui reste ouvert », et la prudence asymptotique.
