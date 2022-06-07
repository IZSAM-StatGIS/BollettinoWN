''' 
Lanciare questo script prima di eseguire il run.py che genera i dataset
per verificare che i file excel di input non contengano codici istat non compresi in BDN

NB:
Prima di lanciare lo script verificare che 
- i file wn.xls e usutu.xls non abbiano valori null per la colonna CodIstat
- lo shapefile dei centroidi bdn (input/shp/centroidi_comuni_bdn.shp) sia aggiornato e che contenga il codice istat 236 per San Marino

'''

import pandas as pd
import geopandas as gpd

cod_istat_xls_wn = pd.read_excel(r'input/xls/wn.xlsx')['CodIstat'].astype(int).tolist()
cod_istat_xls_usu = pd.read_excel(r'input/xls/usutu.xlsx')['CodIstat'].astype(int).tolist()
cod_istat_bdn = gpd.read_file(r"input/shp/centroidi_comuni_bdn.shp")['ISTAT'].astype(int).tolist()

# Verifica file wn.xls
diff_wn = []
for item in cod_istat_xls_wn:
    if item in cod_istat_bdn:
        pass
    else:
        diff_wn.append(item)
        
if len(diff_wn) > 0:
    print('Nel file wn.xls ci sono dei codici istat non presenti in BDN: {0}'.format(diff_usu))
else:
    print('Tutti i codici istat presenti in wn.xls esistono in BDN')

# Verifica file usutu.xls
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