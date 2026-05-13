# Odd-To-Odd Compression Report

For each odd value $m$, define:

$$a(m)=v_2(3m+1), \qquad C(m)=\frac{3m+1}{2^{a(m)}}.$$

The compressed trajectory keeps only odd values and labels each step by $a(m)$.

- Analysed starts: `10000`
- Non-empty compressed trajectories: `9986`
- Mean exponent: `2.2549`
- Mean frequency of exponent `1`: `0.4401`
- Mean net log2 growth budget: `-11.0810`
- Threshold $\log_2(3)$: `1.5850`

Extremal examples:

- Longest compressed trajectory: `n=6171`, `compressed_length=96`, `mean_exponent=1.7188`, `net_log2_factor=-12.8436`
- Highest exponent-1 ratio: `n=151`, `ratio=0.6667`, `compressed_length=3`
- Largest net growth budget: `n=3`, `net_log2_factor=-1.8301`, `compressed_length=2`

Reading guide:

A compressed step has approximate multiplicative factor $3/2^{a_i}$. Values $a_i=1$ locally expand the odd subsequence, while $a_i\geq 2$ locally contract it. The quantity $L\log_2(3)-\sum_i a_i$ summarizes the net log-scale growth budget over a compressed trajectory of length $L$.