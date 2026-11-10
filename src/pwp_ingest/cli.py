"""Interfejs CLI dla importu i audytu PDF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import ingest_paths, rebuild_index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pwp-ingest",
        description="PDF -> stronicowany Markdown, JSONL i raport duplikatów.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="Importuj PDF-y z plików lub katalogów.")
    ingest.add_argument("paths", nargs="+", type=Path)
    ingest.add_argument("--output", type=Path, default=Path("corpus"))
    ingest.add_argument("--no-ocr", action="store_true")
    ingest.add_argument("--ocr-lang", default="pol+eng")
    ingest.add_argument("--min-chars", type=int, default=40)
    ingest.add_argument("--batch-id", default="unassigned", help="Identyfikator partii, np. batch-001")
    audit = commands.add_parser("audit", help="Odtwórz indeks i wykryj duplikaty.")
    audit.add_argument("--output", type=Path, default=Path("corpus"))
    args = parser.parse_args(argv)

    try:
        if args.command == "ingest":
            ingested = ingest_paths(
                args.paths,
                args.output,
                ocr_enabled=not args.no_ocr,
                ocr_lang=args.ocr_lang,
                min_chars=args.min_chars,
                batch_id=args.batch_id,
            )
            summary = rebuild_index(args.output)
            summary["files_examined"] = len(ingested)
        else:
            summary = rebuild_index(args.output)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"BŁĄD: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
