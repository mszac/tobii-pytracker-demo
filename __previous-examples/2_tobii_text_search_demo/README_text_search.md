# tobii_text_search_demo

## Eksperyment: wyszukiwanie konkretnej informacji w krótkim tekście

Gotowy projekt demonstracyjny dla **tobii-pytracker** pokazujący wykorzystanie
eye-trackingu w zadaniu wyszukiwania informacji w tekście.

Uczestnik otrzymuje krótkie pytanie oraz tekst przypominający fragment
regulaminu, FAQ, instrukcji lub komunikatu użytkowego. Jego zadaniem jest
odnalezienie informacji potrzebnej do udzielenia odpowiedzi **TAK / NIE**.

Przykład:

> **PYTANIE:** Czy klient ma 30 dni na zwrot produktu?  
> **TEKST:** Dostawa standardowa trwa dwa dni robocze. Płatność kartą jest
> dostępna bez dodatkowej opłaty. **Zwrot jest możliwy przez czternaście dni
> od zakupu.**

Poprawna odpowiedź: **NIE**.

Eye tracker pozwala sprawdzić nie tylko, czy odpowiedź była poprawna, ale
również **jak uczestnik szukał informacji, kiedy pierwszy raz skierował na nią
wzrok i ile uwagi jej poświęcił**.

---

# 1. Cel eksperymentu

## Cel ogólny

Zbadanie strategii wzrokowego wyszukiwania konkretnej informacji w krótkim
tekście użytkowym.

Eksperyment odpowiada na pytanie:

> **Czy użytkownik szybko odnajduje fragment tekstu zawierający odpowiedź oraz
> jak położenie tej informacji wpływa na przebieg wyszukiwania?**

## Zastosowanie biznesowe

Taki eksperyment można wykorzystać do oceny m.in.:

- regulaminów sklepów internetowych,
- FAQ,
- opisów usług,
- instrukcji użytkownika,
- polityk zwrotów i reklamacji,
- warunków dostawy,
- formularzy pomocy,
- komunikatów zawierających ważne zasady lub ograniczenia.

W kontekście UX interesuje nas nie tylko to, **czy informacja znajduje się na
stronie**, ale przede wszystkim:

- czy użytkownik ją zauważa,
- jak szybko ją odnajduje,
- ile tekstu musi przeszukać wcześniej,
- czy po odnalezieniu informacji udziela poprawnej odpowiedzi.

## Zastosowanie naukowe

Eksperyment może służyć jako prosty przykład badania:

- alokacji uwagi wzrokowej,
- strategii skanowania tekstu,
- wyszukiwania informacji,
- czasu dotarcia do AOI,
- związku pomiędzy gaze a poprawnością odpowiedzi,
- wpływu pozycji informacji na zachowanie wzrokowe.

---

# 2. Pytanie badawcze

Główne pytanie badawcze:

> **Jak położenie informacji kluczowej w krótkim tekście wpływa na szybkość
> jej odnalezienia i strategię skanowania tekstu?**

Eksperyment porównuje dwie sytuacje:

- **EARLY** – informacja kluczowa znajduje się na początku części `TEKST`,
- **LATE** – informacja kluczowa znajduje się pod koniec części `TEKST`.

Przykład:

### EARLY

> **Zwrot jest możliwy przez trzydzieści dni od zakupu.**  
> Dostawa standardowa trwa dwa dni robocze.  
> Płatność kartą jest dostępna bez dodatkowej opłaty.

### LATE

> Dostawa standardowa trwa dwa dni robocze.  
> Płatność kartą jest dostępna bez dodatkowej opłaty.  
> **Zwrot jest możliwy przez czternaście dni od zakupu.**

---

# 3. Hipotezy

## H1 – uwaga na informację kluczową

> **Uczestnicy będą kierować uwagę wzrokową na fragment zawierający informację
> potrzebną do udzielenia odpowiedzi.**

Oczekujemy, że w większości prób wystąpi co najmniej jedna fiksacja na
informacji kluczowej.

Najważniejsze metryki:

- `target_seen`,
- `target_fixation_count`,
- `target_dwell_s`,
- `target_dwell_share`.

---

## H2 – wpływ pozycji informacji

> **Informacja znajdująca się wcześniej w tekście będzie odnajdywana szybciej
> niż informacja umieszczona pod koniec tekstu.**

Oczekiwany wzorzec:

