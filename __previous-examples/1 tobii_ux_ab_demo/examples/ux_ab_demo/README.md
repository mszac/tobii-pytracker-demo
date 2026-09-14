# UX A/B demo dla tobii-pytracker (`psychopy`)

Ta paczka jest przygotowana jako **overlay na oficjalne repozytorium**
`tobii-pytracker`, branch `psychopy`.

Nie zawiera własnych wersji:

```text
configs/eyetracker_config.yaml
configs/mouse_eyetracker_config.yaml
```

ponieważ te pliki są już częścią repozytorium i powinny pozostać zgodne z
wersją `tobii-pytracker`, którą uruchamiasz.

## 1. Docelowa struktura po skopiowaniu do repozytorium

```text
tobii-pytracker/
├── configs/
│   ├── config.yaml                       # oryginalny config repo
│   ├── config_ux_ab_demo.yaml            # TEN DEMO
│   ├── eyetracker_config.yaml            # oryginalny plik repo
│   └── mouse_eyetracker_config.yaml      # oryginalny plik repo
│
├── datasets/
│   ├── ux_ab_demo.csv                    # TEN DEMO
│   └── ux_ab_length_report.csv
│
├── examples/
│   └── ux_ab_demo/
│       ├── README.md
│       ├── EXPERIMENT.md
│       ├── analyze_results.py
│       ├── run_mouse.bat
│       ├── run_tobii.bat
│       ├── run_mouse.sh
│       ├── run_tobii.sh
│       ├── analyze.bat
│       └── analyze.sh
│
└── output/
    └── ux_ab_demo/
        └── <timestamp>/
            └── data.csv
```

## 2. Co jest zgodne z aktualną dokumentacją

Demo ma **jeden główny config**:

```text
configs/config_ux_ab_demo.yaml
```

i dokładnie jeden aktywny typ datasetu:

```yaml
dataset:
  text:
    label_column_name: answer
    text_column_name: selected_text
    color: white
    background_color: black
    bbox_model: word
    path: datasets/ux_ab_demo.csv
```

Eye tracker jest wybierany osobnym argumentem CLI:

```text
--eyetracker_config_file configs/...
```

Czyli nie tworzymy osobnego głównego configu dla myszy i osobnego dla Tobii.

## 3. Instalacja

Z katalogu nadrzędnego:

```bash
git clone --branch psychopy https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
```

Następnie skopiuj zawartość tej paczki do katalogu repozytorium tak, aby
`configs/`, `datasets/` i `examples/` zostały scalone z istniejącymi katalogami.

Utwórz środowisko zgodne z repozytorium:

```bash
conda create --name pytracker-env python=3.10
conda activate pytracker-env
pip install .
pip install "psychopy>=2024.1.4,<2025.1.0" --no-deps
pip install pandas numpy matplotlib
```

## 4. Przed uruchomieniem — monitor

W:

```text
configs/config_ux_ab_demo.yaml
```

ustaw rzeczywiste parametry stanowiska:

```yaml
display:
  monitor:
    resolution:
      - 2560
      - 1440
    width: 35
    distance: 60
    display_number: 0
```

`resolution` oznacza rozdzielczość w pikselach, `width` szerokość monitora w cm,
a `distance` odległość uczestnika od ekranu w cm.

## 5. Najpierw sprawdź samo GUI bez eye trackera

Z katalogu głównego `tobii-pytracker`:

```bash
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --loop_count 16
```

To jest najlepszy pierwszy test, ponieważ eliminuje problemy z ioHub i sprzętem.

Powinieneś zobaczyć tekst oraz przyciski odpowiedzi.


## 6. Emulator myszy

Używamy **oryginalnego** pliku repozytorium:

```text
configs/mouse_eyetracker_config.yaml
```

Uruchom z katalogu głównego repo:

```bash
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --eyetracker_config_file configs/mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 16
```

W oficjalnej konfiguracji MouseGaze ruch gaze jest generowany przy użyciu
przycisku skonfigurowanego jako `controls.move` — domyślnie `RIGHT_BUTTON`.

## 7. Fizyczny Tobii

Używamy **oryginalnego**:

```text
configs/eyetracker_config.yaml
```

Uruchom:

```bash
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 16
```

Nie modyfikuj tego pliku bez potrzeby. Jeżeli konkretny model Tobii wymaga innej
częstotliwości próbkowania, zmień tylko ustawienia wymagane przez urządzenie.

## 8. Gdzie zapisują się dane

Config ma:

```yaml
output:
  folder: output/ux_ab_demo
```

`tobii-pytracker` doda katalog sesji:

```text
output/ux_ab_demo/
└── YYYYMMDD_HHMMSS/
    ├── data.csv
    └── ...
```

W trybie PsychoPy `data.csv` jest plikiem rozdzielanym średnikami i zawiera:

```text
screenshot_file
input_data
classification
user_classification
gaze_data
objects_bboxes
voice_file
voice_start_timestamp
```

## 9. Dataset

```text
datasets/ux_ab_demo.csv
```

zawiera 16 prób:

```text
8 × A_FORMAL
8 × B_SIMPLE
```

Każdy item występuje w obu wersjach. W każdej parze liczba słów w samym
komunikacie jest identyczna.

Dodatkowa tabela kontrolna:

```text
datasets/ux_ab_length_report.csv
```

