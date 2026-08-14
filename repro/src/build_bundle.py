"""Build the deterministic, repository-native evidence bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_paths() -> list[Path]:
    paths = [
        ROOT / "repro/configs/live_claims.json",
        ROOT / "sources.json",
        ROOT / "README.md",
        ROOT / "STATUS.md",
        ROOT / "pyproject.toml",
        ROOT / "docs/CLAIM_EVIDENCE.md",
        ROOT / "docs/SOURCE_AUDIT.md",
        ROOT / "docs/BRANCH_AUDIT.md",
        ROOT / "docs/PUBLICATION_GATE.md",
        ROOT / "docs/primary-v2.pdf",
        ROOT / "source/arxiv-v2/arxiv-2605.19052.tar",
        ROOT / "source/arxiv-v2/icml2026-arxiv.tex",
        ROOT / "source/arxiv-v2/icml_appendix.tex",
        ROOT / "outputs/claims_raw.json",
        ROOT / "outputs/claim_verdicts.json",
    ]
    paths += sorted((ROOT / "repro/src").glob("*.py"))
    paths += sorted((ROOT / "repro/tests").glob("test_*.py"))
    return paths


def main() -> None:
    paths = selected_paths()
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"bundle inputs missing: {missing}")
    records = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        record = {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "encoding": "json" if path.suffix == ".json" else "binary",
        }
        if path.suffix == ".json":
            record["payload"] = json.loads(path.read_text())
        records.append(record)
    bundle = ROOT / "outputs/evidence_bundle.jsonl"
    bundle.write_text(
        "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records) + "\n"
    )
    print(json.dumps({"records": len(records), "bytes": bundle.stat().st_size, "sha256": sha256(bundle)}, indent=2))


if __name__ == "__main__":
    main()
