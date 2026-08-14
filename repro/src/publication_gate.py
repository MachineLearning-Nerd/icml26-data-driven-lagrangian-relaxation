"""Run and validate the complete six-claim public evidence gate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = "OwLuqetJuB"
ARXIV = "2605.19052"
EXPECTED_STATUSES = ["verified"] * 6
GATE_OUTPUTS = {
    "publication_gate.json",
    "outputs/publication_gate.json",
    "outputs/PUBLICATION_GATE_PASSED.json",
    "outputs/CUMULATIVE_SCIENCE_GATE.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")


def verify_source() -> dict[str, object]:
    source = json.loads((ROOT / "sources.json").read_text())
    paper = source["paper"]
    contract = source["claim_contract"]
    assert paper["openreview_id"] == PAPER
    assert paper["arxiv_id"] == ARXIV
    contract_path = ROOT / contract["local_path"]
    assert sha256(contract_path) == contract["local_sha256"]
    contract_payload = json.loads(contract_path.read_text())
    assert contract_payload["paper_id"] == PAPER
    assert len(contract_payload["claims"]) == contract["claim_count"] == 6

    artifacts = {}
    for key, metadata in source["paper_artifacts"].items():
        path = ROOT / metadata["local_path"]
        assert path.is_file() and path.stat().st_size == metadata["bytes"]
        assert sha256(path) == metadata["sha256"]
        artifacts[key] = {"path": metadata["local_path"], "bytes": metadata["bytes"], "sha256": metadata["sha256"]}
    archive_listing = subprocess.run(
        ["tar", "-tf", str(ROOT / source["paper_artifacts"]["source_archive"]["local_path"])],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert len(archive_listing) == source["paper_artifacts"]["source_archive"]["archive_members"]
    main_tex = (ROOT / source["paper_artifacts"]["main_tex"]["local_path"]).read_text()
    appendix = (ROOT / source["paper_artifacts"]["appendix_tex"]["local_path"]).read_text()
    for anchor in (
        "thm:upper-bound-learning-lagrangian",
        "thm:minimax-lower-bound",
        "thm:minimax-SGA",
        "thm:upper-bound-warm-start",
        "thm:minimax-lower-bound-warm-start",
        "lm:covering-upper-bound",
        "prop:geometric-property",
    ):
        assert anchor in main_tex
    assert "If $v_k = 0$: $\\bbP(c_k = 2) = \\frac{1 + \\epsilon}{2}" in appendix
    return {"paper": paper, "artifacts": artifacts, "archive_members": len(archive_listing)}


def verify_raw_evidence() -> dict[str, object]:
    verdict = json.loads((ROOT / "outputs/claim_verdicts.json").read_text())
    assert verdict["paper_id"] == PAPER
    assert verdict["all_claims_complete"]
    assert verdict["substantive_outcomes"] == 6
    assert [row["verdict"] for row in verdict["claims"]] == EXPECTED_STATUSES
    metrics = verdict["metrics"]
    assert metrics["source_pins"]
    assert metrics["packing_pairs"] == 32766
    assert metrics["min_fano_error"] > 0.25
    assert -0.65 < metrics["erm_n_slope"] < -0.35
    assert -0.65 < metrics["sga_n_slope"] < -0.35
    assert -1.12 < metrics["warm_n_slope"] < -0.88
    assert metrics["max_sga_bound_ratio"] < 1
    assert metrics["max_warm_exact_relative_error"] < 0.03
    assert 5.6 < metrics["rademacher_normalized_constant"] < 5.7
    assert metrics["producer_geometry_trials"] == 3000
    independent = metrics["independent_geometry"]
    assert independent["trials"] == 2500
    assert independent["wrong_gradient_failures"] > 0
    assert independent["max_control_failures"] > 0
    return {
        "claim_count": 6,
        "verified": 6,
        "falsified": 0,
        "metrics": metrics,
    }


def validate_bundle(bundle: Path, root: Path = ROOT) -> dict[str, object]:
    from repro.src.build_bundle import selected_paths

    records = [json.loads(line) for line in bundle.read_text().splitlines() if line.strip()]
    expected = [path.relative_to(root).as_posix() for path in selected_paths()]
    if [record["path"] for record in records] != expected:
        raise RuntimeError("bundle path order mismatch")
    for record in records:
        path = root / record["path"]
        if not path.is_file():
            raise RuntimeError(f"bundle path missing: {record['path']}")
        if path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise RuntimeError(f"bundle size/hash mismatch: {record['path']}")
        if record["encoding"] == "json":
            if json.loads(path.read_text()) != record["payload"]:
                raise RuntimeError(f"bundle payload mismatch: {record['path']}")
    if any(".trackio" in record["path"] or record["path"].startswith("upstream/") for record in records):
        raise RuntimeError("private or legacy source path in bundle")
    return {"records": len(records), "bytes": bundle.stat().st_size, "sha256": sha256(bundle)}


def verify_manifest() -> dict[str, object]:
    manifest_path = ROOT / "outputs/artifact_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    seen = set()
    for record in manifest["files"]:
        assert record["path"] not in seen
        seen.add(record["path"])
        path = ROOT / record["path"]
        assert path.is_file() and path.stat().st_size == record["bytes"] and sha256(path) == record["sha256"]
    required = {
        "README.md",
        "sources.json",
        "docs/primary-v2.pdf",
        "outputs/claims_raw.json",
        "outputs/claim_verdicts.json",
        "outputs/evidence_bundle.jsonl",
    }
    assert required <= seen
    assert not any(".trackio" in path or path.startswith("upstream/") for path in seen)
    return {"files": len(seen), "sha256": sha256(manifest_path)}


def hygiene() -> dict[str, object]:
    secret = re.compile(r"(?i)(hf_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|BEGIN (?:OPENSSH )?PRIVATE KEY)")
    forbidden = ("DineshAI/", "huggingface.co/spaces/DineshAI", "/home/", "/Users/", "jinjaladinesh@gmail.com")
    text_suffixes = {".py", ".sh", ".json", ".jsonl", ".md", ".txt", ".toml", ".yaml", ".yml"}
    policy_paths = {"repro/src/publication_gate.py", "outputs/evidence_bundle.jsonl"}
    bad = []
    scanned = 0
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if (
            not path.is_file()
            or relative in GATE_OUTPUTS
            or relative in policy_paths
            or any(part in {".git", ".venv", ".pytest_cache", "__pycache__"} for part in path.parts)
            or path.suffix not in text_suffixes
        ):
            continue
        text = path.read_text(errors="replace")
        if secret.search(text) or any(fragment.lower() in text.lower() for fragment in forbidden):
            bad.append(relative)
        scanned += 1
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    assert not any(".trackio" in path and (ROOT / path).exists() for path in tracked)
    assert not any(path.startswith("upstream/") and (ROOT / path).exists() for path in tracked)
    assert not bad, bad
    assert not (ROOT / ".trackio").exists()
    assert not (ROOT / "upstream").exists()
    return {"passed": True, "scanned_text_files": scanned, "tracked_files": len([p for p in tracked if (ROOT / p).exists()])}


def main() -> None:
    source = verify_source()
    run([sys.executable, "-m", "repro.src.run_claims"])
    run([sys.executable, "-m", "repro.src.verify_all"])
    raw = verify_raw_evidence()
    run([sys.executable, "-m", "repro.src.build_bundle"])
    run([sys.executable, "-m", "repro.src.artifact_manifest"])
    bundle = validate_bundle(ROOT / "outputs/evidence_bundle.jsonl")
    manifest = verify_manifest()
    run([sys.executable, "-m", "pytest", "-q"])
    run([sys.executable, "-m", "repro.src.build_logbook"])
    clean = hygiene()
    gate = {
        "gate_version": "publication-v1",
        "paper": PAPER,
        "arxiv": ARXIV,
        "status": "SCOPED_PASS",
        "overall_status": "VERIFIED_SCOPED_WITH_ONE_SOURCE_CORRECTION",
        "strict_status": "NOT_READY",
        "publication_gate_passed": True,
        "claim_count": 6,
        "possible_points": 12,
        "claim_outcomes": [
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED_WITH_SOURCE_CORRECTION",
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED_WITH_CONVENTION_NOTE",
        ],
        "source": source,
        "raw_evidence": {"verified_claims": raw["verified"], "falsified_claims": raw["falsified"], "metrics": raw["metrics"]},
        "evidence_bundle": bundle,
        "artifact_manifest": manifest,
        "tests_passed": True,
        "documentation_check_passed": True,
        "hygiene": clean,
        "limitations": [
            "C4 retains the literal Appendix Theorem 6.2 probability defect and verifies the complementary repair separately.",
            "The pinned arXiv source contains no author executable implementation; numerical code here is clean-room.",
            "No application-scale MILP benchmark or competition score is claimed.",
            "No author endorsement is claimed.",
        ],
        "score_forecast": None,
    }
    serialized = json.dumps(gate, indent=2, sort_keys=True) + "\n"
    for relative in GATE_OUTPUTS:
        (ROOT / relative).write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
