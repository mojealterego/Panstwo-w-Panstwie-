# Raport przyjęcia — batch-010 (PDF 54–62)

**Dokumenty:** 9 otrzymanych oryginałów PDF, 27 stron, 9 osobnych rekordów przyjęcia. **Nowych unikatowych plików źródłowych (SHA-256): 8**, co dodaje 24 strony do indeksu.

**Integralność:** każdy PDF ma SHA-256 obliczony z bajtów oryginału; transkrypcja PyMuPDF `get_text("text", sort=True)` z normalizacją NFC oraz numeracją stron od 1. Każda strona ma osobny plik Markdown. Oryginały pozostają w archiwum i Bibliotece ChatGPT, poza publicznym GitHub.

## Spis i relacje duplikatów

| PDF | Strony | Id dokumentu | Stan | Tematyka |
|---:|---:|---|---|---|
| 54 | 3 | `pdf-08a147dfeaf21ac51ab0be36` | Identyczny PDF z batch-009; nowy receipt, bez duplikowania indeksu | Narodowy Instytut Wolności (NIW-CRSO) — ponowne przyjęcie identycznych bajtów |
| 55 | 3 | `pdf-9c8fb9bbe4bc15235592ab79` | Nowy PDF | Fundacja Rozwoju Centrum Macierz Polonii — finanse i kontrola dotacji |
| 56 | 3 | `pdf-9091675960665c791df80293` | Nowy PDF | Dyrekcja Generalna ds. Sprawiedliwości (DG JUST), CERV i raporty MCC Brussels |
| 57 | 3 | `pdf-2b8499a2f51fd43a5ca6c0db` | Nowy PDF | Ministerstwo Rodziny, Pracy i Polityki Społecznej — finansowanie programów społecznych |
| 58 | 3 | `pdf-140df6c81fd68a4b601fb823` | Nowy PDF | Fundacja Rozwoju Centrum Macierz Polonii — analiza dotacji i audytów (odrębne opracowanie) |
| 59 | 3 | `pdf-bb17a46b8d9f9ea787a76621` | Nowy PDF | Opiniodawcze Zespoły Sądowych Specjalistów (OZSS) |
| 60 | 3 | `pdf-3b0b51ee7c46fa5536eb2f0e` | Nowy źródłowy PDF; identyczny tekst z PDF 42, ale inne bajty | Open Society Foundations — tekst identyczny z PDF (42), odrębny plik binarny |
| 61 | 3 | `pdf-37254d6527f59b2fd93c25f8` | Nowy PDF | Brave Movement, Together for Girls i kampanie ochrony dzieci |
| 62 | 3 | `pdf-62627771f29ec44a185aa436` | Nowy PDF | Purpose Europe — finansowanie kampanii i aktywizm |

## Deduplicacja i weryfikacja

- **PDF (54):** `SHA-256` jest identyczny z plikiem przyjętym jako batch-009. Zachowano oryginalne bajty i nowy rekord przyjęcia. Nie powstaje drugi kanoniczny dokument.
- **PDF (60) i PDF (42):** tekst wyodrębniony jest identyczny, ale źródłowe bajty PDF mają **różne SHA-256**. Oba zachowują odrębną tożsamość kanoniczną. Dopisano relację `exact_text` do `corpus/duplicates.json`.
- Pozostałe siedem nowych PDF-ów nie wykazało zbieżności ponad progi `exact_text`, `near_duplicate` albo `contained_in` z transkrypcjami z poprzednich pakietów 001–009.

## Uwaga redakcyjna

Wszystkie dziewięć materiałów zawiera oskarżenia lub oceny prawne i polityczne dotyczące rzeczywistych organizacji, instytucji i osób. Przechowywanie źródła **nie jest potwierdzeniem żadnego zarzutu**. Przed publikacją w książce trzeba porównać dokumenty pierwotne, ustalenia audytowe, decyzje, odpowiedzi zainteresowanych i stan postępowań.

Szczególnie sprawdzić: akty NIK i NIW-CRSO (PDF 54,55,58), dokumentację DG JUST/CERV (56), źródła NIK dotyczące MRPiPS (57), akty normatywne i raporty RPO/NIK w sprawie OZSS (59), źródła pierwotne OSF (60), raporty finansowe Brave Movement/Together for Girls i Purpose Europe (61,62).

**Stan korpusu po zatwierdzeniu na GitHub:** 55 kanonicznych dokumentów, 212 stron, 59 rekordów przyjęcia, 6 relacji duplikacji tekstowej. Luki: PDF 53 oraz sloty 01–05 partii 002.
