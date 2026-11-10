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
pwp-ingest ingest incoming --output corpus
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
src/pwp_ingest/                 # pipeline konwersji
tests/                          # testy kolizji, idempotencji, duplikatów i OCR
docs/                           # kontrakty i procedury redakcyjne
AGENTS.md                       # reguły dla agentów AI
```

## Bezpieczeństwo publikacji

**Repozytorium jest publiczne.** Nie umieszczaj w nim bez przeglądu redakcyjnego dokumentów zawierających dane osobowe, informacje wrażliwe ani niezweryfikowane oskarżenia. `incoming/` jest ignorowane przez Git. Wygenerowany `corpus/` **nie jest automatycznie wysyłany** do GitHub: przed `git add` i `git push` przeprowadź kontrolę treści, anonimizację i weryfikację prawną. Jeżeli cały materiał ma pozostać poufny, przechowuj korpus w prywatnym repozytorium.

## Status

Infrastruktura konwersji jest rozwijana. Odbiór konkretnych partii PDF następuje dopiero po odczytaniu oryginalnych bajtów, zarejestrowaniu SHA-256 i sprawdzeniu wyniku ekstrakcji. Nie należy traktować samego podglądu tekstowego w czacie jako zweryfikowanego importu pliku.
