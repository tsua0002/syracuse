# Note de recherche : contraction empirique de la dynamique de Syracuse compressée

## Objet

On étudie la dynamique de Syracuse après compression des chaînes de divisions successives par $2$. Il ne s'agit pas d'ignorer les entiers pairs, mais de les intégrer via leur partie impaire.

Tout entier $n\geq 1$ s’écrit de manière unique :

$$
n=2^{v_2(n)}m,
\qquad
m \text{ impair}.
$$

La trajectoire de $n$ commence alors par une descente déterministe :

$$
n \to \frac n2 \to \frac n{2^2} \to \cdots \to m.
$$

Autrement dit :

$$
T^{v_2(n)}(n)=m.
$$

Les pairs sont donc entièrement pris en compte par la valuation initiale $v_2(n)$, puis la partie non triviale de la dynamique est portée par les transitions entre impairs.

Pour $m$ impair, on pose :

$$
a(m)=v_2(3m+1),
\qquad
C(m)=\frac{3m+1}{2^{a(m)}}.
$$

La transformation $C$ est la version compressée impair-vers-impair de la dynamique de Syracuse. Elle quotient les blocs consécutifs de divisions par $2$ et remplace le bloc :

$$
m \to 3m+1 \to \frac{3m+1}{2} \to \cdots \to \frac{3m+1}{2^{a(m)}}
$$

par une seule transition :

$$
m \xrightarrow{a(m)} C(m).
$$

## Formule de contraction

Pour $m$ impair, on a exactement :

$$
\frac{C(m)}{m}
=
\frac{3+\frac{1}{m}}{2^{a(m)}}.
$$

Pour $m$ grand, cela donne l'approximation :

$$
\frac{C(m)}{m}
\approx
\frac{3}{2^{a(m)}}.
$$

Soit une trajectoire compressée :

$$
m_0 \xrightarrow{a_0} m_1 \xrightarrow{a_1} \cdots \xrightarrow{a_{r-1}} m_r.
$$

Le facteur multiplicatif heuristique sur $r$ étapes est :

$$
\prod_{i=0}^{r-1}\frac{3}{2^{a_i}}
=
\frac{3^r}{2^{\sum_i a_i}}.
$$

En logarithme base $2$, le budget de croissance associé est :

$$
B_r
=
r\log_2(3)-\sum_{i=0}^{r-1}a_i.
$$

La trajectoire est heuristiquement contractante lorsque :

$$
B_r<0,
$$

c’est-à-dire lorsque :

$$
\frac{1}{r}\sum_{i=0}^{r-1}a_i>\log_2(3).
$$

Comme :

$$
\log_2(3)\approx 1.58496,
$$

il suffit que la moyenne des valuations $a_i$ dépasse légèrement ce seuil pour obtenir une contraction logarithmique.

## Observation expérimentale

Sur les entiers $1\leq n\leq 10000$, le calcul assisté par ordinateur donne :

$$
\overline{a}\approx 2.2549.
$$

La fréquence moyenne des étapes avec $a_i=1$ est :

$$
\overline{\mathrm{freq}}(a_i=1)\approx 0.4401.
$$

La plus longue trajectoire compressée observée dans cet intervalle est obtenue pour :

$$
n=6171.
$$

Elle possède :

$$
r=96,
\qquad
\overline{a}\approx 1.7188.
$$

Cette moyenne reste supérieure à $\log_2(3)$, mais elle en est proche. Cela est cohérent avec l'observation empirique que les trajectoires longues correspondent à une contraction moyenne faible, sans être expansive.

## Statut mathématique

Cette observation ne constitue pas une preuve de la conjecture de Syracuse. Elle confirme numériquement une heuristique classique : la dynamique compressée est en moyenne contractante car les divisions par $2$ compensent statistiquement le facteur $3$.

Une preuve globale demanderait un contrôle uniforme excluant toute trajectoire exceptionnelle pour laquelle les valuations $a_i$ resteraient trop souvent petites. En particulier, il faudrait contrôler les segments longs où :

$$
\frac{1}{r}\sum_i a_i
\leq
\log_2(3).
$$

La littérature connue établit des résultats de type "presque tous" ou "densité logarithmique", mais pas la convergence de toutes les orbites.

## Lien avec l'heuristique probabiliste classique

Si l'on modélise $a(m)=v_2(3m+1)$ comme une variable aléatoire géométrique :

$$
\mathbb{P}(a=k)\approx 2^{-k},
\qquad k\geq 1,
$$

alors :

$$
\mathbb{E}[a]=2.
$$

On obtient donc :

$$
\mathbb{E}\left[\log_2\left(\frac{C(m)}{m}\right)\right]
\approx
\log_2(3)-2<0.
$$

Cette inégalité est le cœur de l'heuristique de contraction moyenne.

## Données produites

Dans ce projet, les artefacts associés sont :

- `outputs/odd_compression_summary_1_to_10000.csv`
- `outputs/odd_compression_diagnostics_1_to_10000.png`
- `outputs/odd_compression_report_1_to_10000.md`
- `plans/syracuse/compression-impairs.md`

Le code vérifie explicitement l'exemple :

$$
11 \xrightarrow{1} 17 \xrightarrow{2} 13 \xrightarrow{3} 5 \xrightarrow{4} 1.
$$

## Références

1. J. C. Lagarias, "The $3x+1$ Problem and its Generalizations", *American Mathematical Monthly*, 92(1), 1985, p. 3-23.  
   Référence de synthèse classique sur le problème $3x+1$, les temps d'arrêt, les variantes accélérées et les heuristiques probabilistes.

2. J. C. Lagarias, "The $3x+1$ Problem: An Annotated Bibliography (1963-1999)", arXiv:math/0309224.  
   Bibliographie annotée donnant le contexte historique et les références aux travaux de Terras, Everett, Crandall, Wirsching, etc.

3. R. Terras, "A stopping time problem on the positive integers", *Acta Arithmetica*, 30, 1976, p. 241-252.  
   Résultat fondateur montrant que presque tout entier possède un temps d'arrêt fini, dans un sens asymptotique.

4. C. J. Everett, "Iteration of the number-theoretic function $f(2n)=n$, $f(2n+1)=3n+2$", *Advances in Mathematics*, 25(1), 1977, p. 42-45.  
   Étude des vecteurs de parité et de propriétés structurelles de l'itération.

5. T. Tao, "Almost all orbits of the Collatz map attain almost bounded values", arXiv:1909.03562, 2019.  
   Résultat moderne montrant que presque toutes les orbites atteignent des valeurs presque bornées, au sens de la densité logarithmique.

## Conclusion

La formule empirique :

$$
\frac{1}{r}\sum_{i=0}^{r-1}a_i>\log_2(3)
$$

est une formulation naturelle du mécanisme de contraction moyenne de la dynamique de Syracuse compressée. Elle est conforme aux heuristiques classiques et aux données calculées sur $1\leq n\leq 10000$. Son intérêt n'est pas de fournir une preuve directe, mais d'identifier une quantité mesurable, comparable et visualisable pour distinguer trajectoires typiques, trajectoires longues et comportements proches du seuil critique.
