# Kontrakt danych i procedura przyjęcia partii

## Tożsamość i wersjonowanie

Identyfikator `pdf-<pierwsze 24 znaki SHA-256>` pochodzi z **bajtów pliku**, nie z nazwy. Pełny SHA-256 jest przechowywany w `metadata.json`. Przy hipotetycznej kolizji skróconego identyfikatora import kończy się błędem.

Każda strona zachowuje numerację 1-based. Korpus zapisuje:
- `document.md`: pełną transkrypcję z granicami stron;
- `document.txt`: tekst bez nagłówków technicznych, do wyszukiwania i deduplikacji;
- `pages/NNNN.md`: stronicowane fragmenty do RAG i cytowania;
- `metadata.json`: pochodzenie, status ekstrakcji i sygnały ostrzegawcze;
- `index.jsonl`: jeden wiersz na unikatowy hash źródłowy;
- `duplicates.json`: pary potencjalnych duplikatów tekstowych i dokumentów zagnieżdżonych;
- `review_queue.jsonl`: strony wymagające kontroli z oryginałem.
- `receipts.jsonl`: rejestr każdego pliku wejściowego z numerem partii, względną ścieżką i SHA-256 (bez ujawniania absolutnych ścieżek lokalnych).

## Algorytm podobieństwa

Porównanie pełnych bajtów: SHA-256 (dokładny duplikat źródła). Porównanie tekstu: normalizacja białych znaków, 5-wyrazowe shingles, Jaccard i containment. Dla wspólnej części co najmniej 20 shingles: `near_duplicate` przy Jaccard >= 0,9; `contained_in` przy containment >= 0,9. Te progi służą **do flagowania**, nie do automatycznego odrzucania plików. Krótkie wspólne fragmenty mogą wymagać ręcznej analizy.

## OCR i ograniczenia

Tekst osadzony w PDF jest pobierany przez PyMuPDF. Jeżeli strona zawiera mniej niż domyślne 40 znaków, wykonywana jest próba lokalnego OCR za pomocą Tesseract (`pol+eng`). Brak OCR, błąd albo niedostateczna ilość tekstu trafiają do kolejki przeglądu. Tekst z tabel, przypisów, wielokolumnowego składu, wykresów i obrazów może wymagać porównania wizualnego. Ten pipeline nie gwarantuje wierności tabel i układu graficznego.

Limit pojedynczego PDF: 150 MiB. Zaszyfrowane i uszkodzone PDF-y są odrzucane z komunikatem, bez tworzenia fałszywej transkrypcji.

## Protokół partii 10 PDF-ów

1. Zachowaj wszystkie oryginały w osobnym, zabezpieczonym archiwum.
2. Umieść je w `incoming/batch-001/`, `incoming/batch-002/` itd. Nazwy w różnych katalogach mogą się powtarzać.
3. Uruchom `pwp-ingest ingest incoming/batch-001 --output corpus --batch-id batch-001`.
4. Sprawdź `review_queue.jsonl`, `duplicates.json` i porównaj losowe strony z oryginałem.
5. Sporządź raport przyjęcia: liczba PDF-ów, nowe hashe, duplikaty bajtowe, zbieżności tekstowe, błędy/OCR.
6. Przed publikacją w GitHub dokonaj przeglądu danych osobowych i zarzutów. Nigdy nie publikuj surowych PDF-ów automatycznie.

## Statusy

- `quality_status=extracted`: tekst uzyskano; nie oznacza to 100% zgodności wizualnej.
- `quality_status=review_required`: co najmniej jedna strona wymaga sprawdzenia.
- `fact_check_status=unverified_source_material`: twierdzenia z dokumentu nie zostały niezależnie potwierdzone.

## Zakres obecnej implementacji

To pipeline ekstrakcji i indeksowania, a nie pełny system analizy dowodów. Rozpoznawanie przypisów, grafów powiązań, ekstrakcja twierdzeń i niezależna weryfikacja źródeł wymagają oddzielnego procesu badawczego.
