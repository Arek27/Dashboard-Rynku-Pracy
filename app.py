# -*- coding: utf-8 -*-                #Deklaracja kodowania pliku źródłowego. Informuje interpreter Pythona, że plik zapisany jest w kodowaniu UTF-8, co umożliwia poprawne używanie znaków spoza ASCII
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
import streamlit as st
import pandas as pd
import requests

from loaders.geo import load_gminy                                                 #import funkcji z folderu loaders służącej do załadowania danych dotyczących współrzędnych gmin w Polsce
from loaders.wynagrodzenia import load_Wynagrodzenia                               #import funkcji z folderu loaders służącej do załadowania danych dotyczących średniej i mediany wynagrodzeń w polskich gminach
from components.mapa_mediana2 import mediana_gminy                                 #import funkcji odpowiedzialnej za wyświetlanie mapy mediany wynagrodzeń w Polskich gminach

st.set_page_config(                                                                #konfiguruje podstawowe parametry strony aplikacji Streamlit.
    page_title="Dashboard",                                           #ustawienie tytułu strony wyświetlanego w karcie przeglądarki
    layout="wide"                                                                  #Ustawienie szerokiego układu strony
)

st.title("Dashboard: Rynek Pracy")                                                 # ustawienie głównego tytułu aplikacji w interfejsie użytkownika Streamlit.

HEADERS = {"X-ClientId": "9d4c3601-0cfe-46c6-549f-08de2b04124b"}                   #klucz do API BDL

@st.cache_data                                                                     #dekorator Streamlit, który włącza mechanizm cache’owania wyników poniższej funkcji
def fetch_data_bdl(var_id, years):                                                 #Definicja funkcji odpowiedzialnej za pobieranie danych z BDL dla wskazanej zmiennej oraz zakresu lat.
    url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{var_id}"              #Budowanie adresu API BDL
    params = {"format": "json", "year": [str(y) for y in years]}                   #Tworzy parametry zapytania HTTP, w tym format odpowiedzi (JSON) oraz listę lat przekazywaną jako tekst.
    r = requests.get(url, headers=HEADERS, params=params)                          #Wysyła żądanie HTTP GET do API GUS z wymaganymi nagłówkami autoryzacyjnymi.
    r.raise_for_status()                                                           #Wymusza zgłoszenie wyjątku w przypadku błędu HTTP, co zapobiega dalszemu przetwarzaniu niepoprawnych danych
    for unit in r.json()["results"]:
        if unit["id"] == "000000000000":                                           #Wybiera dane zagregowane dla całego kraju
            return unit["values"]
    return []


def get_SB():                                                                                     #Definicja funkcji odpowiedzialnej za przygotowanie danych dotyczących stopy bezrobocia rejestrowanego w ujęciu miesięcznym.
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P3559", "page-size": 100, "lang": "pl"}                              #subject-id ogranicza wyniki do obszaru tematycznego rynku pracy, page-size określa maksymalną liczbę rekordów, lang ustawia język metadanych na polski.
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])        #Wysyła zapytanie HTTP do API GUS i zapisuje zmienne w formacie Data Frame
    df = df[df["n2"] == "stopa bezrobocia rejestrowanego"]                                        #filtruje zbiór zmiennych, pozostawiając wyłącznie te, które dotyczą stopy bezrobocia rejestrowanego.

       #część kodu utworzonego przy użyciu AI"
    rows = []                                                                                     #Inicjalizuje listę, do której będą zapisywane przetworzone obserwacje czasowe.
    for _, row in df.iterrows():
        values = fetch_data_bdl(row["id"], range(2020, 2026))                                     #Pobieranie wartości zmiennych z lat 2020-2026
        for v in values:
            rows.append({"rok": int(v["year"]), "miesiąc": row["n1"], "wartość": v["val"]})       #rozbija dane na pojedyncze obserwacje zawierające odpowiednio rok, miesiąc i wartość stopy bezrobocia

    months = [                                                                                    #lista miesięcy zapisanych w chronologicznej kolejności
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]

    df_final = pd.DataFrame(rows)                                                                  #Stworzenie ostatecznej ramki danych, posrtowanymi chronologicznie
    df_final["miesiąc"] = pd.Categorical(df_final["miesiąc"], categories=months, ordered=True)     #Ustawia kolumnę „miesiąc” jako zmienną kategoryczną z określoną kolejnością, co zapobiega sortowaniu alfabetycznemu.
    return df_final.sort_values(["rok", "miesiąc"]).reset_index(drop=True)                         #Sortuje dane chronologicznie (rok → miesiąc) i resetuje indeks, zwracając gotowy zbiór danych do dalszej analizy
       #koniec części kodu utworzonego przy użyciu AI"

