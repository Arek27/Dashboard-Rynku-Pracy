# -*- coding: utf-8 -*-

import geopandas as gpd

def load_gminy(path: str):
    gdf = gpd.read_file(path)
    gdf["terc"] = gdf["terc"].astype(str)
    return gdf
