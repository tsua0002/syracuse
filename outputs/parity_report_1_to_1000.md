# Syracuse Parity Report

Each trajectory is encoded by the binary word:

$$\varepsilon_k(n)=u_k(n)\bmod 2.$$

A `1` marks an odd value and a `0` marks an even value.

- Analysed starts: `1000`
- Mean stopping time: `59.54`
- Mean odd-value ratio: `0.3165`
- Mean odd transition count: `19.65`
- Mean longest zero-run: `5.08`

Extremal examples:

- Longest trajectory: `n=871`, `steps=178`, `odd_transitions=65`
- Most odd transitions: `n=871`, `odd_transitions=65`, `steps=178`
- Longest even run: `n=151`, `max_zero_run=10`, `steps=15`

Reading guide:

Long runs of `0` correspond to repeated divisions by 2. Large odd-transition counts indicate trajectories with many upward `3n+1` moves. Comparing these metrics with the heatmap helps connect visual strata to parity patterns.