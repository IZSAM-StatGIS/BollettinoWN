''' 
Lanciare questo script prima di eseguire lo script di generazione dei dataset (01_genera_dataset.py)
per verificare che i file excel di input non contengano codici istat non compresi in BDN

NB:
Prima di lanciare lo script verificare che 
- i file wn.xls e usutu.xls non abbiano valori null per la colonna CodIstat
- lo shapefile dei centroidi bdn (input/{ANNO}/centroidi_comuni_bdn.shp) sia aggiornato e che contenga il codice istat 236 per San Marino

'''

import os
import pandas as pd
import geopandas as gpd
from helpers import genera_centroidi

anno = '2024'

genera_centroidi(anno=anno)

path_wn = os.path.join('input', anno, 'wn.xlsx')
path_usu = os.path.join('input', anno, 'usutu.xlsx')

cod_istat_bdn = gpd.read_file(os.path.join('input', anno, 'centroidi_comuni_bdn.shp'))['ISTAT'].astype(int).tolist()

if os.path.exists(path_wn):
    cod_istat_xls_wn = pd.read_excel(path_wn)['CodIstat'].astype(int).tolist()
else:
    cod_istat_xls_wn = None
    print('File wn.xlsx non trovato, verifica WN saltata.')

if os.path.exists(path_usu):
    cod_istat_xls_usu = pd.read_excel(path_usu)['CodIstat'].astype(int).tolist()
else:
    cod_istat_xls_usu = None
    print('File usutu.xlsx non trovato, verifica USUTU saltata.')

# Verifica file wn.xls
if cod_istat_xls_wn is not None:
    diff_wn = []
    for item in cod_istat_xls_wn:
        if item in cod_istat_bdn:
            pass
        else:
            diff_wn.append(item)

    if len(diff_wn) > 0:
        print('Nel file wn.xls ci sono dei codici istat non presenti in BDN: {0}'.format(diff_wn))
    else:
        print('Tutti i codici istat presenti in wn.xls esistono in BDN')

# Verifica file usutu.xls

if cod_istat_xls_usu is not None:
    diff_usu = []
    for item in cod_istat_xls_usu:
        if item in cod_istat_bdn:
            pass
        else:
            diff_usu.append(item)

    if len(diff_usu) > 0:
        print('Nel file usutu.xls ci sono dei codici istat non presenti in BDN: {0}'.format(diff_usu))
    else:
        print('Tutti i codici istat presenti in usutu.xls esistono in BDN')
