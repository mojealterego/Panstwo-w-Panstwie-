"""Kontrola kanonicznego przyjęcia pięciu oryginalnych PDF-ów partii 002."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
EXPECTED = {
    "slot-06": ("c05be847e9d8021742d2dcd16b91a56d1305ea5da827ca63d299206c5171dd2c", 15),
    "slot-07": ("d5c3679c9edde172b32dd104fdfef524d0b2632db3388a26d1b4c4f066543f89", 16),
    "slot-08": ("6edbf3eec296b875e3cb12cf9e24337bd653c143601657e3df5396819ed21964", 17),
    "slot-09": ("732ee27637b976af87dcd8010d07ba98b9617a65107f264fcc79c3da44d87d53", 18),
    "slot-10": ("3c72d41ede3605285e497a06516421de5bf9c277a5c075db52ff1f0c5b726f00", 19),
}


def test_batch_002_source_mapping_and_integrity():
    manifest = json.loads((CORPUS / "batches" / "batch-002.json").read_text(encoding="utf-8"))
    resolution = json.loads((CORPUS / "staging" / "batch-002" / "resolution.json").read_text(encoding="utf-8"))
    index = [json.loads(line) for line in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines()]
    receipts = [json.loads(line) for line in (CORPUS / "receipts.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(index) >= manifest["canonical_total_documents"]
    assert sum(row["page_count"] for row in index) >= manifest["canonical_total_pages"]
    assert len(receipts) >= 15
    assert manifest["document_count"] == 5
    assert manifest["new_document_count"] == 3
    assert manifest["already_indexed_document_count"] == 2
    assert manifest["page_count"] == 15
    assert manifest["pending_slots"] == ["slot-01", "slot-02", "slot-03", "slot-04", "slot-05"]
    assert len(resolution["sources"]) == 5
    assert len([row for row in receipts if row["batch_id"] == "batch-002"]) == 5
    assert len({row["document_id"] for row in index}) == len(index)

    for source in resolution["sources"]:
        slot = source["slot"]
        sha, number = EXPECTED[slot]
        doc_id = "pdf-" + sha[:24]
        assert source["source_sha256"] == sha
        assert source["document_id"] == doc_id
        assert source["preview_pages_match_source_extraction"] is True
        assert source["original_filename"].endswith(f"({number}).PDF")
        match = [row for row in index if row["document_id"] == doc_id]
        assert len(match) == 1
        assert match[0]["source_sha256"] == sha
        assert len([row for row in receipts if row["batch_id"] == "batch-002" and row["document_id"] == doc_id]) == 1
        folder = CORPUS / "documents" / doc_id
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] == sha
        assert meta["page_count"] == 3
        assert meta["fact_check_status"] == "unverified_source_material"
        plain = (folder / "document.txt").read_text(encoding="utf-8")
        staged = (CORPUS / "staging" / "batch-002" / slot / "document.txt").read_text(encoding="utf-8")
        assert plain == staged
        assert hashlib.sha256(plain.removesuffix("\n").encode("utf-8")).hexdigest() == meta["text_sha256"]
        assert len(list((folder / "pages").glob("*.md"))) == 3


def test_distinct_pdf_hashes_with_same_text_are_preserved():
    index = [json.loads(line) for line in (CORPUS / "index.jsonl").read_text(encoding="utf-8").splitlines()]
    by_id = {row["document_id"]: row for row in index}
    for first, second in [("slot-06", "slot-07"), ("slot-09", "slot-10")]:
        a = "pdf-" + EXPECTED[first][0][:24]
        b = "pdf-" + EXPECTED[second][0][:24]
        assert a != b
        assert by_id[a]["source_sha256"] != by_id[b]["source_sha256"]
        assert by_id[a]["text_sha256"] == by_id[b]["text_sha256"]
    pairs = json.loads((CORPUS / "duplicates.json").read_text(encoding="utf-8"))
    assert len(pairs) >= 5
    assert any(
        {pair["left_document_id"], pair["right_document_id"]}
        == {"pdf-3c72d41ede3605285e497a06", "pdf-732ee27637b976af87dcd801"}
        and pair["relation"] == "exact_text"
        for pair in pairs
    )
