# Dense Support Thickening Report

For each threshold $\lambda$, define:

$$D_\lambda=\{\mu_N\geq\lambda\}.$$

The analysed object is the smallest 8-neighbourhood thickening that connects the support:

$$D_{\lambda,\varepsilon}=\operatorname{dilate}_\varepsilon(D_\lambda).$$

| threshold | epsilon | cells | thickened cells | beta0 before | beta1 before | beta1 after | largest radius |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20 | 54930 | 729883 | 20233 | 0 | 0 | 376.00 |
| 2 | 20 | 44068 | 655598 | 17005 | 0 | 3 | 355.58 |
| 5 | 20 | 30285 | 517063 | 12788 | 0 | 0 | 326.00 |
| 10 | 30 | 22516 | 459585 | 10991 | 0 | 1 | 296.00 |
| 20 | 20 | 14593 | 384933 | 8728 | 0 | 0 | 277.00 |
| 50 | 20 | 4317 | 306586 | 3424 | 0 | 2 | 159.00 |
| 100 | 71 | 628 | 307726 | 577 | 0 | 0 | 214.35 |

Highlights:

- Largest inscribed discrete disk: threshold `1`, epsilon `20`, radius `376.00` cells, center approximately at step `0.38`, log-value `0.376`.
- Most holes after minimal thickening: threshold `2`, holes `3`.

Interpretation:

This is a cubical thickening of a density support, not a smooth manifold. A positive and stable inscribed radius indicates local two-dimensional thickness at this grid scale. Holes that survive the minimal connecting thickening are better candidates for robust lacunae.