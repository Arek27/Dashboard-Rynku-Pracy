# Dashboard: Rynek Pracy

Aplikacja webowa stworzona w **Streamlit**, prezentująca dane z rynku pracy w Polsce. Źródłem danych jest API Banku Danych Lokalnych (BDL) GUS oraz pliki lokalne zawierające dane o wynagrodzeniach wg gmin udostępnione przez GUS.

---

## Charakterystyka oprogramowania

**Nazwa skrócona:**  
Dashboard Pracy

**Nazwa pełna:**  
Dashboard: Rynek Pracy w Polsce

**Opis i cele:**  
Interaktywny dashboard umożliwiający analizę statystyk rynku pracy w Polsce. Dane pochodzą z Banku Danych Lokalnych GUS – część danych jest pobierana dynamicznie przez API, natomiast dane o wynagrodzeniach wg gmin zostały pobrane ręcznie i zapisane w repozytorium jako pliki lokalne.

Celem projektu jest zapewnienie prostego w użyciu narzędzia do wizualnej analizy bezrobocia, zatrudnienia oraz wynagrodzeń na poziomie lokalnym (gminy), dostępnego lokalnie bez potrzeby wdrażania na serwerze.

---

## Prawa autorskie

**Autor:**  
Aleksandra Belowska, Arkadiusz Gałczyński, Hanna Jasik

**Licencja:**  
Projekt udostępniony na licencji MIT. Dane pochodzą z publicznych zasobów GUS i są wykorzystywane zgodnie z zasadami otwartych danych.

---

## Funkcje

- Wskaźniki rynku pracy:  
  - Stopa bezrobocia  
  - Liczba bezrobotnych  
  - Liczba wolnych miejsc pracy  
  - Wskaźnik zatrudnienia  

- Wykresy trendów czasowych dla powyższych zmiennych  
- Interaktywna mapa mediany wynagrodzenia według gmin  
- Wybór konkretnej gminy i prezentacja jej danych: mediana, średnia oraz różnica wynagrodzenia  

---

## Specyfikacja wymagań

| ID   | Nazwa                         | Opis                                                                 | Priorytet | Kategoria        | Moduł     |
|------|-------------------------------|----------------------------------------------------------------------|-----------|------------------|-----------|
| F-01 | Wyświetlanie wskaźników        | Prezentacja 4 kluczowych wskaźników rynku pracy                      | 1         | funkcjonalne     | Dashboard |
| F-02 | Wykresy trendów               | Wizualizacja zmian w czasie                                          | 1         | funkcjonalne     | Dashboard |
| F-03 | Mapa wynagrodzeń              | Mapa gmin z kolorowaniem wg mediany wynagrodzeń                      | 1         | funkcjonalne     | Mapa      |
| F-04 | Wybór gminy                   | Wyświetlenie danych wybranej gminy                                   | 1         | funkcjonalne     | Mapa      |
| NF-01| Buforowanie danych            | Ograniczenie liczby zapytań do API                                   | 2         | pozafunkcjonalne | API       |
| NF-02| Uruchamianie lokalne           | Działanie na Windows, macOS, Linux                                   | 1         | pozafunkcjonalne | System    |

---

## Architektura systemu

### Architektura rozwoju

| Technologia        | Przeznaczenie                                 | Wersja  |
|--------------------|----------------------------------------------|---------|
| Python             | Główny język                                 | 3.9+    |
| Streamlit          | Interfejs webowy                             | 1.30.0  |
| Pandas             | Analiza danych                               | 2.x     |
| NumPy              | Operacje numeryczne                          | 1.26.x  |
| Matplotlib         | Wykresy i kolorowanie map                   | 3.x     |
| Requests           | Komunikacja z API BDL                       | 2.x     |
| Git / GitHub       | Kontrola wersji                             | -       |
| Visual Studio Code | Edytor kodu                                 | -       |

### Architektura uruchomieniowa

