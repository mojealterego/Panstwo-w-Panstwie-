# Batch 011 — przyjęcie pięciu źródeł PDF

**Wykonano:** 2026-11-10 18:31 UTC. Źródło: oryginalne binaria przesłane w rozmowie. Status wszystkich twierdzeń: `unverified_source_material`.

- Przyjęto **5 PDF-ów (63–67), łącznie 26 stron**. Wszystkie mają różne źródłowe SHA-256.
- Do dodania do indeksu: **5 nowych dokumentów, 26 nowych stron**. Stan po imporcie: **60 dokumentów, 238 stron, 64 rekordy przyjęcia**.
- Przygotowano pełną transkrypcję wszystkich stron, unikatowe identyfikatory SHA-256 i metadane ekstrakcji.
- Oryginały zachowano w ZIP i Bibliotece ChatGPT, **nie publikowano binarnych PDF-ów w GitHub**.
- Zachowano dwie nowe relacje `contained_in`: **PDF (63) → (64)**, **PDF (63) → (66)**. Pełne transkrypcje nadal są odrębne.
- Stwierdzono 9 par dokładnie identycznych stron pomiędzy (63), (64), (66) — patrz `corpus/batches/batch-011-relations.json`.
- PDF (65) i PDF (67) dotyczą zagadnień zawartych częściowo w kompilacji (66), ale **nie spełniły standardowego progu deduplikacji pełnego tekstu**; zapisano je niezależnie.
- Brak wcześniejszych: numer (53) oraz pięć historycznych slotów partii 002.

## Otrzymane materiały

| PDF | Strony | Temat | SHA-256 oryginału |
|---:|---:|---|---|
| 63 | 4 | As You Sow — raport o aktywizmie korporacyjnym i ESG | `5206d071984502a92fc2064acbfd2dad9e76768b18d6e792ed04450d81f71e38` |
| 64 | 7 | As You Sow / Omidyar Group — kompilacja dwóch opracowań | `d38c13a826d8a8f1e25871f1b587dc5db3c50713ac57434ed13cdfc60233b10f` |
| 65 | 3 | Omidyar Group — finansowanie i polityka cyfrowa | `ebd2c8623be89110ae841f5c8f97f941a7b5ae1ec085df6248190c28bf3f7ba2` |
| 66 | 9 | As You Sow / Omidyar / Biuro RPO — kompilacja trzech opracowań | `fcd864fafc99d3d7e1fd345afb07d77aa0c7a07cbbc487b60749732ba8061de8` |
| 67 | 3 | Biuro Rzecznika Praw Obywatelskich — analiza instytucjonalna | `13cd85e13fee2309c0212d472670cd8ffba23f4caccf4da8d76057e26bf47228` |

## Granice dowodowe i bezpieczeństwo publikacji

Dokumenty są **materiałami autorskimi o charakterze polemicznym** i zawierają niezweryfikowane zarzuty wobec rozpoznawalnych podmiotów oraz osób. Samo przyjęcie do korpusu nie potwierdza tych zarzutów ani ich podstawy prawnej. Przed wykorzystaniem w publikacji należy pozyskać źródła pierwotne, uzyskać stanowiska zainteresowanych i wykonać ocenę prawną/redakcyjną. Powtórzony tekst lub połączone pliki nie stanowią niezależnego potwierdzenia informacji.

## Odtwarzalność

Każdy źródłowy PDF ma identyfikator `pdf-<24 hex z SHA-256 surowych bajtów>`. Tekst stron wyodrębniono `page.get_text("text", sort=True).strip()`, scalono podwójną nową linią i zakończono pojedynczym `\n`. Strony numerowane od 1. Ścisłe sumy SHA-256 oryginałów i zawartości archiwum są zawarte w `SHA256SUMS.txt`.