```text
EARLY → krótszy TTFF
LATE  → dłuższy TTFF
```

Główna metryka:

- `ttff_target_s` – Time to First Fixation na informacji kluczowej.

Pomocniczo:

- `fixations_before_target`.

---

## H3 – gaze a poprawność odpowiedzi

> **Poprawna odpowiedź będzie częstsza w próbach, w których uczestnik
> rzeczywiście skierował wzrok na informację kluczową.**

Porównujemy:

```text
target_seen = True
vs.
target_seen = False
```

oraz:

- `correct`.

---

# 4. Konstrukcja eksperymentu

Projekt zawiera **12 prób**.

Rozkład:

| warunek | TAK | NIE | razem |
|---|---:|---:|---:|
| EARLY | 3 | 3 | 6 |
| LATE | 3 | 3 | 6 |
| **razem** | **6** | **6** | **12** |

Dzięki temu:

- liczba prób EARLY i LATE jest zrównoważona,
- liczba odpowiedzi TAK i NIE jest zrównoważona,
- odpowiedź nie jest bezpośrednio powiązana z pozycją informacji.

Tematy bodźców obejmują m.in.:

- zwroty,
- dostawę,
- reklamacje,
- konto użytkownika,
- zwrot środków,
- rezerwacje.

---

# 5. Schemat pojedynczej próby

Każda próba ma prosty przebieg:

```text
        punkt fiksacji
              ↓
      PYTANIE + TEKST
              ↓
     rejestracja gaze
              ↓
   wyszukiwanie informacji
              ↓
       odpowiedź TAK / NIE
              ↓
        zapis wyników
              ↓
         następna próba
```

Pytanie jest prezentowane **przed właściwą informacją w tekście**, dzięki czemu
uczestnik wie, czego szuka.

Badamy więc przede wszystkim **wyszukiwanie informacji**, a nie zapamiętywanie
całego tekstu.

---

# 6. Dataset

Dataset znajduje się w:

```text
datasets/text_search.csv
```

Najważniejsze kolumny:

| kolumna | znaczenie |
|---|---|
| `item_id` | identyfikator próby |
| `topic` | temat tekstu |
| `condition` | `EARLY` lub `LATE` |
| `answer` | poprawna odpowiedź `TAK` / `NIE` |
| `critical_phrase` | fragment będący informacją kluczową |
| `selected_text` | pełny bodziec prezentowany uczestnikowi |

Przykładowy rekord:

```csv
item_id,topic,condition,answer,critical_phrase,selected_text
1,zwrot,EARLY,TAK,"zwrot jest możliwy przez trzydzieści dni","PYTANIE: Czy klient ma 30 dni na zwrot produktu? TEKST: Zwrot jest możliwy przez trzydzieści dni od zakupu. Dostawa standardowa trwa dwa dni robocze. Płatność kartą jest dostępna bez dodatkowej opłaty."
```

## Dlaczego `critical_phrase` jest ważne?

Kolumna ta wskazuje fragment tekstu, który zawiera właściwą informację.

Przykład:

```text
Zwrot jest możliwy przez trzydzieści dni od zakupu.
└──────────────────────────────────────┘
              critical phrase
```

Podczas analizy fraza jest dopasowywana do bounding boxów słów utworzonych
przez `tobii-pytracker`.

---

# 7. AOI – Area of Interest

Eksperyment wykorzystuje:

```yaml
bbox_model: word
```

Każde słowo otrzymuje własny bounding box.

Przykładowo:

```text
Zwrot | jest | możliwy | przez | trzydzieści | dni | od | zakupu
 bbox   bbox    bbox      bbox       bbox       bbox  bbox   bbox
```

Dla:

```text
critical_phrase = "zwrot jest możliwy przez trzydzieści dni"
```

tworzony jest logiczny **target AOI**, złożony z bounding boxów kolejnych słów.

Dzięki temu można sprawdzić:

- czy fiksacja trafiła na target,
- kiedy nastąpiła pierwsza fiksacja,
- ile fiksacji wystąpiło,
- jak długo trwały fiksacje w AOI.

---

# 8. Najważniejsze metryki

## `target_seen`

Czy uczestnik wykonał co najmniej jedną fiksację na informacji kluczowej.

```text
True  → target został wzrokowo odwiedzony
False → brak wykrytej fiksacji na target
```

---

## `ttff_target_s`

**Time to First Fixation**.

Czas od początku próby do pierwszej fiksacji na informacji kluczowej.

