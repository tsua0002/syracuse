# Note méthodologique : choix des complexes TDA

## Objet

On souhaite étudier la topologie des supports géométriques associés aux orbites de Syracuse dans le plan temps-valeur logarithmique.

L'objet idéal est un épaississement continu :

$$
P_N^\varepsilon=\{z : d(z,P_N)\leq \varepsilon\},
$$

où :

$$
P_N=\{(k,\log_{10}(u_k(n))) : 1\leq n\leq N,\ 0\leq k\leq \tau(n)\}.
$$

## Čech

Le complexe de Čech est le plus fidèle à l'union de boules :

$$
\check C_\varepsilon(P_N).
$$

Il bénéficie du théorème du nerf : sous de bonnes hypothèses, il possède le même type d'homotopie que l'union des boules.

Cependant, il est généralement coûteux à calculer pour de grands nuages de points.

## Vietoris-Rips

Le complexe de Vietoris-Rips est plus pratique :

$$
VR_\varepsilon(P_N).
$$

Il ajoute un simplexe dès que les points sont deux à deux à distance au plus $\varepsilon$.

Il est moins fidèle géométriquement que Čech, mais beaucoup plus accessible numériquement, avec des bibliothèques optimisées.

Il existe des inclusions classiques entre Čech et Rips, à un facteur d'échelle près. Rips est donc une approximation contrôlée, utile pour l'exploration.

## Alpha Complex

En dimension $2$, l'alpha complex est probablement le meilleur compromis pour valider localement les résultats.

Il est proche de Čech dans l'esprit, mais s'appuie sur la triangulation de Delaunay. Il est donc plus efficace en basse dimension.

## Recommandation

L'ordre de travail recommandé est :

1. Complexes cubiques sur grille fixe pour les grands $N$.
2. Vietoris-Rips sur des sous-échantillons ou fenêtres locales.
3. Alpha complex sur des fenêtres locales pour valider géométriquement l'épaississement continu.
4. Čech complet seulement si nécessaire, sur de petits ensembles.

## Position actuelle

Pour l'étude globale à très grand $N$, les complexes cubiques sur grille fixe restent les plus raisonnables.

Pour l'étude locale fine d'une région dense ou d'un trou persistant, l'alpha complex semble plus pertinent que Rips si l'on veut approcher l'union de boules.

Rips reste recommandé pour une première exploration rapide, mais pas comme validation géométrique finale.

## Première validation locale

Une première fenêtre dense du support normalisé a été testée par alpha complex.

Paramètres :

- limite : $N=10^6$ ;
- grille source : $1000\times1000$ ;
- fenêtre normalisée : $x\in[0.15,0.55]$, $y\in[0.25,0.70]$ ;
- nombre maximal de points : `5000`.

Artefacts :

- `outputs/alpha_window_points.png`
- `outputs/alpha_window_diagram.png`
- `outputs/alpha_window_barcode.png`
- `outputs/alpha_window_report.md`

Résultat :

$$
\max \operatorname{pers}(H_1)\approx 0.00010929.
$$

Interprétation prudente : la fenêtre contient de nombreux petits cycles, mais pas de grand trou local robuste à cette échelle. L'alpha complex confirme donc plutôt une micro-lacunarité qu'une obstruction topologique forte dans cette fenêtre dense.
