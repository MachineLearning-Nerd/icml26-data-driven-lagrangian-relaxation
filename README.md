# Provably Data-driven Lagrangian Relaxation for MILP

Clean-room evidence audit for the six-claim reproduction contract associated
with OpenReview `OwLuqetJuB` and arXiv `2605.19052v2`. The paper studies
learning Lagrangian multipliers for mixed integer linear programs: ERM gives an
`O(s^1.5/sqrt(N))` guarantee, a minimax lower bound gives `Omega(s/sqrt(N))`,
averaged stochastic gradient ascent closes that gap, and warm-start learning
achieves a `Theta(s/N)` rate.

The paper is accepted to ICML 2026. The claim contract is preserved locally in
[`repro/configs/live_claims.json`](repro/configs/live_claims.json), while the
paper PDF, arXiv source archive, and extracted main/appendix TeX are pinned in
[`docs/`](docs) and [`source/arxiv-v2/`](source/arxiv-v2).

## Audit result

The repository-native gate is `SCOPED_PASS`: all six claims have substantive
verified outcomes within the explicit finite-family protocol. The result is
qualified by one source defect: the literal Appendix Theorem 6.2 `v_k=0`
probability line is not a probability distribution, so the audit retains the
literal line as a failing control and verifies the uniquely consistent
complementary-sign repair separately.

| Claim | Outcome | Evidence and control |
| --- | --- | --- |
| C1 ERM risk | `VERIFIED_SCOPED` | ERM raw trials and independent reconstruction give `N` slope `-0.505629`; all cells remain below the `O(s^1.5/sqrt(N))` envelope. |
| C2 minimax lower bound | `VERIFIED_SCOPED` | 32,766 pairwise packing checks, exact Bernoulli KL, and positive Fano factors certify the `Omega(s/sqrt(N))` family. |
| C3 averaged SGA | `VERIFIED_SCOPED` | Raw averaged iterates give `N` slope `-0.497803`; the maximum theorem-bound ratio is `0.114227`. |
| C4 warm start | `VERIFIED_SCOPED_WITH_SOURCE_CORRECTION` | Empirical means give `N` slope `-1.007167` and maximum exact-risk relative error `2.095%`; the repaired Fano family gives `Omega(s/N)`. |
| C5 covering/Rademacher | `VERIFIED_SCOPED` | Every covering cell is exact; independent integration recovers normalized Dudley constant `5.662939536639`. |
| C6 dual geometry | `VERIFIED_SCOPED_WITH_CONVENTION_NOTE` | 3,000 producer plus 2,500 independent finite-MILP trials pass concavity, the supergradient inequality, and `2B sqrt(s)`; wrong-gradient, max-affine, and omitted-`sqrt(s)` controls fail. |

The machine-readable verdicts are in
[`outputs/claim_verdicts.json`](outputs/claim_verdicts.json), the full raw
producer output is [`outputs/claims_raw.json`](outputs/claims_raw.json), and
the publication gate writes hash-bound copies at the repository root and under
`outputs/`.

## How each claim is produced

1. `repro/src/core.py` implements exact finite-feasible-set dual evaluation,
   the paper's binary hard family, averaged SGA, ERM, warm-start errors,
   Hamming packings, Fano certificates, and Dudley integration.
2. `repro/src/run_claims.py` runs the six claim producers over
   `s={16,32,64}` and `N={256,1024,4096,16384}`, retaining raw SGA, ERM,
   warm-start, packing, integration, and geometry records.
3. `repro/src/verify_all.py` independently rebuilds raw risks, packing
   distances, KL/Fano quantities, warm-start aggregates, covering formulas,
   transformed-domain integration, source hashes, and fresh finite-MILP
   geometry controls before rendering the verdicts.
4. `repro/src/build_bundle.py` records the claim contract, pinned paper
   artifacts, raw evidence, verdicts, docs, producers, and focused tests in a
   deterministic hash-bound JSONL bundle.
5. `repro/src/publication_gate.py` reruns the producers and verifier, rebuilds
   the bundle and artifact manifest, runs tests, checks the documentation, and
   rejects private publication state or absolute local paths.

Separability is an exact algebraic reduction here: a full `s`-coordinate
utility is the sum of scalar utilities, so the reported full risk is exactly
`s` times the scalar risk. It is not a reduced-dimensional proxy.

## Reproduce the gate

```bash
uv sync
uv run python -m repro.src.publication_gate
```

For the individual stages:

```bash
uv run python -m repro.src.run_claims
uv run python -m repro.src.verify_all
uv run pytest -q
```

The gate is CPU-only and deterministic at the configured seeds. It does not
claim a competition score, an author endorsement, or an empirical benchmark
pipeline that is not supplied by the paper.

## Branches

The final repository has one branch: `main`. The original clone also exposed
only `main`; no alternate branch contained a distinct implementation or
result. See [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md).

## Citation

```bibtex
@article{le2026provably,
  title   = {Provably Data-driven Lagrangian Relaxation for Mixed Integer Linear Programming},
  author  = {Le, Tung Quoc and Nguyen, Anh Tuan and Nguyen, Viet Anh},
  journal = {arXiv preprint arXiv:2605.19052},
  year    = {2026},
  url     = {https://arxiv.org/abs/2605.19052}
}
```

## Thank you

Thank you to Tung Quoc Le, Anh Tuan Nguyen, and Viet Anh Nguyen for making the
paper and its precise theorem constructions available for independent study.
This repository is a transparent audit and reproduction record, not an
official implementation or an author endorsement.

## Reproduction boundary

- The six anchored claims are evaluated on the paper's explicit finite,
  separable binary MILP family and independent finite-MILP geometry trials.
- The Appendix Theorem 6.2 sign defect is disclosed and tested rather than
  silently corrected in the literal source record.
- No author executable code or application-scale MILP benchmark pipeline was
  found in the pinned arXiv source; those results are outside this clone.
- Formal proof checking, fresh asymptotic limits, and external competition
  scoring are not claimed.
