# Normalized Epsilon Sweep Report

For each limit $N$, this report analyses the normalized support:

$$D_1(N)=\{\mu_N\geq 1\}.$$

The main quantity is the smallest normalized thickening scale making the support connected:

$$\varepsilon_*(N)=\frac{\text{minimal dilation in cells}}{\text{grid size}}.$$

| N | bins | epsilon cells | epsilon normalized | radius normalized | occupied cells | beta0 before | beta1 after |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 200000 | 2000 | 29 | 0.014500 | 0.369834 | 208107 | 47951 | 0 |
| 500000 | 2000 | 28 | 0.014000 | 0.351500 | 275850 | 53263 | 3 |
| 1000000 | 2000 | 28 | 0.014000 | 0.342500 | 325761 | 57408 | 3 |

Initial reading:

Across this sampled range, $\varepsilon_*(N)$ decreases from `0.014500` to `0.014000`.
The normalized largest inscribed radius does not increase from `0.369834` to `0.342500`.

If $\varepsilon_*(N)$ trends toward zero as $N$ grows, it supports the idea that the raw supports approach a connected continuum. If it stabilizes away from zero, the limiting support may retain macroscopic gaps at this normalization.