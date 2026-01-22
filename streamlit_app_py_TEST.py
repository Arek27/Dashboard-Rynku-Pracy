# -*- coding: utf-8 -*-
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import streamlit as st


@st.cache_data
def get_data():
    gdf = load_gminy("data/poland.municipalities.json")
    df = load_Wynagrodzenia("data/Wynagrodzenia.xlsx")
    return gdf, df


from loaders.geo import load_gminy
from loaders.wynagrodzenia import load_Wynagrodzenia
from components.mapa_mediana2 import mediana_gminy

HEADERS = {"X-ClientId": "9d4c3601-0cfe-46c6-549f-08de2b04124b"}

st.set_page_config(
    page_title="Dashboard rynku pracy w Polsce",
    layout="wide"
)
st.title("Dashboard rynku pracy w Polsce")

top = st.container()
map_section = st.container()
bottom = st.container()

def get_WMP():
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {
        "subject-id": "P4294",
        "page-size": 50,
        "lang": "pl"
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["results"])

df_vars = get_WMP()

def get_yearly_data(var_id, years):
    url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{var_id}"
    params = {
        "format": "json",
        "year": [str(y) for y in years]
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()

    results = resp.json()["results"]

    for unit in results:
        if unit["id"] == "000000000000":  # Polska
            return unit["values"]

    return []

years = list(range(2010, 2025))
values = get_yearly_data(var_id, years)
# wybieramy zmienną "wolne miejsca pracy"
var_wolne = df_vars[df_vars["n1"] == "wolne miejsca pracy"].iloc[0]
var_id = var_wolne["id"]
df_roczne = pd.DataFrame(values)
df_roczne["rok"] = df_roczne["year"].astype(int)
df_roczne["wartość"] = df_roczne["val"]
df_roczne = df_roczne[["rok", "wartość"]]
st.subheader("Wolne miejsca pracy w Polsce (dane roczne)")

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df_roczne["rok"], df_roczne["wartość"], color="steelblue")

ax.set_title("Wolne miejsca pracy — Polska")
ax.set_xlabel("Rok")
ax.set_ylabel("Liczba wolnych miejsc pracy")

# bez notacji naukowej
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.ticklabel_format(style="plain", axis="y")

ax.set_xticks(df_roczne["rok"])
ax.set_xticklabels(df_roczne["rok"], rotation=45)

st.pyplot(fig)

@st.cache_data
def load_data():
    gdf = load_gminy("data/poland.municipalities.json")
    df = load_Wynagrodzenia("data/Wynagrodzenia.xlsx")

    gdf = gdf.merge(
        df[["Kod", "Mediana", "Średnia"]],
        left_on="terc",
        right_on="Kod",
        how="left"
    )
    
    vmin = gdf["Mediana"].min()
    vmax = gdf["Mediana"].max()

    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap("YlGnBu")

    def colorize(value):
        if np.isnan(value):
            return [211, 211, 211, 200]  # lightgray like Folium
        r, g, b, _ = cmap(norm(value))
        return [int(r*255), int(g*255), int(b*255), 200]

    gdf["fill_color"] = gdf["Mediana"].apply(colorize)
    return gdf

gdf = load_data()


with top:
    selected_name = st.selectbox(
        "Wybierz gminę",
        options=sorted(gdf["name"].dropna().unique())
    )

selected_row = gdf[gdf["name"] == selected_name].iloc[0]

gdf["selected"] = gdf["name"] == selected_name
with map_section:
    st.subheader("Mediana wynagrodzenia wg gminy")
    mediana_gminy(gdf, "Mediana")
with bottom:
    col1, col2, col3 = st.columns(3)

col1.metric(
    "Mediana wynagrodzenia",
    f"{selected_row['Mediana']:.0f} PLN"
)

col2.metric(
    "Średnie wynagrodzenie",
    f"{selected_row['Średnia']:.0f} PLN"
)

col3.metric(
    "Różnica (Średnia − Mediana)",
    f"{(selected_row['Średnia'] - selected_row['Mediana']):.0f} PLN"
)

