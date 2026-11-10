"""Testy integralności batch-004: źródła PDF (24)–(28)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
EXPECTED = {
    24: ("411d62ed3c0a2294a28901b4d771b6eb35daf68898fd1937fc8a261bd4659008", 3),
    25: ("5d31d49fa3655d09e05578ca772392283bfbec01ad8cdbdeff5d041879e82074", 3),
    26: ("2c6ff17cb3f41c3f06a474f24807e161a4039a04303dca29c19d536c5f5bb010", 3),
    27: ("25e4ddfbf7ea7d75fcb9a467914698a65d48293b5d310e6af8c51d4324021951", 3),
    28: ("8189ffe29a6ec13e04ccff4370c391c408347f383522592fad10d4a4f0a56fea", 3),
}


def test_batch_004_manifest_and_index():
    manifest = json.loads((CORPUS / "batches" / "batch-004.json").read_text(encoding="utf-8"))
    index = [json.loads(line) for line in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines() if line]
    receipts = [json.loads(line) for line in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines() if line]
    assert manifest["source_count"] == 5
    assert manifest["source_page_count"] == 15
    assert manifest["new_document_count"] == 5
    assert manifest["previously_indexed_count"] == 0
    assert len(index) >= manifest["canonical_total_documents"]
    assert sum(r["page_count"] for r in index) >= manifest["canonical_total_pages"]
    assert len(receipts) >= manifest["total_receipts"]
    batch_receipts = [r for r in receipts if r["batch_id"] == "batch-004"]
    assert len(batch_receipts) == 5
    assert len({r["source_sha256"] for r in batch_receipts}) == 5
    assert len({r["document_id"] for r in index}) == len(index)
    assert len({r["source_sha256"] for r in index}) == len(index)
    assert len({(r["batch_id"], r["source_relative_path"], r["source_sha256"]) for r in receipts}) == len(receipts)
    for number, (digest, pages) in EXPECTED.items():
        document_id = "pdf-" + digest[:24]
        filename = f"Badanie Zespołów Interdyscyplinarnych ds. Przemocy({number}).PDF"
        rows = [r for r in index if r["document_id"] == document_id]
        assert len(rows) == 1
        assert rows[0]["source_sha256"] == digest
        assert rows[0]["page_count"] == pages
        assert len([r for r in batch_receipts if r["document_id"] == document_id and r["original_filename"] == filename]) == 1
        folder = CORPUS / "documents" / document_id
        metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert metadata["source_sha256"] == digest
        assert metadata["fact_check_status"] == "unverified_source_material"
        assert metadata["quality_status"] == "extracted"
        assert metadata["page_count"] == pages
        assert len(metadata["page_characters"]) == pages
        assert len(list((folder / "pages").glob("*.md"))) == pages
        plain = (folder / "document.txt").read_text(encoding="utf-8")
        assert hashlib.sha256(plain.removesuffix("\n").encode("utf-8")).hexdigest() == metadata["text_sha256"]
        assert (folder / "document.md").is_file()
        for page_number in range(1, pages + 1):
            text = (folder / "pages" / f"{page_number:04d}.md").read_text(encoding="utf-8")
            assert len(text) > 100
            assert f"strona {page_number}" in text


def test_batch_004_duplicates_and_no_pdf_binaries():
    pairs = json.loads((CORPUS / "duplicates.json").read_text(encoding="utf-8"))
    assert len(pairs) >= 5
    assert not any(p.suffix.lower() == ".pdf" for p in CORPUS.rglob("*") if p.is_file())
