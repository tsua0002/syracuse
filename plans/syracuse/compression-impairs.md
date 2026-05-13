# Compression impair-vers-impair

## Definition

On part de la fonction de Syracuse :

$$
T(n)=
\begin{cases}
\dfrac{n}{2} & \text{si } n \equiv 0 \pmod 2,\\
3n+1 & \text{si } n \equiv 1 \pmod 2.
\end{cases}
$$

Pour un entier impair $m$, on a toujours :

$$
3m+1 \equiv 0 \pmod 2.
$$

On peut donc ecrire de maniere unique :

$$
3m+1 = 2^{a(m)}m',
$$

ou $m'$ est impair et :

$$
a(m)=v_2(3m+1).
$$

On definit alors la transformation compressee :

$$
C(m)=\frac{3m+1}{2^{v_2(3m+1)}}.
$$

Ainsi, $C$ envoie un impair vers un impair.

## Exemple

Pour $n=11$, la suite complete est :

$$
11 \to 34 \to 17 \to 52 \to 26 \to 13 \to 40 \to 20 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1.
$$

En ne gardant que les impairs :

$$
11 \to 17 \to 13 \to 5 \to 1.
$$

Mais on garde aussi les exposants $a_i$ :

$$
3\cdot 11+1=34=2^1\cdot 17,
$$

$$
3\cdot 17+1=52=2^2\cdot 13,
$$

$$
3\cdot 13+1=40=2^3\cdot 5,
$$

$$
3\cdot 5+1=16=2^4\cdot 1.
$$

Donc la trajectoire compressee est :

$$
11 \xrightarrow{1} 17 \xrightarrow{2} 13 \xrightarrow{3} 5 \xrightarrow{4} 1.
$$

## Proposition de correction

Soit $m$ impair. Posons :

$$
a=v_2(3m+1)
$$

et :

$$
m'=\frac{3m+1}{2^a}.
$$

Alors $m'$ est impair, et la suite de Syracuse issue de $m$ atteint $m'$ apres exactement $a+1$ applications de $T$.

En effet :

$$
T(m)=3m+1=2^a m'.
$$

Puis, comme $2^a m'$ est pair, on divise successivement par $2$ :

$$
T^2(m)=2^{a-1}m',
$$

$$
T^3(m)=2^{a-2}m',
$$

et ainsi de suite jusqu'a :

$$
T^{a+1}(m)=m'.
$$

Donc l'etape compressee :

$$
m \mapsto C(m)
$$

resume exactement le bloc :

$$
m \to 3m+1 \to \frac{3m+1}{2} \to \cdots \to \frac{3m+1}{2^{a}}.
$$

## Consequence

Si une suite de Syracuse atteint $1$, alors la trajectoire compressee des impairs atteint aussi $1$.

Inversement, connaitre toutes les etapes compressees :

$$
m_0 \xrightarrow{a_0} m_1 \xrightarrow{a_1} m_2 \xrightarrow{a_2} \cdots \xrightarrow{a_{r-1}} m_r=1
$$

permet de reconstruire la suite complete en remplacant chaque fleche :

$$
m_i \xrightarrow{a_i} m_{i+1}
$$

par :

$$
m_i \to 3m_i+1 \to \frac{3m_i+1}{2} \to \cdots \to \frac{3m_i+1}{2^{a_i}}=m_{i+1}.
$$

La compression ne perd donc pas d'information dynamique essentielle : elle supprime seulement les divisions par $2$ intermediaires, tout en les conservant sous forme de labels $a_i$.

## Croissance locale

L'etape compressee verifie :

$$
\frac{C(m)}{m}
=
\frac{3m+1}{m2^{a(m)}}
=
\frac{3+\frac{1}{m}}{2^{a(m)}}.
$$

Pour $m$ grand, on a donc l'approximation :

$$
\frac{C(m)}{m}
\approx
\frac{3}{2^{a(m)}}.
$$

Ainsi :

- si $a(m)=1$, l'etape compressee est localement croissante ;
- si $a(m)=2$, l'etape compressee est approximativement contractante ;
- si $a(m)\geq 3$, l'etape compressee est fortement contractante.

Sur une trajectoire compressee de longueur $r$, le facteur heuristique total est :

$$
\prod_{i=0}^{r-1}\frac{3}{2^{a_i}}
=
\frac{3^r}{2^{\sum_i a_i}}.
$$

En echelle logarithmique base $2$, le budget de croissance est :

$$
r\log_2(3)-\sum_{i=0}^{r-1}a_i.
$$

Ce nombre devient un invariant experimental naturel pour comparer les trajectoires longues et les trajectoires typiques.
