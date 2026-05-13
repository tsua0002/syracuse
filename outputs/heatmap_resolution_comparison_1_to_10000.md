# Density Resolution Comparison

This report compares the same empirical measure across several vertical bin resolutions.

| vertical bins | occupied cells | total cells | occupied ratio | max visits in one cell |
|---:|---:|---:|---:|---:|
| 120 | 14427 | 31440 | 45.8874% | 1225 |
| 240 | 23797 | 62880 | 37.8451% | 681 |
| 480 | 36831 | 125760 | 29.2867% | 347 |
| 960 | 53888 | 251520 | 21.4249% | 190 |

Reading guide:

If the same high-density regions remain visible while the occupied ratio and cell counts change, the structure is likely robust at this scale. If the regions move or disappear, the apparent continuity is mostly a binning artifact.