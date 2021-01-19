import pandas as pd
import geopandas as gpd
import os
from clean_WN_data_cols import clean

# Dati spaziali (Centroidi dei Comuni dalla BDN)
gdf_comuni = gpd.read_file(r"input/shp/centroidi_comuni_bdn.shp")[['ISTAT','geometry']]
gdf_comuni.rename(columns={'ISTAT':'CodIstat'}, inplace=True)
gdf_comuni["CodIstat"] = gdf_comuni["CodIstat"].astype(int)

# ##########################################################
# WEST NILE DISEASE
# ##########################################################

# 1 - Importazione e pulizia dati excel
df_wn = pd.read_excel(r'input/xls/wn.xlsx')
df_wn = clean(df_wn)
df_wn.rename(columns={'Categorie':'Categoria'}, inplace=True)
df_wn = df_wn.query("DataSospetto >= '2008-01-01' & DataSospetto <= '2018-12-31'").sort_values(by=["DataSospetto"])
# 2 - Aggregazione e merge con i centroidi dei comuni
df_wn_group_anno = df_wn.groupby(['AnnoSospetto','CodIstat','Categoria','Regione','Prov','Comune'])["CodIstat"].count().reset_index(name="count")
df_wn_group_data = df_wn.groupby(['DataSospetto','CodIstat','Categoria','Regione','Prov','Comune'])["CodIstat"].count().reset_index(name="count")
distribuzione_wn_anno = gdf_comuni.merge(df_wn_group_anno, on='CodIstat')
distribuzione_wn_data = gdf_comuni.merge(df_wn_group_data, on='CodIstat')
# 3 - Esportazione
distribuzione_wn_anno.to_file(r"output/distr_wn_centroidi.geojson", driver='GeoJSON')
distribuzione_wn_data.to_file(r"output/distr_wn_centroidi_data.geojson", driver='GeoJSON')

# ##########################################################
# USUTU VIRUS
# ##########################################################

# 1 - Importazione dati excel
df_usutu = pd.read_excel(r"input/xls/usutu.xlsx")
# 2 - Aggregazione e conteggio delle due categorie previste 
df_insetti = df_usutu.query("SpecieCampione == 'CULEX PIPIENS'")
df_uccelli = df_usutu.query("SpecieCampione == 'UCCELLO SELVATICO'")

df_insetti_group = df_insetti.groupby(['Anno','Sede','Provincia','Comune'])["Comune"].count().reset_index(name="N_insetti")
df_uccelli_group = df_uccelli.groupby(['Anno','Sede','Provincia','Comune'])["Comune"].count().reset_index(name="N_uccelli")

df_usutu_group = df_insetti_group.append(df_uccelli_group).fillna(0)
df_usutu_group['N_insetti'] = df_usutu_group['N_insetti'].astype(int)
df_usutu_group['N_uccelli'] = df_usutu_group['N_uccelli'].astype(int)

df_usu = df_usutu_group.groupby(['Anno','Sede','Provincia','Comune'],as_index=False).agg('sum')
df_usu['Anno'] = df_usu['Anno'].astype(int)
# df_us.query('N_insetti > 0 & N_uccelli > 0')

# 3 - Merge con i centroidi dei comuni
# To-Do... manca codice istat in dati usutu di partenza

# 4 - Esportazione
# To-Do... temporanemente esporta csv
df_usu.to_csv(r"output/distr_usu_centroidi.csv", index=False)


