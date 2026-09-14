# tobii_text_search_demo

Minimalny projekt demonstracyjny dla **tobii-pytracker**:
wyszukiwanie konkretnej informacji w krótkim tekście.

## 1. Struktura katalogów

```text
tobii_text_search_demo/
├── README.md
├── EXPERIMENT.md
├── configs/
│   ├── config_text_search.yaml
│   ├── mouse_eyetracker_config.yaml
│   └── eyetracker_config.yaml
├── datasets/
│   └── text_search.csv
├── analysis/
│   └── analyze_results.py
├── output/          # tutaj tobii-pytracker zapisze sesje
└── results/         # tutaj powstaną tabele i wykresy
```

**Wszystkie komendy uruchamiaj z katalogu `tobii_text_search_demo/`.**
Ścieżki w YAML są względne wobec tego katalogu.

## 2. Instalacja

Zalecane środowisko: **Python 3.10**.

Przykład z Condą:

```bash
conda create -n pytracker-text python=3.10
conda activate pytracker-text
pip install tobii-pytracker
pip install "psychopy>=2024.1.4,<2025.1.0" --no-deps
pip install pandas numpy matplotlib
```

Jeżeli wersja z PyPI nie obsługuje konfiguracji `dataset.text`, zainstaluj
aktualną wersję repozytorium zgodnie z instrukcją dokumentacji projektu.

## 3. Przed pierwszym uruchomieniem

Otwórz:

`configs/config_text_search.yaml`

i ustaw parametry swojego stanowiska:

```yaml
resolution: [1920, 1080]   # rzeczywista rozdzielczość
width: 53                  # fizyczna szerokość monitora w cm
distance: 60               # odległość oczu od monitora w cm
display_number: 0
```

Nie zmieniaj nazw kolumn `answer` i `selected_text`, jeśli nie aktualizujesz
również konfiguracji.

## 4. Test bez Tobii – emulator myszy

Uruchom:

```bash
tobii-pytracker   --config_file configs/config_text_search.yaml   --eyetracker_config_file configs/mouse_eyetracker_config.yaml   --enable_eyetracker   --loop_count 12
```

W emulatorze przytrzymanie **prawego przycisku myszy i ruch myszy**
symuluje zmianę pozycji gaze. Zwykły ruch kursora bez przycisku nie zapisuje gaze.

Po zakończeniu powstanie katalog podobny do:

```text
output/
└── 20260908_180000/
    ├── data.csv
    └── ... screenshoty ...
```

## 5. Eksperyment z fizycznym Tobii

Podłącz tracker i uruchom:

```bash
tobii-pytracker   --config_file configs/config_text_search.yaml   --eyetracker_config_file configs/eyetracker_config.yaml   --enable_eyetracker   --loop_count 12
```

Plik `configs/eyetracker_config.yaml` jest minimalną konfiguracją przykładową.
Jeżeli dany model Tobii wymaga innych ustawień lub częstotliwości próbkowania,
zastąp go oficjalnym `configs/eyetracker_config.yaml` z używanej wersji
`tobii-pytracker` i dostosuj do sprzętu.

## 6. Analiza wyników

Po zebraniu co najmniej jednej sesji:

```bash
python analysis/analyze_results.py
```

Skrypt automatycznie analizuje wszystkie katalogi `output/*/data.csv`.

Powstaną:

```text
results/
├── trial_metrics.csv
├── condition_summary.csv
├── hypothesis_summary.txt
├── ttff_by_condition.png
├── accuracy_by_target_seen.png
└── example_trial_gaze.png       # jeśli screenshot został odnaleziony
```

### Najważniejsze kolumny `trial_metrics.csv`

- `correct` – poprawność odpowiedzi,
- `target_seen` – czy fiksacja trafiła na informację kluczową,
- `ttff_target_s` – czas do pierwszej fiksacji na informacji,
- `target_dwell_s` – łączny czas fiksacji na informacji,
- `target_fixation_count` – liczba fiksacji na informacji,
- `fixations_before_target` – liczba fiksacji przed dotarciem do targetu.

## 7. Jak zaprezentować wynik

Wystarczą 4 elementy:

1. **Stimulus + gaze plot** – `example_trial_gaze.png`.
2. **H1:** pokaż `target_seen_rate` oraz `mean_target_dwell_s`.
3. **H2:** pokaż `ttff_by_condition.png`; oczekiwanie: EARLY < LATE.
4. **H3:** pokaż `accuracy_by_target_seen.png`; oczekiwanie: większa
   poprawność po fiksacji na informacji kluczowej.

`condition_summary.csv` można wkleić bezpośrednio do prezentacji jako tabelę.

## 8. Ważna uwaga metodologiczna

To jest **demo workflow**, a nie gotowy protokół do wnioskowania
statystycznego. Przy badaniu właściwym należy zwiększyć liczbę prób i
uczestników, randomizować/kontrować kolejność bodźców oraz zaplanować
model statystyczny z uwzględnieniem uczestnika i itemu.

## 9. Jeśli pojawi się dodatkowy przycisk `none`

Niektóre wersje `TextDataset` mogą dodawać klasę `none`. W tym eksperymencie
uczestnik powinien wybierać wyłącznie **TAK** albo **NIE**.