## 10. Analiza

Po wykonaniu co najmniej jednej sesji:

```bash
python examples/ux_ab_demo/analyze_results.py
```

Skrypt czyta:

```text
output/ux_ab_demo/*/data.csv
```

i tworzy:

```text
examples/ux_ab_demo/results/
├── trial_metrics.csv
├── version_summary.csv
├── 01_message_dwell.png
├── 02_fixation_count.png
├── 03_regressions.png
└── 04_ttff_action.png
```

## 11. Główne metryki

- `message_dwell_s` — suma czasu fiksacji przypisanych do słów komunikatu;
- `message_fixation_count` — liczba fiksacji na komunikacie;
- `regression_count` — liczba przejść do słowa położonego co najmniej dwa słowa wcześniej;
- `ttff_action_s` — czas od pierwszej zarejestrowanej próbki gaze do pierwszej fiksacji na instrukcji działania;
- `action_dwell_s` — dwell time na instrukcji działania;
- `correct` — zgodność `user_classification` z `classification`.

## 12. Oczekiwany wzorzec

Hipotezy demonstracyjne:

```text
B_SIMPLE < A_FORMAL  dla message_dwell_s
B_SIMPLE < A_FORMAL  dla message_fixation_count
B_SIMPLE < A_FORMAL  dla regression_count
B_SIMPLE < A_FORMAL  dla ttff_action_s
B_SIMPLE >= A_FORMAL dla accuracy
```

Nie są to wyniki — to kierunek hipotez, który trzeba sprawdzić na danych.

## 13. Najczęstsze problemy

### `Configuration file ... not found`

Uruchamiaj polecenia z katalogu głównego repozytorium `tobii-pytracker`.

### Dataset nie został znaleziony

Config zawiera ścieżkę względną:

```text
datasets/ux_ab_demo.csv
```

Dlatego bieżącym katalogiem musi być root repozytorium.

### GUI działa, ale eye tracker nie

Jeżeli:

```bash
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --loop_count 16
```

działa, a wersja z `--enable_eyetracker` nie działa, problem dotyczy konfiguracji
ioHub / PsychoPy / urządzenia, a nie datasetu lub głównego configu.

### `objects_bboxes` jest puste

Sprawdź, czy używasz brancha `psychopy` zgodnego z aktualnym `TextDataset`
i czy w configu jest:

```yaml
bbox_model: word
```

### Brak danych gaze w emulatorze

W oficjalnym pliku `mouse_eyetracker_config.yaml` MouseGaze zapisuje zmianę
pozycji podczas używania przycisku `controls.move` (domyślnie prawy przycisk).

## 14. Szybki test poprawności

Wykonuj po kolei:

```bash
# 1. Czy config + dataset działają?
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --loop_count 2

# 2. Czy działa MouseGaze?
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --eyetracker_config_file configs/mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 2

# 3. Pełne demo
tobii-pytracker --config_file configs/config_ux_ab_demo.yaml --eyetracker_config_file configs/mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 16

# 4. Analiza
python examples/ux_ab_demo/analyze_results.py
```

Jeżeli krok 1 nie działa, problem jest w głównym configu / datasecie / instalacji.
Jeżeli krok 1 działa, a krok 2 nie, problem jest po stronie ioHub / PsychoPy / konfiguracji trackera.

## Poprawka dla polskich znaków i przycisku `none`

Branch `psychopy` w `CustomConfig.read_config()` otwiera obecnie YAML przez
zwykłe `open(filename, "r")`. Na Windows oznacza to zależność od systemowego
kodowania tekstu. Dlatego demo stosuje dwie warstwy zabezpieczenia:

1. `configs/config_ux_ab_demo.yaml` jest plikiem ASCII, a polskie znaki w
   instrukcjach zapisano jako standardowe sekwencje YAML `\uXXXX`.
   `yaml.safe_load()` zamienia je na prawidłowe Unicode.
2. Do forka warto zastosować poprawkę źródłową, aby wszystkie pliki YAML były
   zawsze czytane jako UTF-8.

Dodatkowo `TextDataset` na branchu `psychopy` dopisuje klasę:

```python
self.classes.append("none")
```

To właśnie dlatego GUI pokazuje przycisk `NONE`. Nie jest on tworzony przez
dataset CSV ani przez `config_ux_ab_demo.yaml`.

### Zastosowanie poprawek do forka

Po skopiowaniu plików demo do repozytorium uruchom z katalogu głównego:

```bash
python examples/ux_ab_demo/apply_demo_source_patch.py
```

Skrypt wprowadza:

```python
# src/tobii_pytracker/configs/custom_config.py
with open(filename, "r", encoding="utf-8") as f:
```

oraz:

```python
# src/tobii_pytracker/datasets/custom_dataset.py
self.classes.append("nie wiem")
```

Następnie:

```bash
git diff
pip install -e .
```

Po zmianie przyciski dla tekstowego datasetu będą:

```text
TAK
NIE
NIE WIEM
```

Kliknięcie `NIE WIEM` zostanie zapisane w `user_classification` jako
`nie wiem`, co jest spójne z aktualnym mechanizmem GUI.

Jeżeli tworzysz własny fork, te dwie zmiany najlepiej **commitować do forka**.
Wtedy po kolejnym `git clone` nie trzeba uruchamiać patchera ponownie.