Przykład:

```text
start próby                       pierwsza fiksacja
    │                                    │
    ├────────────────────────────────────┤
                   1.42 s
```

Niższy TTFF oznacza szybsze odnalezienie informacji.

To główna metryka dla hipotezy H2.

---

## `target_dwell_s`

Łączny czas fiksacji na informacji kluczowej.

Przykład:

```text
fiksacja 1 = 0.18 s
fiksacja 2 = 0.26 s
fiksacja 3 = 0.21 s
-------------------
dwell time = 0.65 s
```

---

## `target_fixation_count`

Liczba fiksacji znajdujących się wewnątrz target AOI.

---

## `target_dwell_share`

Udział czasu fiksacji na informacji kluczowej względem całkowitego czasu
fiksacji w próbie.

Przykład:

```text
całkowity dwell = 2.5 s
target dwell    = 0.75 s

target_dwell_share = 0.30
```

czyli około 30% czasu fiksacji zostało poświęcone informacji kluczowej.

---

## `fixations_before_target`

Liczba fiksacji wykonanych przed pierwszą fiksacją na informacji kluczowej.

To bardzo użyteczna prosta miara strategii wyszukiwania.

Przykład:

```text
fiksacja 1 → tekst neutralny
fiksacja 2 → tekst neutralny
fiksacja 3 → tekst neutralny
fiksacja 4 → TARGET
```

wynik:

```text
fixations_before_target = 3
```

Dla `LATE` oczekujemy przeciętnie większych wartości niż dla `EARLY`.

---

## `correct`

Czy uczestnik udzielił poprawnej odpowiedzi na pytanie.

Pozwala połączyć:

```text
eye tracking
     +
odpowiedź użytkownika
     ↓
czy sposób patrzenia wiązał się ze zrozumieniem informacji?
```

---

# 9. Struktura projektu

Po rozpakowaniu projekt powinien mieć strukturę:

```text
tobii_text_search_demo/
├── README.md
├── EXPERIMENT.md
│
├── configs/
│   ├── config_text_search.yaml
│   ├── mouse_eyetracker_config.yaml
│   └── eyetracker_config.yaml
│
├── datasets/
│   └── text_search.csv
│
├── analysis/
│   └── analyze_results.py
│
├── output/
│   └── ...
│
├── results/
│   └── ...
│
├── run_mouse.bat
├── run_tobii.bat
└── analyze.bat
```

**Wszystkie komendy należy uruchamiać z katalogu głównego
`tobii_text_search_demo/`.**

Ścieżki w konfiguracji są ścieżkami względnymi.

---

# 10. Instalacja środowiska

Zalecane środowisko:

```text
Python 3.10
```

Przykład z Condą:

```bash
conda create -n pytracker-text python=3.10
conda activate pytracker-text
```

Instalacja pakietów:

```bash
pip install tobii-pytracker
pip install "psychopy>=2024.1.4,<2025.1.0" --no-deps
pip install pandas numpy matplotlib
```

W zależności od systemu i używanej wersji PsychoPy mogą być potrzebne
dodatkowe zależności.

Jeżeli wersja `tobii-pytracker` z PyPI nie obsługuje składni użytej w tym
projekcie, należy użyć aktualnej wersji repozytorium zgodnej z dokumentacją
`latest`.

---

# 11. Konfiguracja monitora

Przed pierwszym eksperymentem otwórz:

```text
configs/config_text_search.yaml
```

i sprawdź:

```yaml
display:
  monitor:
    name: experiment_monitor
    resolution:
      - 1920
      - 1080
    width: 53
    distance: 60
    display_number: 0
```

Należy ustawić:

- `resolution` – rzeczywistą rozdzielczość monitora,
- `width` – fizyczną szerokość ekranu w cm,
- `distance` – przybliżoną odległość oczu uczestnika od ekranu,
- `display_number` – numer monitora używanego do eksperymentu.

Poprawne parametry monitora są istotne dla prawidłowej prezentacji bodźca oraz
interpretacji współrzędnych gaze.

---

# 12. Konfiguracja datasetu

W pliku:

```text
configs/config_text_search.yaml
```

znajduje się:

```yaml
dataset:
  text:
    label_column_name: answer
    text_column_name: selected_text
    color: white
    background_color: black
    bbox_model: word
    path: datasets/text_search.csv
```

Znaczenie:

