# Importazione moduli
import pandas as pd
import geopandas as gpd
import numpy as np
import os
import sys

# Anno
anno_dati = '2024'

# Cartella output
output_dir = os.path.join('output', anno_dati)

# Verifica file di input richiesti
input_dir = os.path.join('input', anno_dati)
shp_path = os.path.join(input_dir, "centroidi_comuni_bdn.shp")
wn_path = os.path.join(input_dir, "wn.xlsx")
usutu_path = os.path.join(input_dir, "usutu.xlsx")

if not os.path.exists(shp_path):
    print("Errore: file di input mancante:")
    print(f"- {shp_path}")
    sys.exit(1)

missing_optional = [path for path in [wn_path, usutu_path] if not os.path.exists(path)]
if missing_optional:
    print("Attenzione: file opzionali mancanti (verranno saltati):")
    for path in missing_optional:
        print(f"- {path}")

# Dati spaziali (Centroidi dei Comuni dalla BDN)
gdf_comuni = gpd.read_file(shp_path)[['ISTAT','geometry']]
gdf_comuni.rename(columns={'ISTAT':'CodIstat'}, inplace=True)
gdf_comuni["CodIstat"] = gdf_comuni["CodIstat"].astype(int)
# gdf_comuni["CodIstat"] = pd.to_numeric(gdf_comuni["CodIstat"])
# print(gdf_comuni.dtypes)

# ##########################################################
# WEST NILE DISEASE
# ##########################################################

if os.path.exists(wn_path):
    # 1 - Importazione dati excel
    # ---------------------------------------------------
    # Evita che sigle come "NA" (Napoli) vengano interpretate come NaN
    df_wn = pd.read_excel(wn_path, keep_default_na=False)
    # Elimina gli spazi dai nomi delle colonne, se presenti
    df_wn.columns = df_wn.columns.str.strip()

    # 2 - Adattamenti formati e calcolo campi utility
    # ---------------------------------------------------
    # Modifica datatype di CodIstat in stringa
    df_wn[['AnnoBollettino','CodIstat']] = df_wn[['AnnoBollettino','CodIstat']].astype(int)

    df_wn['DataSospetto'] = pd.to_datetime(df_wn['DataSospetto'], format='%Y-%m-%d')
    # Creazione campo AnnoSospetto
    df_wn['AnnoSospetto'] = pd.DatetimeIndex(df_wn['DataSospetto']).year
    # Sostituzione dei valori non numerici con un valore (anno)
    df_wn["AnnoSospetto"] = df_wn["AnnoSospetto"].replace({np.nan: anno_dati, float('inf'): anno_dati})
    # Coversione valori float a interi
    df_wn['AnnoSospetto'] = df_wn['AnnoSospetto'].astype(int)
    # Rimuove spazi a inizio/fine e converte 'Categoria' in maiuscolo
    df_wn['Categoria'] = df_wn['Categoria'].astype(str).str.strip().str.upper()

    # print(df_wn.sort_values(by='NumCapiMalati', ascending=True).head(10))

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
    # Crea cartella di output se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    distribuzione_wn_anno.to_file(os.path.join(output_dir,"distr_wn_centroidi.geojson"), driver='GeoJSON')
    distribuzione_wn_data.to_file(os.path.join(output_dir,"distr_wn_centroidi_data.geojson"), driver='GeoJSON')

# ##########################################################
# USUTU VIRUS
# ##########################################################

if os.path.exists(usutu_path):
    # 1 - Importazione dati excel
    df_usu = pd.read_excel(usutu_path)
    # Elimina gli spazi dai nomi delle colonne, se presenti
    df_usu.columns = df_usu.columns.str.strip()
    # 2 - Merge con i centroidi dei comuni
    distribuzione_usu = gdf_comuni.merge(df_usu, on='CodIstat')
    # 5 - Esportazione
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    distribuzione_usu.to_file(os.path.join(output_dir, "distr_usu_centroidi.geojson"), driver='GeoJSON')
