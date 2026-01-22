import streamlit as st
import pydeck as pdk


def mediana_gminy(gdf, value_column: str):
    geojson = gdf.__geo_interface__

    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        pickable=True,
        stroked=True,
        filled=True,
        get_fill_color=f"""
            [
                255,
                255 - ({value_column} / 50),
                120,
                180
            ]
        """,
        get_line_color=[90, 90, 90],
        line_width_min_pixels=0.4,
    )

    view_state = pdk.ViewState(
        longitude=19.0,
        latitude=52.0,
        zoom=5.5,
        min_zoom=5.0,
        max_zoom=8.0,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "{name}\nMediana: {Mediana}"
        },
    )

    st.pydeck_chart(deck, use_container_width=True)
