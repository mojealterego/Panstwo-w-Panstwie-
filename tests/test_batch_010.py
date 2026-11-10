"""Kontrola integralności batch-010, 9 receipts, 8 nowych SHA-256."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/"corpus"
EXPECTED={54: ('08a147dfeaf21ac51ab0be3660e6395c8e02fd4d4c305f53f4f49c060b9f8ae6', 3), 55: ('9c8fb9bbe4bc15235592ab791590ff65343379e4c103f608a76be1123f558781', 3), 56: ('9091675960665c791df80293ce9fc7af354fdef662bfc4b12bfa3c6362a06567', 3), 57: ('2b8499a2f51fd43a5ca6c0db6d1a0d2472ee111a3784fe7cce35f30312d4020c', 3), 58: ('140df6c81fd68a4b601fb823bc2fa32a135f6a5dd2346889d80d3fcfcbaf2b8a', 3), 59: ('bb17a46b8d9f9ea787a76621233496cd07b8619520175978b9a20d6de159c9c3', 3), 60: ('3b0b51ee7c46fa5536eb2f0e16c7de4eaa571a8c7c077e79b575c87077efb74c', 3), 61: ('37254d6527f59b2fd93c25f89dbaf7785c2cabe2f99117dafb7df14fce64704d', 3), 62: ('62627771f29ec44a185aa43635030306773d31dd590789e8c2909c4b04e4b6c2', 3)}
DOC42="pdf-5f7db050861bc7f40b971cd1"
OLD54="pdf-08a147dfeaf21ac51ab0be36"

def rows(path):
    return [json.loads(v) for v in path.read_text(encoding="utf-8").splitlines() if v.strip()]

def test_batch_010_manifest_index_and_receipts():
    m=json.loads((CORPUS/"batches/batch-010.json").read_text(encoding="utf-8"))
    index=rows(CORPUS/"index.jsonl")
    receipts=rows(CORPUS/"receipts.jsonl")
    assert m["batch_id"]=="batch-010"
    assert m["source_count"]==9
    assert m["source_page_count"]==27
    assert m["new_document_count"]==8
    assert m["previously_indexed_count"]==1
    assert m["new_unique_pages"]==24
    assert m["source_pdf_sha256_verified"] is True
    assert m["raw_pdf_in_repo"] is False
    assert len(index)>=55
    assert sum(x["page_count"] for x in index)>=212
    assert len(receipts)>=59
    assert len({x["source_sha256"] for x in index})==len(index)
    batch=[r for r in receipts if r["batch_id"]=="batch-010"]
    assert len(batch)==9
    assert len({r["source_sha256"] for r in batch})==9
    for n,(sourcehash,count) in EXPECTED.items():
        docid="pdf-"+sourcehash[:24]
        matching=[r for r in index if r["document_id"]==docid]
        assert len(matching)==1 and matching[0]["page_count"]==count
        assert matching[0]["source_sha256"]==sourcehash
        assert sum(r["source_sha256"]==sourcehash for r in batch)==1
    other54=[r for r in receipts if r["document_id"]==OLD54]
    assert sum(r["batch_id"]=="batch-009" for r in other54)==1
    assert sum(r["batch_id"]=="batch-010" for r in other54)==1

def test_batch_010_transcriptions_and_hashes():
    for n,(sourcehash,count) in EXPECTED.items():
        docid="pdf-"+sourcehash[:24]
        folder=CORPUS/"documents"/docid
        meta=json.loads((folder/"metadata.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"]==sourcehash
        assert meta["fact_check_status"]=="unverified_source_material"
        assert meta["quality_status"]=="extracted"
        assert meta["page_count"]==count
        assert len(meta["page_characters"])==count
        text=(folder/"document.txt").read_text(encoding="utf-8").removesuffix("\n")
        assert hashlib.sha256(text.encode("utf-8")).hexdigest()==meta["text_sha256"]
        assert (folder/"document.md").is_file()
        for page in range(1,count+1):
            contents=(folder/"pages"/f"{page:04d}.md").read_text(encoding="utf-8")
            assert f"strona {page}" in contents
            assert len(contents)>150

def test_batch_010_exact_text_not_merged():
    index=rows(CORPUS/"index.jsonl")
    docs={r["document_id"]:r for r in index}
    doc60="pdf-3b0b51ee7c46fa5536eb2f0e"
    assert doc60 in docs and DOC42 in docs
    assert docs[doc60]["source_sha256"]!=docs[DOC42]["source_sha256"]
    a=(CORPUS/docs[doc60]["text_path"]).read_text(encoding="utf-8")
    b=(CORPUS/docs[DOC42]["text_path"]).read_text(encoding="utf-8")
    assert " ".join(a.casefold().split())==" ".join(b.casefold().split())
    relations=json.loads((CORPUS/"duplicates.json").read_text(encoding="utf-8"))
    assert any({r["left_document_id"],r["right_document_id"]}=={doc60,DOC42} and r["relation"]=="exact_text" for r in relations)

def test_batch_010_no_raw_pdfs():
    assert not list(CORPUS.rglob("*.pdf"))
    assert not list(CORPUS.rglob("*.PDF"))
