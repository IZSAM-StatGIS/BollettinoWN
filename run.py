# Importazione moduli
from turtle import down
import pandas as pd
import geopandas as gpd
import numpy as np
import locale
import os

# Dati spaziali (Centroidi dei Comuni dalla BDN)
gdf_comuni = gpd.read_file(r"input/shp/centroidi_comuni_bdn.shp")[['ISTAT','geometry']]
gdf_comuni.rename(columns={'ISTAT':'CodIstat'}, inplace=True)
gdf_comuni["CodIstat"] = gdf_comuni["CodIstat"].astype(int)
# gdf_comuni["CodIstat"] = pd.to_numeric(gdf_comuni["CodIstat"])

print(gdf_comuni.dtypes)

# ##########################################################
# WEST NILE DISEASE
# ##########################################################

# 1 - Importazione dati excel
# ---------------------------------------------------
df_wn = pd.read_excel(r'input/xls/wn.xlsx')
# Elimina gli spazi dai nomi delle colonne, se presenti
df_wn.columns = df_wn.columns.str.strip()

# 2 - Adattamenti formati e calcolo campi utility
# ---------------------------------------------------
# Modifica datatype di CodIstat in stringa
df_wn[['AnnoBollettino','CodIstat']] = df_wn[['AnnoBollettino','CodIstat']].astype(int)
# Trasformazione in data da stringa DD-MMM-YY a YYYY-MM-DD
locale.setlocale(locale.LC_ALL, 'it_IT')
df_wn['DataSospetto'] = pd.to_datetime(df_wn['DataSospetto'], format='%d-%b-%y')
# Creazione campi AnnoSospetto e MeseSospetto
df_wn['AnnoSospetto'] = pd.DatetimeIndex(df_wn['DataSospetto']).year
df_wn['AnnoSospetto'] = df_wn['AnnoSospetto'].astype(int)

# 3 - Aggregazione
# ---------------------------------------------------
df_wn_group_anno = df_wn.groupby(['AnnoSospetto','CodIstat','Categoria','Regione','Prov','Comune'], as_index=False).agg({'NumCapiMalati':'sum','NumFocolai':'sum'})
df_wn_group_data = df_wn.groupby(['DataSospetto','CodIstat','Categoria','Regione','Prov','Comune'], as_index=False).agg({'NumCapiMalati':'sum','NumFocolai':'sum'})
# 4 -  merge con i centroidi dei comuni
# ---------------------------------------------------
distribuzione_wn_anno = gdf_comuni.merge(df_wn_group_anno, on='CodIstat')
distribuzione_wn_data = gdf_comuni.merge(df_wn_group_data, on='CodIstat')
# 5 - Esportazione
# ---------------------------------------------------
distribuzione_wn_anno.to_file(r"output/distr_wn_centroidi.geojson", driver='GeoJSON')
distribuzione_wn_data.to_file(r"output/distr_wn_centroidi_data.geojson", driver='GeoJSON')

# ##########################################################
# USUTU VIRUS
# ##########################################################

# 1 - Importazione dati excel
df_usu = pd.read_excel(r"input/xls/usutu.xlsx")
# Elimina gli spazi dai nomi delle colonne, se presenti
df_usu.columns = df_usu.columns.str.strip()
# 2 - Merge con i centroidi dei comuni
distribuzione_usu = gdf_comuni.merge(df_usu, on='CodIstat')
# 5 - Esportazione
distribuzione_usu.to_file(r"output/distr_usu_centroidi.geojson", driver='GeoJSON')