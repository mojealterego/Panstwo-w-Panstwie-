"""Sprawdza kanoniczny import batch-012, 7 nowych źródeł i integralność 74 transkrypcji."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/"corpus"
EXPECTED={68: ('c0b771697ff10b27eec9539c1740c37851488b35b469b825a2bec88f33aeda22', 4), 69: ('7720c05c27d757a90c288a01237c8d9b5cc2e05c94e37fd7d1749598a90739e2', 14), 70: ('bdd5005055b9336a06a0a1f8709febf8d46ffe19ac86d5abe1430ff1bb77813a', 5), 71: ('f4b4fcc93724c4398c5e47d0d91137c422448c6c15b2d1ef1ef209317e0c990e', 6), 72: ('7c44ee9f0e4e121ae948cc5b8afdc2d5a37e70834dadf532b50c37a1b69aa4e7', 3), 73: ('e1dca27117c8a97691cb12aa8c14fbd1d6f5e72f0ce2e69d69d2f200f4334766', 21), 74: ('917c79f42f2b924868f00ab7181b9740e4522f569527f7bac19100e09256f871', 21)}

def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def test_batch_012_manifest_receipts():
    m=json.loads((CORPUS/"batches/batch-012.json").read_text(encoding="utf-8"))
    idx=rows(CORPUS/"index.jsonl")
    rec=rows(CORPUS/"receipts.jsonl")
    assert m["batch_id"]=="batch-012"
    assert m["source_count"]==7
    assert m["source_page_count"]==74
    assert m["new_document_count"]==7
    assert m["source_pdf_sha256_verified"] is True
    assert m["raw_pdf_in_repo"] is False
    assert len(idx)>=67 and sum(r["page_count"] for r in idx)>=312
    assert len(rec)>=71
    assert len({r["source_sha256"] for r in idx})==len(idx)
    batch=[r for r in rec if r["batch_id"]=="batch-012"]
    assert len(batch)==7
    for num,(sourcehash,pages) in EXPECTED.items():
        target="pdf-"+sourcehash[:24]
        found=[r for r in idx if r["document_id"]==target]
        assert len(found)==1
        assert found[0]["source_sha256"]==sourcehash
        assert found[0]["page_count"]==pages
        assert len([r for r in batch if r["source_sha256"]==sourcehash])==1

def test_batch_012_page_text_hashes():
    for num,(hash_source,pages) in EXPECTED.items():
        did="pdf-"+hash_source[:24]
        path=CORPUS/"documents"/did
        meta=json.loads((path/"metadata.json").read_text(encoding="utf-8"))
        content=(path/"document.txt").read_bytes()
        assert hashlib.sha256(content).hexdigest()==meta["text_sha256"]
        assert meta["source_sha256"]==hash_source
        assert meta["fact_check_status"]=="unverified_source_material"
        assert meta["page_count"]==pages
        assert meta["extraction_methods"]==["embedded_text"]*pages
        data=[]
        for page in range(1,pages+1):
            fp=path/"pages"/f"{page:04d}.md"
            assert fp.is_file()
            txt=fp.read_text(encoding="utf-8")
            assert txt.startswith(f"# {did} — strona {page}\n\n")
            data.append(txt.split("\n\n",1)[1].strip())
        assert content.decode("utf-8")=="\n\n".join(data)+"\n"

def test_batch_012_duplicate_relation_integrity():
    relations=json.loads((CORPUS/"batches/batch-012-relations.json").read_text(encoding="utf-8"))["relations"]
    allpairs=json.loads((CORPUS/"duplicates.json").read_text(encoding="utf-8"))
    idx=rows(CORPUS/"index.jsonl")
    known={r["document_id"] for r in idx}
    for relation in relations:
        assert relation["left_document_id"] in known
        assert relation["right_document_id"] in known
        match=[r for r in allpairs if r["left_document_id"]==relation["left_document_id"] and r["right_document_id"]==relation["right_document_id"]]
        assert len(match)==1 and match[0]["relation"]==relation["relation"]

def test_batch_012_short_final_page_preserved():
    did="pdf-"+EXPECTED[74][0][:24]
    txt=(CORPUS/"documents"/did/"pages"/"0021.md").read_text(encoding="utf-8")
    assert "odrzucić narzuconą nam rolę ofiar w ich dochodowym teatrze." in txt
