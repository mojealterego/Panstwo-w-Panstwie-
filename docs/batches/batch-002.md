# Raport przyjęcia — batch-002

Data: 2026-11-10.

**Stan: pięć dostępnych oryginalnych plików PDF zaimportowano kanonicznie; sloty 01–05 pozostają niedostępne.**

## Wynik

- Oryginały PDF: **5**, łącznie **15 stron**; sumy SHA-256 obliczono z oryginalnych bajtów.
- Wcześniej w indeksie: **2** źródła (15 i 16, partia 001); nowe w indeksie: **3** (17, 18, 19).
- Cały korpus: **13** unikatowych plików PDF według SHA-256, **81** unikatowych stron, **15** rekordów przyjęcia.
- Transkrypcje: **15/15 stron** zgodnych znak po znaku z tekstami staging.
- Duplikaty tekstowe w korpusie: **5 par**. Różne hashe PDF zachowują odrębne rekordy.
- Status zarzutów i twierdzeń: `unverified_source_material` (niezweryfikowane).

## Wykaz źródeł

| Slot | Nazwa PDF | SHA-256 | Dokument kanoniczny | Status |
|---|---|---|---|---|
| slot-06 | `Badanie Zespołów Interdyscyplinarnych ds. Przemocy(15).PDF` | `c05be847e9d8021742d2dcd16b91a56d1305ea5da827ca63d299206c5171dd2c` | `pdf-c05be847e9d8021742d2dcd1` | już w partii 001; nowy receipt |
| slot-07 | `Badanie Zespołów Interdyscyplinarnych ds. Przemocy(16).PDF` | `d5c3679c9edde172b32dd104fdfef524d0b2632db3388a26d1b4c4f066543f89` | `pdf-d5c3679c9edde172b32dd104` | już w partii 001; nowy receipt |
| slot-08 | `Badanie Zespołów Interdyscyplinarnych ds. Przemocy(17).PDF` | `6edbf3eec296b875e3cb12cf9e24337bd653c143601657e3df5396819ed21964` | `pdf-6edbf3eec296b875e3cb12cf` | nowy import |
| slot-09 | `Badanie Zespołów Interdyscyplinarnych ds. Przemocy(18).PDF` | `732ee27637b976af87dcd8010d07ba98b9617a65107f264fcc79c3da44d87d53` | `pdf-732ee27637b976af87dcd801` | nowy import |
| slot-10 | `Badanie Zespołów Interdyscyplinarnych ds. Przemocy(19).PDF` | `3c72d41ede3605285e497a06516421de5bf9c277a5c075db52ff1f0c5b726f00` | `pdf-3c72d41ede3605285e497a06` | nowy import |

## Kontrola integralności

Oryginalne PDF-y były dostępne w środowisku lokalnym, w którym obliczono SHA-256. Tekst każdej strony odczytano z załączników i porównano znak po znaku z zapisami tymczasowymi. Wszystkie piętnaście porównań zakończyło się zgodnością. Binarne oryginały nie są publikowane w repozytorium publicznym. Historyczne rekordy staging pozostają zachowane; aktualne przyporządkowanie źródeł zapisano w `corpus/staging/batch-002/resolution.json`.

**Nieprzetworzone:** sloty 01–05, których oryginałów nie ma w dostępnej rozmowie. Nie przypisano im treści ani hashy. Weryfikacja merytoryczna zarzutów nie jest częścią tego importu.