| Technologia       | Przeznaczenie                    | Wersja |
|-------------------|----------------------------------|--------|
| Python            | Uruchomienie aplikacji           | 3.9+   |
| pip               | Instalacja zależności            | 23+    |
| Streamlit         | Silnik aplikacji webowej         | 1.30.0 |
| System operacyjny | Windows / macOS / Linux          | -      |
| Przeglądarka      | Interfejs użytkownika            | -      |

---

## Testy

### Scenariusze testów

| ID   | Nazwa testu               | Wejście                         | Oczekiwany rezultat                               |
|------|---------------------------|----------------------------------|---------------------------------------------------|
| T-01 | Start aplikacji           | Uruchomienie                     | Widoczne wszystkie metryki                        |
| T-02 | Wykresy                   | Przegląd sekcji trendów          | Poprawne wykresy                                  |
| T-03 | Mapa                      | Wejście do sekcji mapy           | Widoczna mapa gmin                                |
| T-04 | Wybór gminy               | Wybór z listy                    | Wyświetlenie danych gminy                         |
| T-05 | Buforowanie               | Odświeżenie aplikacji            | Szybsze ładowanie                                 |
| T-06 | Windows                   | `run_app.bat`                    | Uruchomienie w przeglądarce                       |
| T-07 | macOS/Linux               | `run.sh`                         | Uruchomienie w przeglądarce                       |

---

## Źródła danych

- [BDL API GUS](https://bdl.stat.gov.pl/api/v1/)
- Plik `Wynagrodzenia.xlsx`  
  Źródło: GUS BDL – podgrupa:  
  *Mediana wynagrodzeń miesięcznych brutto według badania „Rozkład wynagrodzeń w gospodarce narodowej” (P4610),  
  Przeciętne miesięczne wynagrodzenie brutto według badania „Rozkład wynagrodzeń w gospodarce narodowej” (P4609); czerwiec 2025*
- Plik `poland.municipalities.json` (granice gmin)

---

## Wymagania

- Python 3.9+
- pip
- Przeglądarka internetowa (np. Chrome, Safari, Firefox)

### macOS / Linux

Dodatkowo wymagane:
- git
- Terminal

### Windows

Dodatkowo wymagane:
- Git
- PowerShell lub CMD

---

## Instalacja i uruchomienie

Poniższe polecenia należy wykonać w terminalu systemowym:

---

### macOS / Linux

Otwórz **Terminal** i wpisz kolejno:

```bash
git clone https://github.com/Arek27/Dashboard-Rynku-Pracy.git
cd Dashboard-Rynku-Pracy
pip install -r requirements.txt
chmod +x run.sh
./run.sh
```

Aplikacja otworzy się automatycznie w domyślnej przeglądarce.

---

### Windows

Otwórz **PowerShell** lub **Wiersz polecenia (CMD)** i wpisz:

```powershell
git clone https://github.com/Arek27/Dashboard-Rynku-Pracy.git
cd Dashboard-Rynku-Pracy
pip install -r requirements.txt
.\run_app.bat
```

Alternatywnie możesz uruchomić aplikację poleceniem:

```powershell
python start.py
```

Po chwili aplikacja zostanie otwarta automatycznie w przeglądarce.

---

## Struktura projektu

```
.
├── app.py
├── start.py
├── run.sh
├── run_app.bat
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── components/
│   └── mapa_mediana2.py
├── loaders/
│   ├── geo.py
│   └── wynagrodzenia.py
├── data/
│   ├── Wynagrodzenia.xlsx
│   └── poland.municipalities.json
└── README.md
```

---

## Uwagi

- Do korzystania z BDL API wymagany jest nagłówek `X-ClientId`.
- Dane są cache’owane przez `@st.cache_data`.
- Pliki z danymi muszą znajdować się w katalogu `data/`.

---

## Licencja

Projekt udostępniony na licencji MIT.
