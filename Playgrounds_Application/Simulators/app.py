# ==============THE LIBRARIES
# region Description: Import all required libraries for this simulator
#from Pages import home, stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator
import json
from logging import PlaceHolder
import time

import streamlit as st
from streamlit import session_state
from streamlit_lottie import st_lottie

import urllib.request
import requests
from PIL import Image
import pathlib
from pathlib import Path
# endregion


navLogo = Path(__file__).parents[0] / 'Assets/glow.png'
navLogo = Image.open(navLogo)

lottie_waiting = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_wvwimamz.json')

#animatedLoading = Path(__file__).parents[1] /'Assets/sphere_dots_intro.json'


#state = _get_state()

st.page_config = st.set_page_config(
    page_title="Olympus Playgrounds", page_icon=':bar_chart:'
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

#lottie_hello = load_lottiefile('12855-dot-cluster-loader.json')

col1, col2, col3 = st.columns((1, 5, 1))

with col1:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
with col2:
    st.image(navLogo)
    st.markdown("<h3 style='text-align: center; color: #00bff3; font-famil:fieldwork'>Soon™</h3>", unsafe_allow_html=True)
st.write('------------------')
with col3:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')

#lottie_waiting = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_wvwimamz.json')
st_lottie(lottie_waiting, speed=1, reverse=False, loop=True, renderer='svg', height=200, key=None)


#https://assets7.lottiefiles.com/packages/lf20_wvwimamz.json
#https://assets10.lottiefiles.com/packages/lf20_hhvgzywn.json
#https://assets3.lottiefiles.com/packages/lf20_75vM6p.json
#https://assets8.lottiefiles.com/packages/lf20_yygwoab7.json

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
