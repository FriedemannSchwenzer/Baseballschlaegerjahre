import streamlit as st
from data_loader import load_dataframes
from elements import (
    inject_page_styles,
    headline,
    initial_state,
    render_intro,
    divider,
    map_and_tweet,
    expander_1,
    expander_2,
    expander_3,
    ZITATION,
)

# -----------------------------
# Page Layout
# -----------------------------
st.set_page_config(
    page_title="#Baseballschlägerjahre – ein Hashtag und seine Geschichten",
    layout="centered",
)
inject_page_styles(max_width=1100, padding="2rem")

# -----------------------------
# Load Data
# -----------------------------
DATA_PATH = "data/tweets.xlsx"
PDF_PATH = "data/#baseballschlaegerjahre.ostdeutschland erinnern.pdf"

df_complete, df_with_loc, df_no_loc = load_dataframes(DATA_PATH)

# -----------------------------
# Session State Setup
# -----------------------------
initial_state(df_with_loc, df_no_loc)

# -----------------------------
# Page Content
# -----------------------------

#Headline wird angezeigt 
headline("#Baseballschlägerjahre – ein Hashtag und seine Geschichten")

#Intro wird angezeigt 
render_intro()

#Ein divider wird angezeigt 
divider()

# Karte und Tweets werden angezeigt 
map_and_tweet(df_with_loc)

#Ein divider wird angezeigt 
divider()

#Expander werden angezeigt 
expander_1()
expander_2(df_no_loc)
expander_3(pdf_path=PDF_PATH, zitation_text=ZITATION, email_text="hallo.friedemann(at)posteo.de")
