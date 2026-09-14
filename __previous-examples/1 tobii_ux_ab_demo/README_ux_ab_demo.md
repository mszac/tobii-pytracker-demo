# tobii_ux_ab_demo

## Eksperyment: porównanie formalnych i prostych komunikatów UX

Gotowy projekt demonstracyjny dla **tobii-pytracker** pokazujący wykorzystanie
eye-trackingu do porównania dwóch sposobów formułowania komunikatów interfejsu.

Eksperyment porównuje:

```text
A_FORMAL
vs.
B_SIMPLE
```

gdzie:

- **A_FORMAL** – komunikat bardziej formalny, mniej bezpośredni i bardziej
  „systemowy”,
- **B_SIMPLE** – komunikat prostszy, bardziej bezpośredni i bliższy codziennemu
  językowi użytkownika.

Każda para dotyczy tej samej sytuacji, prowadzi do tej samej poprawnej odpowiedzi
i zawiera **dokładnie taką samą liczbę słów w komunikacie**.

Dzięki temu porównujemy przede wszystkim **sposób sformułowania treści**, a nie
samą długość tekstu.

---

# 1. Cel eksperymentu

## Cel ogólny

Celem jest sprawdzenie, czy prostszy sposób formułowania komunikatu UX zmniejsza
pracę wzrokową potrzebną do jego zrozumienia.

Główne pytanie badawcze:

> **Czy prostszy i bardziej bezpośredni komunikat UX jest przetwarzany wzrokowo
> sprawniej niż formalny komunikat o tej samej długości, przy zachowaniu podobnej
> lub wyższej poprawności zrozumienia?**

Interesuje nas więc nie tylko:

```text
czy użytkownik odpowiedział poprawnie?
```

ale również:

```text
jak czytał komunikat?
ile wykonał fiksacji?
jak długo przetwarzał komunikat?
czy wracał wzrokiem do wcześniejszych słów?
jak szybko dotarł do instrukcji działania?
```

---

# 2. Kontekst UX i biznesowy

Komunikaty systemowe pojawiają się w niemal każdym interfejsie:

- błędy płatności,
- błędy logowania,
- walidacja formularzy,
- brak połączenia z internetem,
- przekroczenie limitu rozmiaru pliku,
- komunikaty dotyczące cookies,
- informacje o dostawie,
- ustawienia konta.

Dwa komunikaty mogą przekazywać praktycznie tę samą informację, ale różnić się
stylem.

Przykład:

### A_FORMAL

> Nie można zrealizować płatności, ponieważ autoryzacja karty zakończyła się
> niepowodzeniem. Zweryfikuj dane karty albo wybierz inną metodę płatności.

### B_SIMPLE

> Nie udało się zrealizować płatności, ponieważ karta nie została zaakceptowana.
> Sprawdź dane karty albo wybierz inną metodę płatności.

Oba komunikaty:

- opisują tę samą sytuację,
- zawierają tę samą liczbę słów,
- przekazują tę samą instrukcję działania,
- prowadzą do tej samej odpowiedzi na pytanie.

Różnią się przede wszystkim **stylem języka**.

---

# 3. Główne pytanie badawcze

Eksperyment odpowiada na pytanie:

> **Czy język prostszy i bardziej bezpośredni zmniejsza koszt wzrokowego
> przetwarzania komunikatu UX w porównaniu z językiem bardziej formalnym?**

Porównujemy:

```text
A_FORMAL
bardziej formalny
bardziej abstrakcyjny
bardziej systemowy

vs.

B_SIMPLE
prostszy
bardziej bezpośredni
bardziej użytkowy
```

---

# 4. Pytania szczegółowe

## RQ1 – czas przetwarzania

> Czy komunikaty `B_SIMPLE` wymagają krótszego łącznego czasu fiksacji niż
> `A_FORMAL`?

---

## RQ2 – liczba fiksacji

> Czy komunikaty `B_SIMPLE` wymagają mniejszej liczby fiksacji?

---

## RQ3 – regresje

> Czy prostszy język powoduje mniej powrotów wzroku do wcześniejszych fragmentów
> komunikatu?

---

## RQ4 – zrozumienie

> Czy uproszczenie języka zachowuje lub poprawia poprawność odpowiedzi?

---

## RQ5 – instrukcja działania

> Czy użytkownik szybciej odnajduje fragment mówiący, co należy zrobić, w wersji
> `B_SIMPLE`?

---

# 5. Konstrukcja eksperymentu

Projekt zawiera **8 par komunikatów**, czyli łącznie:

```text
16 prób
```

Rozkład:

| Wersja | TAK | NIE | Razem |
|---|---:|---:|---:|
| A_FORMAL | 4 | 4 | 8 |
| B_SIMPLE | 4 | 4 | 8 |
| **Razem** | **8** | **8** | **16** |

Każdy z 8 tematów występuje:

```text
1 × A_FORMAL
1 × B_SIMPLE
```

czyli każdy item ma swoją parę A/B.

---

# 6. Tematy bodźców

Projekt obejmuje osiem typowych sytuacji UX:

```text
1. payment
2. password
3. form
4. network
5. file
6. cookies
7. delivery
8. account
```

Są to sytuacje, które użytkownik może spotkać w rzeczywistym interfejsie
internetowym lub aplikacji.

---

# 7. Kontrola długości komunikatów

Jednym z najważniejszych elementów konstrukcji jest kontrola liczby słów.

Dla każdej pary:

```text
A_FORMAL word count = B_SIMPLE word count
```

Przykładowo:

