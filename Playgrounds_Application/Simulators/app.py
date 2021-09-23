"""Main module for the stream lit app"""
import streamlit as st
from Pages import home, stakingSimulator, stakingSimulator_Learn

st.set_page_config(layout="wide")
PAGES = {
    "Home": home,
    "Staking: Learn": stakingSimulator_Learn,
    "Staking:  Playground": stakingSimulator,
}

st.sidebar.image("Assets/playgroundOHM.png", use_column_width=True)
st.sidebar.write('------------------')
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('------------------')
page.app()