```text
label_column_name → kolumna zawierająca poprawną odpowiedź
text_column_name  → kolumna zawierająca prezentowany tekst
bbox_model        → poziom automatycznego podziału tekstu na AOI
path              → lokalizacja datasetu
```

W tym eksperymencie:

```text
bbox_model = word
```

ponieważ chcemy przypisywać gaze do konkretnych słów tworzących
`critical_phrase`.

---

# 13. Test bez fizycznego Tobii

Projekt można najpierw przetestować przy użyciu emulatora myszy.

## Windows

Uruchom:

```text
run_mouse.bat
```

lub ręcznie:

```bash
tobii-pytracker ^
  --config_file configs/config_text_search.yaml ^
  --eyetracker_config_file configs/mouse_eyetracker_config.yaml ^
  --enable_eyetracker ^
  --loop_count 12
```

W PowerShell lub Bash można użyć jednej linii:

```bash
tobii-pytracker --config_file configs/config_text_search.yaml --eyetracker_config_file configs/mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 12
```

## Sterowanie emulatorem

W przygotowanej konfiguracji:

- **prawy przycisk myszy + ruch myszy** → symulacja gaze,
- zwykły ruch bez przycisku → brak gaze,
- lewy/prawy przycisk może być wykorzystywany przez emulator do zdarzeń oka,
  zależnie od konfiguracji.

Emulator jest szczególnie użyteczny do:

- sprawdzenia layoutu,
- testowania zapisu danych,
- testowania AOI,
- przygotowania analizy bez dostępu do fizycznego trackera.

Nie należy jednak traktować danych z myszy jako prawdziwych danych
okulograficznych.

---

# 14. Eksperyment z fizycznym Tobii

Po podłączeniu trackera można uruchomić:

```text
run_tobii.bat
```

lub:

```bash
tobii-pytracker --config_file configs/config_text_search.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 12
```

Plik:

```text
configs/eyetracker_config.yaml
```

jest przykładową konfiguracją.

Przed właściwym badaniem należy sprawdzić:

- model trackera,
- obsługiwaną częstotliwość próbkowania,
- konfigurację kalibracji,
- wymagania aktualnej wersji `tobii-pytracker`,
- poprawne wykrycie urządzenia.

Jeżeli używany model ma własny sprawdzony plik konfiguracyjny, najlepiej użyć
go zamiast przykładowego pliku z projektu.

---

# 15. Zalecany przebieg sesji z uczestnikiem

## Przed rozpoczęciem

1. Uruchom środowisko Python.
2. Sprawdź tracker.
3. Ustaw uczestnika w odpowiedniej odległości od ekranu.
4. Przeprowadź kalibrację.
5. Wyjaśnij zadanie.

Krótka instrukcja dla uczestnika:

> Na ekranie zobaczysz pytanie oraz krótki tekst.  
> Znajdź w tekście informację potrzebną do odpowiedzi na pytanie.  
> Następnie wybierz TAK albo NIE.  
> Czytaj i odpowiadaj w naturalnym tempie.

Nie należy instruować uczestnika, gdzie w tekście może znajdować się odpowiedź.

---

# 16. Dane wynikowe

Po zakończeniu sesji `tobii-pytracker` utworzy katalog w:

```text
output/
```

Przykładowo:

```text
output/
└── 20260908_180000/
    ├── data.csv
    ├── ...
    └── screenshoty
```

Najważniejszy jest:

```text
data.csv
```

Skrypt analityczny wykorzystuje m.in.:

- `input_data`,
- `classification`,
- `user_classification`,
- `gaze_data`,
- `objects_bboxes`,
- opcjonalnie informacje o screenshocie.

---

# 17. Analiza wyników

Po zebraniu co najmniej jednej sesji uruchom:

```text
analyze.bat
```

lub ręcznie:

```bash
python analysis/analyze_results.py
```

Skrypt przeszukuje:

```text
output/*/data.csv
```

i analizuje wszystkie znalezione sesje.

---

# 18. Co robi `analyze_results.py`

Pipeline:

```text
data.csv
   │
   ▼
odczyt gaze samples
   │
   ▼
detekcja fiksacji I-DT
   │
   ▼
word bounding boxes
   │
   ▼
dopasowanie critical_phrase
   │
   ▼
target AOI
   │
   ├── target_seen
   ├── TTFF
   ├── dwell time
   ├── fixation count
   └── fixations before target
   │
   ▼
połączenie z odpowiedzią TAK / NIE
   │
   ▼
EARLY vs LATE
```

