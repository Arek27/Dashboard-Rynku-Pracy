# Dashboard: Rynek Pracy

Aplikacja webowa stworzona w **Streamlit**, prezentująca dane z rynku pracy w Polsce. Źródłem danych jest API Banku Danych Lokalnych (BDL) GUS oraz pliki lokalne zawierające dane o wynagrodzeniach wg gmin.

## Funkcje

- Wskaźniki rynku pracy:  
  - Stopa bezrobocia  
  - Liczba bezrobotnych  
  - Liczba wolnych miejsc pracy  
  - Wskaźnik zatrudnienia  

- Wykresy trendów czasowych dla powyższych zmiennych  
- Interaktywna mapa mediany wynagrodzenia według gmin  
- Wybór konkretnej gminy i prezentacja jej danych: mediana, średnia oraz różnica wynagrodzenia  

## Źródła danych

- [BDL API GUS](https://bdl.stat.gov.pl/api/v1/)
- Plik `Wynagrodzenia.xlsx` (dane o wynagrodzeniach)
- Plik `poland.municipalities.json` (granice gmin)

## Wymagania

- Python 3.9+
- pip
- Przeglądarka internetowa (np. Chrome, Safari, Firefox)

### macOS / Linux

Dodatkowo wymagane:
- git (najczęściej preinstalowany w macOS)
- Terminal

### Windows

Dodatkowo wymagane:
- Git (np. z [git-scm.com](https://git-scm.com/))
- PowerShell lub CMD
- (Opcjonalnie) Wirtualne środowisko: `venv` lub `conda`

---

## Instalacja i uruchomienie

### macOS / Linux

Uruchom w terminalu:

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

1. Sklonuj repozytorium lub pobierz ZIP:

```powershell
git clone https://github.com/Arek27/Dashboard-Rynku-Pracy.git
cd Dashboard-Rynku-Pracy
```

2. Zainstaluj wymagane pakiety:

```powershell
pip install -r requirements.txt
```

3. Uruchom aplikację:

```powershell
.\run_app.bat
```

Aplikacja otworzy się automatycznie w przeglądarce.

Alternatywnie możesz użyć:

```powershell
python start.py
```

---

## Struktura projektu

```
.
├── app.py                       # Główna aplikacja Streamlit
├── start.py                     # Alternatywny sposób uruchomienia aplikacji
├── run.sh                       # Skrypt uruchamiający dla macOS/Linux
├── run_app.bat                  # Skrypt uruchamiający dla Windows
├── requirements.txt             # Lista zależności Pythona
├── .streamlit/
│   └── config.toml              # Konfiguracja aplikacji Streamlit
├── components/
│   └── mapa_mediana2.py         # Komponent do rysowania mapy wynagrodzeń
├── loaders/
│   ├── geo.py                   # Loader danych geograficznych (GeoJSON)
│   └── wynagrodzenia.py         # Loader danych o wynagrodzeniach
├── data/
│   ├── Wynagrodzenia.xlsx       # Dane o wynagrodzeniach (lokalne)
│   └── poland.municipalities.json  # Granice gmin (GeoJSON)
└── README.md
```

## Uwagi

- Do korzystania z BDL API wymagany jest nagłówek `X-ClientId`. W kodzie znajduje się przykładowy identyfikator.
- Dane z BDL są cache’owane przez mechanizm `@st.cache_data`, aby uniknąć nadmiernych zapytań do API.
- Pliki z danymi muszą znajdować się w katalogu `data/`.

## Licencja

Projekt udostępniony na licencji MIT.

