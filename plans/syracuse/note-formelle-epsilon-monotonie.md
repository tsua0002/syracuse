# Note formelle : échelle de connexion et monotonie

## Objet métrique fixe

On considère les orbites de Syracuse :

$$
u_0(n)=n,
\qquad
u_{k+1}(n)=T(u_k(n)).
$$

Pour $N\geq 1$, on définit l'ensemble :

$$
P_N=
\{(k,\log_{10}(u_k(n))) :
1\leq n\leq N,\ 0\leq k\leq \tau(n)\}.
$$

On munit le plan d'une métrique fixe. Par exemple, pour un paramètre $\alpha>0$ :

$$
d_\alpha((k,y),(k',y'))
=
\sqrt{\alpha^2(k-k')^2+(y-y')^2}.
$$

Le paramètre $\alpha$ fixe le poids relatif entre l'axe du temps et l'axe logarithmique des valeurs.

## Épaississement continu

Pour $\varepsilon\geq 0$, on définit l'épaississement :

$$
P_N^\varepsilon=
\{z\in\mathbb R^2 : d_\alpha(z,P_N)\leq\varepsilon\}.
$$

Autrement dit, $P_N^\varepsilon$ est l'union des boules fermées de rayon $\varepsilon$ centrées sur les points de $P_N$ :

$$
P_N^\varepsilon=
\bigcup_{p\in P_N}\overline B_\alpha(p,\varepsilon).
$$

## Échelle de connexion

On définit :

$$
\varepsilon_*(N)
=
\inf\{\varepsilon\geq 0 :
P_N^\varepsilon \text{ est connexe}\}.
$$

Cette quantité mesure l'échelle minimale à laquelle les orbites issues de $1,\ldots,N$ deviennent connectées dans le plan temps-valeur logarithmique.

## Lemme de monotonie

Pour tout $N\geq 1$, on a :

$$
P_N\subseteq P_{N+1}.
$$

Donc, pour tout $\varepsilon\geq 0$ :

$$
P_N^\varepsilon\subseteq P_{N+1}^\varepsilon.
$$

Si $P_N^\varepsilon$ est connexe, alors $P_{N+1}^\varepsilon$ contient cet ensemble connexe ainsi que de nouveaux points épaissis.

Cependant, attention : ajouter un ensemble disjoint à un ensemble connexe peut rendre l'union non connexe. La monotonie de la connexité n'est donc pas automatique pour l'épaississement complet si les nouveaux points apparaissent loin du support précédent.

La bonne quantité monotone est plutôt l'échelle de raccordement des nouvelles orbites au support précédent :

$$
\delta(N+1)=d_\alpha(P_{N+1}\setminus P_N,\ P_N).
$$

On a alors :

$$
P_{N+1}^{\varepsilon}
\text{ est connecté à }P_N^{\varepsilon}
\quad\text{dès que}\quad
\varepsilon\geq \frac{\delta(N+1)}{2}.
$$

Ainsi, l'étude de la limite doit distinguer :

1. la connexité interne de $P_N^\varepsilon$ ;
2. la distance des nouvelles orbites au support déjà construit.

## Conséquence méthodologique

La fonction $\varepsilon_*(N)$ n'est pas trivialement décroissante pour l'épaississement continu de l'union complète : une nouvelle orbite peut créer une nouvelle composante éloignée.

En revanche, l'intuition géométrique pertinente est :

$$
\delta(N)=d_\alpha(P_N\setminus P_{N-1},P_{N-1})
$$

et l'hypothèse expérimentale devient :

$$
\delta(N)\to 0.
$$

Cela signifie que les nouvelles orbites apparaissent de plus en plus près du support déjà construit.

## Lien avec les expériences précédentes

Les expériences sur grilles normalisées mesuraient une quantité apparentée, mais avec une normalisation variable ou discrète. Elles suggèrent que l'échelle de raccordement diminue quand $N$ augmente.

La reformulation via $\delta(N)$ est plus robuste mathématiquement :

- elle utilise un espace métrique fixe ;
- elle évite l'ambiguïté de la normalisation dépendant de $N$ ;
- elle correspond directement à l'idée que les nouvelles courbes "repassent" près des régions déjà explorées.

## Programme numérique

Pour tester cette formulation, on peut approximer :

$$
\delta_N^{\mathrm{bloc}}
=
d_\alpha(P_{N_2}\setminus P_{N_1},P_{N_1})
$$

pour des blocs :

$$
N_1<N_2.
$$

Concrètement :

1. construire le support des orbites jusqu'à $N_1$ ;
2. construire le support ajouté entre $N_1+1$ et $N_2$ ;
3. mesurer la distance minimale entre les deux supports ;
4. répéter pour des blocs croissants.

Si ces distances décroissent, cela soutient l'idée que les nouvelles orbites se raccordent à une échelle de plus en plus petite.

## Statut

Cette note corrige une intuition initiale trop rapide : la monotonie de $\varepsilon_*(N)$ n'est pas automatique.

La quantité plus naturellement monotone ou asymptotiquement pertinente est la distance de raccordement des nouveaux points au support antérieur.
