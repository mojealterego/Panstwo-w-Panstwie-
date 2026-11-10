"""Integralność kanonicznego batch-009: PDF (49),(50),(51),(52),(54)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EXPECTED = {49: ('c39a5edb045a24a237c65b8f9a79e429f90d1cf14310bb2e25afb74cfc2f6cc8', 3), 50: ('8c25955effbef42f1f96ee663f2a8821c13e5a1b4f4b9493c68e92198fc863b7', 3), 51: ('c4ee5756827c9ae496c58581e7676c0a6c897413103b5459912a09175088ac09', 3), 52: ('eeb20cfbc31ac7865ec9d1aded15345c233f558703eb2f7af2596d3efa2ff6ab', 3), 54: ('08a147dfeaf21ac51ab0be3660e6395c8e02fd4d4c305f53f4f49c060b9f8ae6', 3)}

def _jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def test_batch_009_manifest_receipts_and_uniqueness():
    m = json.loads((CORPUS / "batches/batch-009.json").read_text(encoding="utf-8"))
    index = _jsonl(CORPUS / "index.jsonl")
    receipts = _jsonl(CORPUS / "receipts.jsonl")
    assert m["batch_id"] == "batch-009"
    assert m["source_count"] == 5
    assert m["source_page_count"] == 15
    assert m["missing_number_53_not_received"] is True
    assert m["source_pdf_sha256_verified"] is True
    assert m["raw_pdf_in_repo"] is False
    assert len(index) >= 47
    assert sum(x["page_count"] for x in index) >= 188
    assert len(receipts) >= 50
    assert len({x["source_sha256"] for x in index}) == len(index)
    batch = [r for r in receipts if r["batch_id"] == "batch-009"]
    assert len(batch) == 5
    assert all(not r["original_filename"].endswith("(53).PDF") for r in batch)
    for n,(digest,count) in EXPECTED.items():
        docid = "pdf-"+digest[:24]
        rows = [x for x in index if x["document_id"]==docid]
        assert len(rows)==1 and rows[0]["source_sha256"]==digest
        assert rows[0]["page_count"] == count
        assert len([r for r in batch if r["source_sha256"]==digest])==1

def test_batch_009_all_pages_and_text_checksums():
    for n,(digest,count) in EXPECTED.items():
        docid = "pdf-" + digest[:24]
        folder = CORPUS/"documents"/docid
        meta = json.loads((folder/"metadata.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] == digest
        assert meta["fact_check_status"] == "unverified_source_material"
        assert meta["quality_status"] == "extracted"
        assert meta["page_count"] == count
        assert len(meta["page_characters"]) == count
        assert len(meta["page_warnings"]) == 0
        assert (folder/"document.md").is_file()
        assert (folder/"document.txt").is_file()
        plain = (folder/"document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest() == meta["text_sha256"]
        for p in range(1,count+1):
            page = (folder/"pages"/f"{p:04d}.md").read_text(encoding="utf-8")
            assert len(page) > 150
            assert f"strona {p}" in page

def test_batch_009_no_pdf_binary_published():
    assert not any(p.suffix.lower()==".pdf" for p in CORPUS.rglob("*") if p.is_file())
