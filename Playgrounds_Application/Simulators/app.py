"""Main module for the stream lit app"""
import streamlit as st
from PIL import Image
from Pages import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator

st.set_page_config(layout="wide")
PAGES = {
    "Home": home,
    "Staking: Learn": stakingSimulator_Learn,
    "Staking:  Playground": stakingSimulator,
    "Bonding: Playground": bondingSimulator
}

st.sidebar.write('------------------')
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('------------------')
page.app()