| Topic | A_FORMAL | B_SIMPLE |
|---|---:|---:|
| payment | 18 | 18 |
| password | 14 | 14 |
| form | 19 | 19 |
| network | 17 | 17 |
| file | 16 | 16 |
| cookies | 18 | 18 |
| delivery | 16 | 16 |
| account | 16 | 16 |

Dzięki temu obserwowana różnica w:

```text
dwell time
fixation count
regression count
```

nie może być łatwo wyjaśniona samym faktem, że jedna wersja jest dłuższa.

To ważna kontrola metodologiczna.

---

# 8. Przykładowa para A/B

## A_FORMAL

```text
KOMUNIKAT:

Logowanie nie zostało zakończone z powodu nieprawidłowych danych
uwierzytelniających. Zweryfikuj hasło i spróbuj ponownie.

PYTANIE:

Czy użytkownik powinien od razu kontaktować się z obsługą?
```

Poprawna odpowiedź:

```text
NIE
```

---

## B_SIMPLE

```text
KOMUNIKAT:

Nie udało się zalogować, ponieważ wpisane hasło jest nieprawidłowe.
Sprawdź hasło i spróbuj ponownie.

PYTANIE:

Czy użytkownik powinien od razu kontaktować się z obsługą?
```

Poprawna odpowiedź:

```text
NIE
```

Obie wersje mają:

```text
14 słów
```

w części komunikatu.

---

# 9. Schemat pojedynczej próby

Każda próba ma prostą strukturę:

```text
          punkt fiksacji
                ↓
        KOMUNIKAT UX
                ↓
          pusta linia
                ↓
            PYTANIE
                ↓
        rejestracja gaze
                ↓
      odpowiedź TAK / NIE
                ↓
          zapis danych
                ↓
          następna próba
```

Uczestnik:

```text
czyta komunikat
      ↓
interpretuje problem
      ↓
odnajduje zalecane działanie
      ↓
czyta pytanie
      ↓
udziela odpowiedzi
```

---

# 10. Dlaczego komunikat jest przed pytaniem?

W tym eksperymencie badamy przede wszystkim **naturalne przetwarzanie komunikatu
UX**.

Użytkownik najpierw widzi komunikat, tak jak zobaczyłby go w rzeczywistym
interfejsie.

Dopiero poniżej znajduje się pytanie sprawdzające zrozumienie.

Schemat:

```text
KOMUNIKAT
    ↓
przetwarzanie komunikatu
    ↓
PYTANIE
    ↓
odpowiedź
```

To odróżnia eksperyment od zadania wyszukiwania konkretnej informacji, w którym
pytanie powinno być widoczne wcześniej.

Tutaj komunikat jest głównym obiektem analizy.

---

# 11. Dataset

Dataset znajduje się w:

```text
datasets/ux_ab_demo.csv
```

Najważniejsze kolumny:

| Kolumna | Znaczenie |
|---|---|
| `item_id` | identyfikator pary A/B |
| `topic` | typ sytuacji UX |
| `version` | `A_FORMAL` lub `B_SIMPLE` |
| `answer` | poprawna odpowiedź `TAK` / `NIE` |
| `message_word_count` | liczba słów w komunikacie |
| `action_phrase` | fragment zawierający instrukcję działania |
| `message_text` | sam komunikat UX |
| `question` | pytanie sprawdzające zrozumienie |
| `selected_text` | pełny bodziec prezentowany uczestnikowi |

---

# 12. `selected_text`

`tobii-pytracker` prezentuje zawartość kolumny:

```text
selected_text
```

Przykładowo:

```text
KOMUNIKAT: Nie można zrealizować płatności, ponieważ autoryzacja karty
zakończyła się niepowodzeniem. Zweryfikuj dane karty albo wybierz inną
metodę płatności.

PYTANIE: Czy użytkownik powinien sprawdzić dane karty?
```

Między komunikatem a pytaniem znajduje się pusta linia.

---

# 13. Odpowiedzi

Dataset wykorzystuje:

```text
TAK
NIE
```

jako poprawne klasy.

Konfiguracja wskazuje:

```yaml
label_column_name: answer
```

co oznacza, że wartości z kolumny:

```text
answer
```

stają się klasami odpowiedzi.

W wersji projektu z poprawką źródłową dodatkowy przycisk:

```text
NONE
```

jest zastępowany przez:

```text
NIE WIEM
```

---

# 14. Główna manipulacja

Najważniejszą zmienną jest:

```text
version
```

z dwoma poziomami:

```text
A_FORMAL
B_SIMPLE
```

Nie manipulujemy:

- długością komunikatu,
- tematem komunikatu,
- poprawną odpowiedzią,
- podstawową informacją,
- zalecanym działaniem.

Manipulowany jest przede wszystkim **sposób sformułowania treści**.

---

# 15. Hipoteza H1 – krótszy dwell time dla B_SIMPLE

> **Prostsze komunikaty `B_SIMPLE` będą wymagały krótszego łącznego czasu
> fiksacji na komunikacie niż `A_FORMAL`.**

Oczekujemy:

```text
message_dwell_s(B_SIMPLE)
<
message_dwell_s(A_FORMAL)
```

Interpretacja:

```text
mniejszy dwell
     ↓
mniej czasu potrzebnego na przetworzenie komunikatu
```

Główna metryka:

```text
message_dwell_s
```

---

# 16. Hipoteza H2 – mniej fiksacji dla B_SIMPLE

> **Komunikaty `B_SIMPLE` będą wymagały mniejszej liczby fiksacji niż
> `A_FORMAL`.**

