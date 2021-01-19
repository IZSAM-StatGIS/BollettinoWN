# BollettinoWN
Questo repository contiene gli script per l'elaborazione dei dati del Bollettino Annuale West Nile e USUTU e il materiale per la composizione delle storymaps.

## Dati di input
I file excel contenenti i focolai disaggregati di west nile e i dati disaggregati usutu vengono utilizzati per la generazione dei dati spaziali aggregati. Lo script si aspetta due file:
  * wn.xlsx
  * usutu.xlsx

### Struttura di *wn.xlsx*
<table style="font-size:10px">
  <tr>
    <th>DataSospetto</th>
    <th>idFocolaio</th>
    <th>Specie</th>
    <th>Categoria</th>
    <th>Regione</th>
    <th>Prov</th>
    <th>Comune</th>
    <th>CodIstat</th>
  </tr>
  <tr>
    <td>23/01/2018</td>
    <td>39847</td>
    <td>GALLUS GALLUS</td>
    <td>AVICOLI</td>
    <td>SICILIA</td>
    <td>CT</td>
    <td>GIARRE</td>
    <td>87017</td>
  </tr>
  <tr>
    <td>15/06/2018</td>
    <td>41390</td>
    <td>GAZZA</td>
    <td>UCCELLI BERSAGLIO</td>
    <td>EMILIA ROMAGNA</td>
    <td>RE</td>
    <td>FABBRICO</td>
    <td>35034</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

I valori validi per il campo **Categoria** sono:
  * EQUIDI
  * AVICOLI
  * UCCELLI BERSAGLIO
  * UCCELLI SELVATICI
  * INSETTI
  
### Struttura di *usutu.xlsx*
<table>
  <tr>
    <th>Anno</th>
    <th>Sede</th>
    <th>SpecieCampione</th>
    <th>Categoria</th>
    <th>Regione</th>
    <th>Provincia</th>
    <th>SiglaProvincia</th>
    <th>Comune</th>
    <th>CodIstat</th>
  </tr>
  <tr>
    <td>2018</td>
    <td>TE</td>
    <td>CULEX PIPIENS</td>
    <td>INSETTI</td>
    <td>EMILIA ROMAGNA</td>
    <td>FERRARA</td>
    <td>FE</td>
    <td>FERRARA</td>
    <td>38008</td>
  </tr>
  <tr>
    <td>2018</td>
    <td>TE</td>
    <td>UCCELLO SELVATICO</td>
    <td>UCCELLI</td>
    <td>ABRUZZO</td>
    <td>TERAMO</td>
    <td>TE</td>
    <td>TERAMO</td>
    <td>67041</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

I valori validi per il campo **Categoria** sono:
  * UCCELLI
  * INSETTI
