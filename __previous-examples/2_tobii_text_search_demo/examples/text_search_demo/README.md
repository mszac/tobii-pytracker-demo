# Text Search Demo — tobii-pytracker (`psychopy`)

Demo pokazuje wykorzystanie `tobii-pytracker` do badania **wyszukiwania konkretnej
informacji w krótkim tekście**.

Uczestnik widzi pytanie i tekst, odnajduje odpowiednią informację, a następnie
wybiera:

```text
TAK | NIE | NIE WIEM
```

Projekt nie zawiera żadnych plików ani skryptów MouseGaze.

---

## 1. Gdzie skopiować pliki

Ta paczka jest overlayem na checkout:

```text
tobii-pytracker/
```

Po skopiowaniu struktura powinna wyglądać:

```text
tobii-pytracker/
├── configs/
│   ├── config.yaml
│   ├── config_text_search_demo.yaml      # demo
│   └── eyetracker_config.yaml            # oryginalny plik repozytorium
│
├── datasets/
│   ├── text_search_demo.csv              # demo
│   └── text_search_length_report.csv
│
├── examples/
│   └── text_search_demo/
│       ├── README.md
│       ├── EXPERIMENT.md
│       ├── analyze_results.py
│       ├── apply_repo_fixes.py
│       ├── run_tobii.bat
│       ├── run_tobii.sh
│       ├── analyze.bat
│       └── analyze.sh
│
└── output/
    └── text_search_demo/
        └── <timestamp>/
            └── data.csv
```

**Nie podmieniaj oficjalnego `configs/eyetracker_config.yaml`.**
Demo używa konfiguracji Tobii dostarczanej przez branch `psychopy`.

---

## 2. Poprawki źródłowe do forka

Aktualny `TextDataset` dopisuje klasę `none`, dlatego bez poprawki GUI pokazuje
przycisk `NONE`.

Aktualny `CustomConfig` otwiera też YAML bez jawnego `encoding="utf-8"`.

Jeżeli nie masz jeszcze tych zmian w swoim forku, uruchom **przed pierwszym
`pip install .`**:

```bash
python examples/text_search_demo/apply_repo_fixes.py
```

Skrypt zmieni:

```python
# src/tobii_pytracker/configs/custom_config.py
with open(filename, "r", encoding="utf-8") as f:
```

oraz:

```python
# src/tobii_pytracker/datasets/custom_dataset.py
df = pd.read_csv(self.dataset_path, header=0, encoding="utf-8")
self.classes.append("nie wiem")
```

Następnie:

```bash
git diff
```

Jeżeli budujesz własny fork, **commituj te zmiany do forka**. Wtedy po przyszłym
`git clone` użytkownik nie musi wykonywać patchera.

Jeżeli jest to pierwsza instalacja repozytorium:

```bash
pip install .
```

nie wymaga później reinstalacji, ponieważ poprawiony kod zostanie zainstalowany
od razu.

---

## 3. Config eksperymentu

Demo używa jednego pliku:

```text
configs/config_text_search_demo.yaml
```

Kluczowa sekcja:

```yaml
dataset:
  text:
    label_column_name: answer
    text_column_name: selected_text
    bbox_model: word
    font_height: 35
    wrap_fraction: 0.95
    path: datasets/text_search_demo.csv
```

`bbox_model: word` pozwala otrzymać bounding boxy poszczególnych słów.

---

## 4. Ustaw monitor

Przed uruchomieniem zmień w:

```text
configs/config_text_search_demo.yaml
```

parametry na zgodne ze stanowiskiem:

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

- `resolution` — rzeczywista rozdzielczość ekranu,
- `width` — fizyczna szerokość monitora w cm,
- `distance` — odległość oczu od ekranu w cm,
- `display_number` — numer monitora używanego do eksperymentu.

---

## 5. Dataset

Plik:

```text
datasets/text_search_demo.csv
```

zawiera 12 prób.

Balans:

| condition | TAK | NIE | razem |
|---|---:|---:|---:|
| EARLY | 3 | 3 | 6 |
| LATE | 3 | 3 | 6 |

Najważniejsze kolumny:

| kolumna | znaczenie |
|---|---|
| `item_id` | identyfikator bodźca |
| `topic` | temat |
| `condition` | EARLY / LATE |
| `answer` | poprawna odpowiedź |
| `critical_phrase` | informacja kluczowa |
| `question` | pytanie |
| `text_body` | właściwy tekst |
| `text_word_count` | długość tekstu |
| `selected_text` | tekst przekazany do TextDataset |

CSV jest zapisany jako **UTF-8 bez BOM**.

---

## 6. Najpierw możesz sprawdzić samo GUI

Bez eye trackera:

```bash
tobii-pytracker --config_file configs/config_text_search_demo.yaml --loop_count 2
```

To pozwala sprawdzić:

- polskie znaki,
- układ tekstu,
- przyciski,
- dataset,
- główny config.

Po poprawce źródłowej przyciski powinny mieć etykiety:

```text
TAK
NIE
NIE WIEM
```

---

## 7. Uruchomienie z Tobii

Podłącz eye tracker.

Z katalogu głównego repozytorium:

```bash
tobii-pytracker --config_file configs/config_text_search_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 12
```

Na Windows możesz też uruchomić:

```text
examples/text_search_demo/run_tobii.bat
```

Na Linux/macOS:

```bash
bash examples/text_search_demo/run_tobii.sh
```

Uruchomienie z `--enable_eyetracker` wymaga podłączonego urządzenia.

---

## 8. Przebieg próby

Każda próba:

```text
punkt fiksacji
      ↓
PYTANIE + TEKST
      ↓
uczestnik szuka informacji
      ↓
TAK / NIE / NIE WIEM
      ↓
zapis data.csv
```

Informacja kluczowa występuje:

```text
EARLY → w pierwszym zdaniu tekstu
LATE  → w ostatnim zdaniu tekstu
```

---

## 9. Dane wyjściowe tobii-pytracker

Config zapisuje dane do:

```text
output/text_search_demo/
```

Każda sesja dostaje osobny katalog:

```text
output/text_search_demo/
└── YYYYMMDD_HHMMSS/
    ├── data.csv
    └── ... screenshoty bodźców ...
```

Aktualny tryb PsychoPy zapisuje w `data.csv`:

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

Plik jest rozdzielany średnikami.

---

## 10. Analiza

Po wykonaniu co najmniej jednej sesji:

```bash
python examples/text_search_demo/analyze_results.py
```

Windows:

```text
examples/text_search_demo/analyze.bat
```

Linux/macOS:

```bash
bash examples/text_search_demo/analyze.sh
```

Analizowane są wszystkie:

```text
output/text_search_demo/*/data.csv
```

---

## 11. Jak działa analiza

```text
gaze_data
   ↓
detekcja fiksacji I-DT
   ↓
objects_bboxes["words"]
   ↓
critical_phrase
   ↓
TARGET AOI
   ↓
TTFF / dwell / fixation count
```

Fraza targetu jest wyszukiwana **wyłącznie po markerze `TEKST:`**, dzięki czemu
podobne słowa znajdujące się w pytaniu nie zostaną błędnie uznane za target.

---

## 12. Wyniki

Powstanie katalog:

```text
examples/text_search_demo/results/
```

z plikami:

```text
trial_metrics.csv
condition_summary.csv
01_ttff_target.png
02_fixations_before_target.png
03_target_dwell.png
04_accuracy_by_target_seen.png
hypothesis_summary.txt
```

---

## 13. Najważniejsze metryki

### `target_seen`

Czy co najmniej jedna wykryta fiksacja trafiła w `critical_phrase`.

### `ttff_target_s`

Time to First Fixation — czas od pierwszej zapisanej próbki gaze do pierwszej
fiksacji na informacji kluczowej.

Główna hipoteza:

```text
EARLY < LATE
```

### `fixations_before_target`

Liczba wykrytych fiksacji przed pierwszym wejściem na target.

Oczekiwanie:

```text
EARLY < LATE
```

### `target_dwell_s`

Suma czasu fiksacji na informacji kluczowej.

### `target_fixation_count`

Liczba fiksacji na informacji kluczowej.

### `correct`

Czy `user_classification` jest zgodne z `classification`.

Odpowiedź `NIE WIEM` jest automatycznie traktowana jako niepoprawna, ponieważ
żaden bodziec nie ma jej jako poprawnej klasy.

---

## 14. Hipotezy

### H1

Informacja kluczowa będzie wzrokowo odwiedzana:

```text
target_seen_rate → wysoki
```

### H2

Informacja umieszczona wcześniej zostanie odnaleziona szybciej:

```text
TTFF EARLY < TTFF LATE
fixations_before_target EARLY < LATE
```

### H3

Próby z fiksacją na informacji kluczowej powinny mieć większą poprawność:

```text
accuracy(target_seen=True) > accuracy(target_seen=False)
```

---

## 15. Co pokazać podczas prezentacji

Wystarczą cztery elementy:

1. **Przykładowy bodziec** — pytanie + regulamin/instrukcja.
2. **Word bounding boxes / critical phrase** — wyjaśnienie, jak tworzony jest target AOI.
3. **`01_ttff_target.png`** — EARLY vs LATE.
4. **`02_fixations_before_target.png`** i **`04_accuracy_by_target_seen.png`**.

Główna narracja:

> Samo TAK/NIE mówi, czy użytkownik odpowiedział poprawnie. Eye tracking pokazuje
> dodatkowo, **czy trafił do właściwej informacji, jak szybko ją znalazł i ile
> tekstu musiał wcześniej przeskanować**.

---

## 16. Ważna uwaga o fiksacjach

`analyze_results.py` zawiera prosty detektor I-DT, aby demo było samowystarczalne.

Domyślne parametry:

```text
dispersion threshold = 50 px
minimum fixation duration = 0.10 s
```

Można je zmienić:

```bash
python examples/text_search_demo/analyze_results.py --dispersion-threshold 60 --min-fixation-duration 0.12
```

Do właściwego badania naukowego parametry powinny być z góry ustalone i
dopasowane do trackera, częstotliwości próbkowania i procedury analitycznej.

---

## 17. Szybki workflow

```bash
# 1. Jednorazowo, przed pierwszą instalacją forka, jeśli poprawki nie są jeszcze w kodzie:
python examples/text_search_demo/apply_repo_fixes.py

# 2. Pierwsza instalacja:
pip install .

# 3. Test GUI:
tobii-pytracker --config_file configs/config_text_search_demo.yaml --loop_count 2

# 4. Pełne demo z Tobii:
tobii-pytracker --config_file configs/config_text_search_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 12

# 5. Analiza:
python examples/text_search_demo/analyze_results.py
```

---

## 18. Ograniczenie metodologiczne

W tym demo każdy bodziec występuje tylko w jednej pozycji, więc `EARLY/LATE`
jest częściowo powiązane z treścią itemu. To jest akceptowalne dla demonstracji
technicznego workflow.

W badaniu właściwym należałoby przygotować kontrbalansowane wersje, w których
ten sam item występuje jako EARLY u części uczestników i LATE u pozostałych.
