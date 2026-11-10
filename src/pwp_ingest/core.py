"""Deterministyczny import PDF z zachowaniem proweniencji i kontroli jakości."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import fitz


SCHEMA_VERSION = 1
MAX_PDF_BYTES = 150 * 1024 * 1024
MIN_SHARED_SHINGLES = 20


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_text(text: str) -> str:
    """Normalizacja bez usuwania polskich znaków i bez parafrazowania źródła."""
    value = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in value.split("\n")).strip()


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, value: Any) -> None:
    _write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _pdf_inputs(inputs: Iterable[Path]) -> list[tuple[Path, str]]:
    """Zwraca pliki wraz ze ścieżką względną, bez ujawniania lokalnych katalogów."""
    discovered: dict[Path, str] = {}
    for source in inputs:
        path = Path(source).expanduser()
        if path.is_file() and path.suffix.lower() == ".pdf":
            discovered[path.resolve()] = path.name
        elif path.is_dir():
            for item in path.rglob("*"):
                if item.is_file() and item.suffix.lower() == ".pdf":
                    discovered[item.resolve()] = item.relative_to(path).as_posix()
        else:
            raise ValueError(f"Brak pliku PDF lub katalogu: {path}")
    if not discovered:
        raise ValueError("Nie znaleziono żadnego pliku PDF.")
    return sorted(discovered.items(), key=lambda item: str(item[0]))


def _ocr_page(page: fitz.Page, language: str) -> str:
    """OCR lokalny: nie wysyła treści do usług zewnętrznych."""
    image = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).tobytes("png")
    result = subprocess.run(
        ["tesseract", "stdin", "stdout", "-l", language, "--psm", "3"],
        input=image,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"Tesseract zakończył pracę z kodem {result.returncode}: {message}")
    return normalize_text(result.stdout.decode("utf-8", errors="replace"))


def _extract_pages(
    raw: bytes, *, ocr_enabled: bool, ocr_lang: str, min_chars: int
) -> list[dict[str, Any]]:
    try:
        document = fitz.open(stream=raw, filetype="pdf")
    except Exception as exc:
        raise ValueError(f"Nieprawidłowy lub uszkodzony PDF: {exc}") from exc

    try:
        if document.needs_pass:
            raise ValueError("PDF jest zaszyfrowany; nie podano hasła.")
        if document.page_count == 0:
            raise ValueError("PDF nie zawiera stron.")

        result: list[dict[str, Any]] = []
        for number in range(document.page_count):
            page = document.load_page(number)
            text = normalize_text(page.get_text("text", sort=True))
            method = "embedded_text"
            warnings: list[str] = []
            if len(text.strip()) < min_chars and ocr_enabled:
                try:
                    recognized = _ocr_page(page, ocr_lang)
                    if len(recognized.strip()) > len(text.strip()):
                        text = recognized
                        method = "local_ocr"
                except (FileNotFoundError, subprocess.TimeoutExpired, RuntimeError, OSError):
                    warnings.append("ocr_unavailable_or_failed")
            if len(text.strip()) < min_chars:
                warnings.append("insufficient_text")
            result.append({
                "page": number + 1,
                "text": text,
                "method": method,
                "characters": len(text),
                "warnings": warnings,
            })
        return result
    finally:
        document.close()


def ingest_one(
    source: Path,
    output: Path,
    *,
    ocr_enabled: bool = True,
    ocr_lang: str = "pol+eng",
    min_chars: int = 40,
) -> dict[str, Any]:
    """Importuje pojedynczy plik. Ta sama nazwa nie wpływa na tożsamość."""
    if min_chars < 0:
        raise ValueError("min_chars nie może być ujemne.")
    if source.stat().st_size > MAX_PDF_BYTES:
        raise ValueError(f"PDF przekracza limit 150 MiB: {source}")
    raw = source.read_bytes()
    if not raw.startswith(b"%PDF-"):
        raise ValueError(f"Plik nie ma nagłówka PDF: {source}")
    digest = sha256_bytes(raw)
    doc_id = "pdf-" + digest[:24]
    folder = output / "documents" / doc_id
    metadata_path = folder / "metadata.json"

    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("source_sha256") != digest:
            raise RuntimeError(f"Kolizja identyfikatora dokumentu: {doc_id}")
        aliases = sorted(set(metadata["original_filenames"]) | {source.name})
        if aliases != metadata["original_filenames"]:
            metadata["original_filenames"] = aliases
            _write_json(metadata_path, metadata)
        return metadata

    pages = _extract_pages(
        raw, ocr_enabled=ocr_enabled, ocr_lang=ocr_lang, min_chars=min_chars
    )
    plain = "\n\n".join(page["text"] for page in pages)
    full_markdown = [
        f"# Dokument źródłowy {doc_id}",
        "",
        "> Transkrypcja automatyczna. Treść źródła nie jest weryfikacją zawartych w nim twierdzeń.",
        "",
    ]
    for page in pages:
        number = page["page"]
        full_markdown.extend([f"## Strona {number}", "", page["text"], ""])
        _write_text(
            folder / "pages" / f"{number:04d}.md",
            f"# {doc_id} — strona {number}\n\n{page['text']}\n",
        )

    _write_text(folder / "document.md", "\n".join(full_markdown).rstrip() + "\n")
    _write_text(folder / "document.txt", plain + "\n")
    metadata = {
        "schema_version": SCHEMA_VERSION,
        "document_id": doc_id,
        "source_sha256": digest,
        "text_sha256": sha256_bytes(plain.encode("utf-8")),
        "original_filenames": [source.name],
        "page_count": len(pages),
        "page_characters": [page["characters"] for page in pages],
        "extraction_methods": [page["method"] for page in pages],
        "page_warnings": [
            {"page": page["page"], "reason": warning}
            for page in pages for warning in page["warnings"]
        ],
        "quality_status": "review_required" if any(page["warnings"] for page in pages) else "extracted",
        "fact_check_status": "unverified_source_material",
        "markdown_path": f"documents/{doc_id}/document.md",
        "text_path": f"documents/{doc_id}/document.txt",
    }
    _write_json(metadata_path, metadata)
    return metadata


def _word_shingles(text: str, size: int = 5) -> set[tuple[str, ...]]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    words = re.findall(r"\w+", normalized, flags=re.UNICODE)
    if not words:
        return set()
    if len(words) < size:
        return {tuple(words)}
    return {tuple(words[index:index + size]) for index in range(len(words) - size + 1)}


def classify_texts(left: str, right: str) -> dict[str, Any] | None:
    """Oznacza zbieżność, bez automatycznego scalania materiałów."""
    left_normalized = " ".join(left.casefold().split())
    right_normalized = " ".join(right.casefold().split())
    if left_normalized and left_normalized == right_normalized:
        return {"relation": "exact_text", "jaccard": 1.0, "containment": 1.0}
    a, b = _word_shingles(left), _word_shingles(right)
    if min(len(a), len(b)) < MIN_SHARED_SHINGLES:
        return None
    shared = len(a & b)
    if shared < MIN_SHARED_SHINGLES:
        return None
    jaccard = shared / len(a | b)
    containment = shared / min(len(a), len(b))
    if jaccard >= 0.9:
        relation = "near_duplicate"
    elif containment >= 0.9:
        relation = "contained_in"
    else:
        return None
    return {
        "relation": relation,
        "jaccard": round(jaccard, 5),
        "containment": round(containment, 5),
        "shared_shingles": shared,
    }


def rebuild_index(output: Path) -> dict[str, int]:
    """Odtwarza indeks, kolejkę kontroli i relacje duplikatów z metadanych."""
    records: list[dict[str, Any]] = []
    for metadata_file in sorted((output / "documents").glob("*/metadata.json")):
        record = json.loads(metadata_file.read_text(encoding="utf-8"))
        if record["schema_version"] != SCHEMA_VERSION:
            raise ValueError(f"Nieobsługiwany schemat: {metadata_file}")
        records.append(record)
    records.sort(key=lambda record: record["document_id"])

    index = [
        {
            key: record[key]
            for key in (
                "document_id", "source_sha256", "text_sha256", "original_filenames",
                "page_count", "quality_status", "fact_check_status",
                "markdown_path", "text_path"
            )
        }
        for record in records
    ]
    _write_text(
        output / "index.jsonl",
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in index),
    )

    review = [
        {"document_id": record["document_id"], **warning}
        for record in records for warning in record["page_warnings"]
    ]
    _write_text(
        output / "review_queue.jsonl",
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in review),
    )

    duplicates: list[dict[str, Any]] = []
    texts = {
        record["document_id"]: (output / record["text_path"]).read_text(encoding="utf-8")
        for record in records
    }
    for left_index, left in enumerate(records):
        for right in records[left_index + 1:]:
            result = classify_texts(texts[left["document_id"]], texts[right["document_id"]])
            if result is not None:
                duplicates.append({
                    "left_document_id": left["document_id"],
                    "right_document_id": right["document_id"],
                    **result,
                })
    _write_json(output / "duplicates.json", duplicates)
    return {"documents": len(records), "review_items": len(review), "duplicate_pairs": len(duplicates)}


def ingest_paths(
    inputs: Iterable[Path],
    output: Path,
    *,
    ocr_enabled: bool = True,
    ocr_lang: str = "pol+eng",
    min_chars: int = 40,
    batch_id: str = "unassigned",
) -> list[dict[str, Any]]:
    """Przetwarza każdą pozycję wejściową i zachowuje historię partii."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", batch_id):
        raise ValueError("batch_id: wymagane 1–64 znaki ASCII: litery, cyfry, _ lub -.")
    files = _pdf_inputs(inputs)
    output = Path(output)
    receipts_path = output / "receipts.jsonl"
    receipts: dict[tuple[str, str, str], dict[str, Any]] = {}
    if receipts_path.exists():
        for line in receipts_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                key = (row["batch_id"], row["source_relative_path"], row["source_sha256"])
                receipts[key] = row

    records: list[dict[str, Any]] = []
    for source, relative_path in files:
        metadata = ingest_one(
            source, output,
            ocr_enabled=ocr_enabled,
            ocr_lang=ocr_lang,
            min_chars=min_chars,
        )
        records.append(metadata)
        receipt = {
            "batch_id": batch_id,
            "source_relative_path": relative_path,
            "original_filename": source.name,
            "source_sha256": metadata["source_sha256"],
            "document_id": metadata["document_id"],
            "quality_status": metadata["quality_status"],
        }
        receipts[(batch_id, relative_path, metadata["source_sha256"])] = receipt

    _write_text(
        receipts_path,
        "".join(
            json.dumps(receipts[key], ensure_ascii=False, sort_keys=True) + "\n"
            for key in sorted(receipts)
        ),
    )
    rebuild_index(output)
    return records
