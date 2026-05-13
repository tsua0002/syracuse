# Syracuse Parity Report

Each trajectory is encoded by the binary word:

$$\varepsilon_k(n)=u_k(n)\bmod 2.$$

A `1` marks an odd value and a `0` marks an even value.

- Analysed starts: `10000`
- Mean stopping time: `84.97`
- Mean odd-value ratio: `0.3216`
- Mean odd transition count: `28.20`
- Mean longest zero-run: `5.70`

Extremal examples:

- Longest trajectory: `n=6171`, `steps=261`, `odd_transitions=96`
- Most odd transitions: `n=6171`, `odd_transitions=96`, `steps=261`
- Longest even run: `n=7407`, `max_zero_run=15`, `steps=57`

Reading guide:

Long runs of `0` correspond to repeated divisions by 2. Large odd-transition counts indicate trajectories with many upward `3n+1` moves. Comparing these metrics with the heatmap helps connect visual strata to parity patterns.