Oczekujemy:

```text
message_fixation_count(B_SIMPLE)
<
message_fixation_count(A_FORMAL)
```

Interpretacja:

```text
mniej fiksacji
     ↓
mniej jednostek informacji wymagających ponownego przetworzenia
```

Główna metryka:

```text
message_fixation_count
```

---

# 17. Hipoteza H3 – mniej regresji dla B_SIMPLE

> **Prostszy język będzie powodował mniej regresji wzrokowych.**

Regresja oznacza sytuację, w której wzrok wraca do wcześniejszego fragmentu
komunikatu.

Przykład:

```text
Nie udało się zrealizować płatności...
        ↓
...karta nie została zaakceptowana
        ↓
        ← powrót
...zrealizować płatności...
```

Oczekujemy:

```text
regression_count(B_SIMPLE)
<
regression_count(A_FORMAL)
```

Główna metryka:

```text
regression_count
```

---

# 18. Hipoteza H4 – podobna lub wyższa poprawność

> **Uproszczenie języka nie powinno obniżać poprawności rozumienia komunikatu.**

Oczekujemy:

```text
accuracy(B_SIMPLE)
>=
accuracy(A_FORMAL)
```

Ważne:

celem nie jest tylko:

```text
szybsze czytanie
```

ale:

```text
szybsze / prostsze przetwarzanie
+
zachowane zrozumienie
```

Główna metryka:

```text
correct
```

---

# 19. Hipoteza H5 – szybsze odnalezienie instrukcji działania

> **W wersji `B_SIMPLE` użytkownik szybciej skieruje wzrok na fragment mówiący,
> co powinien zrobić.**

Każdy item ma kolumnę:

```text
action_phrase
```

Przykład:

```text
Sprawdź dane karty albo wybierz inną metodę płatności
```

lub:

```text
Zweryfikuj dane karty albo wybierz inną metodę płatności
```

Oczekujemy:

```text
ttff_action_s(B_SIMPLE)
<
ttff_action_s(A_FORMAL)
```

Główna metryka:

```text
ttff_action_s
```

---

# 20. `action_phrase`

`action_phrase` jest kluczowym elementem analizy.

Każdy komunikat zawiera fragment mówiący użytkownikowi, co powinien zrobić.

Przykład:

```text
Nie udało się zrealizować płatności, ponieważ karta nie została zaakceptowana.
[Sprawdź dane karty albo wybierz inną metodę płatności.]
```

Fragment w nawiasie reprezentuje:

```text
action AOI
```

Kolumna:

```text
action_phrase
```

pozwala automatycznie odnaleźć odpowiednie słowa w zapisanych bounding boxach.

---

# 21. AOI – Area of Interest

Eksperyment wykorzystuje:

```yaml
bbox_model: word
```

`tobii-pytracker` tworzy bounding box dla każdego słowa bodźca.

Przykładowo:

```text
Sprawdź | dane | karty | albo | wybierz | inną | metodę | płatności
  bbox    bbox    bbox    bbox    bbox     bbox    bbox      bbox
```

Z tych bboxów można zbudować logiczne AOI:

```text
action_phrase
```

czyli obszar odpowiadający instrukcji działania.

---

# 22. Dwa poziomy analizy AOI

W demo analizujemy dwa główne poziomy.

## Poziom 1 – cały komunikat

Analizowane są wszystkie słowa przed markerem:

```text
PYTANIE
```

Daje to:

```text
message_fixation_count
message_dwell_s
regression_count
```

---

## Poziom 2 – instrukcja działania

Z `action_phrase` tworzony jest mniejszy logiczny AOI.

Daje to:

```text
action_seen
ttff_action_s
action_dwell_s
action_fixation_count
```

---

# 23. `message_dwell_s`

Łączny czas fiksacji przypisanych do słów części:

```text
KOMUNIKAT
```

Przykład:

```text
fiksacja 1 = 0.20 s
fiksacja 2 = 0.16 s
fiksacja 3 = 0.23 s
fiksacja 4 = 0.18 s
-------------------
message dwell = 0.77 s
```

Niższy wynik może oznaczać mniejszą ilość pracy wzrokowej potrzebnej do
przetworzenia komunikatu.

---

# 24. `message_fixation_count`

Liczba wykrytych fiksacji na słowach komunikatu.

Przykład:

```text
fiksacja 1 → "Nie"
fiksacja 2 → "zrealizować"
fiksacja 3 → "karta"
fiksacja 4 → "Sprawdź"
```

wynik:

```text
message_fixation_count = 4
```

---

# 25. `regression_count`

Regresja jest wykrywana jako powrót do wcześniejszego słowa.

W obecnej analizie skok wstecz musi wynosić co najmniej:

```text
2 słowa
```

aby został policzony jako regresja.

Przykład indeksów kolejnych fiksowanych słów:

```text
3 → 6 → 9 → 5 → 10
```

Przejście:

```text
9 → 5
```

jest regresją.

Interpretacja:

```text
więcej regresji
     ↓
więcej powrotów do wcześniej przeczytanej informacji
```

Regresja może być związana m.in. z:

- trudnością językową,
- niejasnością,
- potrzebą ponownej interpretacji,
- kontrolą informacji.

Nie należy jednak automatycznie traktować każdej regresji jako błędu
użytkownika.

---

# 26. `action_seen`

Informacja binarna:

```text
True
False
```

oznaczająca, czy wykryto co najmniej jedną fiksację w `action_phrase`.

Przykład:

```text
action_seen = True
```

oznacza, że uczestnik skierował wzrok na instrukcję działania.

