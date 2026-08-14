"""Hash every published checkout artifact except generated gate copies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "outputs/artifact_manifest.json"
EXCLUDED_FILES = {
    "publication_gate.json",
    "outputs/publication_gate.json",
    "outputs/PUBLICATION_GATE_PASSED.json",
    "outputs/CUMULATIVE_SCIENCE_GATE.json",
    "outputs/artifact_manifest.json",
}
EXCLUDED_PARTS = {".git", ".venv", ".pytest_cache", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in EXCLUDED_FILES
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    )


def main() -> None:
    records = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in files()
    ]
    payload = {"version": 1, "files": records}
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"files": len(records), "sha256": sha256(MANIFEST)}, indent=2))


if __name__ == "__main__":
    main()
