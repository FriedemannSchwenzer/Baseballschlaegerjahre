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

    # 3) Orte bereinigen: "NAN" zu echtem Nullwert
    df_complete["ort"] = df_complete["ort"].replace("NAN", pd.NA)

    # 4) Lat/Lon aus "lat lon" extrahieren 
    latlon = df_complete["lat lon"].astype(str).str.split(",", expand=True)

    df_complete["lat"] = pd.to_numeric(latlon[0], errors="coerce", downcast="float")
    df_complete["lon"] = pd.to_numeric(latlon[1], errors="coerce", downcast="float")


    # 5) Datum formatieren
    df_complete["datum"] = pd.to_datetime(df_complete["datum"], errors="coerce").dt.strftime("%d.%m.%Y")

    # 6) Split nach Ort vorhanden / nicht vorhanden
    df_with_loc = df_complete.dropna(subset=["ort"]).reset_index(drop=True)
    df_no_loc = df_complete[df_complete["ort"].isna()].copy()

    # Starttweet einfügen
    df_with_loc = add_start_tweet(df_with_loc)

    return df_complete, df_with_loc, df_no_loc

#Setzt den Tweet von Christian Bangel als Starttweet
def add_start_tweet(df_with_loc: pd.DataFrame) -> pd.DataFrame:
    """Fügt einen festen Start-Tweet als erste Zeile ein."""

    start_tweet = pd.DataFrame([{
    "tweet": "Ihr Zeugen der Baseballschlägerjahre. Redet und schreibt von den Neunzigern und Nullern. It’s about time.",
    "ort": "Start",
    "lat lon": pd.NA,
    "autor": "@christianbangel",
    "datum": "29.10.2019"
}])

    # sicherstellen, dass alle Spalten gleich sind
    for col in df_with_loc.columns:
        if col not in start_tweet.columns:
            start_tweet[col] = pd.NA
            
    start_tweet = start_tweet[df_with_loc.columns]

    return pd.concat([start_tweet, df_with_loc], ignore_index=True)

