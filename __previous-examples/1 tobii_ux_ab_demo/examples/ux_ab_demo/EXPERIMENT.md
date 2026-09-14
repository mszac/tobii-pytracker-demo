# UX A/B demo — opis eksperymentu

## Cel

Porównanie dwóch sposobów formułowania komunikatów UX:

- **A_FORMAL** — język bardziej formalny i mniej bezpośredni,
- **B_SIMPLE** — język prostszy i bardziej bezpośredni.

Główne pytanie:

> Czy prostszy komunikat wymaga mniej pracy wzrokowej przy zachowaniu poprawnego zrozumienia?

## Bodźce

Dataset zawiera 8 par komunikatów, czyli 16 prób. Każda para opisuje tę samą sytuację
i ma identyczną liczbę słów w wariancie formalnym i prostym.

Tematy: płatność, hasło, formularz, sieć, plik, cookies, dostawa, konto.

Każdy bodziec zawiera:

1. `KOMUNIKAT`,
2. `PYTANIE`,
3. odpowiedź uczestnika `TAK` / `NIE`.

## Hipotezy

- **H1:** B_SIMPLE będzie miał niższy `message_dwell_s`.
- **H2:** B_SIMPLE będzie miał mniej `message_fixation_count`.
- **H3:** B_SIMPLE będzie miał mniej `regression_count`.
- **H4:** B_SIMPLE osiągnie podobną lub wyższą `accuracy`.
- **H5:** B_SIMPLE będzie miał krótszy `ttff_action_s`.

## AOI

Główny config używa:

```yaml
bbox_model: word
```

`tobii-pytracker` zapisuje bounding boxy słów w `objects_bboxes`.
Skrypt analityczny wykorzystuje kolumnę `action_phrase` z datasetu do utworzenia
logicznego AOI odpowiadającego instrukcji działania.

## Uwaga metodologiczna

Ten projekt jest **demo**, dlatego jedna sesja pokazuje oba warianty każdej sytuacji.
Do właściwego eksperymentu naukowego lepszy będzie schemat międzygrupowy lub
kontrbalansowany, tak aby uczestnik nie widział obu wariantów tego samego itemu.
Kontrbalansowanie należy wtedy przygotować na poziomie procedury badania lub osobnych
datasetów, ale nie wymaga ono tworzenia dwóch głównych plików konfiguracyjnych.
