#!/usr/bin/env bash
# Regenerate block attachment, d_alpha sensitivity, and per-block arithmetic reports
# matching outputs/block_attachment_bins_1000*, alpha_attachment_bins_1000*, block_arithmetic*.
# Requires a populated SQLite sequence cache up to max(block limits).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
CACHE="${SYRACUSE_CACHE:-${ROOT}/outputs/cache/syracuse.sqlite}"
mkdir -p "$(dirname "${CACHE}")"

exec syracuse-generate \
  --output-dir "${ROOT}/outputs" \
  --sequence-cache "${CACHE}" \
  --block-attachment-limits \
    10000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 \
  --block-attachment-bins 1000 \
  --alpha-attachment \
  --alpha-values 0.25 0.5 1 2 4 \
  --block-arithmetic