---

# 27. `ttff_action_s`

**Time to First Fixation** na instrukcji działania.

Schemat:

```text
pierwsza zapisana próbka gaze
        │
        ├───────────────────────────────┐
                                        │
                              pierwsza fiksacja
                              na action_phrase
```

Różnica czasu daje:

```text
ttff_action_s
```

Niższa wartość oznacza szybsze dotarcie do instrukcji działania.

---

# 28. Ważne ograniczenie TTFF

W obecnym workflow:

```text
ttff_action_s
```

jest liczony względem **pierwszej zapisanej próbki gaze** w próbie.

Nie jest to idealnie to samo co:

```text
stimulus onset timestamp
```

Dlatego metrykę należy interpretować jako demonstracyjny:

> czas od początku dostępnego zapisu gaze do pierwszej fiksacji na action AOI.

Do ścisłej analizy czasowej framework powinien zapisywać osobny timestamp
pojawienia się bodźca.

---

# 29. `action_dwell_s`

Łączny czas fiksacji na instrukcji działania.

Przykład:

```text
Sprawdź dane karty albo wybierz inną metodę płatności
        ↑           ↑               ↑
      0.20 s      0.18 s          0.25 s
```

wynik:

```text
action_dwell_s = 0.63 s
```

---

# 30. `action_fixation_count`

Liczba fiksacji znajdujących się wewnątrz `action_phrase`.

Pozwala sprawdzić, czy szybsze dotarcie do instrukcji było również związane z
mniejszą liczbą ponownych odczytań tej instrukcji.

---

# 31. `correct`

Czy odpowiedź uczestnika zgadza się z poprawną odpowiedzią.

Przykład:

```text
expected_answer = TAK
user_answer     = TAK

correct = True
```

lub:

```text
expected_answer = NIE
user_answer     = TAK

correct = False
```

---

# 32. Konfiguracja datasetu

Główny config zawiera:

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

Znaczenie:

```text
label_column_name
    ↓
kolumna zawierająca poprawną klasę TAK / NIE

text_column_name
    ↓
pełny tekst prezentowany uczestnikowi

bbox_model = word
    ↓
bounding box dla każdego słowa

path
    ↓
plik CSV z bodźcami
```

---

# 33. Konfiguracja monitora

W:

```text
configs/config_ux_ab_demo.yaml
```

znajduje się m.in.:

```yaml
display:
  monitor:
    name: spectrum_monitor
    resolution:
      - 2560
      - 1440
    width: 35
    distance: 60
    display_number: 0
```

Przed właściwym eksperymentem należy dostosować:

- `resolution` – rozdzielczość monitora,
- `width` – fizyczną szerokość monitora,
- `distance` – odległość uczestnika od ekranu,
- `display_number` – numer używanego monitora.

---

# 34. Obszar prezentacji tekstu

Config wykorzystuje:

```yaml
aoe:
  - 750
  - 750
```

Oznacza to obszar, w którym prezentowany jest bodziec tekstowy.

Stały obszar prezentacji pomaga zachować porównywalny układ pomiędzy
komunikatami.

---

# 35. Instrukcja dla uczestnika

Config zawiera instrukcję:

```text
Porównanie komunikatów UX

Przeczytaj komunikat oraz pytanie.
Następnie wybierz odpowiedź TAK albo NIE.
Czytaj w naturalnym tempie.
```

W badaniu właściwym nie należy mówić uczestnikowi:

- która wersja jest formalna,
- która wersja jest prostsza,
- że interesuje nas instrukcja działania,
- które słowa są AOI.

Uczestnik powinien czytać komunikat naturalnie.

---

# 36. Struktura projektu

Po połączeniu plików z repozytorium struktura może wyglądać:

```text
tobii-pytracker/
├── configs/
│   ├── config.yaml
│   ├── config_ux_ab_demo.yaml
│   └── eyetracker_config.yaml
│
├── datasets/
│   └── ux_ab_demo.csv
│
├── examples/
│   └── ux_ab_demo/
│       ├── README.md
│       ├── EXPERIMENT.md
│       ├── apply_demo_source_patch.py
│       └── ...
│
└── output/
    └── ux_ab_demo/
```

Wszystkie komendy najlepiej uruchamiać z katalogu głównego repozytorium:

```text
tobii-pytracker/
```

---

# 37. Test samego GUI

Najpierw warto sprawdzić prezentację bez fizycznego eye trackera:

```bash
tobii-pytracker \
  --config_file configs/config_ux_ab_demo.yaml \
  --loop_count 2
```

Powinny pojawić się:

- komunikat,
- pytanie,
- przyciski odpowiedzi.

Jeżeli GUI działa, a wersja z Tobii nie działa, problem prawdopodobnie nie
dotyczy datasetu ani głównego configu.

---

# 38. Uruchomienie pełnego eksperymentu

Dla 16 prób:

```bash
tobii-pytracker \
  --config_file configs/config_ux_ab_demo.yaml \
  --eyetracker_config_file configs/eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 16
```

Używamy:

```text
configs/eyetracker_config.yaml
```

zgodnego z aktualnym repozytorium i urządzeniem.

---

# 39. Dane wynikowe

Config zapisuje dane do:

```yaml
output:
  folder: output/ux_ab_demo
```

Typowa struktura:

```text
output/
└── ux_ab_demo/
    └── <timestamp>/
        └── data.csv
```

Najważniejsze pola `data.csv`:

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

---

# 40. Znaczenie pól `data.csv`

## `input_data`

Pełny tekst bodźca:

```text
KOMUNIKAT + PYTANIE
```

Na tej podstawie można połączyć wynik próby z odpowiednim rekordem datasetu.

---

## `classification`

Poprawna odpowiedź pochodząca z:

```text
answer
```

czyli:

```text
TAK
lub
NIE
```

---

## `user_classification`

Odpowiedź uczestnika.

---

## `gaze_data`

Lista zarejestrowanych próbek gaze.

---

## `objects_bboxes`

Bounding boxy słów wygenerowane dla bodźca.

To właśnie one pozwalają przejść od:

```text
surowe współrzędne gaze
```

do:

```text
konkretne słowo komunikatu
```

---

# 41. Analiza wyników

Pipeline analityczny:

```text
                data.csv
                   │
                   ▼
            dopasowanie bodźca
                   │
                   ▼
              gaze samples
                   │
                   ▼
          detekcja fiksacji I-DT
                   │
                   ▼
            word bounding boxes
                   │
          ┌────────┴────────┐
          ▼                 ▼
   cały KOMUNIKAT      action_phrase
          │                 │
          ▼                 ▼
      dwell time            TTFF
      fixations             dwell
      regressions           fixations
          │                 │
          └────────┬────────┘
                   ▼
           odpowiedź TAK/NIE
                   │
                   ▼
          A_FORMAL vs B_SIMPLE
```

---

# 42. Detekcja fiksacji

Analiza może wykorzystywać prosty algorytm I-DT.

Przykładowe parametry demonstracyjne:

```text
dispersion threshold = 50 px
minimum fixation duration = 0.10 s
```

Parametry powinny być stosowane konsekwentnie dla wszystkich uczestników.

Przy badaniu właściwym należy je dobrać do:

- częstotliwości próbkowania,
- dokładności trackera,
- geometrii monitora,
- przyjętego protokołu analitycznego.

---

# 43. Oczekiwane pliki analizy

Przykładowy zestaw:

```text
results/
├── trial_metrics.csv
├── version_summary.csv
├── hypothesis_summary.txt
├── 01_reading_time.png
├── 02_fixations.png
├── 03_regressions.png
└── 04_ttff_action.png
```

---

# 44. `trial_metrics.csv`

Jeden wiersz odpowiada jednej próbie.

Najważniejsze kolumny:

| Kolumna | Znaczenie |
|---|---|
| `participant` | identyfikator sesji / uczestnika |
| `trial_index` | numer próby |
| `item_id` | identyfikator pary A/B |
| `topic` | temat komunikatu |
| `version` | `A_FORMAL` / `B_SIMPLE` |
| `expected_answer` | poprawna odpowiedź |
| `user_answer` | odpowiedź uczestnika |
| `correct` | poprawność |
| `message_word_count` | liczba słów komunikatu |
| `message_fixation_count` | liczba fiksacji na komunikacie |
| `message_dwell_s` | dwell time komunikatu |
| `regression_count` | liczba regresji |
| `action_seen` | czy action AOI był fiksowany |
| `ttff_action_s` | czas do pierwszej fiksacji na action AOI |
| `action_dwell_s` | dwell time action AOI |
| `action_fixation_count` | liczba fiksacji na action AOI |
| `word_bboxes_found` | czy bounding boxy słów zostały odnalezione |

---

# 45. `version_summary.csv`

Ten plik agreguje wyniki dla:

```text
A_FORMAL
vs.
B_SIMPLE
```

Przykładowe kolumny:

```text
n_trials
accuracy
mean_message_dwell_s
mean_fixation_count
mean_regression_count
action_seen_rate
mean_ttff_action_s
mean_action_dwell_s
```

To główna tabela do prezentacji wyników demo.

---

# 46. Interpretacja H1

Sprawdź:

```text
mean_message_dwell_s
```

Oczekiwany kierunek:

```text
B_SIMPLE < A_FORMAL
```

Interpretacja:

> Prostszy komunikat wymagał mniej czasu fiksacji podczas przetwarzania treści.

Ważne:

nie należy automatycznie utożsamiać krótszego dwell time z lepszym UX.

Krótszy czas jest korzystny tylko wtedy, gdy:

```text
accuracy
```

pozostaje na podobnym lub wyższym poziomie.

---

# 47. Interpretacja H2

Sprawdź:

```text
mean_fixation_count
```

Oczekujemy:

```text
B_SIMPLE < A_FORMAL
```

Możliwa interpretacja:

> Użytkownicy potrzebowali mniej jednostek wzrokowego przetwarzania, aby
> zrozumieć prostszy komunikat.

---

# 48. Interpretacja H3

Sprawdź:

```text
mean_regression_count
```

Oczekujemy:

```text
B_SIMPLE < A_FORMAL
```

Możliwa interpretacja:

> Formalna wersja częściej wymagała powrotu wzroku do wcześniej przeczytanych
> fragmentów.

---

# 49. Interpretacja H4

Sprawdź:

```text
accuracy
```

Oczekujemy:

```text
B_SIMPLE >= A_FORMAL
```

Najbardziej pożądany wzorzec UX:

```text
B_SIMPLE:
mniejszy dwell
mniej fiksacji
mniej regresji
podobna lub wyższa accuracy
```

To sugerowałoby poprawę efektywności bez kosztu dla zrozumienia.

---

# 50. Interpretacja H5

Sprawdź:

```text
mean_ttff_action_s
```

Oczekujemy:

```text
B_SIMPLE < A_FORMAL
```

Interpretacja:

> W prostszej wersji użytkownicy szybciej docierali wzrokiem do instrukcji
> mówiącej, co należy zrobić.

