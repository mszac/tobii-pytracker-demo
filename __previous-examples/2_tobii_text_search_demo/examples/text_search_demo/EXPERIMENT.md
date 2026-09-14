# Demo: wyszukiwanie konkretnej informacji w krótkim tekście

## Cel

Uczestnik otrzymuje pytanie oraz krótki tekst przypominający regulamin, FAQ,
instrukcję lub komunikat użytkowy. Zadaniem jest odnalezienie informacji
potrzebnej do odpowiedzi **TAK / NIE / NIE WIEM**.

Celem jest sprawdzenie, **jak szybko użytkownik trafia wzrokiem do właściwego
fragmentu tekstu oraz jak wygląda strategia skanowania przed jego odnalezieniem**.

## Manipulacja

Dataset ma 12 unikalnych prób:

- 6 × `EARLY` — informacja kluczowa znajduje się w pierwszym zdaniu tekstu,
- 6 × `LATE` — informacja kluczowa znajduje się w ostatnim zdaniu tekstu.

W każdej kondycji znajdują się:

- 3 poprawne odpowiedzi `TAK`,
- 3 poprawne odpowiedzi `NIE`.

`NIE WIEM` jest dodatkową możliwością odpowiedzi uczestnika, ale nie jest
poprawną klasą żadnego bodźca.

## Hipotezy

### H1 — informacja kluczowa przyciąga uwagę

Uczestnicy będą wykonywać fiksacje na fragmencie zawierającym odpowiedź.

Metryki:

- `target_seen`,
- `target_fixation_count`,
- `target_dwell_s`,
- `target_dwell_share`.

### H2 — położenie wpływa na szybkość odnalezienia

Informacja `EARLY` będzie odnajdywana szybciej niż `LATE`.

Metryki:

- `ttff_target_s`,
- `fixations_before_target`.

Oczekiwany kierunek:

```text
TTFF: EARLY < LATE
fiksacje przed targetem: EARLY < LATE
```

### H3 — dotarcie wzroku do targetu wiąże się z poprawnością

Próby, w których `target_seen=True`, powinny częściej kończyć się poprawną
odpowiedzią niż próby bez wykrytej fiksacji na informacji kluczowej.

## AOI

Config używa:

```yaml
bbox_model: word
```

`tobii-pytracker` zapisuje bounding boxy słów w `objects_bboxes`.
Kolumna `critical_phrase` określa sekwencję słów tworzących target AOI.

## Dlaczego bodźce nie zawierają ręcznych nowych linii

W aktualnym `TextDataset` tekst jest renderowany przez PsychoPy, a bounding boxy
słów są następnie obliczane przez ponowne zawijanie słów. Aby obraz bodźca i
word bounding boxes pozostały maksymalnie zgodne, `selected_text` jest jednym
akapitowym ciągiem:

```text
PYTANIE: ... TEKST: ...
```

PsychoPy sam zawija go zgodnie z `wrap_fraction`.

## Ograniczenia

To jest demonstracja workflow, nie pełny protokół badania naukowego. W badaniu
właściwym należy m.in. zwiększyć liczbę itemów i uczestników, zastosować
kontrbalansowanie pozycji tej samej informacji pomiędzy uczestnikami oraz
zaplanować analizę inferencyjną.
