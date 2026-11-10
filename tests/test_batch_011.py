"""Kontrola kanonicznego przyjęcia partii 011 (63–67), w tym wykrywanie tekstów zawartych."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/"corpus"
EXPECTED={63: ('5206d071984502a92fc2064acbfd2dad9e76768b18d6e792ed04450d81f71e38', 4), 64: ('d38c13a826d8a8f1e25871f1b587dc5db3c50713ac57434ed13cdfc60233b10f', 7), 65: ('ebd2c8623be89110ae841f5c8f97f941a7b5ae1ec085df6248190c28bf3f7ba2', 3), 66: ('fcd864fafc99d3d7e1fd345afb07d77aa0c7a07cbbc487b60749732ba8061de8', 9), 67: ('13cd85e13fee2309c0212d472670cd8ffba23f4caccf4da8d76057e26bf47228', 3)}

def read_jsonl(path:Path)->list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def test_batch_011_manifest_and_receipts():
    manifest=json.loads((CORPUS/"batches/batch-011.json").read_text(encoding="utf-8"))
    index=read_jsonl(CORPUS/"index.jsonl")
    receipts=read_jsonl(CORPUS/"receipts.jsonl")
    assert manifest["source_count"]==5
    assert manifest["source_page_count"]==26
    assert manifest["new_document_count"]==5
    assert manifest["source_pdf_sha256_verified"] is True
    assert manifest["raw_pdf_in_repo"] is False
    assert len(index)>=60
    assert sum(x["page_count"] for x in index)>=238
    assert len(receipts)>=64
    assert len({r["source_sha256"] for r in index})==len(index)
    batch_receipts=[r for r in receipts if r["batch_id"]=="batch-011"]
    assert len(batch_receipts)==5
    for number,(sha,page_count) in EXPECTED.items():
        doc_id="pdf-"+sha[:24]
        records=[x for x in index if x["document_id"]==doc_id]
        assert len(records)==1
        assert records[0]["source_sha256"]==sha
        assert records[0]["page_count"]==page_count
        assert len([x for x in batch_receipts if x["source_sha256"]==sha])==1

def test_batch_011_exact_text_hash_and_pages():
    for number,(sha,page_count) in EXPECTED.items():
        doc_id="pdf-"+sha[:24]
        root=CORPUS/"documents"/doc_id
        m=json.loads((root/"metadata.json").read_text(encoding="utf-8"))
        txt=(root/"document.txt").read_bytes()
        assert m["source_sha256"]==sha
        assert hashlib.sha256(txt).hexdigest()==m["text_sha256"]
        assert m["quality_status"]=="extracted"
        assert m["fact_check_status"]=="unverified_source_material"
        assert m["page_count"]==page_count
        assert m["extraction_methods"]==["embedded_text"]*page_count
        pages=[]
        for page in range(1,page_count+1):
            fp=root/"pages"/f"{page:04d}.md"
            content=fp.read_text(encoding="utf-8")
            assert content.startswith(f"# {doc_id} — strona {page}\n\n")
            pages.append(content.split("\n\n",1)[1].strip())
        assert txt.decode("utf-8")=="\n\n".join(pages)+"\n"

def test_batch_011_containment_does_not_collapse_sources():
    relations=json.loads((CORPUS/"duplicates.json").read_text(encoding="utf-8"))
    required=[(63,64),(63,66)]
    for x,y in required:
        pair={"pdf-"+EXPECTED[x][0][:24],"pdf-"+EXPECTED[y][0][:24]}
        matching=[r for r in relations if {r["left_document_id"],r["right_document_id"]}==pair]
        assert len(matching)==1
        assert matching[0]["relation"]=="contained_in"
        assert matching[0]["containment"]==1.0
    data=json.loads((CORPUS/"batches/batch-011-relations.json").read_text(encoding="utf-8"))
    assert len(data["relations"])==2
    assert len(data["exact_page_duplicates"])==9
    assert len(set(EXPECTED.values()))==5
