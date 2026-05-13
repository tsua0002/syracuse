# Epsilon Sweep Robustness Note

## Question

We test whether the normalized connection scale

$$
\varepsilon_*(N)
$$

appears to decrease as the number of Syracuse trajectories grows.

The object is the normalized support:

$$
D_1(N)=\{\mu_N\geq 1\}
$$

on a square grid. The value $\varepsilon_*(N)$ is the smallest grid dilation, divided by the grid size, that makes the support connected.

## Resolution Check

For the same limits and two grid resolutions:

| N | epsilon, 1000 bins | epsilon, 2000 bins |
|---:|---:|---:|
| 1000 | 0.0280 | 0.0280 |
| 3000 | 0.0240 | 0.0245 |
| 10000 | 0.0200 | 0.0200 |
| 30000 | 0.0190 | 0.0185 |
| 50000 | 0.0180 | 0.0185 |

The agreement is good. This suggests the observed scale is not mainly a grid-resolution artifact at these resolutions.

## Larger N Check

At 1000 bins:

| N | epsilon normalized | radius normalized |
|---:|---:|---:|
| 10000 | 0.0200 | 0.3760 |
| 30000 | 0.0190 | 0.3544 |
| 50000 | 0.0180 | 0.3860 |
| 100000 | 0.0160 | 0.3840 |
| 200000 | 0.0140 | 0.3700 |

The normalized connection scale keeps decreasing up to $N=200000$.

The largest inscribed radius remains large, roughly in the range:

$$
0.35 \leq r_{\max} \leq 0.39.
$$

## Interpretation

The approximation is currently supported by two independent checks:

1. changing the grid resolution from `1000` to `2000` gives nearly the same normalized $\varepsilon_*(N)$;
2. increasing $N$ from `10000` to `200000` decreases $\varepsilon_*(N)$ from `0.020` to `0.014`.

This supports the working hypothesis that the normalized raw support becomes more connected as $N$ grows.

It does not yet prove that:

$$
\varepsilon_*(N)\to 0.
$$

But the current data are consistent with that possibility.

## Current Limitation

The sweep still depends on:

- the chosen normalization of axes;
- a square grid approximation;
- threshold $\lambda=1$;
- 8-neighbour discrete connectivity;
- the finite range of tested $N$.

The next stronger test is to push $N$ further and repeat the larger-$N$ sweep at `2000` bins for selected values.
