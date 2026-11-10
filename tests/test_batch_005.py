"""Testy integralności batch-005: źródła PDF (29)–(33)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
EXPECTED = {
    29: ("4a3f24d5e59f46a90dc822f5de30851bc35e0f50d53e61c38eae252cbe54f384", 3),
    30: ("72a9b4d11f7265c94f06e237c0bda8be50cdb32324e2cc845e86fed0be7a9382", 3),
    31: ("0e210fd366d54d7d4d82fd56fc470449475aeb0a715a2021ea8d55b76e606cb4", 3),
    32: ("f4094f0f47e53de71e578b4a956c1f4653fd2b92a44ae51c01becf91ff6294a7", 3),
    33: ("bcc6cd1a537d1ec8e64ca1c63a3f969ea0b1e1e7c6576248621e1d3c93ad0abe", 3),
}

def test_batch_005_manifest_and_canonical_index():
    manifest = json.loads((CORPUS / "batches" / "batch-005.json").read_text(encoding="utf-8"))
    index = [json.loads(x) for x in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines() if x]
    receipts = [json.loads(x) for x in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert manifest["source_count"] == 5
    assert manifest["source_page_count"] == 15
    assert manifest["new_document_count"] == 5
    assert manifest["previously_indexed_count"] == 0
    assert len(index) >= manifest["canonical_total_documents"]
    assert sum(r["page_count"] for r in index) >= manifest["canonical_total_pages"]
    assert len(receipts) >= manifest["total_receipts"]
    batch_receipts = [r for r in receipts if r["batch_id"] == "batch-005"]
    assert len(batch_receipts) == 5
    assert len({r["source_sha256"] for r in index}) == len(index)
    assert len({(r["batch_id"], r["source_relative_path"], r["source_sha256"]) for r in receipts}) == len(receipts)
    for number, (digest, count) in EXPECTED.items():
        docid = "pdf-" + digest[:24]
        filename = f"Badanie Zespołów Interdyscyplinarnych ds. Przemocy({number}).PDF"
        rows = [r for r in index if r["document_id"] == docid]
        assert len(rows) == 1
        assert rows[0]["source_sha256"] == digest
        assert rows[0]["page_count"] == count
        assert len([r for r in batch_receipts if r["document_id"] == docid and r["original_filename"] == filename]) == 1
        folder = CORPUS / "documents" / docid
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] == digest
        assert meta["fact_check_status"] == "unverified_source_material"
        assert meta["quality_status"] == "extracted"
        assert meta["page_count"] == count
        assert len(meta["page_characters"]) == count
        assert len(list((folder / "pages").glob("*.md"))) == count
        plain = (folder / "document.txt").read_text(encoding="utf-8")
        assert hashlib.sha256(plain.removesuffix("\n").encode("utf-8")).hexdigest() == meta["text_sha256"]
        for page in range(1, count + 1):
            text = (folder / "pages" / f"{page:04d}.md").read_text(encoding="utf-8")
            assert len(text) > 100
            assert f"strona {page}" in text

def test_batch_005_no_original_pdf_binaries():
    assert not any(p.suffix.lower() == ".pdf" for p in CORPUS.rglob("*") if p.is_file())
