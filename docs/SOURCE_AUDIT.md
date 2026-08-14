# Source audit

## Paper identity

- Title: *Provably Data-driven Lagrangian Relaxation for Mixed Integer Linear Programming*
- Authors: Tung Quoc Le, Anh Tuan Nguyen, Viet Anh Nguyen
- arXiv: `2605.19052v2` — [abstract and metadata](https://arxiv.org/abs/2605.19052)
- OpenReview: `OwLuqetJuB` — [submission record](https://openreview.net/forum?id=OwLuqetJuB)
- Venue status: accepted to ICML 2026 according to the arXiv record.

## Pinned artifacts

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| arXiv v2 PDF, 19 pages | `docs/primary-v2.pdf` | `6ebb06729fd814155c4a2b2dfd7b1d8a1ed5d0a7bd0d6330ec268b9796158716` |
| arXiv source archive, 10 members | `source/arxiv-v2/arxiv-2605.19052.tar` | `c1dea639b1137784cf075b486f29c3b6accbfc34b7a2ba717eb0b02bd347231e` |
| main TeX | `source/arxiv-v2/icml2026-arxiv.tex` | `96252bc23d6416698a83d62ce7aeaffd5c9cec421fb97d548c8b4c08da5709e5` |
| appendix TeX | `source/arxiv-v2/icml_appendix.tex` | `5a9bc0ecd7eb90d53e14d9e05f786b52cc5abf216e10cfebd0bcd8fccd32ec22` |
| live six-claim contract | `repro/configs/live_claims.json` | `ad28e6d9fee99582c59350ca2094c2c5f0d734cfbe067bbdf9deecfd9c562815` |

The source archive contains TeX/style/bibliography artifacts and no author
Python, shell, notebook, Julia, or R implementation. The numerical code in
`repro/src/` is therefore labeled as a clean-room reconstruction of the paper's
explicit finite family.

## Disclosed source correction

The Appendix Theorem 6.2 line for `v_k=0` prints both point probabilities as
`(1+epsilon)/2`. At `epsilon=0.2` they sum to `1.2`, so the literal pair is not
a distribution. The complementary pair `(1-epsilon)/2` and
`(1+epsilon)/2` is consistent with the stated mean and is tested as a separate
repair. The audit reports this qualification rather than silently changing the
paper.
