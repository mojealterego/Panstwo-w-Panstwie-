"""Partia 006: nie wolno mylić notatek z podglądu z kanonicznym PDF."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "corpus"
STAGING = ROOT / "staging" / "batch-006"


def test_batch_006_preview_is_noncanonical_and_page_scoped():
    manifest = json.loads((STAGING / "manifest.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (STAGING / "attachments.jsonl").read_text(encoding="utf-8").splitlines() if line]
    assert manifest["status"] == "staging_preview_only"
    assert manifest["source_pdf_sha256_verified"] is False
    assert manifest["verbatim_transcriptions_stored"] is False
    assert manifest["canonical_import"] is False
    assert manifest["pending_slots"] == ["slot-01"]
    assert len(rows) == manifest["preview_count"] == 4
    assert sum(row["page_count"] for row in rows) == manifest["preview_page_count"] == 15
    assert {r["source_ref"] for r in rows} == {"turn454file1", "turn454file2", "turn454file3", "turn454file4"}
    assert len({r["document_id"] for r in rows}) == len(rows)
    for row in rows:
        assert row["source_sha256"] is None
        assert row["text_sha256"] is None
        assert row["original_filename"] is None
        assert row["quality_status"] == "awaiting_binary_pdf"
        assert row["preview_kind"] == "page_summary_only"
        slot = row["document_id"].removeprefix("chat-batch-006-")
        folder = STAGING / slot
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["document_id"] == row["document_id"]
        assert meta["source_sha256"] is None
        assert meta["text_sha256"] is None
        assert meta["canonical_import"] is False
        assert meta["verbatim_transcription_stored"] is False
        assert (folder / "page_notes.md").is_file()
        assert not (folder / "document.txt").exists()
        assert not (folder / "document.md").exists()
        pages = list((folder / "pages").glob("*.md"))
        assert len(pages) == row["page_count"]
        for number in range(1, row["page_count"] + 1):
            note = (folder / "pages" / f"{number:04d}.md").read_text(encoding="utf-8")
            assert f"strona {number}" in note
            assert "nie transkrypcja" in note


def test_batch_006_does_not_change_canonical_identity_or_receipts():
    index = [json.loads(line) for line in (ROOT / "index.jsonl").read_text(encoding="utf-8").splitlines() if line]
    receipts = [json.loads(line) for line in (ROOT / "receipts.jsonl").read_text(encoding="utf-8").splitlines() if line]
    assert len(index) >= 27
    assert sum(r["page_count"] for r in index) >= 124
    assert len(receipts) >= 30
    assert not any(row["document_id"].startswith("chat-batch-006-") for row in index)
    assert not any(row["batch_id"] == "batch-006" for row in receipts)
