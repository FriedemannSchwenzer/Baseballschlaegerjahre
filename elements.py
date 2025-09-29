import streamlit as st
import pandas as pd
import folium
import html
from streamlit_folium import st_folium

# -----------------------------
# Design-Konstanten
# -----------------------------
PRIMARY = "#0000fc"
ACCENT_BG = "#ffe5e5"
CARD_BG = "#f9f9f9"
MONO = "monospace"
QUOTE_COLOR = ACCENT_BG
SHADOW = "0 2px 12px rgba(255,229,229,0.8)"

# -----------------------------
# Global CSS Styles
# -----------------------------
def inject_page_styles(max_width: int = 1100, padding: str = "2rem") -> None:
    """Injects global CSS for layout and reusable classes."""
    st.markdown(f"""
        <style>
        .block-container {{
            max-width: {max_width}px;
            padding-left: {padding};
            padding-right: {padding};
        }}
        .tweet-card {{
            background-color:{CARD_BG};
            padding:30px; border-radius:12px; margin-bottom:20px;
            box-shadow:{SHADOW};
            max-height:650px; overflow-y:auto;
            font-family:{MONO}; font-size:20px; line-height:1.3;
            color:{PRIMARY}; position:relative;
        }}
        .tweet-card span {{
            font-size:70px; line-height:0.6; margin-top:10px;
            position:absolute; left:15px; top:10px; color:{QUOTE_COLOR};
        }}
        .tweet-card-footer {{
            font-size:14px; font-family:{MONO}; color:{PRIMARY};
            text-align:right; margin-top:20px;
        }}
        .subtle-button > button {{
            background-color: {CARD_BG};
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: 0.25rem 0.75rem;
            font-family: {MONO};
            font-size: 14px;
            font-weight: 400;
            line-height: 1.6;
        }}
        .subtle-button > button:hover {{
            border: 1px solid {PRIMARY};
            color: {PRIMARY};
        }}
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Session State Init
# -----------------------------
def initial_state(df_with_loc: pd.DataFrame, df_no_loc: pd.DataFrame) -> None:
    """Initialisiert Session State Variablen mit Defaults."""
    st.session_state.setdefault("tweet_idx", 0)  # immer den Christian Bangel tweet nehmen
    st.session_state.setdefault(
        "rand_no_loc_idx",
        (None if df_no_loc.empty else df_no_loc.index[0])
    )

# -----------------------------
# Reusable Elements
# -----------------------------
def divider(color: str = ACCENT_BG, thickness: str = "2px", margin: str = "25px 0") -> None:
    st.markdown(
        f"""<hr style="border:none;border-top:{thickness} solid {color};margin:{margin};">""",
        unsafe_allow_html=True
    )

def headline(text: str, margin_bottom: str = "35px") -> None:
    st.markdown(
        f"""<h1 style='margin-bottom:{margin_bottom};'>{text}</h1>""",
        unsafe_allow_html=True
    )

def styled_paragraph(
    text: str,
    size: int = 20,
    margin_top: str = "0.6rem",
    margin_bottom: str = "0.5rem"
) -> None:
    
    st.markdown(
        f"""
        <p style="
            font-size:{size}px; line-height:1.6; font-family:{MONO};
            margin-top:{margin_top}; margin-bottom:{margin_bottom};">{text}</p>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Card Renderer
# -----------------------------
def render_card(body_html: str, footer_html: str = "") -> None:
    st.markdown(
        f"""
        <div class="tweet-card">
            <span>&ldquo;</span>
            <div style="margin-left:40px;">{body_html}</div>
            <div class="tweet-card-footer">{footer_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def tweet_card(tweet: str, author: str, date_str: str) -> None:
    render_card(
        body_html=html.escape(tweet),
        footer_html=f"{html.escape(author)} | {html.escape(date_str)}"
    )

# -----------------------------
# Intro
# -----------------------------
INTRO = [
    """2019 war das 30. Jubiläumsjahr der Friedlichens Revolution. Doch ungetrübte Feierstimmung wollte nicht aufkommen. Der Mord an Walter Lübcke, der Anschlag von Halle und die Umfrageergebnisse der AfD – vor allem im Osten – prägten die Debatten. Das Erbe der Friedlichen Revolution, so schien es, musste neu verhandelt werden.""",
    """Am 29. Oktober 2019 postete der Journalist Christian Bangel ein 
<a href="https://www.freitag.de/autoren/hendrik-bolz/sieg-heil-rufe-wiegten-mich-in-den-schlaf"
target="_blank" style="color:#0000fc; text-decoration:underline;">
Essay</a> 
des Rappers Hendrick Bolz auf Twitter. Es verhandelt eine von rechter Gewalt geprägte Jugend im Ostdeutschland der Nachwendezeit. Eine Generationenerfahrung.""",
    """Hunderte Nutzer*innen folgten dem Aufruf Bangels und teilten ihre autobiographischen Erinnerungen unter dem Hashtag #Baseballschlägerjahre. Für meine Masterarbeit habe ich diese Tweets erhoben und ausgewertet. Hier sind die Geschichten und die Orte von Hashtag #Baseballschlägerjahre dokumentiert."""
]

def render_intro() -> None:
    with st.container(border=None):
        for text in INTRO:
            styled_paragraph(text)

# -----------------------------
# Map + Tweets
# -----------------------------
def map_and_tweet(df_with_loc: pd.DataFrame) -> None:
    """Zeigt links die Karte und rechts die aktuelle Tweet-Card."""
    col_map, col_info = st.columns([1, 1], gap="large")

    # --- Karte
    with col_map:
        styled_paragraph(" ")
        m = folium.Map(
            location=[52.5, 12.5],
            zoom_start=6.2,
            min_zoom=6.7,
            tiles="OpenStreetMap",
        )

        df_points = df_with_loc.dropna(subset=["lat", "lon"]).copy()
        df_points["lat_r"] = df_points["lat"].round(5)
        df_points["lon_r"] = df_points["lon"].round(5)

        for row in df_points.itertuples(index=True):
            popup_html = (
                f'<div style="font-size:12px; font-family:{MONO}; color:{PRIMARY}; '
                f'padding:6px 10px; border-radius:8px; text-align:center;">'
                f'{html.escape(str(row.ort))}</div>'
            )
            folium.CircleMarker(
                location=[row.lat, row.lon],
                radius=6,
                color=PRIMARY,
                fill=True,
                fill_color=ACCENT_BG,
                fill_opacity=0.8,
                tooltip=row.ort,
                popup=folium.Popup(popup_html, max_width=250),
            ).add_to(m)

        st_data = st_folium(m, width=None, height=650)

        if st_data and st_data.get("last_object_clicked"):
            lat = round(st_data["last_object_clicked"]["lat"], 5)
            lon = round(st_data["last_object_clicked"]["lng"], 5)
            match = df_points[(df_points["lat_r"] == lat) & (df_points["lon_r"] == lon)]
            if not match.empty:
                st.session_state.tweet_idx = match.index[0]

    # --- Tweet
    with col_info:
        styled_paragraph(" ")
        idx = st.session_state.get("tweet_idx")
        if idx is not None and not df_with_loc.empty:
            row = df_with_loc.loc[idx]
            tweet_card(
                str(row.get("tweet", "")),
                str(row.get("autor", "")),
                str(row.get("datum", "")),
            )

# -----------------------------
# Expanders
# -----------------------------
def expander_1() -> None:
    with st.expander("Wie kommt diese Karte zustande?", expanded=False):
        st.markdown(
            """
            Die Tweets habe ich im Rahmen meiner Masterarbeit erhoben. Mein thematischer Fokus war auf
            Ostdeutschland, weshalb ich (die wenigen, aber vorhandenen!) Tweets mit Bezug auf westdeutsche
            Orte nicht in meinen Datensatz aufgenommen habe. Auf der Karte werden nur Tweets angezeigt,
            die tatsächlich verortbar sind. Bei Angabe von Bundesländern oder Städten habe ich für die
            Darstellung einen zufälligen Punkt innerhalb der entsprechenden Fläche ausgewählt.
            """
        )

def expander_2(df_no_loc: pd.DataFrame) -> None:
    with st.expander("Was ist mit den Tweets ohne Ortsangaben?", expanded=False):

        st.markdown("Die kannst Du hier lesen:")

        if not df_no_loc.empty and "rand_no_loc_idx" in st.session_state:
            row = df_no_loc.loc[st.session_state.rand_no_loc_idx]
            tweet_card(
                str(row.get("tweet", "")),
                str(row.get("autor", "")),
                str(row.get("datum", "")),
            )
            col1, _ = st.columns([4, 1])
            with col1:
                if st.button("Nächster Tweet", key="btn_no_loc"):
                    st.session_state.rand_no_loc_idx = df_no_loc.sample(1).index[0]
        else:
            st.info("Keine Tweets ohne Ortsangabe gefunden.")


def expander_3(pdf_path: str, zitation_text: str, email_text: str = "hallo.friedemann@posteo.de") -> None:
    with st.expander("Was ist das für eine Masterarbeit? Und darf ich die lesen?", expanded=False):
        st.markdown(
            """
            Die Masterarbeit *#Baseballschlägerjahre. Ostdeutschland erinnern* habe ich im Jahr 2021 
            an der Universität Potsdam erfolgreich eingereicht.  

            Hier kannst Du sie herunterladen:
            """
        )

        try:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name=pdf_path.split("/")[-1],
                    mime="application/pdf",
                    use_container_width=False
                )
        except FileNotFoundError:
            st.error(f"PDF nicht gefunden unter: {pdf_path}")

        st.markdown(" ")
        st.markdown(
            "Ich freue mich, wenn Du über die #Baseballschlägerjahre schreibst. "
            "Noch mehr freue ich mich, wenn Dir meine Masterarbeit neue Perspektiven dafür gibt. "
            "Am meisten freue ich mich, wenn Du die Arbeit dabei nach den üblichen akademischen Gepflogenheiten zitierst: "
        )
        st.code(zitation_text, language="text")
        st.markdown(" ")
        st.markdown(f"Schreib mir gern eine Email an: {email_text}. ")

# -----------------------------
# Zitation
# -----------------------------
ZITATION = (
    "Schwenzer, Friedemann (2021): #Baseballschlägerjahre. Ostdeutschland erinnern. "
    "Unveröffentlichte Masterarbeit. Universität Potsdam."
)
