# Państwo w Państwie — korpus źródłowy książki

Repozytorium narzędzi do przekształcania ponad 100 dokumentów PDF w **audytowalny korpus dla agenta redakcyjno-badawczego**. Nie jest to jeszcze gotowa książka ani zweryfikowany zbiór faktów.

## Założenia

- Każdy plik jest analizowany po **bajtach**, nie po nazwie. Identyczne nazwy i różne treści dają odrębne rekordy.
- Identyczne pliki (SHA-256) są rejestrowane jako jeden obiekt źródłowy z listą nazw wejściowych; żadna nazwa nie jest tracona.
- Każda strona otrzymuje własny plik Markdown; dostępne są też pełny tekst, metadane JSON i indeks JSONL.
- Duplikaty tekstowe i dokumenty zawierające cudze fragmenty są **oznaczane, nie usuwane**.
- Tekst wyodrębniony z PDF nie jest automatycznie dowodem prawdziwości zawartych w nim zarzutów.

## Uruchomienie lokalne

Wymagany Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
# Opcjonalnie OCR skanów: sudo apt-get install tesseract-ocr tesseract-ocr-pol
mkdir -p incoming
# Umieść tu pliki PDF (również te o identycznych nazwach, rozdzielając je katalogami).
pwp-ingest ingest incoming --output corpus --batch-id batch-001
pwp-ingest audit --output corpus
pytest -q
```

W Windows aktywacja środowiska to `.venv\Scripts\activate`. Katalog wejściowy jest skanowany rekurencyjnie; nie zmieniaj nazw oryginałów tylko po to, aby uniknąć kolizji.

## Struktura

```text
incoming/                       # oryginalne PDF-y, lokalnie, poza Git
corpus/
  documents/<sha256-prefix>/
    metadata.json               # hash pliku, nazwy, jakość ekstrakcji
    document.md                 # pełny tekst z oznaczeniami stron
    pages/0001.md               # tekst pojedynczej strony
  index.jsonl                   # indeks dokumentów dla agentów
  duplicates.json               # pary: exact/near/contained
  review_queue.jsonl            # problemy ekstrakcji do ręcznej kontroli
  receipts.jsonl                # każde wystąpienie pliku w danej partii
src/pwp_ingest/                 # pipeline konwersji
tests/                          # testy kolizji, idempotencji, duplikatów i OCR
docs/                           # kontrakty i procedury redakcyjne
AGENTS.md                       # reguły dla agentów AI
```

## Bezpieczeństwo publikacji

**Repozytorium jest publiczne.** Nie umieszczaj w nim bez przeglądu redakcyjnego dokumentów zawierających dane osobowe, informacje wrażliwe ani niezweryfikowane oskarżenia. `incoming/` jest ignorowane przez Git. Wygenerowany `corpus/` **nie jest automatycznie wysyłany** do GitHub: przed `git add` i `git push` przeprowadź kontrolę treści, anonimizację i weryfikację prawną. Jeżeli cały materiał ma pozostać poufny, przechowuj korpus w prywatnym repozytorium.

## Stan przyjęcia źródeł (2026-11-10)

**27 unikatowych PDF-ów / 124 strony** w kanonicznym `corpus/` (wg SHA-256 bajtów źródłowych). Łącznie **30 rekordów przyjęcia** w `corpus/receipts.jsonl`. Oryginały binarne PDF pozostają poza publicznym repozytorium.

- **batch-001:** 10 oryginałów, 72 strony — [raport](docs/batches/batch-001.md).
- **batch-002:** 5 dostępnych oryginałów, 15 stron (3 nowe dokumenty, 9 nowych unikatowych stron) — [raport](docs/batches/batch-002.md).
- **batch-003:** 5 oryginałów, 16 stron (4 nowe dokumenty, 13 nowych unikatowych stron; PDF 19 był już w indeksie) — [raport](docs/batches/batch-003.md). Tabela z PDF 22, strona 3, jest również dostępna w formatach Markdown i JSON.
- **batch-004:** 5 oryginałów, 15 stron (5 nowych dokumentów) — [raport](docs/batches/batch-004.md). Brak nowych duplikatów tekstowych.
- **batch-005:** 5 oryginałów, 15 stron (5 nowych dokumentów) — [raport](docs/batches/batch-005.md). Brak nowych relacji duplikacji tekstu.
- **Niedostarczone:** sloty 01–05 partii 002; nie są uwzględnione w indeksie.

Wszystkie twierdzenia źródłowe mają status `unverified_source_material`. Publiczne repozytorium nie jest potwierdzeniem zarzutów.
