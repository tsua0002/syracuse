# Note de recherche : support géométrique normalisé des orbites de Syracuse

## Objet

On considère les orbites de Syracuse issues des entiers $1\leq n\leq N$ :

$$
u_0(n)=n,
\qquad
u_{k+1}(n)=T(u_k(n)).
$$

On étudie leur support dans le plan temps-valeur logarithmique :

$$
P_N=
\{(k,\log_{10}(u_k(n))) :
1\leq n\leq N,\ 0\leq k\leq \tau(n)\}.
$$

On normalise ensuite les deux axes :

$$
x=\frac{k}{k_{\max}(N)},
\qquad
y=\frac{\log_{10}(u_k(n))}{\log_{10}(u_{\max}(N))},
$$

où :

$$
k_{\max}(N)=\max_{1\leq n\leq N}\tau(n),
$$

et :

$$
u_{\max}(N)=\max_{1\leq n\leq N}\max_k u_k(n).
$$

On obtient ainsi un nuage normalisé :

$$
\widetilde P_N\subset [0,1]^2.
$$

## Support brut discrétisé

Pour une grille carrée de taille $B\times B$, on définit la mesure empirique :

$$
\mu_{N,B}(i,j)=
\#\{(x,y)\in \widetilde P_N :
(x,y)\text{ tombe dans la cellule }(i,j)\}.
$$

Le support brut est :

$$
D_1(N,B)=\{(i,j):\mu_{N,B}(i,j)\geq 1\}.
$$

Le seuil $1$ signifie que l'on garde toute cellule visitée au moins une fois. Ce choix vise à rester au plus proche de l'objet géométrique brut, sans filtrer par densité.

## Échelle de connexion

On définit l'épaississement discret :

$$
D_1(N,B)^{(\varepsilon)}
=
\operatorname{dilate}_{\varepsilon}(D_1(N,B)),
$$

où $\varepsilon$ est un nombre entier de cellules.

On note :

$$
\varepsilon_*(N,B)
=
\min\{\varepsilon :
D_1(N,B)^{(\varepsilon)}
\text{ est connexe}\}.
$$

La quantité normalisée est :

$$
\widehat\varepsilon_*(N,B)
=
\frac{\varepsilon_*(N,B)}{B}.
$$

Elle mesure l'échelle minimale, dans le carré normalisé $[0,1]^2$, nécessaire pour connecter le support brut.

## Hypothèse expérimentale

Les données calculées suggèrent que :

$$
\widehat\varepsilon_*(N,B)
$$

diminue quand $N$ augmente.

L'hypothèse géométrique naturelle est :

$$
\widehat\varepsilon_*(N,B)\to 0
\quad\text{quand}\quad N\to\infty,
$$

pour des résolutions $B$ suffisamment fines.

Cette hypothèse ne dit pas que les orbites remplissent tout le carré $[0,1]^2$. Elle suggère seulement que le support brut normalisé devient connexe à une échelle de plus en plus petite.

## Épaisseur interne

On mesure aussi le rayon du plus grand disque discret inscrit dans le support épaissi minimal :

$$
r_{\max}(N,B).
$$

Les expériences montrent que ce rayon reste macroscopique, typiquement autour de :

$$
0.34\leq r_{\max}(N,B)\leq 0.39
$$

dans les tests effectués.

Cela suggère que l'objet n'est pas seulement un réseau filamenteux : il contient des zones qui se comportent comme des domaines bidimensionnels épais à l'échelle observée.

## Données actuelles

Pour $B=1000$, les données obtenues sont :

| $N$ | $\widehat\varepsilon_*(N,1000)$ | $r_{\max}(N,1000)$ |
|---:|---:|---:|
| 10000 | 0.020 | 0.376 |
| 50000 | 0.018 | 0.386 |
| 100000 | 0.016 | 0.384 |
| 200000 | 0.014 | 0.370 |
| 500000 | 0.014 | 0.362 |
| 1000000 | 0.014 | 0.345 |
| 2000000 | 0.013 | 0.377 |
| 5000000 | 0.012 | 0.365 |
| 10000000 | 0.011 | 0.354 |

Pour $B=2000$, on observe notamment :

| $N$ | $\widehat\varepsilon_*(N,2000)$ |
|---:|---:|
| 200000 | 0.0145 |
| 500000 | 0.0140 |
| 1000000 | 0.0140 |

La comparaison $B=1000$ contre $B=2000$ indique que les valeurs obtenues ne sont pas seulement un artefact grossier de résolution.

## Raccordement par blocs

La quantité $\widehat\varepsilon_*(N,B)$ est utile expérimentalement, mais elle n'est pas automatiquement monotone : une nouvelle orbite peut créer une nouvelle composante éloignée.