def get_bezrobotni():                                                                              #Definicja funkcji, której zadaniem jest pobranie i przygotowanie danych dotyczących liczby bezrobotnych w ujęciu miesięcznym.
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P2961", "page-size": 100, "lang": "pl"}                               #subject-id ogranicza wyniki do obszaru tematycznego bezrobocia, page-size określa maksymalną liczbę rekordów, lang ustawia język metadanych na polski.
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])         #Wysyła zapytanie HTTP do API GUS i zapisuje zmienne w formacie Data Frame
    df = df[df["n2"].str.contains("ogółem", case=False, na=False)].copy()                          #Filtruje pobrane dane, pozostawiając wyłącznie te zmienne, które dotyczą wartości liczby bezrobotnych ogółem

        #część kodu utworzonego przy użyciu AI"                                                    #Ta częśc kodu służy do tego samego co w przypadku funkcji get_SB
    rows = []                                                                                      #w celu zrozumienia tej części kodu proszę spojrzeć na komentarze użyte do opisania funkcji get_SB
    for _, row in df.iterrows():
        values = fetch_data_bdl(row["id"], range(2020, 2026))
        for v in values:
            rows.append({"rok": int(v["year"]), "miesiąc": row["n1"], "wartość": v["val"]})

    months = [
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]

    df_final = pd.DataFrame(rows)
    df_final["miesiąc"] = pd.Categorical(df_final["miesiąc"], categories=months, ordered=True)
    return df_final.sort_values(["rok", "miesiąc"]).reset_index(drop=True)
        #koniec części kodu utworzonego przy użyciu AI"

def get_WMP():                                                                                 #Definicja funkcji odpowiedzialnej za pobranie i przygotowanie danych dotyczących nowo utworzonych wolnych miejsc pracy w ujęciu rocznym.
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P4294", "page-size": 50, "lang": "pl"}                            #subject-id ogranicza wyniki do obszaru tematycznego nowoutworzonych wolnych miejsc pracy, page-size określa maksymalną liczbę rekordów, lang ustawia język metadanych na polski.
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])     #Wysyła zapytanie HTTP do API GUS i zapisuje zmienne w formacie Data Frame
    var = df[df["n1"] == "wolne miejsca pracy"].iloc[0]                                        #Filtruje pobrane dane, pozostawiając jedynie kategorie „wolne miejsca pracy”
    values = fetch_data_bdl(var["id"], range(2010, 2026))                                      #Pobieranie wartości zmiennych z lat 2010-2026

    df_final = pd.DataFrame(values)
    df_final["rok"] = df_final["year"].astype(int)                                             #Tworzy nową kolumnę „rok” poprzez konwersję pola tekstowego year na typ liczbowy
    df_final["wartość"] = df_final["val"].astype(float)                                        #Tworzy kolumnę „wartość”, która zawiera faktyczną liczbę wolnych miejsc pracy
    return df_final[["rok", "wartość"]].sort_values("rok")                                     #sortuje dane rosnąco według roku i zwraca gotowy zbiór danych do dalszej analizy