W skrypcie zastosowany jest prosty algorytm I-DT do wykrywania fiksacji.
Parametry można zmienić:

```bash
python analysis/analyze_results.py --dispersion-threshold 50 --min-duration 0.10
```

Domyślnie:

```text
dispersion threshold = 50 px
minimum fixation duration = 0.10 s
```

Są to parametry demonstracyjne. Przy badaniu właściwym powinny zostać dobrane
do częstotliwości próbkowania, monitora i założeń analitycznych.

---

# 19. Pliki wynikowe

Po analizie w katalogu:

```text
results/
```

powstaną:

```text
results/
├── trial_metrics.csv
├── condition_summary.csv
├── hypothesis_summary.txt
├── ttff_by_condition.png
├── accuracy_by_target_seen.png
└── example_trial_gaze.png
```

`example_trial_gaze.png` powstanie, jeżeli skrypt odnajdzie screenshot bodźca.

---

# 20. `trial_metrics.csv`

Jeden wiersz odpowiada jednej próbie jednego uczestnika.

Najważniejsze kolumny:

| kolumna | znaczenie |
|---|---|
| `participant` | identyfikator sesji |
| `item_id` | numer bodźca |
| `topic` | temat |
| `condition` | EARLY / LATE |
| `expected_answer` | poprawna odpowiedź |
| `user_answer` | odpowiedź uczestnika |
| `correct` | poprawność |
| `critical_phrase` | target |
| `target_bbox_found` | czy znaleziono bounding box targetu |
| `target_seen` | czy target był fiksowany |
| `ttff_target_s` | czas do pierwszej fiksacji |
| `target_dwell_s` | łączny dwell na target |
| `target_fixation_count` | liczba fiksacji na target |
| `target_dwell_share` | udział dwell targetu |
| `fixations_before_target` | liczba fiksacji przed targetem |
| `total_fixation_count` | wszystkie fiksacje |
| `total_fixation_dwell_s` | całkowity czas fiksacji |

---

# 21. `condition_summary.csv`

Ten plik agreguje wyniki dla:

```text
EARLY
vs.
LATE
```

Zawiera m.in.:

- liczbę prób,
- accuracy,
- target seen rate,
- średni TTFF,
- średni dwell time targetu,
- średnią liczbę fiksacji na target,
- średnią liczbę fiksacji przed targetem.

Jest to podstawowa tabela do prezentacji wyników.

---

# 22. Interpretacja hipotez

## H1

Sprawdź:

```text
target_seen_rate
mean_target_dwell_s
mean_target_fixation_count
```

Jeżeli `target_seen_rate` jest wysoki, oznacza to, że uczestnicy zazwyczaj
rzeczywiście docierali wzrokiem do informacji zawierającej odpowiedź.

---

## H2

Najważniejszy wynik:

```text
mean_ttff_target_s
```

Oczekujemy:

```text
EARLY < LATE
```

Dodatkowo:

```text
mean_fixations_before_target
```

powinno być niższe dla EARLY.

Interpretacja:

> Użytkownik musi wykonać więcej pracy wzrokowej, zanim dotrze do informacji
> umieszczonej później w tekście.

---

## H3

Porównujemy poprawność dla:

```text
target_seen = True
target_seen = False
```

Oczekujemy:

```text
accuracy(target_seen=True)
>
accuracy(target_seen=False)
```

Jeżeli zależność wystąpi, jest to prosty przykład pokazujący, że gaze pomaga
wyjaśnić zachowanie uczestnika.

---

# 23. Jak prezentować wyniki

Najbardziej czytelna prezentacja może składać się z pięciu kroków.

## Slajd / krok 1 – zadanie

Pokaż przykładowy bodziec:

```text
PYTANIE:
Czy klient ma 30 dni na zwrot produktu?

TEKST:
Dostawa standardowa trwa dwa dni robocze.
Płatność kartą jest dostępna bez dodatkowej opłaty.
Zwrot jest możliwy przez czternaście dni od zakupu.
```

Wyjaśnij:

> Eye tracker pozwala zobaczyć nie tylko odpowiedź NIE, ale również drogę
> wzroku prowadzącą do informacji o 14 dniach.

---

## Slajd / krok 2 – gaze plot

Pokaż:

```text
results/example_trial_gaze.png
```

Cel:

> wizualnie połączyć tekst z zarejestrowanym gaze.

