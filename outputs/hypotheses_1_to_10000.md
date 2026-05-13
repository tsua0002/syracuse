# Syracuse Hypotheses

## Termination on the tested range

- Hypothesis: Every start value in the tested range reaches 1.
- Result: confirmed on this finite range
- Evidence: Checked 10000 sequences; all final values are 1: True.

## Powers of two

- Hypothesis: A power of two reaches 1 in log2(n) steps and never exceeds its start.
- Result: confirmed on this finite range
- Evidence: Checked powers of two up to 10000: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192].

## Longest sequence versus highest peak

- Hypothesis: The start value with the longest sequence is also the one with the highest peak.
- Result: rejected
- Evidence: Longest sequence: start=6171, steps=261, max=975400. Highest peak: start=9663, steps=184, max=27114424.

## Odd starts versus even starts

- Hypothesis: Odd start values have a higher average stopping time than even start values.
- Result: confirmed on this finite range
- Evidence: Odd average steps=91.34; even average steps=78.59.
