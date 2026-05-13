# Parity Heatmap Cross Analysis

The parity metric heatmaps project trajectory-level parity metrics onto each visited point.

For a cell in the plane, the displayed value is the average metric among all trajectories visiting that cell.

This helps identify whether visual regions are mostly carried by trajectories with many odd transitions, high odd ratios, long even runs, or long stopping times.

## Longest stopping times

| start | steps | odd transitions | odd ratio | max zero-run | maximum |
|---:|---:|---:|---:|---:|---:|
| 6171 | 261 | 96 | 0.3702 | 6 | 975400 |
| 9257 | 259 | 95 | 0.3692 | 6 | 975400 |
| 6943 | 256 | 94 | 0.3696 | 6 | 975400 |
| 7963 | 251 | 92 | 0.3690 | 7 | 497176 |
| 8959 | 246 | 90 | 0.3684 | 7 | 497176 |
| 6591 | 243 | 89 | 0.3689 | 6 | 975400 |
| 9887 | 241 | 88 | 0.3678 | 6 | 975400 |
| 9897 | 241 | 88 | 0.3678 | 5 | 481624 |
| 7422 | 238 | 87 | 0.3682 | 5 | 481624 |
| 7423 | 238 | 87 | 0.3682 | 5 | 481624 |

## Longest even runs

| start | max zero-run | steps | odd transitions | odd ratio | maximum |
|---:|---:|---:|---:|---:|---:|
| 7407 | 15 | 57 | 17 | 0.3103 | 427192 |
| 9375 | 15 | 47 | 13 | 0.2917 | 360448 |
| 5461 | 14 | 15 | 1 | 0.1250 | 16384 |
| 7281 | 14 | 18 | 2 | 0.1579 | 21844 |
| 8192 | 13 | 13 | 0 | 0.0714 | 8192 |
| 1365 | 12 | 13 | 1 | 0.1429 | 4096 |
| 1887 | 12 | 37 | 10 | 0.2895 | 28672 |
| 2730 | 12 | 14 | 1 | 0.1333 | 4096 |
| 2831 | 12 | 35 | 9 | 0.2778 | 28672 |
| 3774 | 12 | 38 | 10 | 0.2821 | 28672 |

Initial reading:

Long stopping times are mainly associated with many odd transitions, not simply with a single long run of divisions by 2. Long zero-runs appear as sharp descent events and can occur in comparatively short trajectories.