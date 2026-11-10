# Partia 006 — rejestr podglądów, import kanoniczny oczekuje

**Status:** `staging_preview_only`. Dostępne są cztery podglądy załączników o łącznej liczbie **15 stron**. Nie uzyskano bajtów oryginalnych plików PDF ani wiarygodnych sum SHA-256. W konsekwencji **nie dopisano** dokumentów do `corpus/index.jsonl` ani przyjęć do `corpus/receipts.jsonl`; nie utworzono pozornych transkrypcji. Zapisano wyłącznie notatki przypisane do numerów stron, a nie teksty źródłowe.

| Slot | Ref podglądu rozmowy | Strony | Temat | Status |
|---|---|---:|---|---|
| slot-01 | niedostępny | nieustalona | pierwszy załącznik: treść/metadane niewidoczne w narzędziach | oczekuje |
| slot-02 | `turn454file1` | 3 | GREVIO — kompetencje, prawo rodzinne i finansowanie | notatki stron; brak PDF SHA-256 |
| slot-03 | `turn454file2` | 4 | Tetra Pak i rodzina Rausingów — antymonopol, podatki, filantropia | notatki stron; brak PDF SHA-256 |
| slot-04 | `turn454file3` | 4 | FemFund — granty, finanse i programy wsparcia | notatki stron; brak PDF SHA-256 |
| slot-05 | `turn454file4` | 4 | Centrum Praw Kobiet — zarządzanie, spory pracownicze i sprawozdania | notatki stron; brak PDF SHA-256 |

## Zadania przy późniejszym imporcie

1. Uzyskać oryginalne pliki PDF, policzyć SHA-256 z bajtów, odczytać nazwy i liczbę stron; wykryć duplikaty względem całego korpusu.
2. Przeprowadzić PyMuPDF ekstrakcję tekstu 1-based, kontrolę układu i tabel (zwłaszcza FemFund strony 2–3 i Centrum Praw Kobiet strona 3).
3. Porównać wyodrębniony tekst z podglądami, bez utożsamiania streszczeń z transkrypcją; utworzyć `pdf-<sha24>`, metadane, receipts i kanoniczny indeks dopiero po weryfikacji.
4. Zachować oryginały w lokalnym archiwum, bez dodawania PDF do publicznego repozytorium.

## Priorytety fact-checkingu

- **GREVIO:** oryginalny raport o Polsce, przepisy Konwencji Stambulskiej i rozróżnienie rekomendacji od obowiązującego prawa. Wnioski o „dyktowaniu wyroków” nie wynikają automatycznie z raportu.
- **Tetra Pak:** decyzja antymonopolowa Komisji Europejskiej z 1991 r., decyzja chińskiego organu z 2016 r., oficjalne dane dotyczące podatków i darowizn. Nie przypisywać odpowiedzialności osobistej za działania innych członków rodziny.
- **FemFund:** roczne sprawozdania KRS, dokumenty grantowe i przypisy do kosztów finansowych; wykazać lub odrzucić hipotezy o przepływach na podstawie dokumentów, nie spekulacji.
- **Centrum Praw Kobiet:** źródłowe reportaże, stanowisko organizacji, status komisji i postępowań, sprawozdania KRS. Wynik netto nie jest równoznaczny z niewypłacalnością.

Wszystkie zarzuty wobec nazwanych osób i organizacji mają status `unverified_source_material`. Przed publikacją wymagają niezależnego potwierdzenia, prawa do odpowiedzi i przeglądu prawnego. Nie należy publikować danych wrażliwych.

**Stan kanoniczny bez zmian:** 27 unikatowych PDF-ów, 124 strony, 30 rekordów przyjęcia. Nierozwiązane sloty 01–05 partii 002 pozostają bez zmian.