---

## Slajd / krok 3 – AOI

Zaznacz informację:

```text
[Zwrot jest możliwy przez czternaście dni]
```

i wyjaśnij:

```text
word bounding boxes
        ↓
critical_phrase
        ↓
target AOI
```

---

## Slajd / krok 4 – EARLY vs LATE

Pokaż:

```text
results/ttff_by_condition.png
```

Najważniejsza interpretacja:

> Czy informacja umieszczona wcześniej została odnaleziona szybciej?

---

## Slajd / krok 5 – gaze a odpowiedź

Pokaż:

```text
results/accuracy_by_target_seen.png
```

Interpretacja:

> Czy uczestnicy, którzy faktycznie spojrzeli na informację kluczową,
> częściej udzielali poprawnej odpowiedzi?

---

# 24. Przykładowy oczekiwany wzorzec wyników

Poniższa tabela przedstawia **hipotetyczny kierunek**, a nie rzeczywiste wyniki:

| metryka | EARLY | LATE |
|---|---|---|
| TTFF | niższy | wyższy |
| fiksacje przed targetem | mniej | więcej |
| target seen | wysoki | wysoki |
| poprawność | wysoka | wysoka lub nieco niższa |

Najważniejsza różnica powinna dotyczyć strategii dotarcia do informacji, a nie
koniecznie samej poprawności.

---

# 25. Strategia skanowania tekstu

Prosty przykład EARLY:

```text
PYTANIE
   ↓
TARGET
   ↓
odpowiedź
```

Przykład LATE:

```text
PYTANIE
   ↓
fragment 1
   ↓
fragment 2
   ↓
fragment 3
   ↓
TARGET
   ↓
odpowiedź
```

W obecnym skrypcie najprostszą liczbową reprezentacją tej różnicy jest:

```text
fixations_before_target
```

Bardziej rozbudowaną analizę można później rozszerzyć o:

- scanpath,
- regresje,
- przejścia pomiędzy liniami,
- kolejność odwiedzania AOI,
- saccades.

---

# 26. Co dokładnie demonstruje `tobii-pytracker`

Ten eksperyment pokazuje cały podstawowy workflow:

```text
CSV dataset
    ↓
TextDataset
    ↓
PsychoPy
    ↓
Tobii / mouse emulator
    ↓
gaze recording
    ↓
word bounding boxes
    ↓
odpowiedź TAK / NIE
    ↓
data.csv
    ↓
fixation detection
    ↓
gaze → konkretne słowa
    ↓
critical AOI
    ↓
TTFF / dwell / fixation count
    ↓
porównanie EARLY vs LATE
```

Najważniejsza wartość demonstracyjna:

> **Przechodzimy od surowych współrzędnych gaze do semantycznie znaczącej
> informacji: czy i kiedy użytkownik spojrzał na właściwy fragment tekstu.**

---

# 27. Ważne uwagi metodologiczne

Projekt jest przede wszystkim **demonstracją możliwości biblioteki**.

Jeżeli eksperyment miałby służyć do właściwego badania naukowego, należy
rozważyć dodatkowe elementy.

## Więcej uczestników

Jedna sesja wystarcza do demonstracji technicznej, ale nie do wnioskowania
statystycznego.

---

## Więcej bodźców

12 prób jest celowo niewielką liczbą.

Badanie właściwe powinno zawierać więcej itemów reprezentujących różne teksty.

---

## Kontrbalansowanie

W obecnej wersji różne itemy występują jako EARLY i LATE.

Silniejszy projekt eksperymentalny może wykorzystywać dwie listy, w których
ten sam item występuje w obu warunkach pomiędzy uczestnikami:

```text
uczestnik 1 → item X = EARLY
uczestnik 2 → item X = LATE
```

Pozwala to lepiej oddzielić efekt pozycji od efektu konkretnej treści.

---

## Randomizacja

Przy badaniu właściwym warto randomizować kolejność prób.

---

## Długość tekstu

EARLY i LATE powinny mieć możliwie podobną:

- liczbę słów,
- liczbę zdań,
- strukturę graficzną,
- trudność językową.

Manipulowana powinna być przede wszystkim **pozycja informacji kluczowej**.

---

## Pozycja pytania

Pytanie powinno być widoczne przed rozpoczęciem przeszukiwania tekstu.

Jeżeli pytanie zostanie pokazane dopiero po przeczytaniu tekstu, zadanie
zmienia się z wyszukiwania informacji w zadanie pamięciowe.

