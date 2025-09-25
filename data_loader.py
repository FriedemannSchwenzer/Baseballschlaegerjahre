import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_dataframes(xlsx_path):
    """
    Lädt den Datensatz aus Excel und bereitet drei DataFrames auf:
      - df_complete:   kompletter Datensatz (bereinigt)
      - df_with_loc:        nur Zeilen mit Ortsangabe
      - df_no_loc: nur Zeilen ohne Ortsangabe
    """
    
    # 1) Datei laden
    df_complete = pd.read_excel(xlsx_path)

    # 2) Spaltennamen normalisieren
    df_complete.columns = df_complete.columns.str.strip().str.lower()

    # 3) Orte bereinigen: "NAN" → echtes NaN
    df_complete["ort"] = df_complete["ort"].replace("NAN", pd.NA)

    # 4) Lat/Lon aus "lat lon" extrahieren (falls nötig)
    if "lat lon" in df_complete.columns and ("lat" not in df_complete.columns or "lon" not in df_complete.columns):
        latlon = (
            df_complete["lat lon"]
            .astype(str)
            .str.replace(";", ",")
            .str.split(",", expand=True)
        )
        if latlon.shape[1] >= 2:
            df_complete["lat"] = pd.to_numeric(latlon[0], errors="coerce")
            df_complete["lon"] = pd.to_numeric(latlon[1], errors="coerce")

    # 5) Datum formatieren
    if "datum" in df_complete.columns:
        df_complete["datum"] = pd.to_datetime(df_complete["datum"], errors="coerce").dt.strftime("%d.%m.%Y")
   

    # 6) Split nach Ort vorhanden / nicht vorhanden
    df_with_loc = df_complete.dropna(subset=["ort"]).reset_index(drop=True)
    df_no_loc = df_complete[df_complete["ort"].isna()].copy()
    
    return df_complete, df_with_loc, df_no_loc
