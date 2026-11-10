"""Batch-014: integralność 10 oryginałów, 55 stron, pochodzenie i prywatność."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'corpus'
SOURCES = {
    'Badanie Zespołów Interdyscyplinarnych ds. Przemocy(84).PDF': ('2b478148e1dabf2b3cc5b3a4f93d83fe0aac28bd36a0c9cebdaf04ccf9146a2d', 4),
    'Dokument bez nazwy.PDF': ('ad2aee68b29f72b1246ff8633a9aa5724f19f5e0acb6a5809dca9e0aa6f34af6', 2),
    'Dokument bez nazwy(1).PDF': ('edcfbd06ef08337f0e219c7aace593eabb6b5bcc0a15639f95a62a988464b7ca', 3),
    'Dokument bez nazwy(2).PDF': ('f93181c5e4e31c3b12880f1c59361e3b823eaa04544a67cec0d527bc88c73263', 4),
    'Dokument bez nazwy(3).PDF': ('8ab1669090b4d21ea690629b5849f1542b945cc623971414f1f0c7660ea5b1b5', 3),
    'Dokument bez nazwy(4).PDF': ('0f063f8856dd7a1950fec7b3dcce87a0afc1fb50ab709968157eff53fbbce769', 2),
    'Dokument bez nazwy(5).PDF': ('7d157b42970d21e70b3fd06c858ece91fe5cc3307477614b36a166ad9be3f81b', 15),
    'Ford Foundation_ Śledztwo Finansowe i Wpływy.PDF': ('46f458b9f7ab457835a90e83501fab79f612ea7521a5b21bee7f3bb0b09c6aa9', 10),
    'LONDYŃSKA KROPLÓWKA I KOLONIZACJA PRAWA. Sigrid Ra...PDF': ('0d0a4fc9a1165cac7beae50053b59614eacf063b39d1c0530cbc52ef5afab12b', 3),
    'Stiftung Mercator_ Śledztwo Finansowe i Wpływy.PDF': ('0599b948111930ce7fa4770bc240f162f2cf5d3254a219a15fc824d4ee241e2d', 9),
}


def jlines(p: Path) -> list[dict]:
    return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]


def test_batch_014_manifest_and_page_metadata():
    manifest = json.loads((CORPUS / 'batches/batch-014.json').read_text(encoding='utf-8'))
    assert manifest['batch_id'] == 'batch-014'
    assert manifest['source_count'] == 10
    assert manifest['source_page_count'] == 55
    assert manifest['new_document_count'] == 10
    assert manifest['new_unique_pages'] == 55
    assert manifest['source_pdf_sha256_verified'] is True
    assert manifest['raw_pdf_in_repo'] is False
    assert manifest['fact_check_status'] == 'unverified_source_material'
    assert {o['filename']: (o['source_sha256'], o['pages']) for o in manifest['originals']} == SOURCES


def test_batch_014_preserves_every_page_and_hash():
    for filename, (digest, page_count) in SOURCES.items():
        doc_id = 'pdf-' + digest[:24]
        path = CORPUS / 'documents' / doc_id
        metadata = json.loads((path / 'metadata.json').read_text(encoding='utf-8'))
        assert metadata['document_id'] == doc_id
        assert metadata['source_sha256'] == digest
        assert metadata['original_filenames'] == [filename]
        assert metadata['page_count'] == page_count
        assert metadata['extraction_methods'] == ['embedded_text'] * page_count
        assert metadata['fact_check_status'] == 'unverified_source_material'
        assert metadata['quality_status'] == 'extracted'
        assert metadata['editorial_review_required'] is True
        raw = (path / 'document.txt').read_bytes()
        assert hashlib.sha256(raw).hexdigest() == metadata['text_sha256']
        extracted = []
        for page in range(1, page_count + 1):
            md = (path / 'pages' / f'{page:04d}.md').read_text(encoding='utf-8')
            assert md.startswith(f'# {doc_id} — strona {page}\n\n')
            extracted.append(md.split('\n\n', 1)[1].strip())
        assert raw.decode('utf-8') == '\n\n'.join(extracted) + '\n'
        if (ROOT / 'originals' / filename).is_file():
            assert hashlib.sha256((ROOT / 'originals' / filename).read_bytes()).hexdigest() == digest


def test_batch_014_tables_and_conflict_review():
    manifest = json.loads((CORPUS / 'batches/batch-014.json').read_text(encoding='utf-8'))
    tables = json.loads((CORPUS / 'batches/batch-014-tables.json').read_text(encoding='utf-8'))
    conflicts = json.loads((CORPUS / 'batches/batch-014-editorial-review.json').read_text(encoding='utf-8'))
    assert len(tables['tables']) == manifest['recognized_tables_count']
    assert len(tables['tables']) >= 6
    assert conflicts['fact_check_status'] == 'unverified_source_material'
    assert conflicts['publication_review_required'] is True
    assert len(conflicts['conflicting_assessments']) >= 1


def test_batch_014_repo_receipts_and_duplicate_relations():
    # Standalone batch ZIP does not contain historical index: validate in-repo only.
    if not (CORPUS / 'index.jsonl').exists():
        return
    index = jlines(CORPUS / 'index.jsonl')
    receipts = jlines(CORPUS / 'receipts.jsonl')
    assert len(index) >= 86
    assert sum(x['page_count'] for x in index) >= 458
    assert len(receipts) >= 90
    assert len({x['source_sha256'] for x in index}) == len(index)
    b = [x for x in receipts if x['batch_id'] == 'batch-014']
    assert len(b) == 10
    assert {x['source_sha256'] for x in b} == {h for h, _ in SOURCES.values()}
    pairs = json.loads((CORPUS / 'duplicates.json').read_text(encoding='utf-8'))
    batch = json.loads((CORPUS / 'batches/batch-014-relations.json').read_text(encoding='utf-8'))
    for rel in batch['relations']:
        assert rel in pairs
        assert rel['left_document_id'] in {x['document_id'] for x in index}
        assert rel['right_document_id'] in {x['document_id'] for x in index}
