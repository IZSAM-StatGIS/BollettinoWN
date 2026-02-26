''' 
Questo script lavora sui feature layer ospitati su ArcGIS Online per il Bollettino WN/USU:

- Distribuzione WN [data] (id: 66984cf968d94714a48ca87984a17e26)
- Distribuzione WN (id: 27fe74994d054d1e9c36dbc243116ef2)
- Distribuzione USU (id: b2c7149108064d349af4bfd4a48a3c1c)

Serve per cancellare le feature non corrette selezionandole con una query.

Esempio:
I dati WN dell'anno 2023 sono stati caricati su ArcGIS Online ed accodati nei Feature Layer ospitati, ma si scopre che il file excel di origine conteneva degli errori.
Invece di collegarsi ai dati tramite ArcGIS Pro per cancellare la porzione errata, si può usare questo script per selezionare ed eliminare le feature non corrette più comodamente.

'''

"""
NB: script da revisionare!
"""

import pandas as pd
from arcgis.gis import GIS
from arcgis.features import GeoAccessor, GeoSeriesAccessor
import os
from urllib3.exceptions import InsecureRequestWarning
import warnings

# Sopprime i warning 
warnings.simplefilter("ignore", InsecureRequestWarning)

username = os.getenv("ARC_GIS_USERNAME")
password = os.getenv("ARC_GIS_PASSWORD")

# Connect to ArcGIS Online
gis = GIS("https://izsam.maps.arcgis.com/", username=username, password=password)

# Connect to the feature layer
fl_id = {
    "wn_centroidi_data": "66984cf968d94714a48ca87984a17e26",
    "wn_centroidi": "27fe74994d054d1e9c36dbc243116ef2",
    "usu_centroidi": "b2c7149108064d349af4bfd4a48a3c1c"
}

# ANNO BOLLETTINO
###################################################
anno = '2025'
###################################################

# Operazioni sui FL Hosted

###################################################
# WN CENTROIDI
###################################################
wn_item = gis.content.get(fl_id["wn_centroidi"])
wn_flayer = wn_item.layers[0]
# Create a Spatially Enabled DataFrame object to check the data
wn_sdf = pd.DataFrame.spatial.from_layer(wn_flayer)
wn_query = "AnnoSospetto == {}".format(anno)
wn_sdff = wn_sdf.query(wn_query)
print("Dati Centroidi WN, anno {}, su ArcGIS Online:".format(anno))
print(wn_sdff.head(5))

# !!! ATTENZIONE !!! Cancella seleziona e cancella i dati dal Feature Layer Ospitato!
# wn_flayer.delete_features(where=wn_query)

###################################################
# WN CENTROIDI [DATA]
###################################################
wn_data_item = gis.content.get(fl_id["wn_centroidi_data"])
wn_data_flayer = wn_data_item.layers[0]
# Create a Spatially Enabled DataFrame object to check the data
wn_data_sdf = pd.DataFrame.spatial.from_layer(wn_data_flayer)
wn_data_query = "DataSospetto >= '{}-01-01'".format(anno)
wn_data_sdff = wn_data_sdf.query(wn_data_query)
print("Dati Centroidi WN raggruppati per Data, anno {}, su ArcGIS Online:".format(anno))
print(wn_data_sdff.head(5))

# !!! ATTENZIONE !!! Cancella seleziona e cancella i dati dal Feature Layer Ospitato!
# wn_data_flayer.delete_features(where=wn_data_query)

###################################################
# USUTU CENTROIDI
###################################################
usu_item = gis.content.get(fl_id["usu_centroidi"])
usu_flayer = wn_item.layers[0]
# Create a Spatially Enabled DataFrame object to check the data
usu_sdf = pd.DataFrame.spatial.from_layer(usu_flayer)
usu_query = "AnnoSospetto == {}".format(anno)
usu_sdff = usu_sdf.query(usu_query)
print("Dati Centroidi USUTU, anno {}, su ArcGIS Online:".format(anno))
print(usu_sdff.head(5))

# !!! ATTENZIONE !!! Cancella seleziona e cancella i dati dal Feature Layer Ospitato!
# usu_flayer.delete_features(where=usu_query)