On introduit donc une quantité complémentaire. Pour deux bornes $N_1<N_2$, on mesure la distance de raccordement :

$$
\delta(N_1,N_2)
=
d(P_{N_2}\setminus P_{N_1},P_{N_1}).
$$

Numériquement, sur une grille fixe $1000\times1000$, chaque bloc testé jusqu'à $10^7$ touche le support précédent à l'échelle minimale de la grille :

| Bloc | distance minimale normalisée |
|---:|---:|
| 10001-50000 | 0.001 |
| 50001-100000 | 0.001 |
| 100001-200000 | 0.001 |
| 200001-500000 | 0.001 |
| 500001-1000000 | 0.001 |
| 1000001-2000000 | 0.001 |
| 2000001-5000000 | 0.001 |
| 5000001-10000000 | 0.001 |

Cela suggère que les nouveaux blocs ne se déposent pas comme des ensembles indépendants éloignés, mais se raccordent immédiatement au support déjà construit à l'échelle de la discrétisation.

## Sensibilité à la métrique

On teste aussi une famille de métriques fixes :

$$
d_\alpha((x,y),(x',y'))
=
\sqrt{\alpha^2(x-x')^2+(y-y')^2}.
$$

Pour $\alpha\in\{0.25,0.5,1,2,4\}$, les distances minimales de raccordement restent à l'échelle minimale imposée par la grille. Cela indique que le phénomène de raccordement n'est pas seulement dû à un choix particulier du poids relatif entre l'axe du temps et l'axe logarithmique.

## Lecture arithmétique par blocs

On agrège également des grandeurs arithmétiques sur les blocs de racines. Les métriques suivies sont notamment :

- temps d'arrêt moyen ;
- maximum logarithmique moyen ;
- ratio moyen de termes impairs ;
- fréquence des étapes compressées avec $a_i=1$ ;
- moyenne de $v_2(3m+1)$ ;
- budget moyen $r\log_2(3)-\sum_i a_i$.

Les blocs croissants montrent :

| Bloc | temps moyen | moyenne de $v_2(3m+1)$ | fréquence de $a_i=1$ | budget moyen |
|---:|---:|---:|---:|---:|
| 10001-50000 | 104.39 | 2.1867 | 0.4544 | -13.97 |
| 50001-100000 | 114.57 | 2.1628 | 0.4598 | -15.39 |
| 100001-200000 | 121.85 | 2.1484 | 0.4630 | -16.39 |
| 200001-500000 | 130.65 | 2.1338 | 0.4664 | -17.59 |
| 500001-1000000 | 138.60 | 2.1238 | 0.4686 | -18.71 |
| 1000001-2000000 | 145.75 | 2.1159 | 0.4705 | -19.71 |
| 2000001-5000000 | 154.42 | 2.1076 | 0.4724 | -20.91 |
| 5000001-10000000 | 162.46 | 2.1006 | 0.4741 | -22.03 |

La fréquence de $a_i=1$ augmente avec les blocs, ce qui correspond à davantage d'étapes localement expansives dans la dynamique compressée. Cependant, la moyenne de $v_2(3m+1)$ reste au-dessus de $\log_2(3)$, donc la dynamique reste contractante en moyenne.

Cette observation relie la géométrie du support aux valuations $2$-adiques : les nouveaux blocs remplissent le support avec des trajectoires plus longues et plus proches du seuil critique, sans devenir globalement expansives.

## Interprétation prudente

Les données soutiennent l'idée suivante :

> Le support empirique normalisé des orbites de Syracuse semble devenir de plus en plus connecté à petite échelle lorsque $N$ augmente, tout en conservant une épaisseur macroscopique.

Cette formulation est géométrique et expérimentale. Elle ne constitue pas une preuve de la conjecture de Syracuse.

## Questions ouvertes

1. La quantité $\widehat\varepsilon_*(N,B)$ tend-elle vers $0$ quand $N$ augmente ?
2. Quelle est la loi empirique la plus plausible : puissance de $N$, puissance de $\log N$, ou autre ?
3. L'effet persiste-t-il pour des résolutions $B=4000$ ou plus ?
4. L'épaississement des courbes affines par morceaux donne-t-il la même tendance que l'épaississement du support discrétisé ?
5. Les régions remplies correspondent-elles à des régimes arithmétiques identifiables via la dynamique compressée impair-vers-impair ?
6. Où se localisent précisément les zones de raccordement des nouveaux blocs ?

## Statut

Cette piste fournit un objet mesurable :

$$
\widehat\varepsilon_*(N,B),
$$

et une hypothèse expérimentale précise. Elle semble fertile pour relier visualisation, topologie computationnelle et dynamique arithmétique, sans prétendre résoudre la conjecture.
