# Dense Support Thickening Report

For each threshold $\lambda$, define:

$$D_\lambda=\{\mu_N\geq\lambda\}.$$

The analysed object is the smallest 8-neighbourhood thickening that connects the support:

$$D_{\lambda,\varepsilon}=\operatorname{dilate}_\varepsilon(D_\lambda).$$

| threshold | epsilon | cells | thickened cells | beta0 before | beta1 before | beta1 after | largest radius |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 40 | 76078 | 2917410 | 33451 | 0 | 0 | 751.17 |
| 2 | 40 | 58749 | 2612279 | 27038 | 0 | 2 | 710.19 |
| 5 | 40 | 37118 | 2041306 | 18857 | 0 | 0 | 651.29 |
| 10 | 40 | 24409 | 1675065 | 14963 | 0 | 0 | 554.00 |
| 20 | 40 | 13034 | 1499667 | 10078 | 0 | 0 | 554.00 |
| 50 | 77 | 3135 | 1284754 | 3027 | 0 | 0 | 528.49 |
| 100 | 40 | 518 | 642003 | 518 | 0 | 0 | 218.00 |

Highlights:

- Largest inscribed discrete disk: threshold `1`, epsilon `40`, radius `751.17` cells, center approximately at step `0.38`, log-value `0.376`.
- Most holes after minimal thickening: threshold `2`, holes `2`.

Interpretation:

This is a cubical thickening of a density support, not a smooth manifold. A positive and stable inscribed radius indicates local two-dimensional thickness at this grid scale. Holes that survive the minimal connecting thickening are better candidates for robust lacunae.