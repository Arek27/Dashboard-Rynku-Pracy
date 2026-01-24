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
        get_fill_color="""
        selected ?
        [255, 0, 0, 220] :
        properties.fill_color
    """,

        get_line_color=[120, 120, 120],
        line_width_min_pixels=0.4,
    )
    minx, miny, maxx, maxy = gdf.total_bounds

    center_lon = (minx + maxx) / 2
    center_lat = (miny + maxy) / 2
  
    view_state = pdk.ViewState(
        longitude=center_lon,
        latitude=center_lat,
        zoom=5.7,
        min_zoom=5.5,
        max_zoom=7.5,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "text": "{name}\nMediana: {Mediana}"
            },
        ),
        use_container_width=True,
    )
