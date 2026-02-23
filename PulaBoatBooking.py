import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime


st.set_page_config(layout="wide") # Široki prikaz da stane više polja u red

st.title("⛴️ Rezervacija Krstarenja")
st.write("Popunite obrazac za rezervaciju vašeg putovanja.")

# Povezivanje s Google tablicom (link zalijepi ovdje ili u secrets)
url = "https://docs.google.com/spreadsheets/d/1gTvWomvCck2r9_ItoeEOaHIUMwvKSw9jRtZ055f7KPk/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)



# --- KONTAKT INFORMACIJE ---
col1, col2 = st.columns(2)
with col1:
    ime = st.text_input("Name *")
    telefon = st.text_input("Phone Number (eg. +385 (91) 12345678) *")
with col2:
    prezime = st.text_input("Surname *")
    drzava = st.text_input("Country *")

email = st.text_input("Email *")

# --- DETALJI VOŽNJE ---
col3, col4 = st.columns(2)
with col3:
    ride = st.selectbox("Choose your ride *", ["HARBOUR CRUISE", "SUNSET CRUISE", "ISLAND HOPPING"])
with col4:
    datum = st.date_input("Choose a date *", datetime.date.today())

# --- BROJ PUTNIKA ---
col5, col6, col7 = st.columns(3)
with col5:
    odrasli = st.number_input("Number of Adult 13+ *", min_value=1, step=1)
with col6:
    djeca_2_12 = st.number_input("Number of kids 2-12 Years", min_value=0, step=1)
with col7:
    bebe_0_2 = st.number_input("Number of kids 0-2 Years", min_value=0, step=1)

# --- JELO I PIĆE ---
st.subheader("Menu selection")
col8, col9, col10, col11 = st.columns(4)
with col8:
    pice = st.number_input("Drinks without food", min_value=0, step=1, help="Number (0 for none)")
with col9:
    meso = st.number_input("Meat", min_value=0, step=1, help="Number of meat menus (0 for none)")
with col10:
    riba = st.number_input("Fish", min_value=0, step=1, help="Number of fish menus (0 for none)")
with col11:
    vegetarijansko = st.number_input("Vegetarian", min_value=0, step=1, help="Number of vegetarian menus (0 for none)")

# --- PORUKA ---
poruka = st.text_area("Your Message")

# --- GUMB ZA SLANJE ---
if st.button("Submit Booking"):
    if not ime or not prezime or not email or not telefon:
        st.error("Molimo popunite sva obavezna polja označena zvjezdicom (*)")
    else:
# Priprema podataka za tablicu
        novi_podaci = pd.DataFrame([{
            "Ime": ime,
            "Prezime": prezime,
            "Telefon": telefon,
            "Drzava": drzava,
            "Email": email,
            "Voznja": ride,
            "Datum": str(datum),
            "Odrasli": odrasli,
            "Djeca": djeca_2_12,
            "Bebe": bebe_0_2,
            "Pice": pice,
            "Meso": meso,
            "Ribe": riba,
            "Vegetarijansko": vegetarijansko,
            "Poruka": poruka
        }])
        
        
        # Čitanje postojećih i dodavanje novih
        stari_podaci = conn.read(spreadsheet=url, usecols=list(range(15)))
        azurirani_podaci = pd.concat([stari_podaci, novi_podaci], ignore_index=True)
        
        # Slanje natrag u Google Sheets
        conn.update(spreadsheet=url, data=azurirani_podaci)
        
        st.success("Rezervacija uspješno spremljena u bazu!")
        st.balloons()