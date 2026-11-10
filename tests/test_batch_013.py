"""Kontrola integralności batch-013, 9 źródeł, 91 stron i duplikatów tekstowych."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/"corpus"
EXPECTED={75: ('072dff5525d0e6778dfcdda019e43c39b56f9cdc86b9332ec97720d3e2e9392c', 21), 76: ('bbf9a3d3b5f143bcc261012251f5bfb75fd7e64a52bc5f4e4a681fefd086bcf0', 23), 77: ('752786eb5c544b0e3f2daa82f45a02175b8686760fcaa3451c8c8e0065709c0e', 24), 78: ('cef8f114682b0261ae22f97694b27da34d571d18aa4bcab0864546e63508cad4', 3), 79: ('946c9dcea35dae6d2d74c5fec0504e40ec1a2c3d84db82370e2e1edf9a7e6dbe', 3), 80: ('87b3b042a0aa5938650431e9f801b7ae73e9bcbb0eccbc099c4eceec631f62c2', 4), 81: ('2b0304d6d4fec68517a41cce9bee050106707849b941d198eec724dd12498eb0', 5), 82: ('e926b0c6f1c3d378a7daed263ab46ba52e2c1d7e00d7f1380f08148545f47bb3', 5), 83: ('883276f1643113333126fda2e4174affe1b9aecf48cd2fa5411ffc060a3045de', 3)}

def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def test_batch_013_manifest_receipts_and_uniqueness():
    m=json.loads((CORPUS/"batches/batch-013.json").read_text(encoding="utf-8"))
    idx=rows(CORPUS/"index.jsonl")
    rc=rows(CORPUS/"receipts.jsonl")
    assert m["batch_id"]=="batch-013"
    assert m["source_count"]==9 and m["source_page_count"]==91
    assert m["new_document_count"]==9 and m["new_unique_pages"]==91
    assert m["source_pdf_sha256_verified"] is True and m["raw_pdf_in_repo"] is False
    assert len(idx)>=76 and sum(x["page_count"] for x in idx)>=403
    assert len(rc)>=80
    assert len({x["source_sha256"] for x in idx})==len(idx)
    batch=[x for x in rc if x["batch_id"]=="batch-013"]
    assert len(batch)==9 and len({x["source_sha256"] for x in batch})==9
    for n,(h,pages) in EXPECTED.items():
        matches=[x for x in idx if x["source_sha256"]==h]
        assert len(matches)==1 and matches[0]["page_count"]==pages
        assert sum(x["source_sha256"]==h for x in batch)==1

def test_batch_013_transcripts_sha256_page_preservation():
    for n,(source_hash,pages) in EXPECTED.items():
        did="pdf-"+source_hash[:24]
        base=CORPUS/"documents"/did
        meta=json.loads((base/"metadata.json").read_text(encoding="utf-8"))
        raw=(base/"document.txt").read_bytes()
        assert hashlib.sha256(raw).hexdigest()==meta["text_sha256"]
        assert meta["source_sha256"]==source_hash
        assert meta["page_count"]==pages
        assert meta["extraction_methods"]==["embedded_text"]*pages
        assert meta["fact_check_status"]=="unverified_source_material"
        assert meta["quality_status"]=="extracted"
        texts=[]
        for p in range(1,pages+1):
            f=base/"pages"/f"{p:04d}.md"
            assert f.is_file()
            s=f.read_text(encoding="utf-8")
            assert s.startswith(f"# {did} — strona {p}\n\n")
            texts.append(s.split("\n\n",1)[1].strip())
        assert raw.decode("utf-8")=="\n\n".join(texts)+"\n"

def test_batch_013_cross_reference_relations():
    group=json.loads((CORPUS/"batches/batch-013-relations.json").read_text(encoding="utf-8"))
    allpairs=json.loads((CORPUS/"duplicates.json").read_text(encoding="utf-8"))
    ids={x["document_id"] for x in rows(CORPUS/"index.jsonl")}
    assert len(group["relations"])>=1
    for relation in group["relations"]:
        assert relation["left_document_id"] in ids
        assert relation["right_document_id"] in ids
        matches=[p for p in allpairs if p["left_document_id"]==relation["left_document_id"] and p["right_document_id"]==relation["right_document_id"]]
        assert len(matches)==1 and matches[0]["relation"]==relation["relation"]

def test_batch_013_sensitive_source_editorial_flag():
    for n in (78,79,80,81,82):
        did="pdf-"+EXPECTED[n][0][:24]
        meta=json.loads((CORPUS/"documents"/did/"metadata.json").read_text(encoding="utf-8"))
        assert "minor" in meta["editorial_risk"].lower()