---

# 51. Najważniejszy wzorzec wyników

Hipotetyczny, oczekiwany kierunek:

| Metryka | A_FORMAL | B_SIMPLE |
|---|---|---|
| `message_dwell_s` | wyższy | **niższy** |
| `message_fixation_count` | wyższy | **niższy** |
| `regression_count` | wyższy | **niższy** |
| `ttff_action_s` | wyższy | **niższy** |
| `accuracy` | podobna | **podobna lub wyższa** |

To nie są rzeczywiste wyniki.

Są to hipotezy, które należy sprawdzić na zarejestrowanych danych.

---

# 52. Dlaczego samo accuracy nie wystarcza?

Możliwa sytuacja:

```text
A_FORMAL accuracy = 100%
B_SIMPLE accuracy = 100%
```

Na podstawie samej odpowiedzi wyglądałoby na to, że wersje są identyczne.

Eye tracking może jednak pokazać:

```text
A_FORMAL:
12 fiksacji
2.8 s dwell
3 regresje

B_SIMPLE:
8 fiksacji
1.9 s dwell
1 regresja
```

Wtedy obie wersje są zrozumiałe, ale jedna wymaga mniej pracy wzrokowej.

To jest główna wartość demonstracyjna eksperymentu.

---

# 53. Jak prezentować wyniki

Najbardziej czytelna prezentacja demo może składać się z pięciu kroków.

## Krok 1 – pokaż parę A/B

Na jednym slajdzie:

```text
A_FORMAL
vs.
B_SIMPLE
```

z zaznaczeniem:

```text
ta sama sytuacja
ta sama liczba słów
ta sama odpowiedź
inny sposób sformułowania
```

---

## Krok 2 – pokaż fiksacje

Na jednym komunikacie pokaż punkty fiksacji.

Wyjaśnij:

> Sama odpowiedź mówi, czy uczestnik zrozumiał komunikat. Fiksacje pokazują,
> jak dużo pracy wzrokowej było potrzebne.

---

## Krok 3 – pokaż action AOI

Zaznacz:

```text
[Sprawdź dane karty albo wybierz inną metodę płatności]
```

Wyjaśnij:

```text
word bboxes
    ↓
action_phrase
    ↓
action AOI
    ↓
TTFF + dwell + fixation count
```

---

## Krok 4 – pokaż A_FORMAL vs B_SIMPLE

Otwórz wykresy:

```text
01_reading_time.png
02_fixations.png
03_regressions.png
04_ttff_action.png
```

---

## Krok 5 – połącz gaze z accuracy

Najważniejsze pytanie:

> Czy prostsza wersja wymaga mniej pracy wzrokowej bez pogorszenia zrozumienia?

---

# 54. Co dokładnie demonstruje tobii-pytracker?

Ten eksperyment pokazuje workflow:

```text
CSV dataset
    ↓
TextDataset
    ↓
PsychoPy
    ↓
komunikat UX
    ↓
Tobii gaze
    ↓
word bounding boxes
    ↓
odpowiedź TAK / NIE
    ↓
data.csv
    ↓
fixation detection
    ↓
gaze → słowa
    ↓
KOMUNIKAT + action AOI
    ↓
dwell / fixations / regressions / TTFF
    ↓
A_FORMAL vs B_SIMPLE
```

Najważniejsza wartość demonstracyjna:

> **Eye tracking pozwala porównać nie tylko poprawność dwóch wersji komunikatu,
> ale również koszt wzrokowego przetwarzania prowadzącego do tej samej decyzji.**

---

# 55. Ważne ograniczenie projektu demo

W obecnym demo jedna sesja zawiera:

```text
A_FORMAL
oraz
B_SIMPLE
```

dla tego samego itemu.

Oznacza to, że uczestnik może zobaczyć dwie wersje tej samej sytuacji.

Może wystąpić:

- efekt pamięci,
- efekt powtórzenia,
- szybsze rozpoznanie drugiej wersji,
- przewidywanie poprawnej odpowiedzi.

Dlatego obecna wersja jest bardzo dobra jako:

```text
demo techniczne
```

ale słabsza jako finalny eksperyment naukowy.

---

# 56. Lepszy projekt badania właściwego

Dla właściwego badania można zastosować kontrbalansowanie.

Przykład:

```text
LISTA 1
payment  → A
password → B
form     → A
network  → B
...

LISTA 2
payment  → B
password → A
form     → B
network  → A
...
```

Każdy uczestnik widzi wtedy:

```text
tylko jedną wersję każdego itemu
```

ale w całej próbie badawczej każdy item pojawia się zarówno jako:

```text
A_FORMAL
```

jak i:

```text
B_SIMPLE
```

---

# 57. Dlaczego kontrbalansowanie jest ważne?

Bez kontrbalansowania:

```text
uczestnik widzi payment A
        ↓
poznaje odpowiedź
        ↓
później widzi payment B
```

Wtedy czas czytania drugiego wariantu może być krótszy nie dlatego, że język jest
lepszy, tylko dlatego, że sytuacja jest już znana.

Kontrbalansowanie ogranicza ten problem.

---

# 58. Item jako własna kontrola

Dużą zaletą projektu A/B jest to, że ten sam temat może pełnić rolę własnej
kontroli.

Porównujemy:

```text
payment A
vs.
payment B

password A
vs.
password B

form A
vs.
form B
```

Dzięki temu ograniczamy wpływ różnic pomiędzy tematami.

---

# 59. Kontrola odpowiedzi TAK / NIE

