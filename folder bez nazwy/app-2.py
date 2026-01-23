import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Dashboard: Rynek Pracy",
    layout="wide"
)

HEADERS = {"X-ClientId": "9d4c3601-0cfe-46c6-549f-08de2b04124b"}

st.title("Dashboard: Rynek Pracy")


@st.cache_data
def fetch_data_bdl(var_id, years):
    url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{var_id}"
    params = {"format": "json", "year": [str(y) for y in years]}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    for unit in r.json()["results"]:
        if unit["id"] == "000000000000":
            return unit["values"]
    return []


def get_stop_bezrobocia_df():
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P3559", "page-size": 100, "lang": "pl"}
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])
    df = df[df["n2"] == "stopa bezrobocia rejestrowanego"]

    rows = []
    for _, row in df.iterrows():
        values = fetch_data_bdl(row["id"], range(2020, 2026))
        for v in values:
            rows.append({"rok": int(v["year"]), "miesiąc": row["n1"], "wartość": v["val"]})

    miesiace_order = [
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]

    df_final = pd.DataFrame(rows)
    df_final["miesiąc"] = pd.Categorical(df_final["miesiąc"], categories=miesiace_order, ordered=True)
    return df_final.sort_values(["rok", "miesiąc"]).reset_index(drop=True)


def get_bezrobotni_df():
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P2961", "page-size": 100, "lang": "pl"}
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])
    df = df[df["n2"].str.contains("ogółem", case=False, na=False)].copy()

    rows = []
    for _, row in df.iterrows():
        values = fetch_data_bdl(row["id"], range(2020, 2026))
        for v in values:
            rows.append({"rok": int(v["year"]), "miesiąc": row["n1"], "wartość": v["val"]})

    miesiace_order = [
        "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]

    df_final = pd.DataFrame(rows)
    df_final["miesiąc"] = pd.Categorical(df_final["miesiąc"], categories=miesiace_order, ordered=True)
    return df_final.sort_values(["rok", "miesiąc"]).reset_index(drop=True)


def get_wolne_miejsca_df():
    url = "https://bdl.stat.gov.pl/api/v1/variables"
    params = {"subject-id": "P4294", "page-size": 50, "lang": "pl"}
    df = pd.DataFrame(requests.get(url, headers=HEADERS, params=params).json()["results"])
    var = df[df["n1"] == "wolne miejsca pracy"].iloc[0]
    values = fetch_data_bdl(var["id"], range(2010, 2026))

    df_final = pd.DataFrame(values)
    df_final["rok"] = df_final["year"].astype(int)
    df_final["wartość"] = df_final["val"]
    return df_final[["rok", "wartość"]].sort_values("rok")


def get_zatrudnienie_df():
    quarters = {
        "1 kwartał": 1615457,
        "2 kwartał": 1615511,
        "3 kwartał": 1615565,
        "4 kwartał": 1615619
    }

    rows = []
    for kwartal, var_id in quarters.items():
        values = fetch_data_bdl(var_id, range(2020, 2026))
        for v in values:
            rows.append({"rok": int(v["year"]), "kwartał": kwartal, "wartość": v["val"]})

    kw_order = ["1 kwartał", "2 kwartał", "3 kwartał", "4 kwartał"]

    df = pd.DataFrame(rows)
    df["kwartał"] = pd.Categorical(df["kwartał"], categories=kw_order, ordered=True)
    return df.sort_values(["rok", "kwartał"]).reset_index(drop=True)


def show_metric(col, df, label, jednostka=""):
    val = df["wartość"].iloc[-1]
    prev = df["wartość"].iloc[-2]
    delta = round(val - prev, 2)
    delta_color = "inverse" if delta < 0 else "normal"
    col.metric(label, f"{val} {jednostka}", f"{delta:+} {jednostka}", delta_color=delta_color)


# === Dane i metryki ===

col1, col2, col3, col4 = st.columns(4)

stopa_df = get_stop_bezrobocia_df()
bezrobotni_df = get_bezrobotni_df()
wolne_df = get_wolne_miejsca_df()
zatrudnienie_df = get_zatrudnienie_df()

show_metric(col1, stopa_df, "Stopa bezrobocia", "%")
show_metric(col2, bezrobotni_df, "Bezrobotni (ogółem)", "os.")
show_metric(col3, wolne_df, "Wolne miejsca pracy", "tys.")
show_metric(col4, zatrudnienie_df, "Wskaźnik zatrudnienia", "%")


# === Wykresy ===

st.subheader("Trendy czasowe")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Stopa bezrobocia")
    df = stopa_df.copy()
    df["czas"] = df["rok"].astype(str) + "-" + df["miesiąc"].astype(str)
    st.line_chart(df.set_index("czas")["wartość"])

with chart_col2:
    st.markdown("#### Bezrobotni zarejestrowani")
    df = bezrobotni_df.copy()
    df["czas"] = df["rok"].astype(str) + "-" + df["miesiąc"].astype(str)
    st.line_chart(df.set_index("czas")["wartość"])

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("#### Wolne miejsca pracy")
    st.bar_chart(wolne_df.set_index("rok")["wartość"])

with chart_col4:
    st.markdown("#### Wskaźnik zatrudnienia")
    df = zatrudnienie_df.copy()
    df["czas"] = df["rok"].astype(str) + " " + df["kwartał"].astype(str)
    st.line_chart(df.set_index("czas")["wartość"])
