# Parity Heatmap Cross Analysis

The parity metric heatmaps project trajectory-level parity metrics onto each visited point.

For a cell in the plane, the displayed value is the average metric among all trajectories visiting that cell.

This helps identify whether visual regions are mostly carried by trajectories with many odd transitions, high odd ratios, long even runs, or long stopping times.

## Longest stopping times

| start | steps | odd transitions | odd ratio | max zero-run | maximum |
|---:|---:|---:|---:|---:|---:|
| 871 | 178 | 65 | 0.3687 | 5 | 190996 |
| 937 | 173 | 63 | 0.3678 | 6 | 250504 |
| 703 | 170 | 62 | 0.3684 | 6 | 250504 |
| 763 | 152 | 55 | 0.3660 | 6 | 9232 |
| 775 | 152 | 55 | 0.3660 | 5 | 9232 |
| 859 | 147 | 53 | 0.3649 | 6 | 9232 |
| 865 | 147 | 53 | 0.3649 | 6 | 9232 |
| 873 | 147 | 53 | 0.3649 | 5 | 9232 |
| 879 | 147 | 53 | 0.3649 | 5 | 10024 |
| 889 | 147 | 53 | 0.3649 | 7 | 21688 |

## Longest even runs

| start | max zero-run | steps | odd transitions | odd ratio | maximum |
|---:|---:|---:|---:|---:|---:|
| 151 | 10 | 15 | 3 | 0.2500 | 1024 |
| 201 | 10 | 18 | 4 | 0.2632 | 1024 |
| 227 | 10 | 13 | 2 | 0.2143 | 1024 |
| 302 | 10 | 16 | 3 | 0.2353 | 1024 |
| 341 | 10 | 11 | 1 | 0.1667 | 1024 |
| 402 | 10 | 19 | 4 | 0.2500 | 1024 |
| 403 | 10 | 19 | 4 | 0.2500 | 1816 |
| 423 | 10 | 32 | 9 | 0.3030 | 3220 |
| 454 | 10 | 14 | 2 | 0.2000 | 1024 |
| 537 | 10 | 22 | 5 | 0.2609 | 1816 |

Initial reading:

Long stopping times are mainly associated with many odd transitions, not simply with a single long run of divisions by 2. Long zero-runs appear as sharp descent events and can occur in comparatively short trajectories.