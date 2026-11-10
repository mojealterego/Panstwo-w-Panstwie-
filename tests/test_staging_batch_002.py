"""Weryfikacja tymczasowego korpusu drugiej partii."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "corpus"
STAGING = ROOT / "staging" / "batch-002"


def test_batch_002_staging_is_separate_and_complete():
    rows = [json.loads(line) for line in (STAGING / "attachments.jsonl").read_text(encoding="utf-8").splitlines() if line]
    assert len(rows) == 5
    assert sum(row["page_count"] for row in rows) == 15
    assert len({row["document_id"] for row in rows}) == 5
    for row in rows:
        assert row["source_sha256"] is None
        assert row["quality_status"] == "awaiting_binary_pdf"
        slot = row["document_id"].removeprefix("chat-batch-002-")
        folder = STAGING / slot
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["document_id"] == row["document_id"]
        assert meta["canonical_import"] is False
        assert meta["source_sha256"] is None
        assert meta["page_count"] == 3
        plain = (folder / "document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest() == meta["text_sha256"] == row["text_sha256"]
        assert len(list((folder / "pages").glob("*.md"))) == 3
        assert (folder / "document.md").is_file()
        assert (folder / "document.txt").is_file()
        for number in range(1, 4):
            assert (folder / "pages" / f"{number:04d}.md").is_file()
    canonical = (ROOT / "index.jsonl").read_text(encoding="utf-8")
    assert "chat-batch-002" not in canonical


def test_batch_002_textual_duplicates_are_preserved_separately():
    def text(slot: str) -> str:
        return (STAGING / slot / "document.txt").read_text(encoding="utf-8")
    assert text("slot-06") == text("slot-07")
    assert text("slot-09") == text("slot-10")
    assert text("slot-08") != text("slot-09")
    assert text("slot-06").startswith("LUBELSKIE ELDORADO")
    assert text("slot-08").startswith("LUBELSKIE IMPERIUM")
    assert text("slot-09").startswith("FOLWARK NA JAŚMINOWEJ")
