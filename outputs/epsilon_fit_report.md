# Epsilon Fit Report

This report fits empirical models to the normalized connection scale:

$$\varepsilon_*(N).$$

## Data

| N | epsilon |
|---:|---:|
| 10000 | 0.020000 |
| 50000 | 0.018000 |
| 100000 | 0.016000 |
| 200000 | 0.014000 |
| 500000 | 0.014000 |
| 1000000 | 0.014000 |
| 2000000 | 0.013000 |
| 5000000 | 0.012000 |
| 10000000 | 0.011000 |

## Fits

| model | C | alpha | R^2 |
|---|---:|---:|---:|
| `C * N^(-alpha)` | 0.04188352 | 0.082153 | 0.952123 |
| `C * log(N)^(-alpha)` | 0.19778797 | 1.027171 | 0.957469 |

## Reading

The best fit among these two simple models is `C * log(N)^(-alpha)` by $R^2$.

This is descriptive only. The data range is still short and should not be read as an asymptotic law.