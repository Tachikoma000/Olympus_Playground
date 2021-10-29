import streamlit as st
from PIL import Image
from Experimental import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator, mainDashboard, disclaimer
import pathlib
from pathlib import Path



menu_items = {
	'Report a bug': 'https://ohm.fyi/feedback',
    'Get help': 'https://discord.com/invite/6QjjtUcfM4',
}
st.set_page_config(layout="wide", menu_items=menu_items)

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
    "Bonding: Playground": bondingSimulator,
    "Disclaimer": disclaimer
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
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#MainMenu {visibility: hidden;}
page.app()
