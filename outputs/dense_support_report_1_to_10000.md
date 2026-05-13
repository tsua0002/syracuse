# Dense Support Thickening Report

For each threshold $\lambda$, define:

$$D_\lambda=\{\mu_N\geq\lambda\}.$$

The analysed object is the smallest 8-neighbourhood thickening that connects the support:

$$D_{\lambda,\varepsilon}=\operatorname{dilate}_\varepsilon(D_\lambda).$$

| threshold | epsilon | cells | thickened cells | beta0 before | beta1 before | beta1 after | largest radius |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 23797 | 45221 | 1085 | 711 | 2 | 85.00 |
| 2 | 5 | 20393 | 41654 | 843 | 742 | 3 | 89.00 |
| 5 | 5 | 16182 | 33332 | 645 | 524 | 0 | 84.00 |
| 10 | 5 | 13530 | 30425 | 614 | 413 | 0 | 79.00 |
| 20 | 5 | 10738 | 26492 | 703 | 330 | 0 | 67.74 |
| 50 | 5 | 6135 | 21411 | 1064 | 215 | 0 | 67.00 |
| 100 | 5 | 2446 | 14939 | 674 | 10 | 0 | 34.01 |

Highlights:

- Largest inscribed discrete disk: threshold `2`, epsilon `5`, radius `89.00` cells, center approximately at step `88.50`, log-value `2.741`.
- Most holes after minimal thickening: threshold `2`, holes `3`.

Interpretation:

This is a cubical thickening of a density support, not a smooth manifold. A positive and stable inscribed radius indicates local two-dimensional thickness at this grid scale. Holes that survive the minimal connecting thickening are better candidates for robust lacunae.