import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import geopandas as gpd
from arcgis import GIS

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Sopprime i warning 
warnings.simplefilter("ignore", InsecureRequestWarning)

def genera_centroidi(
    anno: int,
    gis_url: str = "https://izsam.maps.arcgis.com",
    username: str | None = None,
    password: str | None = None,
    output_name: str = "centroidi_comuni_bdn.shp",
):
    if load_dotenv is not None:
        load_dotenv()

    username = username or os.getenv("ARC_GIS_USERNAME")
    password = password or os.getenv("ARC_GIS_PASSWORD")
    if not username or not password:
        raise ValueError(
            "Credenziali mancanti. Imposta ARC_GIS_USERNAME e ARC_GIS_PASSWORD "
            "nelle variabili d'ambiente o passa username/password alla funzione."
        )

    output_dir = os.path.join("input", str(anno))
    output_path = os.path.join(output_dir, output_name)
    if os.path.exists(output_path):
        return output_path

    os.makedirs(output_dir, exist_ok=True)

    gis = GIS(gis_url, username=username, password=password, verify_cert=True)

    # Comuni
    out_fields = (
        "ISTAT_REGIONE, REGIONE, ISTAT_PROVINCIA, PROVINCIA, SIGLA_PROVINCIA, "
        "ISTAT_COMUNE, ISTAT, COMUNE, CENTROIDE_X, CENTROIDE_Y"
    )
    fl_comuni_bdn = gis.content.get("70165e42908440d7a68b668421392665").layers[0]
    fset_comuni_bdn = fl_comuni_bdn.query(
        where="1=1",
        return_geometry="False",
        out_fields=out_fields,
    )
    try:
        df_comuni_bdn = fset_comuni_bdn.sdf
    except Exception:
        df_comuni_bdn = pd.DataFrame([f.attributes for f in fset_comuni_bdn.features])

    # Rinomina i campi per mantenere compatibilita col passato
    df_comuni_bdn = df_comuni_bdn.rename(
        columns={
            "ISTAT_REGIONE": "ISTAT_REG",
            "ISTAT_PROVINCIA": "ISTAT_PRO",
            "SIGLA_PROVINCIA": "SIGLA_PROV",
            "ISTAT_COMUNE": "ISTAT_COM",
        },
        errors="ignore",
    )

    # Aggiunta centroide San Marino
    sm_record = {
        "ISTAT_REG": 236,
        "REGIONE": "SAN MARINO",
        "ISTAT_PRO": 236,
        "PROVINCIA": "SAN MARINO",
        "SIGLA_PROV": "RSM",
        "ISTAT_COM": 236,
        "ISTAT": 236,
        "COMUNE": "SAN MARINO",
        "CENTROIDE_X": 12.463,
        "CENTROIDE_Y": 43.938,
    }
    df_comuni_bdn = pd.concat([df_comuni_bdn, pd.DataFrame([sm_record])], ignore_index=True)

    # Geodataframe punti dai centroidi
    gdf_comuni_bdn = gpd.GeoDataFrame(
        df_comuni_bdn.drop(columns=["OBJECTID", "CENTROIDE_X", "CENTROIDE_Y"], errors="ignore"),
        geometry=gpd.points_from_xy(df_comuni_bdn["CENTROIDE_X"], df_comuni_bdn["CENTROIDE_Y"]),
        crs="EPSG:4326",
    )

    gdf_comuni_bdn.to_file(output_path, driver="ESRI Shapefile")
    return output_path



