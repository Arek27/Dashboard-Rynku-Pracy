# -*- coding: utf-8 -*-

import streamlit as st

@st.cache_data
def get_data():
    gdf = load_gminy("data/poland.municipalities.json")
    df = load_Wynagrodzenia("data/Wynagrodzenia.xlsx")
    return gdf, df


from loaders.geo import load_gminy
from loaders.wynagrodzenia import load_Wynagrodzenia
from components.mapa_mediana2 import mediana_gminy

st.set_page_config(
    page_title="Dashboard rynku pracy w Polsce",
    layout="wide"
)
st.title("Dashboard rynku pracy w Polsce")

top = st.container()
map_section = st.container()
bottom = st.container()

@st.cache_data
def load_data():
    gdf = load_gminy("data/poland.municipalities.json")
    df = load_Wynagrodzenia("data/Wynagrodzenia.xlsx")

    gdf = gdf.merge(
        df[["Kod", "Mediana"]],
        left_on="terc",
        right_on="Kod",
        how="left"
    )

    return gdf

gdf = load_data()

with map_section:
    st.subheader("Mediana wynagrodzenia wg gminy")
    mediana_gminy(gdf, "Mediana")

with top:
    col1, col2, col3 = st.columns(3)
    col1.metric("Placeholder", "—")
    col2.metric("Placeholder", "—")
    col3.metric("Placeholder", "—")

with bottom:
    st.subheader("Additional visualisations")
