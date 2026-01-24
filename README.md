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

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Requests
- Pliki danych:
  - `data/Wynagrodzenia.xlsx`
  - `data/poland.municipalities.json`

## Uruchomienie aplikacji

1. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

2. Upewnij się, że pliki danych znajdują się w katalogu `data/`.

3. Uruchom aplikację Streamlit:

```bash
streamlit run app.py
```

## Struktura projektu

```
.
├── app.py                       # Główna aplikacja Streamlit
├── components/
│   └── mapa_mediana2.py        # Komponent do rysowania mapy wynagrodzeń
├── loaders/
│   ├── geo.py                  # Loader danych geograficznych (GeoJSON)
│   └── wynagrodzenia.py        # Loader danych o wynagrodzeniach
├── data/
│   ├── Wynagrodzenia.xlsx      # Dane o wynagrodzeniach (lokalne)
│   └── poland.municipalities.json  # Granice gmin (GeoJSON)
└── README.md
```

## Uwagi

- Do korzystania z BDL API wymagany jest nagłówek `X-ClientId`. W kodzie znajduje się przykładowy identyfikator.
- Dane z BDL są cache’owane przez mechanizm `@st.cache_data`, aby uniknąć nadmiernych zapytań do API.

## Licencja

Projekt udostępniony na licencji MIT.
