# Claim-to-evidence map

The six live claims are copied verbatim into
`repro/configs/live_claims.json` and checked for exact wording by the gate.
The producer output is `outputs/claims_raw.json`; the independently rebuilt
verdicts are `outputs/claim_verdicts.json`.

| Claim | Producer | Independent check | Key evidence |
| --- | --- | --- | --- |
| C1 — ERM `O(s^1.5/sqrt(N))` | `run_claims.py` → `claim_1_erm_raw`/`claim_1_erm_summary` | `verify_all.py` recomputes every scalar risk and log slope | raw ERM decisions, exact population risk, 16 scaling cells |
| C2 — minimax `Omega(s/sqrt(N))` | `core.py` → `greedy_hamming_packing`/`fano_certificate` | `verify_all.py` rebuilds Hamming distances, exact Bernoulli KL, envelope, and Fano constants | 32,766 pairwise checks and positive normalized lower certificates |
| C3 — averaged SGA | `core.py` → `averaged_sga_scalar`; `run_claims.py` | `verify_all.py` recomputes risk from every averaged iterate and theorem ratio | raw iterates, 32 risk cells, `N` slope `-0.497803` |
| C4 — warm start `Theta(s/N)` | `core.py` → `warm_start_errors`; `run_claims.py` | `verify_all.py` independently aggregates squared errors and checks both probability laws | exact risk comparison, 12 cells, literal malformed-law control, repaired Fano rows |
| C5 — covering/Rademacher | `core.py` → `dudley_integral`; `run_claims.py` | `verify_all.py` uses an independent 300,001-point transformed-domain trapezoid integral | covering rows, producer Gauss–Laguerre integral, normalized constant |
| C6 — dual geometry | `run_claims.py` → `geometry_audit` | `verify_all.py` uses a separate seed and implementation over 2,500 fresh finite MILPs | concavity, supergradient, norm, wrong-gradient, max-affine, and omitted-`sqrt(s)` controls |

## Controls that must fail

- The literal Theorem 6.2 `v_k=0` probabilities sum to `1.2` at
  `epsilon=0.2`, so the law is rejected.
- Omitting `sqrt(s)` from `2B sqrt(s)` fails on the tight `s=16` witness.
- Replacing the dual supergradient with `b` fails in the independent geometry
  trials.
- Replacing the pointwise minimum of affine functions with a maximum fails the
  concavity control.
- Mutated raw evidence, source pins, claim wording, and bundle hashes are
  rejected by the verifier/gate.

The source defect is not hidden in the verdict: C4 is marked
`VERIFIED_SCOPED_WITH_SOURCE_CORRECTION` and the literal line remains in the
raw contract audit.
