# Syracuse Hypotheses

## Termination on the tested range

- Hypothesis: Every start value in the tested range reaches 1.
- Result: confirmed on this finite range
- Evidence: Checked 1000 sequences; all final values are 1: True.

## Powers of two

- Hypothesis: A power of two reaches 1 in log2(n) steps and never exceeds its start.
- Result: confirmed on this finite range
- Evidence: Checked powers of two up to 1000: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512].

## Longest sequence versus highest peak

- Hypothesis: The start value with the longest sequence is also the one with the highest peak.
- Result: rejected
- Evidence: Longest sequence: start=871, steps=178, max=190996. Highest peak: start=703, steps=170, max=250504.

## Odd starts versus even starts

- Hypothesis: Odd start values have a higher average stopping time than even start values.
- Result: confirmed on this finite range
- Evidence: Odd average steps=65.80; even average steps=53.29.
