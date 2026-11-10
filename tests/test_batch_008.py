"""Batch-008: pięć kanonicznych PDF-ów (44–48), z weryfikacją hashy i stron."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

CORPUS=Path(__file__).resolve().parents[1]/"corpus"
EXPECTED={
    44: ('1d51af05a83b159ee680396088043da45e3fff54a98e99d0bd4eb1e9ee34d4a1', 3),
    45: ('876abb28ab844af9f19eef2368da388c4560f5178e16aed827bda2463896179f', 3),
    46: ('04acbf1a8a01fd109e75180909791d38c76b1097bd0b5e57355717a481dbd778', 3),
    47: ('7061e6da329eb072e7463624c0a4600ef3a162f90b462d35f453a61a7e35e52a', 3),
    48: ('6f95f22921414a9ac46d7d20bbc2e8a1078a770899baa19e40a96df219e5bd18', 3),
}


def test_batch_008_index_receipts_and_pages():
    manifest=json.loads((CORPUS/"batches/batch-008.json").read_text("utf-8"))
    index=[json.loads(x) for x in (CORPUS/"index.jsonl").read_text("utf-8").splitlines() if x]
    receipts=[json.loads(x) for x in (CORPUS/"receipts.jsonl").read_text("utf-8").splitlines() if x]
    assert manifest["source_count"]==5
    assert manifest["source_page_count"]==15
    assert manifest["new_document_count"]==5
    assert manifest["source_pdf_sha256_verified"] is True
    assert len(index)>=manifest["canonical_total_documents"]
    assert sum(x["page_count"] for x in index)>=manifest["canonical_total_pages"]
    assert len(receipts)>=manifest["total_receipts"]
    assert len({x["source_sha256"] for x in index})==len(index)
    assert len({(x["batch_id"],x["source_relative_path"],x["source_sha256"]) for x in receipts})==len(receipts)
    batch=[x for x in receipts if x["batch_id"]=="batch-008"]
    assert len(batch)==5
    for n,(digest,page_count) in EXPECTED.items():
        did="pdf-"+digest[:24]
        filename=f"Badanie Zespołów Interdyscyplinarnych ds. Przemocy({n}).PDF"
        row=next(x for x in index if x["document_id"]==did)
        assert row["source_sha256"]==digest
        assert row["page_count"]==page_count
        assert any(x["source_sha256"]==digest and x["original_filename"]==filename for x in batch)
        folder=CORPUS/"documents"/did
        m=json.loads((folder/"metadata.json").read_text("utf-8"))
        assert m["source_sha256"]==digest
        assert m["page_count"]==page_count
        assert m["quality_status"]=="extracted"
        assert m["fact_check_status"]=="unverified_source_material"
        plain=(folder/"document.txt").read_text("utf-8").removesuffix("\n")
        assert hashlib.sha256(plain.encode("utf-8")).hexdigest()==m["text_sha256"]
        assert (folder/"document.md").is_file()
        for i in range(1,page_count+1):
            text=(folder/"pages"/f"{i:04d}.md").read_text("utf-8")
            assert len(text)>100
            assert f"strona {i}" in text


def test_batch_008_donor_table_and_no_public_pdfs():
    manifest=json.loads((CORPUS/"batches/batch-008.json").read_text("utf-8"))
    doc=next(x for x in manifest["originals"] if x["number"]==48)
    folder=CORPUS/"documents"/doc["document_id"]
    table=json.loads((folder/"tables/0001.json").read_text("utf-8"))
    assert table["source_document_number"]==48
    assert table["source_page"]==1
    assert len(table["rows"])==10
    assert {x["currency"] for x in table["rows"]}=={"EUR"}
    assert {x["fact_check_status"] for x in table["rows"]}=={"unverified_source_material"}
    assert (folder/"tables/0001.md").is_file()
    assert not any(p.suffix.lower()==".pdf" for p in CORPUS.rglob("*") if p.is_file())
