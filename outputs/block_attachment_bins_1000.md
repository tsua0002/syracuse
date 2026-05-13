# Block Attachment Report

This report measures how far newly added support cells are from the previous support in a fixed grid.

| block | added cells | min distance | mean distance | max distance |
|---:|---:|---:|---:|---:|
| 10001-50000 | 27862 | 0.001000 | 0.004914 | 0.139714 |
| 50001-100000 | 15936 | 0.001000 | 0.002898 | 0.081154 |
| 100001-200000 | 20041 | 0.001000 | 0.002581 | 0.075326 |
| 200001-500000 | 29861 | 0.001000 | 0.004395 | 0.138033 |
| 500001-1000000 | 24811 | 0.001000 | 0.003793 | 0.111000 |
| 1000001-2000000 | 29347 | 0.001000 | 0.003510 | 0.155416 |
| 2000001-5000000 | 41977 | 0.001000 | 0.002332 | 0.077201 |
| 5000001-10000000 | 37271 | 0.001000 | 0.005243 | 0.163135 |

Reading guide:

The minimum distance checks whether each new block touches the previous support at grid scale. The mean and maximum distances describe how far the genuinely new cells extend away from the known support.