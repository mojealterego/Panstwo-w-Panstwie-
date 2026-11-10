"""Testy integralności batch-003: źródła PDF (19)–(23)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
EXPECTED = {
    19: ("3c72d41ede3605285e497a06516421de5bf9c277a5c075db52ff1f0c5b726f00", 3),
    20: ("f2a072fac8251030cb9ed0d06e7f8c236a4532f116be3eb189e3d6288bac26df", 3),
    21: ("d19da7a41625d9c33e717910546545a4db41ae8b02e254cd1aae13945f161b10", 3),
    22: ("0390036fefba0973ead89ec821141d313bd3ab302a4cee35325643c382f5ae69", 4),
    23: ("38ee245fda3d978ba9d861bfe4cee7040973bfa66b8faca58f270e82e87325d1", 3),
}


def test_batch_003_manifest_receipts_and_documents():
    manifest = json.loads((CORPUS / "batches" / "batch-003.json").read_text(encoding="utf-8"))
    index = [json.loads(line) for line in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines()]
    receipts = [json.loads(line) for line in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines()]
    assert manifest["source_count"] == 5
    assert manifest["source_page_count"] == 16
    assert manifest["new_document_count"] == 4
    assert manifest["previously_indexed_count"] == 1
    assert len(index) >= manifest["canonical_total_documents"]
    assert sum(row["page_count"] for row in index) >= manifest["canonical_total_pages"]
    assert len(receipts) >= manifest["total_receipts"]
    assert len([row for row in receipts if row["batch_id"] == "batch-003"]) == 5
    assert len({row["document_id"] for row in index}) == len(index)
    for n, (sha, page_count) in EXPECTED.items():
        document_id = "pdf-" + sha[:24]
        matches = [row for row in index if row["document_id"] == document_id]
        assert len(matches) == 1
        assert matches[0]["source_sha256"] == sha
        assert matches[0]["page_count"] == page_count
        receipt = [r for r in receipts if r["batch_id"] == "batch-003" and r["document_id"] == document_id]
        assert len(receipt) == 1
        folder = CORPUS / "documents" / document_id
        metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert metadata["source_sha256"] == sha
        assert metadata["fact_check_status"] == "unverified_source_material"
        assert len(list((folder / "pages").glob("*.md"))) == page_count
        plain = (folder / "document.txt").read_text(encoding="utf-8")
        assert hashlib.sha256(plain.removesuffix("\n").encode("utf-8")).hexdigest() == metadata["text_sha256"]


def test_batch_003_repeat_and_table():
    receipts = [json.loads(line) for line in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines()]
    sha19 = EXPECTED[19][0]
    repeated = [r for r in receipts if r["source_sha256"] == sha19]
    assert {r["batch_id"] for r in repeated} == {"batch-002", "batch-003"}
    assert len({r["document_id"] for r in repeated}) == 1
    doc22 = CORPUS / "documents" / ("pdf-" + EXPECTED[22][0][:24])
    table = json.loads((doc22 / "tables" / "0003.json").read_text(encoding="utf-8"))
    assert table["page"] == 3
    assert len(table["columns"]) == 4
    assert len(table["rows"]) == 5
    assert table["rows"][-1][-1] == "2 112,5 tys. zł"
    assert (doc22 / "tables" / "0003.md").exists()
    duplicates = json.loads((CORPUS / "duplicates.json").read_text(encoding="utf-8"))
    assert len(duplicates) >= 5