def get_wsk_zatrudnienia():                                                                    #Definicja funkcji odpowiedzialnej za pobranie i przygotowanie danych dotyczących wskaźnika zatrudnienia w ujęciu kwartalnym.
    quarters = {                                                                               #Słownik mapujący nazwy kwartałów na odpowiadające im identyfikatory zmiennych w BDL
        "1 kwartał": 1615457,
        "2 kwartał": 1615511,
        "3 kwartał": 1615565,
        "4 kwartał": 1615619
    }
               #część kodu utworzonego przy użyciu AI"
    rows = []
    for kwartal, var_id in quarters.items():
        values = fetch_data_bdl(var_id, range(2020, 2026))                                      #Pobieranie wartości zmiennych z lat 2020-2026
        for v in values:
            rows.append({"rok": int(v["year"]), "kwartał": kwartal, "wartość": v["val"]})

    kw_order = ["1 kwartał", "2 kwartał", "3 kwartał", "4 kwartał"]                             #Lista definiująca poprawną, chronologiczną kolejność kwartałów

    df = pd.DataFrame(rows)                                                                     #Stworzenie ostatecznej ramki danych, posrtowanymi chronologicznie
    df["kwartał"] = pd.Categorical(df["kwartał"], categories=kw_order, ordered=True)            #Konwertuje kolumnę „kwartał” na zmienną kategoryczną z określoną kolejnością, co zapobiega sortowaniu alfabetycznemu.
    return df.sort_values(["rok", "kwartał"]).reset_index(drop=True)                            #Sortuje dane najpierw według roku, a następnie według kwartału i zwracagotowy do dlaszej analizy zbiór danych
               #koniec części kodu utworzonego przy użyciu AI"

def show_metric(col, df, label, jednostka="", reverse_colors=False):                            #Definicja funkcji pomocniczej odpowiedzialnej za wyświetlanie najnowszej zmiany wskaźników w aplikacji streamlit
    val = df["wartość"].iloc[-1]                                                                #Pobiera ostatnią wartość wskaźnika z kolumny „wartość”
    prev = df["wartość"].iloc[-2]                                                               #Pobiera wartość zmiennej z poprzedniego okresu
    delta = round(val - prev, 2)                                                                #Oblicza indeks łańcuchowy i zaokrągla liczbę do dwóch miejsc po przecinku

    # Jeśli reverse_colors = True, zmiana dodatnia jest zła (np. bezrobocie)
    if reverse_colors:
        delta_color = "inverse" if delta > 0 else "normal"
    else:
        delta_color = "normal" if delta > 0 else "inverse"

    col.metric(label, f"{val} {jednostka}", f"{delta:+} {jednostka}", delta_color=delta_color)   #Wyświetla metrykę KPI w interfejsie użytkownika: label – opis metryki, druga wartość – aktualna wartość wskaźnika wraz z jednostką, trzecia wartość – zmiana względem poprzedniego okresu, delta_color – sposób kolorowania zmiany.

# === Wskaźniki ===

col1, col2, col3, col4 = st.columns(4)                                                       #Tworzy cztery kolumny w układzie interfejsu Streamlit o równej szerokości i przypisuje je do zmiennych col1, col2, col3 oraz col4.
                                                                                             #Kolumny te będą wykorzystywane do równoległego wyświetlania metryk KPI w jednym wierszu.

stopa_bezrobocia = get_SB()
bezrobotni = get_bezrobotni()
WMP = get_WMP()
wsk_zatrudnienia = get_wsk_zatrudnienia()

show_metric(col1, stopa_bezrobocia, "Stopa bezrobocia", "%", reverse_colors=True)           #Wyświetla w pierwszej kolumnie wskaźnik prezentujujący aktualną stopę bezrobocia wraz ze zmianą względem poprzedniego okresu, wyrażoną w procentach.
show_metric(col2, bezrobotni, "Bezrobotni (ogółem)", "os.", reverse_colors=True)            #Wyświetla w drugiej kolumnie wskaźnik prezentujujący aktualną liczbę bezrobotnych wraz ze zmianą względem poprzedniego okresu, wyrażoną w liczbie osób.
show_metric(col3, WMP, "Wolne miejsca pracy", "tys.", reverse_colors=False)                 #Wyświetla w trzeciej kolumnie wskaźnik prezentujujący liczbę wolnych miejsc pracy wraz ze zmianą względem poprzedniego okresu, tysiącach.
show_metric(col4, wsk_zatrudnienia, "Wskaźnik zatrudnienia", "%", reverse_colors=False)     #Wyświetla w czwartej kolumnie wskaźnik prezentujujący aktualny wskaźnik zatrudnienia wraz ze zmianą względem poprzedniego okresu, wyrażoną w procentach.

