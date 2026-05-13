# Normalized Epsilon Sweep Report

For each limit $N$, this report analyses the normalized support:

$$D_1(N)=\{\mu_N\geq 1\}.$$

The main quantity is the smallest normalized thickening scale making the support connected:

$$\varepsilon_*(N)=\frac{\text{minimal dilation in cells}}{\text{grid size}}.$$

| N | bins | epsilon cells | epsilon normalized | radius normalized | occupied cells | beta0 before | beta1 after |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10000000 | 1000 | 11 | 0.011000 | 0.354120 | 266474 | 16165 | 9 |

Initial reading:

Across this sampled range, $\varepsilon_*(N)$ does not decrease from `0.011000` to `0.011000`.
The normalized largest inscribed radius does not increase from `0.354120` to `0.354120`.

If $\varepsilon_*(N)$ trends toward zero as $N$ grows, it supports the idea that the raw supports approach a connected continuum. If it stabilizes away from zero, the limiting support may retain macroscopic gaps at this normalization.