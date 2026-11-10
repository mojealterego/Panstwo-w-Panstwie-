"""Kanoniczny batch-007: pięć oryginalnych plików PDF (39–43)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
EXPECTED = {
    39: ("5f2c3331760bd079001e28d0b1dc9f4072efbf43bd8d867d4fd1d701c53448d6", 4),
    40: ("0d5192fa264b75ae2929b4b94a98fffd5d453ad4d62fe1ee36c5dff17cc8f4cc", 3),
    41: ("b377dbd9f33b652ea5631ce430855a7b11e15d892bcf357bd43bef7fd4c1568f", 3),
    42: ("5f7db050861bc7f40b971cd13bacc9e51f1b59634926e500a059486d744d7aa0", 3),
    43: ("be239a4dbf211a67e6f60191be6884c5ded552f2c17857871ddb16116566c1d7", 3),
}


def _jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def test_batch_007_manifest_and_page_provenance():
    batch = json.loads((CORPUS / "batches/batch-007.json").read_text(encoding="utf-8"))
    index = _jsonl(CORPUS / "index.jsonl")
    receipts = _jsonl(CORPUS / "receipts.jsonl")
    assert batch["source_count"] == 5
    assert batch["source_page_count"] == 16
    assert batch["source_pdf_sha256_verified"] is True
    assert batch["raw_pdf_in_repo"] is False
    assert batch["new_document_count"] == 5
    assert batch["canonical_total_documents"] == 37
    assert batch["canonical_total_pages"] == 158
    assert batch["total_receipts"] == 40
    assert len(index) >= batch["canonical_total_documents"]
    assert sum(row["page_count"] for row in index) >= batch["canonical_total_pages"]
    assert len(receipts) >= batch["total_receipts"]
    assert len({r["source_sha256"] for r in index}) == len(index)
    assert len({(r["batch_id"], r["source_relative_path"], r["source_sha256"]) for r in receipts}) == len(receipts)
    got_receipts = [r for r in receipts if r["batch_id"] == "batch-007"]
    assert len(got_receipts) == 5
    for number, (digest, pages) in EXPECTED.items():
        name = f"Badanie Zespołów Interdyscyplinarnych ds. Przemocy({number}).PDF"
        doc_id = "pdf-" + digest[:24]
        rows = [r for r in index if r["document_id"] == doc_id]
        assert len(rows) == 1
        assert rows[0]["source_sha256"] == digest
        assert rows[0]["page_count"] == pages
        assert len([r for r in got_receipts if r["document_id"] == doc_id and r["original_filename"] == name]) == 1
        folder = CORPUS / "documents" / doc_id
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] == digest
        assert meta["quality_status"] == "extracted"
        assert meta["fact_check_status"] == "unverified_source_material"
        assert meta["page_count"] == pages
        assert len(meta["page_characters"]) == pages
        assert len(meta["extraction_methods"]) == pages
        assert len(meta["page_warnings"]) == 0
        plain = (folder / "document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest() == meta["text_sha256"]
        assert (folder / "document.md").is_file()
        for page in range(1, pages + 1):
            content = (folder / "pages" / f"{page:04d}.md").read_text(encoding="utf-8")
            assert f"strona {page}" in content
            assert len(content) > 100


def test_batch_007_watchdog_table_and_pdf_separation():
    doc_id = "pdf-" + EXPECTED[40][0][:24]
    folder = CORPUS / "documents" / doc_id / "tables"
    table = json.loads((folder / "0001.json").read_text(encoding="utf-8"))
    assert table["document_id"] == doc_id
    assert table["source_page"] == 1
    assert table["verification_status"] == "unverified_source_material"
    assert table["header"] == ["Sponsor instytucjonalny", "Kwota dotacji (PLN)", "Cel dotacji"]
    assert len(table["rows"]) == 4
    assert table["rows"][0][1] == "580 370,05"
    assert (folder / "0001.md").is_file()
    assert not any(path.suffix.lower() == ".pdf" for path in CORPUS.rglob("*") if path.is_file())
