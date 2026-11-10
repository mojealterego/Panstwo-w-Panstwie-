"""Integralność pierwszej partii opublikowanego korpusu."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"

def test_batch_001_integrity():
    rows = [json.loads(x) for x in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines() if x]
    receipts = [json.loads(x) for x in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines() if x]
    batch = [r for r in receipts if r["batch_id"] == "batch-001"]
    assert len(batch) == 10
    ids = {r["document_id"] for r in batch}
    assert len(ids) == 10
    docs = {r["document_id"]: r for r in rows}
    assert ids.issubset(docs)
    assert sum(docs[x]["page_count"] for x in ids) == 72
    for doc_id in ids:
        row = docs[doc_id]
        folder = CORPUS / "documents" / doc_id
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert row["source_sha256"] == meta["source_sha256"]
        assert doc_id == "pdf-" + meta["source_sha256"][:24]
        plain = (folder / "document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest() == meta["text_sha256"]
        assert len(list((folder / "pages").glob("*.md"))) == meta["page_count"]
        for n in range(1, meta["page_count"] + 1):
            assert (folder / "pages" / f"{n:04d}.md").is_file()
        assert (folder / "document.md").is_file()
    duplicates = json.loads((CORPUS / "duplicates.json").read_text(encoding="utf-8"))
    assert any(d["relation"] == "exact_text" for d in duplicates)