W obu wersjach mamy:

```text
4 × TAK
4 × NIE
```

czyli odpowiedź nie jest powiązana z wariantem językowym.

To ważne, ponieważ w przeciwnym razie uczestnik mógłby nauczyć się np.:

```text
A_FORMAL → częściej TAK
B_SIMPLE → częściej NIE
```

W aktualnym projekcie ten problem jest zminimalizowany.

---

# 60. Kontrola długości a czytelność

Równa liczba słów nie oznacza, że oba komunikaty są identyczne językowo.

Właśnie tego chcemy.

Możemy różnić:

- długość poszczególnych słów,
- stopień formalności,
- abstrakcyjność,
- bezpośredniość,
- użycie strony biernej,
- typ słownictwa.

Ale kontrolujemy:

```text
łączną liczbę słów
```

aby długość komunikatu nie była głównym wyjaśnieniem różnic gaze.

---

# 61. Możliwe dodatkowe metryki

W przyszłości analizę można rozszerzyć o:

```text
mean fixation duration
first-pass reading time
second-pass reading time
number of reread words
scanpath length
saccade amplitude
word skipping rate
action AOI revisits
question dwell time
```

---

# 62. First-pass reading

Ciekawym rozszerzeniem byłoby policzenie czasu pierwszego przejścia przez
komunikat.

Schemat:

```text
pierwsze wejście na słowo 1
        ↓
czytanie do końca komunikatu
        ↓
pierwsze opuszczenie komunikatu
```

Metryka mogłaby lepiej oddzielić:

```text
pierwsze zrozumienie
```

od:

```text
ponownego czytania
```

---

# 63. Regresje do action phrase

Można również sprawdzić, czy po przeczytaniu pytania uczestnik wraca wzrokiem do:

```text
action_phrase
```

Przykład:

```text
KOMUNIKAT
    ↓
PYTANIE
    ↓
← powrót do "Sprawdź dane karty"
    ↓
TAK
```

To mogłoby wskazywać, że odpowiedź wymaga ponownego sprawdzenia instrukcji.

---

# 64. Możliwe rozszerzenie – język ekspercki vs prosty

Zamiast:

```text
A_FORMAL
B_SIMPLE
```

można później przygotować:

```text
TECHNICAL
PLAIN LANGUAGE
```

np.:

```text
"nieprawidłowe dane uwierzytelniające"

vs.

"nieprawidłowe hasło"
```

---

# 65. Możliwe rozszerzenie – aktywna instrukcja

Porównanie:

```text
"Zweryfikuj dane karty"

vs.

"Sprawdź dane karty"
```

Badamy wtedy wpływ pojedynczego sposobu sformułowania call-to-action.

---

# 66. Możliwe rozszerzenie – komunikat bez instrukcji

Porównanie:

```text
opis problemu
```

vs.

```text
opis problemu + konkretne działanie
```

Pytanie:

> Czy dodanie jasnej instrukcji działania skraca czas potrzebny użytkownikowi na
> zrozumienie, co powinien zrobić?

---

# 67. Możliwe rozszerzenie – wyróżnienie action phrase

Porównanie:

```text
zwykły tekst
```

vs.

```text
pogrubiona instrukcja działania
```

Można wtedy mierzyć:

```text
ttff_action_s
action_dwell_s
accuracy
```

---

# 68. Możliwe rozszerzenie – ikona + tekst

Porównanie:

```text
sam komunikat tekstowy
```

vs.

```text
ikona + komunikat
```

Przykład:

```text
⚠ + błąd
✓ + sukces
```

To jednak wymagałoby przejścia z czystego `TextDataset` do bodźców obrazowych
lub bardziej złożonego layoutu.

---

# 69. Analiza statystyczna w badaniu właściwym

Dla większej liczby uczestników nie należy ograniczać się do średnich.

Najlepszym podejściem byłyby modele mieszane.

Przykładowo:

```text
message_dwell_s
~
version
+
(1 | participant)
+
(1 | item)
```

lub bardziej rozbudowany model:

```text
message_dwell_s
~
version
* answer
+
(1 | participant)
+
(1 | item)
```

---

# 70. Model dla accuracy

Dla zmiennej:

```text
correct
```

można zastosować mieszaną regresję logistyczną:

```text
correct
~
version
+
(1 | participant)
+
(1 | item)
```

---

# 71. Model dla liczby regresji

`regression_count` jest zmienną zliczeniową.

Przy większym badaniu można rozważyć:

```text
Poisson
```

lub:

```text
negative binomial
```

w zależności od rozkładu.

---

# 72. Ograniczenie interpretacji dwell time

Większy:

```text
message_dwell_s
```

może oznaczać:

- większą trudność,
- głębsze przetwarzanie,
- ponowne czytanie,
- większe zainteresowanie,
- problem z rozumieniem.

Dlatego dwell time należy interpretować razem z:

```text
accuracy
fixation count
regression count
```

a nie samodzielnie.

---

# 73. Ograniczenie interpretacji regresji

Regresja nie zawsze oznacza problem.

Czytelnik może wracać wzrokiem:

- aby potwierdzić informację,
- aby połączyć dwie części zdania,
- aby odpowiedzieć na pytanie,
- z powodu naturalnego stylu czytania.

Dlatego najbardziej interesująca jest różnica systematyczna:

```text
A_FORMAL
vs.
B_SIMPLE
```

a nie sama bezwzględna liczba regresji.

---

# 74. Rozwiązywanie typowych problemów

## Config nie został znaleziony

Sprawdź, czy polecenie jest uruchamiane z katalogu głównego repo:

