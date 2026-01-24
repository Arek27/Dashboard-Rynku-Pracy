import streamlit as st
import pydeck as pdk


def mediana_gminy(gdf, value_column: str):              #konwertuje obiekt GeoDataFrame do standardowego formatu GeoJSON za pomocą specjalnego interfejsu __geo_interface__.
    geojson = gdf.__geo_interface__

    layer = pdk.Layer(                                  #Tworzy obiekt warstwy mapy. Warstwa definiuje co i w jaki sposób będzie rysowane na mapie.
        "GeoJsonLayer",
        geojson,
        pickable=True,                                  #Umożliwia interakcję z obiektami na mapie:
        stroked=True,                                   #Włącza rysowanie obrysów obiektów geometrycznych, czyli konturów gmin.
        filled=True,                                    #Włącza wypełnianie obszarów gmin kolorem.
        get_fill_color="""                              
        selected ?
        [255, 0, 0, 220] :
        properties.fill_color
    """,                                                #Definiuje sposób ustalania koloru wypełnienia gminy

        get_line_color=[120, 120, 120],                 #Ustawia kolor obrysu gmin na stały odcień szarości
        line_width_min_pixels=0.4,
    )
  
    view_state = pdk.ViewState(                         #Tworzy obiekt, który definiuje początkowe ustawienie kamery mapy (położenie, przybliżenie oraz ograniczenia zoomu).
        longitude=19.0, 
        latitude=52.0,
        zoom=5.5,
        min_zoom=5.0,
        max_zoom=8.0,
    )

    st.pydeck_chart(                                  #Wywołuje funkcję Streamlit odpowiedzialną za renderowanie wykresów opartych na bibliotece pydeck
        pdk.Deck(                                     #Tworzy obiekt Deck, który stanowi główny kontener wizualizacji mapowej i łączy warstwy, widok oraz interakcje.
            layers=[layer],                           
            initial_view_state=view_state,            #Ustawia początkowy stan widoku mapy zgodnie z wcześniej zdefiniowanym obiektem view_state.
            tooltip={
                "text": "{name}\nMediana: {Mediana}"
            },                                        #Definiuje treść tooltipu wyświetlanego po najechaniu kursorem na gminę:
        ),
        use_container_width=True,
    )                                                 #Powoduje, że mapa automatycznie dopasowuje swoją szerokość do dostępnej przestrzeni w układzie aplikacji Streamlit.
