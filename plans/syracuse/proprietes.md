# Proprietes observees de la fonction de Syracuse

## Remarque sur le calcul experimental

Quand on dit que le setup trouve `143` nombres tels que $M(n)=n$, cela signifie :

> parmi les entiers $n$ de $1$ a $1000$, il y en a `143` dont la suite de Syracuse ne depasse jamais la valeur initiale $n$.

Autrement dit, pour ces `143` valeurs :

$$
M(n)=\max_{0 \leq k \leq \tau(n)} u_k(n)=n.
$$

Ce n'est pas une preuve generale. C'est seulement une observation sur l'intervalle fini $[1,1000]$.

## Definitions

On considere la fonction de Syracuse $T : \mathbb{N}^* \to \mathbb{N}^*$ definie par :

$$
T(n)=
\begin{cases}
\dfrac{n}{2} & \text{si } n \equiv 0 \pmod 2,\\
3n+1 & \text{si } n \equiv 1 \pmod 2.
\end{cases}
$$

Pour un entier $n \geq 1$, on note sa suite de Syracuse :

$$
u_0(n)=n,
\qquad
u_{k+1}(n)=T(u_k(n)).
$$

Si la suite atteint $1$, on note son temps d'arret :

$$
\tau(n)=\min\{k \in \mathbb{N} \mid u_k(n)=1\}.
$$

On note aussi le maximum atteint par la suite :

$$
M(n)=\max_{0 \leq k \leq \tau(n)} u_k(n).
$$

## Propriete de suffixe

La fonction $T$ est deterministe : pour chaque entier $n$, il existe un unique successeur $T(n)$.

Donc si une suite issue de $n$ atteint un entier $m$, alors la suite issue de $m$ est exactement le suffixe de la suite issue de $n$ a partir de $m$.

Si $i_n(m)$ designe le premier rang ou $m$ est atteint :

$$
i_n(m)=\min\{k \in \mathbb{N} \mid u_k(n)=m\},
$$

alors :

$$
\forall j \geq 0,
\qquad
u_j(m)=u_{i_n(m)+j}(n).
$$

En particulier :

$$
\tau(n)=i_n(m)+\tau(m).
$$

Donc :

$$
\tau(m)=\tau(n)-i_n(m).
$$

Si $m \neq n$, alors $i_n(m)>0$, donc :

$$
\tau(m)<\tau(n).
$$

## Cas du maximum $M(n)$

En prenant $m=M(n)$, on obtient :

$$
\forall j \geq 0,
\qquad
u_j(M(n))=u_{i_n(M(n))+j}(n).
$$

Ainsi :

$$
\tau(M(n))=\tau(n)-i_n(M(n)).
$$

Donc :

$$
\tau(M(n)) \leq \tau(n).
$$

L'inegalite est stricte lorsque $M(n)$ n'est pas le terme initial :

$$
M(n)\neq n
\quad \Longrightarrow \quad
\tau(M(n))<\tau(n).
$$

En revanche, si $M(n)=n$, alors $i_n(M(n))=0$, et donc :

$$
\tau(M(n))=\tau(n).
$$

## Cas impair

Si $n$ est impair, alors :

$$
T(n)=3n+1.
$$

Donc la suite issue de $n$ commence par :

$$
n \to 3n+1 \to T(3n+1) \to T^2(3n+1) \to \cdots
$$

Autrement dit, la suite de $n$ est obtenue en calculant d'abord la suite issue de $3n+1$, puis en ajoutant $n$ au debut.

Formellement :

$$
u_0(n)=n,
$$

et pour tout $j \geq 0$ :

$$
u_{j+1}(n)=u_j(3n+1).
$$

Donc :

$$
\tau(n)=1+\tau(3n+1).
$$

Et comme $3n+1>n$ pour tout $n \geq 1$, on a :

$$
M(n)=M(3n+1).
$$

Ainsi, pour un entier impair $n>1$, le maximum ne peut pas etre $n$ :

$$
n \text{ impair},\ n>1
\quad \Longrightarrow \quad
M(n)>n.
$$

## Cas pair

Si $n$ est pair, alors :

$$
T(n)=\frac{n}{2}.
$$

La suite issue de $n$ commence donc par :

$$
n \to \frac{n}{2} \to T\left(\frac{n}{2}\right) \to \cdots
$$

Comme pour le cas impair, on obtient :

$$
\tau(n)=1+\tau\left(\frac{n}{2}\right).
$$

Et pour le maximum :

$$
M(n)=\max\left(n, M\left(\frac{n}{2}\right)\right).
$$

Donc :

$$
M(n)=n
\quad \Longleftrightarrow \quad
M\left(\frac{n}{2}\right)\leq n.
$$

Cela explique pourquoi les puissances de $2$ verifient $M(n)=n$, mais aussi pourquoi elles ne sont pas les seuls nombres a verifier cette propriete.

Par exemple :

$$
20 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1.
$$

Ici :

$$
M(20)=20.
$$

Pourtant $20$ n'est pas une puissance de $2$.

## Consequence algorithmique

Quand on calcule entierement la suite issue de $n$, on calcule automatiquement les suites issues de tous les termes rencontres.

Si :

$$
m \in \{u_0(n),u_1(n),\ldots,u_{\tau(n)}(n)\},
$$

alors il est inutile de recalculer la suite issue de $m$.

On connait deja :

$$
\tau(m)=\tau(n)-i_n(m),
$$

et :

$$
M(m)\leq M(n).
$$

Cette propriete suggere une optimisation par memoisation, c'est-a-dire par mise en cache des resultats deja calcules : lorsqu'une suite atteint un nombre deja connu, on peut reutiliser directement les valeurs deja calculees.

Le mot `memoisation` est le terme technique usuel en informatique pour designer cette strategie. Il est proche de `memorisation`, mais plus precis : il ne s'agit pas seulement de retenir une information, il s'agit de reutiliser le resultat d'un calcul associe a une entree donnee.