# === Wykresy Trendu ===

st.subheader("Trendy czasowe")

chart_col1, chart_col2 = st.columns(2)                                                 #Tworzy dwie kolumny o równej szerokości, które umożliwiają równoległe wyświetlenie dwóch wykresów w jednym wierszu.

with chart_col1:                                                                       #Stworzenie wykresu zmian w czasie watrości stopy bezrobocia, przy użyciu wcześniej zdefiniowanych funkcji
    st.markdown("#### Stopa bezrobocia")
    df = stopa_bezrobocia.copy()
    df["czas"] = df["rok"].astype(str) + "-" + df["miesiąc"].astype(str)               #Tworzy nową kolumnę „czas”, łącząc rok i miesiąc w jeden tekstowy znacznik
    st.line_chart(df.set_index("czas")["wartość"])                                     #Wyświetla wykres liniowy przedstawiający zmiany stopy bezrobocia w czasie

with chart_col2:
    st.markdown("#### Bezrobotni zarejestrowani")
    df = bezrobotni.copy()
    df["czas"] = df["rok"].astype(str) + "-" + df["miesiąc"].astype(str)                #Tworzy nową kolumnę „czas”, łącząc rok i miesiąc w jeden tekstowy znacznik
    st.line_chart(df.set_index("czas")["wartość"])                                      #Wyświetla wykres liniowy przedstawiający zmianę wartości liczby bezrobotnych w czasie.

chart_col3, chart_col4 = st.columns(2)                                                  #Tworzy dwie kolumny o równej szerokości, które umożliwiają równoległe wyświetlenie dwóch wykresów w jednym wierszu.

with chart_col3:
    st.markdown("#### Wolne miejsca pracy")
    st.bar_chart(WMP.set_index("rok")["wartość"])                                       #Wyświetla wykres słupkowy przedstawiający zmianę wartości liczby wolnych miejsc pracy w czasie.

with chart_col4:
    st.markdown("#### Wskaźnik zatrudnienia")
    df = wsk_zatrudnienia.copy()
    df["czas"] = df["rok"].astype(str) + " " + df["kwartał"].astype(str)                #Tworzy nową kolumnę „czas”, łącząc rok i kwartał w jeden tekstowy znacznik
    st.line_chart(df.set_index("czas")["wartość"])                                      #Wyświetla wykres liniowy przedstawiający zmiane wartości wsk. zatrudnienia w czasie


# === MAPA MEDIANA GMIN ===

st.subheader("Mediana wynagrodzenia wg gminy")                                          #Wyświetlenie nagłówka dla nowej sekcji dashboardu

