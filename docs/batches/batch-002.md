# Raport roboczy — batch-002

Data: 2026-11-10.

**Stan: częściowo przygotowane, bez kanonicznego importu PDF.**

W bieżącej sesji udostępniono czytelne podglądy tekstowe pięciu załączników: `turn108file5`–`turn108file9`, po 3 strony każdy (**15 stron**). Pełne transkrypcje tych pięciu załączników zapisano w `corpus/staging/batch-002/`, z osobnym rekordem i plikami dla każdej strony.

Nie były dostępne bajty oryginalnych PDF-ów. W konsekwencji nie można rzetelnie wyliczyć SHA-256 źródeł, porównać identyczności plików binarnych ani potwierdzić nazw. Nie dopisano ich do kanonicznego `corpus/index.jsonl` ani `corpus/receipts.jsonl`.

## Wykaz

| Slot | Referencja | Temat | Strony | Relacja |
|---|---|---|---:|---|
| 06 | `turn108file5` | Annopol | 3 | podgląd zgodny z tekstem partii 001 |
| 07 | `turn108file6` | Annopol | 3 | podgląd zgodny z tekstem partii 001 |
| 08 | `turn108file7` | Łęczna: Lubelskie Imperium Inwigilacji | 3 | odrębny tekst |
| 09 | `turn108file8` | Łęczna: Folwark na Jaśminowej | 3 | odrębny tekst |
| 10 | `turn108file9` | Łęczna: Folwark na Jaśminowej | 3 | ten sam podgląd co slot 09 |

Pozostałych pięciu pozycji (sloty 01–05) nie udało się odczytać w tej sesji; nie przypisano im treści, liczby stron ani hashy.

## Ograniczenia

- Status wszystkich pięciu załączników: `awaiting_binary_pdf`.
- Status wszystkich twierdzeń: `unverified_source_material`.
- Zgodność tekstowa nie dowodzi identyczności plików PDF.
- Po pozyskaniu oryginałów wymagana jest weryfikacja transkrypcji i rzeczywistego SHA-256.
