# -*- coding: utf-8 -*-

import pandas as pd

def load_Wynagrodzenia(path: str):
    return pd.read_excel(
        path,
        dtype={"Kod": str}
    )
