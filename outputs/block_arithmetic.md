# Block Arithmetic Report

This report aggregates arithmetic trajectory metrics by root block.

| block | mean steps | max steps | mean exponent | freq exponent 1 | mean net log2 factor |
|---:|---:|---:|---:|---:|---:|
| 10001-50000 | 104.3862 | 323 | 2.1867 | 0.4544 | -13.9680 |
| 50001-100000 | 114.5745 | 350 | 2.1628 | 0.4598 | -15.3872 |
| 100001-200000 | 121.8476 | 382 | 2.1484 | 0.4630 | -16.3873 |
| 200001-500000 | 130.6540 | 448 | 2.1338 | 0.4664 | -17.5908 |
| 500001-1000000 | 138.5993 | 524 | 2.1238 | 0.4686 | -18.7096 |
| 1000001-2000000 | 145.7478 | 556 | 2.1159 | 0.4705 | -19.7097 |
| 2000001-5000000 | 154.4186 | 596 | 2.1076 | 0.4724 | -20.9128 |
| 5000001-10000000 | 162.4573 | 685 | 2.1006 | 0.4741 | -22.0315 |

Reading guide:

The mean compressed exponent should be compared with log2(3). Values above log2(3) correspond to average contraction in the odd-to-odd compressed dynamics.