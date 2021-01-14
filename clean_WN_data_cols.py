import datetime as dt
import pandas as pd
import locale

def clean(df):

  # Rimozione colonne inutili
    drop_fields = [
        'STATO_DEL_RECORD','Malattia',
        'AnnoFocolaioMinsal', 'NumFocolaioMinsal', 'CodSierotipo',
        'NumCapiAbbattuti', 'NumCapiConSintomi', 'NumCapiDistrutti', 
        'NumCapiGuariti', 'NumCapiMalati', 'NumCapiMorti', 'NumCapiPresenti', 'TotaleMorti'
    ]
    
    df.drop(drop_fields, axis = 1, inplace=True)
    
    # Modifica datatype di CodIstat in stringa
    df['CodIstat'] = df['CodIstat'].astype(int)

    # Trasformazione in data da stringa DD-MMM-YY a YYYY-MM-DD
    locale.setlocale(locale.LC_ALL, 'it_IT')
    df['DataSospetto'] = pd.to_datetime(df['DataSospetto'], format='%d-%b-%y')
    df['DataConferma'] = pd.to_datetime(df['DataConferma'], format='%d-%b-%y')

    # Creazione campi AnnoSospetto e MeseSospetto
    df['AnnoSospetto'] = pd.DatetimeIndex(df['DataSospetto']).year
    df['AnnoSospetto'] = df['AnnoSospetto'].astype(int)

    # Seleziona solo i focolai confermati e i campi di interesse per l'aggregazione e l'incrocio con i centroidi
    df = df.query('DataConferma != "NaT"')[["AnnoSospetto","DataSospetto","IdFocolaio","CodIstat","Specie","Categorie","Sierotipo","Regione","Prov","Comune"]]

    return df


