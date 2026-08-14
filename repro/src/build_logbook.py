"""Check that the repository-native publication documents are present."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "README.md",
    "STATUS.md",
    "sources.json",
    "docs/CLAIM_EVIDENCE.md",
    "docs/SOURCE_AUDIT.md",
    "docs/BRANCH_AUDIT.md",
    "docs/PUBLICATION_GATE.md",
)


def main() -> None:
    missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
    if missing:
        raise RuntimeError(f"publication documents missing: {missing}")
    print(f"publication documents present: {len(REQUIRED)}")


if __name__ == "__main__":
    main()
