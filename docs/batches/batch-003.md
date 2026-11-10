# Raport przyjęcia — batch-003

Data: 2026-11-10.

**Zaimportowano 5 oryginalnych PDF-ów (19–23), 16 stron; 4 nowe dokumenty, 1 ponowne wystąpienie źródła.**

## Weryfikacja

- Wszystkie 5 plików odczytano z załączników i policzono SHA-256 z oryginalnych bajtów.
- PDF (19) jest **bajtowo identyczny** z plikiem z batch-002: nie utworzono drugiego dokumentu, dodano osobny rekord przyjęcia do `receipts.jsonl`.
- PDF (20)–(23) zapisano jako **4 nowe źródła** i **13 nowych stron**.
- Łączny stan kanoniczny: **17 dokumentów, 94 strony, 20 rekordów przyjęcia**.
- W korpusie pozostaje **5 wcześniej wykrytych par** duplikatów tekstowych; porównanie nowych transkrypcji z istniejącymi nie wykazało kolejnych relacji `exact_text`, `near_duplicate` ani `contained_in`.
- PDF (22), strona 3: tabelę 4-kolumnową wyodrębniono dodatkowo do `tables/0003.json` i `tables/0003.md`, zachowując oryginalną stronę.
- Oryginalne binaria PDF pozostają poza publicznym repozytorium. Ich SHA-256 i teksty są indeksowane.
- Wszystkie zarzuty, interpretacje i liczby w tekstach źródłowych mają status **niezweryfikowany** (`unverified_source_material`).

## Dokumenty

| PDF | Stron | Identyfikator | Zakres opisany w źródle | Status |
|---|---:|---|---|---|
| (19) | 3 | `pdf-3c72d41ede3605285e497a06` | Łęczna — MOPS i zespół interdyscyplinarny | ponowny receipt |
| (20) | 3 | `pdf-f2a072fac8251030cb9ed0d0` | Lublin — MOPR, finansowanie i organizacje pomocowe | nowy |
| (21) | 3 | `pdf-d19da7a41625d9c33e717910` | Cieszyn — MOPS, Być Razem i dostępność pomocy | nowy |
| (22) | 4 | `pdf-0390036fefba0973ead89ec8` | Fundusz Sprawiedliwości — dotacje i kontrole | nowy |
| (23) | 3 | `pdf-38ee245fda3d978ba9d861bf` | Sejm — nowelizacja przepisów o przemocy domowej | nowy |

## Ograniczenia

Korpus nie stanowi niezależnego potwierdzenia twierdzeń. Stronicowana transkrypcja i osobna tabela służą do cytowania, wyszukiwania i późniejszej kontroli źródeł. Brakujące sloty 01–05 wcześniejszej partii pozostają nieprzetworzone.
