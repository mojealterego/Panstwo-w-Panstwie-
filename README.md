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

**Repozytorium jest publiczne.** Nie umieszczaj w nim bez przeglądu redakcyjnego dokumentów zawierających dane osobowe, informacje wrażliwe ani niezweryfikowane oskarżenia. `incoming/` jest ignorowane przez Git. Wygenerowany `corpus/` **nie jest automatycznie wysyłany** do GitHub: przed publikacją nowych materiałów przeprowadź kontrolę treści, anonimizację i weryfikację prawną. Jeżeli cały materiał ma pozostać poufny, przechowuj korpus w prywatnym repozytorium.

## Stan przyjęcia źródeł (2026-11-11)

**129 unikatowych PDF-ów / 618 stron** w kanonicznym `corpus/` (wg SHA-256 bajtów źródłowych). Łącznie **135 rekordów przyjęcia** w `corpus/receipts.jsonl`. Oryginały PDF partii 015–019 zapisano bajtowo w `corpus/originals/batch-015/`, `corpus/originals/batch-016/` i `corpus/originals/batch-017/` oraz `corpus/originals/batch-018/` i `corpus/originals/batch-019/`; oryginały starszych partii pozostają w odrębnych archiwach Biblioteki.

- **batch-001:** 10 oryginałów, 72 strony — [raport](docs/batches/batch-001.md).
- **batch-002:** 5 dostępnych oryginałów, 15 stron (3 nowe dokumenty, 9 nowych unikatowych stron) — [raport](docs/batches/batch-002.md).
- **batch-003:** 5 oryginałów, 16 stron (4 nowe dokumenty, 13 nowych unikatowych stron; PDF 19 był już w indeksie) — [raport](docs/batches/batch-003.md). Tabela z PDF 22, strona 3, jest również dostępna w formatach Markdown i JSON.
- **batch-004:** 5 oryginałów, 15 stron (5 nowych dokumentów) — [raport](docs/batches/batch-004.md). Brak nowych duplikatów tekstowych.
- **batch-005:** 5 oryginałów, 15 stron (5 nowych dokumentów) — [raport](docs/batches/batch-005.md). Brak nowych relacji duplikacji tekstu.
- **batch-006:** 5 oryginalnych PDF-ów (34–38), 18 stron, 5 nowych dokumentów kanonicznych; oryginały w oddzielnym ZIP i Bibliotece, transkrypcje oraz 3 tabele w repo — [raport](docs/batches/batch-006.md).
- **batch-007:** 5 oryginalnych PDF-ów (39–43), 16 stron, 5 nowych dokumentów; tabela dotacji z PDF 40 w JSON i Markdown, ZIP z oryginałami w Bibliotece — [raport](docs/batches/batch-007.md).
- **batch-008:** 5 oryginalnych PDF-ów (44–48), 15 stron, 5 nowych dokumentów; lista darczyńców EDRi w JSON i Markdown, kopia ZIP w Bibliotece — [raport](docs/batches/batch-008.md).
- **batch-009:** 5 oryginalnych PDF-ów (49, 50, 51, 52, 54), 15 stron, 5 nowych dokumentów; brak PDF 53; kopia ZIP w Bibliotece — [raport](docs/batches/batch-009.md).
- **batch-010:** 9 PDF-ów (54–62), 27 stron; 8 nowych dokumentów i 24 nowe strony. PDF 54: identyczne bajty z batch-009; PDF 60: identyczny tekst z PDF 42, lecz odrębne bajty. ZIP zachowany w Bibliotece — [raport](docs/batches/batch-010.md).
- **batch-011:** 5 oryginalnych PDF-ów (63–67), 26 stron; 5 nowych dokumentów. PDF 63 jest w całości zawarty w PDF 64 i PDF 66 (odrębne bajty); zachowano wszystkie źródła i pełne transkrypcje — [raport](docs/batches/batch-011.md). ZIP oryginałów i pełnego korpusu w Bibliotece.
- **batch-012:** 7 oryginalnych PDF-ów (68–74), 74 strony; 7 nowych dokumentów; 7 nowych relacji zawierania tekstu i 12 par identycznych stron — [raport](docs/batches/batch-012.md). Oryginały i pełny ZIP zachowane w Bibliotece.
- **batch-013:** 9 PDF-ów (75–83), 91 stron, 9 nowych dokumentów; 9 relacji powtarzających się treści, 27 par identycznych stron. Pełny ZIP i oryginały w Bibliotece — [raport](docs/batches/batch-013.md). Materiały wymagają weryfikacji i przeglądu prawnego przed publikacją.
- **batch-014:** 10 oryginalnych PDF-ów (w tym nr 84 i dokumenty opisowe), 55 stron, 10 nowych źródeł i 6 tabel. Dwie relacje zawierania tekstu, przejrzysta dokumentacja rozbieżnych ocen; pełny ZIP i kopia oryginałów w Bibliotece — [raport](docs/batches/batch-014.md). Publikacja wymaga weryfikacji zarzutów i kontroli danych osobowych.
- **batch-015:** 5 PDF-ów, 18 stron; oryginały i pełne teksty dodane do repozytorium; archiwum ZIP w Bibliotece — [raport](docs/batches/batch-015.md).
- **batch-016:** 10 PDF-ów, 46 stron; oryginały i pełne teksty dodane do repozytorium; archiwum ZIP w Bibliotece — [raport](docs/batches/batch-016.md).
- **batch-017:** 10 oryginałów, 31 stron; 9 nowych dokumentów, 28 stron kanonicznych, 1 dokładny duplikat PDF z dwiema zachowanymi nazwami — [raport](docs/batches/batch-017.md). Weryfikację i wcześniejszą publikację części materiałów zadeklarował autor.
- **batch-018:** 10 PDF-ów, 32 strony, 10 nowych źródeł; zachowano oryginały binarne, teksty stronicowane i sumy kontrolne — [raport](docs/batches/batch-018.md). Deklaracja osobistej weryfikacji autora oddzielona od niezależnej kontroli źródeł.
- **batch-019:** 10 oryginalnych PDF-ów, 39 stron; 9 nowych źródeł (36 stron kanonicznych), 1 dokładny duplikat z batch-018. Zapisano binaria, transkrypcje i tabele — [raport](docs/batches/batch-019.md).
- **Niedostarczone:** PDF 53 oraz sloty 01–05 partii 002; nie są uwzględnione w indeksie.

Wszystkie twierdzenia źródłowe mają status `unverified_source_material`. Publiczne repozytorium nie jest potwierdzeniem zarzutów.
