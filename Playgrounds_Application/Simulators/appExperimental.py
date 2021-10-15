import streamlit as st
from PIL import Image
from Experimental import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator, mainDashboard
import pathlib
from pathlib import Path
st.set_page_config(layout="wide")

CURRENT_THEME = "dark"
IS_DARK_THEME = True

navLogo = Path(__file__).parents[0] / 'Assets/glow_5.png'
navLogo = Image.open(navLogo)
PAGES = {
    "Home": home,
    "Playgrounds Ω Explorer": mainDashboard,
    "Staking: Learn": stakingSimulator_Learn,
    "Staking:  Playground": stakingSimulator,
    "Bonding: Learn": bondingSimulator_Learn,
    "Bonding: Playground": bondingSimulator
    # end of section 4
}

st.sidebar.image(navLogo)
st.sidebar.write('------------------')
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('------------------')

hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

page.app()