@st.cache_data                                                                          #dekorator Streamlit, który włącza mechanizm cache’owania wyników poniższej funkcji
def load_data():                                                                        #definicja funkcji służącej do pobrania danych potrzebnych do utworzenia mapy z medianą wynagrodzeń w polskich gminach
    gdf = load_gminy("data/poland.municipalities.json")                                 #wykorzystanie wcześniej zaimportowanej funkcji do załadowania danych o położeniu geograficznym polskich gmin
    df = load_Wynagrodzenia("data/Wynagrodzenia.xlsx")                                  #wykorzystanie wcześniej zaimportowanej funkcji do załadowania danych o medianie i średniej wynagrodzenia w polskich gminach

    gdf = gdf.merge(                                                                    #utworzenie nowego zbioru danych poprzez dołączenie do zbioru z współrzędnymi geograficznymi informacji o medianie i średniej wynagrodzeń, na podstawie kodu TERYT
        df[["Kod", "Mediana", "Średnia"]],
        left_on="terc",
        right_on="Kod",
        how="left"
    )

    vmin = gdf["Mediana"].min()                                                         #wyznaczenie minimalnej a następnie maksymalnej wartości mediany do normalizacji palety kolorów użytej do wykresu mapy
    vmax = gdf["Mediana"].max()
    norm = colors.Normalize(vmin=vmin, vmax=vmax)                                       #Tworzy obiekt normalizujący wartości mediany do zakresu od 0 do 1, co jest wymagane do poprawnego mapowania wartości na kolory.
    cmap = cm.get_cmap("YlGnBu")                                                        #Pobiera skalę kolorów „YlGnBu”, która będzie używana do wizualnego przedstawienia poziomu mediany wynagrodzeń na mapie.

#część kodu utworzonego przy użyciu AI"
    def colorize(value):                                                                #Definicja funkcji pomocniczej, która zamienia wartość mediany wynagrodzenia na kolor w formacie RGBA.
        if np.isnan(value):                                                             #Obsługuje brak danych – gminy bez informacji o medianie wynagrodzeń otrzymują neutralny, szary kolor.
            return [211, 211, 211, 200]
        r, g, b, _ = cmap(norm(value))                                                  #Mapuje znormalizowaną wartość mediany na kolor z wybranej palety barw.
        return [int(r * 255), int(g * 255), int(b * 255), 200]                          #Konwertuje wartości kolorów z zakresu 0–1 do zakresu 0–255 i ustawia stałą przezroczystość.

    gdf["fill_color"] = gdf["Mediana"].apply(colorize)                                  #Tworzy nową kolumnę fill_color, zawierającą kolor przypisany do każdej gminy na podstawie mediany wynagrodzeń.
    return gdf
#koniec części kodu utworzonego przy użyciu AI"

gdf = load_data()

selected_name = st.selectbox(                                                           #Tworzy listę rozwijaną (selectbox) w interfejsie Streamlit, umożliwiającą użytkownikowi wybór jednej gminy.
    "Wybierz gminę",
    options=sorted(gdf["name"].dropna().unique())
)

selected_row = gdf[gdf["name"] == selected_name].iloc[0]                                #stworzenie ramki danych która zawiera komplet danych (geometrycznych i statystycznych) dla wybranej gminy.
gdf["selected"] = gdf["name"] == selected_name                                          #Tworzy nową zmienną, która przyjmuje wartość True dla wybranej gminy oraz False dla pozostałych. Informacja ta jest wykorzystywana do wyróżnienia zaznaczonej gminy na mapie.

mediana_gminy(gdf, "Mediana")                                                           #Wywołuje wcześniej zaimportowaną funkcję odpowiedzialną za renderowanie mapy gmin

col1, col2, col3 = st.columns(3)                                                        #Tworzy trzy kolumny w interfejsie użytkownika, które posłużą do równoległego wyświetlenia metryk opisujących wynagrodzenia dla wybranej gminy.

col1.metric("Mediana wynagrodzenia", f"{selected_row['Mediana']:.0f} PLN")              #Wyświetla w pierwszej kolumnie metrykę prezentującą medianę wynagrodzenia dla wybranej gminy, wyrażoną w polskich złotych
col2.metric("Średnie wynagrodzenie", f"{selected_row['Średnia']:.0f} PLN")              #Wyświetla w drugiej kolumnie metrykę prezentującą średnią wynagrodzenia dla wybranej gminy, wyrażoną w polskich złotych
col3.metric("Różnica (Średnia − Mediana)", f"{(selected_row['Średnia'] - selected_row['Mediana']):.0f} PLN")           #Wyświetla w trzeciej kolumnie metrykę prezentującą różnicę między średnim a medianą wynagrodzenia dla wybranej gminy, wyrażoną w polskich złotych
