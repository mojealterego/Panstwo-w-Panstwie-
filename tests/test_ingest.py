from __future__ import annotations

import json
from pathlib import Path

import fitz
import pytest

from pwp_ingest.core import classify_texts, ingest_paths


def make_pdf(path: Path, text: str, title: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    page.insert_textbox(fitz.Rect(40, 40, 555, 790), text, fontsize=10)
    if title:
        doc.set_metadata({"title": title})
    doc.save(path)
    doc.close()


def index_rows(output: Path) -> list[dict]:
    return [json.loads(line) for line in (output / "index.jsonl").read_text(encoding="utf-8").splitlines()]


def test_same_filename_different_contents_are_distinct(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    make_pdf(root / "batch1" / "raport.pdf", "Raport pierwszy. " * 30)
    make_pdf(root / "batch2" / "raport.pdf", "Raport drugi. " * 30)
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False)

    rows = index_rows(out)
    assert len(rows) == 2
    assert len({row["source_sha256"] for row in rows}) == 2
    assert {row["original_filenames"][0] for row in rows} == {"raport.pdf"}


def test_same_bytes_different_names_preserves_both_aliases(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    make_pdf(root / "pierwszy.pdf", "Dokument o stałej treści. " * 30)
    (root / "drugi.pdf").write_bytes((root / "pierwszy.pdf").read_bytes())
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False)

    rows = index_rows(out)
    assert len(rows) == 1
    assert rows[0]["original_filenames"] == ["drugi.pdf", "pierwszy.pdf"]


def test_same_text_different_pdf_bytes_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    make_pdf(root / "a.pdf", "Identyczna treść dokumentu. " * 35, title="A")
    make_pdf(root / "b.pdf", "Identyczna treść dokumentu. " * 35, title="B")
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False)

    pairs = json.loads((out / "duplicates.json").read_text(encoding="utf-8"))
    assert len(index_rows(out)) == 2
    assert any(pair["relation"] == "exact_text" for pair in pairs)


def test_partial_containment_detected_without_merging() -> None:
    short = " ".join(f"token{i:03d}" for i in range(90))
    long = short + " " + " ".join(f"extension{i:03d}" for i in range(90))

    result = classify_texts(short, long)

    assert result is not None
    assert result["relation"] == "contained_in"
    assert result["containment"] >= 0.9


def test_blank_page_goes_to_review_queue(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    root.mkdir()
    doc = fitz.open()
    doc.new_page()
    doc.save(root / "blank.pdf")
    doc.close()
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False)

    review = [json.loads(line) for line in (out / "review_queue.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(review) == 1
    assert review[0]["page"] == 1
    assert review[0]["reason"] == "insufficient_text"


def test_reingest_is_idempotent(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    make_pdf(root / "a.pdf", "Przykładowa treść. " * 30)
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False)
    first_index = (out / "index.jsonl").read_bytes()
    first_metadata = next((out / "documents").glob("*/metadata.json")).read_bytes()
    ingest_paths([root], out, ocr_enabled=False)

    assert (out / "index.jsonl").read_bytes() == first_index
    assert next((out / "documents").glob("*/metadata.json")).read_bytes() == first_metadata


def test_invalid_pdf_does_not_create_document(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    root.mkdir()
    (root / "bad.pdf").write_bytes(b"not a pdf")

    with pytest.raises(ValueError, match="PDF"):
        ingest_paths([root], tmp_path / "corpus", ocr_enabled=False)

    assert not list((tmp_path / "corpus" / "documents").glob("*/metadata.json"))


def test_page_markers_preserve_traceability(tmp_path: Path) -> None:
    root = tmp_path / "incoming"
    root.mkdir()
    doc = fitz.open()
    doc.new_page().insert_text((40, 40), "Pierwsza strona z dowodem")
    doc.new_page().insert_text((40, 40), "Druga strona z dowodem")
    doc.save(root / "dwie.pdf")
    doc.close()
    out = tmp_path / "corpus"

    ingest_paths([root], out, ocr_enabled=False, min_chars=10)

    doc_dir = next((out / "documents").iterdir())
    body = (doc_dir / "document.md").read_text(encoding="utf-8")
    assert "## Strona 1" in body
    assert "## Strona 2" in body
    assert (doc_dir / "pages" / "0001.md").exists()
    assert (doc_dir / "pages" / "0002.md").exists()
