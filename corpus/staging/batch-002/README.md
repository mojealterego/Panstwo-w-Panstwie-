# Partia 002 — tymczasowe transkrypcje z rozmowy

Ten katalog **nie jest kanonicznym importem PDF**. W tej sesji dostępny był tekst pięciu załączników (referencje `turn108file5`–`turn108file9`), ale nie bajty oryginalnych PDF-ów. Dlatego **nie ma** tu SHA-256 plików binarnych, ich oryginalnych nazw ani identyfikatorów `pdf-<sha256>`. Nie wolno wnioskować o tożsamości plików z samego podobieństwa tekstu.

## Zawartość

- `slot-06`, `slot-07`: dwa oddzielne załączniki o treści zgodnej z transkrypcją Annopola z partii 001; kopie tekstu zachowano osobno.
- `slot-08`: Łęczna, „Lubelskie Imperium Inwigilacji”; trzy strony.
- `slot-09`: Łęczna, „Folwark na Jaśminowej”; trzy strony.
- `slot-10`: kolejny załącznik o tym samym widocznym tekście co `slot-09`; zachowany osobno.

Dla wszystkich pięciu załączników zapisano `document.md`, `document.txt`, `pages/0001.md`–`0003.md`, `metadata.json`. Granice stron pochodzą z podglądów rozmowy. Dokumenty zawierają **niezweryfikowane twierdzenia i zarzuty**; ich publikacja nie potwierdza prawdziwości.

## Przeniesienie do korpusu kanonicznego

Po uzyskaniu bajtów PDF uruchomić `pwp-ingest` z `--batch-id batch-002`, porównać każdą stronę z transkrypcją tymczasową, przypisać rzeczywiste sumy SHA-256, a dopiero potem uznać import za ukończony. Nie usuwać rekordów przyjęcia tylko dlatego, że teksty są takie same.

Pięć wcześniejszych pozycji potencjalnej partii (sloty 01–05) nie zostało odczytanych w dostępnej sesji i nie zostało tu zmyślonych ani oznaczonych jako przetworzone.
