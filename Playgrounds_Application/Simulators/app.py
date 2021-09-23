"""Main module for the stream lit app"""
import streamlit as st
from PIL import Image
from Pages import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator
import pathlib
from pathlib import Path
st.set_page_config(layout="wide")

navLogo = Path(__file__).parents[0] / 'Assets/playgroundOHM.PNG'
navLogo = Image.open(navLogo)
PAGES = {
    "Home": home,
    "Staking: Learn": stakingSimulator_Learn,
    "Staking:  Playground": stakingSimulator,
    "BondingL Learn": bondingSimulator_Learn,
    "Bonding: Playground": bondingSimulator
}

st.write(navLogo)
st.sidebar.write('------------------')
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('------------------')
page.app()
