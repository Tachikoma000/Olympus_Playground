import streamlit as st
from PIL import Image
from Experimental import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator
import pathlib
from pathlib import Path
#st.set_page_config(layout="wide")

navLogo = Path(__file__).parents[0] / 'Assets/Asset_3.png'
navLogo = Image.open(navLogo)
PAGES = {
    "Home": home,
    "Staking: Learn": stakingSimulator_Learn,
    "Staking:  Playground": stakingSimulator,
    "Bonding: Learn": bondingSimulator_Learn,
    "Bonding: Playground": bondingSimulator
    # end of section
}

st.sidebar.image(navLogo)
st.sidebar.write('------------------')
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('------------------')

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



page.app()