---

## Analiza statystyczna

Przy większej próbie można zastosować np.:

- modele mieszane,
- uczestnika jako efekt losowy,
- item jako efekt losowy,
- regresję logistyczną dla poprawności,
- model liniowy / mieszany dla TTFF lub dwell time.

---

# 28. Możliwe rozszerzenia eksperymentu

## Rozszerzenie A – nagłówki

Porównanie tekstu:

```text
bez nagłówków
vs.
z czytelnymi nagłówkami
```

Pytanie:

> Czy nagłówki skracają TTFF do informacji?

---

## Rozszerzenie B – wyróżnienie informacji

Porównanie:

```text
zwykły tekst
vs.
pogrubienie kluczowych informacji
```

---

## Rozszerzenie C – długość dokumentu

Porównanie:

```text
krótki tekst
vs.
dłuższy regulamin
```

---

## Rozszerzenie D – trudność pytania

Porównanie:

```text
pytanie zawierające dokładne słowa z tekstu
vs.
pytanie wymagające interpretacji
```

---

## Rozszerzenie E – layout

Porównanie:

```text
ciągły blok tekstu
vs.
lista punktowana
```

To rozszerzenie ma szczególnie duży potencjał biznesowy dla UX.

---

# 29. Rozwiązywanie typowych problemów

## Brak `data.csv`

Sprawdź:

- czy eksperyment zakończył się poprawnie,
- czy katalog `output/` istnieje,
- czy konfiguracja zawiera poprawny `output.folder`,
- czy aplikacja ma prawo zapisu do katalogu.

---

## Skrypt zgłasza brak `output/<timestamp>/data.csv`

Najpierw przeprowadź co najmniej jedną sesję eksperymentu.

---

## `target_bbox_found = False`

Oznacza to, że skrypt nie odnalazł dokładnej sekwencji słów z
`critical_phrase` w zapisanych bounding boxach.

Sprawdź:

- pisownię `critical_phrase`,
- tekst `selected_text`,
- znaki interpunkcyjne,
- czy `objects_bboxes` zawiera sekcję `words`.

---

## Bardzo mało lub brak fiksacji

Możliwe przyczyny:

- emulator myszy był używany bez właściwego przycisku,
- tracker nie zapisywał gaze,
- parametry detektora fiksacji są zbyt restrykcyjne,
- dane mają inną strukturę niż oczekiwana przez skrypt.

Można testowo zmniejszyć próg minimalnego czasu:

```bash
python analysis/analyze_results.py --min-duration 0.08
```

lub zmienić próg dyspersji:

```bash
python analysis/analyze_results.py --dispersion-threshold 60
```

Zmiany parametrów należy stosować świadomie i konsekwentnie dla wszystkich
uczestników.

---

## Dodatkowy przycisk `none`

Niektóre wersje `TextDataset` mogą generować dodatkową klasę `none`.

W tym eksperymencie uczestnik powinien wybierać wyłącznie:

```text
TAK
NIE
```

---

# 30. Minimalny workflow do demonstracji

Jeżeli celem jest tylko szybka prezentacja możliwości `tobii-pytracker`,
wystarczy:

```text
1. uruchom run_mouse.bat
2. wykonaj 12 prób
3. symuluj gaze prawym przyciskiem myszy
4. uruchom analyze.bat
5. otwórz results/
6. pokaż gaze plot
7. pokaż TTFF EARLY vs LATE
8. pokaż accuracy względem target_seen
```

To pozwala zaprezentować pełny pipeline bez fizycznego urządzenia Tobii.

---

# 31. Najkrótsze podsumowanie eksperymentu

**Zadanie**

Użytkownik ma znaleźć odpowiedź w krótkim tekście.

**Manipulacja**

```text
informacja EARLY
vs.
informacja LATE
```

**Eye tracking**

```text
gdzie patrzył?
kiedy znalazł target?
ile fiksacji wykonał wcześniej?
jak długo patrzył na target?
```

**Behavior**

```text
TAK / NIE
poprawnie / błędnie
```

**Główne wyniki**

```text
TTFF
target dwell time
target fixation count
fixations before target
accuracy
```

**Wartość**

> Eye tracking pokazuje nie tylko, czy użytkownik zna poprawną odpowiedź,
> ale również **jak skutecznie odnalazł potrzebną informację w tekście**.
