# Publication gate

Run the deterministic public gate from a clean checkout:

```bash
uv sync
uv run python -m repro.src.publication_gate
```

The gate:

1. reruns `repro.src.run_claims` and `repro.src.verify_all`;
2. checks the six-claim wording, source/PDF/archive hashes, theorem anchors,
   and the disclosed probability-law control;
3. rebuilds and verifies `outputs/evidence_bundle.jsonl`;
4. rebuilds and verifies `outputs/artifact_manifest.json`;
5. runs the focused pytest suite and documentation checker; and
6. scans publishable text for secrets, private publisher state, absolute local
   paths, and tracked `.trackio`/`upstream` paths.

The gate status is `SCOPED_PASS` with overall status
`VERIFIED_SCOPED_WITH_ONE_SOURCE_CORRECTION`. `NOT_READY` is reserved for a
strict paper-wide replication claim: this repository does not claim an
application-scale benchmark or an author endorsement.

The canonical JSON gate is written identically to:

- `publication_gate.json`
- `outputs/publication_gate.json`
- `outputs/PUBLICATION_GATE_PASSED.json`
- `outputs/CUMULATIVE_SCIENCE_GATE.json`
