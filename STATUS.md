# Audit status — Provably Data-driven Lagrangian Relaxation for MILP

Updated 2026-08-14 for OpenReview `OwLuqetJuB` and arXiv `2605.19052v2`.

## Current state

- Publication gate: `SCOPED_PASS`
- Overall status: `VERIFIED_SCOPED_WITH_ONE_SOURCE_CORRECTION`
- Strict status: `NOT_READY`
- Contract: 6 claims / 12 possible points; 6 verified and 0 falsified
- Branch: `main`
- External score: not claimed
- Public state: repository-native docs/evidence only; private publication state removed

## Claim outcomes

| Claim | Outcome | Key result |
| --- | --- | --- |
| C1 | Verified, scoped | ERM `N` slope `-0.505629`; envelope holds across the recorded cells. |
| C2 | Verified, scoped | 32,766 packing pairs; exact KL and Fano factors remain valid. |
| C3 | Verified, scoped | SGA `N` slope `-0.497803`; maximum bound ratio `0.114227`. |
| C4 | Verified with source correction | Warm-start `N` slope `-1.007167`; maximum exact-risk relative error `2.095%`; literal printed law fails. |
| C5 | Verified, scoped | Normalized Dudley constant `5.662939536639`; covering formula exact on all cells. |
| C6 | Verified with convention note | 3,000 producer and 2,500 independent geometry trials; all stated inequalities pass. |

The raw producer output is under `outputs/`, the independent claim/evidence map
is [`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md), and the source pins are
in [`sources.json`](sources.json). Run the gate with:

```bash
uv sync
uv run python -m repro.src.publication_gate
```

The full claim runs are CPU-only and finish at the configured finite scope; the
gate does not represent a new application-scale MILP benchmark.
