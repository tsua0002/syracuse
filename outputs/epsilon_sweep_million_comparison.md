# Epsilon Sweep Million Comparison

## Setup

We compare the normalized connection scale:

$$
\varepsilon_*(N)
$$

for the raw normalized support:

$$
D_1(N)=\{\mu_N\geq 1\}.
$$

The sweep uses the persistent SQLite sequence cache:

`outputs/cache/syracuse.sqlite`

## Results

| N | epsilon, 1000 bins | epsilon, 2000 bins |
|---:|---:|---:|
| 200000 | 0.0140 | 0.0145 |
| 500000 | 0.0140 | 0.0140 |
| 1000000 | 0.0140 | 0.0140 |

The agreement between `1000` and `2000` bins is strong at high N.

## Interpretation

The earlier decrease of $\varepsilon_*(N)$ continues until about $N=200000$, then the tested values form a plateau near:

$$
\varepsilon_*(N)\approx 0.014.
$$

At this stage, the data no longer supports a clearly decreasing trend beyond $N=200000$ at these grid resolutions.

Two interpretations remain possible:

1. the limiting support retains a macroscopic normalized gap near `0.014`;
2. the grid resolutions `1000` and `2000` are still too coarse to detect later decreases.

The current evidence favours a real plateau at this scale, because doubling the resolution does not significantly change the value.

## Inscribed Radius

At `2000` bins:

| N | normalized radius |
|---:|---:|
| 200000 | 0.369834 |
| 500000 | 0.351500 |
| 1000000 | 0.342500 |

The support remains macroscopically thick even while the largest inscribed radius slowly decreases.

## Next Reliable Test

To distinguish a true plateau from a resolution effect, the next useful tests are:

- run selected high N at `4000` bins;
- or implement curve-level thickening instead of grid-level support thickening.
