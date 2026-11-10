"""Weryfikacja kanonicznego batch-006 po odzyskaniu pięciu oryginalnych PDF."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EXPECTED = {
    34: ('13301bc2e5bd5d7eebe29c0ebb828d802294fcd697f890fd6d2fa8cab015e58a', 3),
    35: ('4126f1e0cbf5e281b1500d77322f5a62036ada6fd664b2819b7ce49278a39430', 3),
    36: ('2ea8d036487e419b11fc007cb3aaa1731c75c2b729408a516410660b0d2a7a9d', 4),
    37: ('0de856f947fbe9cebb5fef360b527bceee78151152f56b85bfeab1084aaf7afd', 4),
    38: ('1bc7364392cdd39685d45528f48f2fbc324c5c60d95e1e6c61008129df6c0d63', 4),
}


def _rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_batch_006_is_canonical_with_exact_source_hashes_and_pages():
    manifest = json.loads((CORPUS / "batches" / "batch-006.json").read_text(encoding="utf-8"))
    index = _rows(CORPUS / "index.jsonl")
    receipts = _rows(CORPUS / "receipts.jsonl")
    assert manifest["source_pdf_sha256_verified"] is True
    assert manifest["raw_pdf_in_repo"] is False
    assert (manifest["source_count"],manifest["source_page_count"],manifest["new_document_count"]) == (5,18,5)
    assert len(index) >= 32
    assert sum(r["page_count"] for r in index) >= 142
    assert len(receipts) >= 35
    assert len({r["source_sha256"] for r in index}) == len(index)
    batch = [r for r in receipts if r["batch_id"] == "batch-006"]
    assert len(batch) == 5
    assert len({r["source_sha256"] for r in batch}) == 5
    for n, (source_hash, pages) in EXPECTED.items():
        docid = "pdf-" + source_hash[:24]
        filename = f"Badanie Zespołów Interdyscyplinarnych ds. Przemocy({n}).PDF"
        record = next(r for r in index if r["document_id"] == docid)
        assert record["source_sha256"] == source_hash
        assert record["page_count"] == pages
        assert len([r for r in batch if r["document_id"] == docid and r["original_filename"] == filename]) == 1
        folder = CORPUS / "documents" / docid
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["original_filenames"] == [filename]
        assert meta["source_sha256"] == source_hash
        assert meta["page_count"] == pages
        assert meta["fact_check_status"] == "unverified_source_material"
        assert meta["quality_status"] == "extracted"
        assert len(meta["page_characters"]) == pages
        assert len(meta["extraction_methods"]) == pages
        assert len(list((folder / "pages").glob("*.md"))) == pages
        plain = (folder / "document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest() == meta["text_sha256"]
        markdown = (folder / "document.md").read_text(encoding="utf-8")
        for p in range(1,pages+1):
            page_text = (folder / "pages" / f"{p:04d}.md").read_text(encoding="utf-8")
            assert len(page_text) > 100
            assert f"strona {p}" in page_text
            assert f"## Strona {p}" in markdown


def test_batch_006_staging_is_resolved_without_falsifying_previews():
    staging = CORPUS / "staging" / "batch-006"
    status = json.loads((staging / "manifest.json").read_text(encoding="utf-8"))
    resolution = json.loads((staging / "resolution.json").read_text(encoding="utf-8"))
    assert status["status"] == "resolved_to_canonical"
    assert status["canonical_import"] is True
    assert status["pending_slots"] == []
    assert status["historical_notes_are_transcriptions"] is False
    assert len(resolution["resolved_slots"]) == 5
    assert len({x["document_id"] for x in resolution["resolved_slots"]}) == 5
    assert resolution["resolved_slots"][0]["slot"] == "slot-01"
    assert resolution["resolved_slots"][0]["page_count"] == 3
    assert not any(p.suffix.lower() == ".pdf" for p in CORPUS.rglob("*") if p.is_file())


def test_batch_006_structured_tables():
    by_num = {n:"pdf-"+h[:24] for n,(h,_) in EXPECTED.items()}
    for n,pages in {37:[2,3],38:[3]}.items():
        for page in pages:
            path = CORPUS / "documents" / by_num[n] / "tables" / f"{page:04d}.json"
            table = json.loads(path.read_text(encoding="utf-8"))
            assert table["document_id"] == by_num[n]
            assert table["source_page"] == page
            assert table["verification_status"] == "unverified_source_material"
            assert len(table["header"]) >= 4
            assert len(table["rows"]) >= 1
            assert (path.with_suffix(".md")).is_file()