```text
tobii-pytracker/
```

oraz czy istnieje:

```text
configs/config_ux_ab_demo.yaml
```

---

## Dataset nie został znaleziony

Config oczekuje:

```text
datasets/ux_ab_demo.csv
```

Sprawdź ścieżkę i bieżący katalog roboczy.

---

## Polskie znaki są niepoprawne

Plik CSV powinien być zapisany w UTF-8.

W poprawionej wersji projektu warto również jawnie używać UTF-8 podczas
odczytu configu i datasetu.

---

## Przycisk nadal pokazuje `NONE`

Sprawdź, czy poprawka:

```python
self.classes.append("nie wiem")
```

została zastosowana w źródle pakietu, który rzeczywiście jest uruchamiany.

Pomocne:

```bash
python -c "import tobii_pytracker.datasets.custom_dataset as m; print(m.__file__)"
```

---

## GUI działa, ale Tobii nie

Uruchom najpierw:

```bash
tobii-pytracker \
  --config_file configs/config_ux_ab_demo.yaml \
  --loop_count 2
```

Jeżeli GUI działa bez:

```text
--enable_eyetracker
```

to dataset i główny config są prawdopodobnie poprawne.

Należy wtedy diagnozować konfigurację:

- PsychoPy,
- ioHub,
- Tobii,
- `eyetracker_config.yaml`.

---

## `objects_bboxes` jest puste

Sprawdź:

```yaml
bbox_model: word
```

oraz wersję `TextDataset`.

Bez bboxów słów nie można automatycznie przypisać fiksacji do:

```text
message words
```

ani:

```text
action_phrase
```

---

## `action_seen = False` dla większości prób

Możliwe przyczyny:

- action phrase nie dopasowuje się do tokenów,
- różnica w interpunkcji lub zapisie,
- brak bboxów,
- zbyt mało danych gaze,
- zbyt restrykcyjna detekcja fiksacji.

Sprawdź zgodność:

```text
action_phrase
```

z:

```text
message_text
```

---

## Bardzo mało fiksacji

Najpierw sprawdź, czy `gaze_data` rzeczywiście zawiera próbki.

Dopiero potem zmieniaj parametry detektora.

Przykładowo można testowo użyć:

```text
dispersion threshold = 60 px
minimum duration = 0.08 s
```

ale parametry muszą być później stosowane konsekwentnie.

---

# 75. Minimalny workflow demo

Jeżeli celem jest krótka prezentacja techniczna:

```text
1. uruchom GUI test
2. pokaż jedną parę A/B
3. wykonaj 16 prób z Tobii
4. uruchom analizę
5. pokaż średni dwell time
6. pokaż fixation count
7. pokaż regression count
8. pokaż TTFF do action phrase
9. porównaj accuracy
```

---

# 76. Pełny workflow eksperymentu

```text
                   DATASET
                      │
                      ▼
              8 par komunikatów
                      │
             ┌────────┴────────┐
             ▼                 ▼
        A_FORMAL           B_SIMPLE
             │                 │
             └────────┬────────┘
                      ▼
                  TextDataset
                      │
                      ▼
            bbox_model = word
                      │
                      ▼
                 PsychoPy
                      │
                      ▼
               punkt fiksacji
                      │
                      ▼
             KOMUNIKAT + PYTANIE
                      │
                      ▼
                  Tobii gaze
                      │
                      ▼
                TAK / NIE
                      │
                      ▼
                   data.csv
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    cały komunikat            action_phrase
          │                       │
          ▼                       ▼
  message dwell              action seen
  fixation count               TTFF
  regressions                  dwell
          │                   fixations
          └───────────┬───────────┘
                      ▼
                   accuracy
                      │
                      ▼
              A_FORMAL vs B_SIMPLE
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       H1-H3         H4          H5
```

---

# 77. Najkrótsze podsumowanie eksperymentu

## Zadanie

Użytkownik czyta komunikat UX i odpowiada na pytanie sprawdzające zrozumienie.

```text
TAK / NIE
```

---

## Manipulacja

```text
A_FORMAL
vs.
B_SIMPLE
```

przy zachowaniu:

```text
tej samej sytuacji
tej samej liczby słów
tej samej poprawnej odpowiedzi
```

---

## Eye tracking

Badamy:

```text
ile fiksacji?
jak długo trwały?
ile było regresji?
jak szybko użytkownik znalazł instrukcję działania?
```

---

## Behavior

```text
TAK / NIE
poprawnie / błędnie
```

---

## Główne metryki

```text
message_dwell_s
message_fixation_count
regression_count
ttff_action_s
action_dwell_s
action_fixation_count
accuracy
```

---

## Hipotezy

```text
H1: B_SIMPLE < A_FORMAL dla message_dwell_s

H2: B_SIMPLE < A_FORMAL dla message_fixation_count

H3: B_SIMPLE < A_FORMAL dla regression_count

H4: B_SIMPLE >= A_FORMAL dla accuracy

H5: B_SIMPLE < A_FORMAL dla ttff_action_s
```

---

## Wartość demonstracyjna

> **Eye tracking pokazuje nie tylko, czy użytkownik poprawnie zrozumiał
> komunikat, ale również ile pracy wzrokowej było potrzebne, aby dojść do tej
> odpowiedzi.**

To pozwala przejść od prostego:

```text
który komunikat ma lepszą accuracy?
```

do bardziej użytecznego pytania UX:

```text
który komunikat jest równie dobrze rozumiany,
ale wymaga mniej pracy wzrokowej?
```
