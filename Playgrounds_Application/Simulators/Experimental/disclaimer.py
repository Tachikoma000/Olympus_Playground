# ==============THE LIBRARIES
# region Description: Import all required libraries for this simulator

import math  # Needed for basic math operations\n",
import pandas as pd  # Needed fpr dataframe creation and operations\n",
import numpy as np  # Needed for array manipulations\n",
from itertools import islice  # Needed for more complex row and coloumn slicing\n",
import matplotlib.pyplot as plt  # Needed for quickly ploting results"
import pathlib  # url management
import plotly.express as px  # cleaner graphs
import plotly.graph_objects as go  # cleaner graphs
import streamlit as st
from PIL import Image
import pathlib
from pathlib import Path
import base64
import json
from logging import PlaceHolder
import time
from streamlit import session_state
from streamlit_lottie import st_lottie
import requests
import urllib.request
from Experimental import stakingSimulator, stakingSimulator_Learn, bondingSimulator_Learn, bondingSimulator
# endregion

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

data_metrics_mission = Path(__file__).parents[1] / 'Assets/ark_transparent.png'
data_metrics_mission  = Image.open(data_metrics_mission)

data_metrics_vision = Path(__file__).parents[1] / 'Assets/Asset_1.png'
data_metrics_vision  = Image.open(data_metrics_vision)

playgroundHome = Path(__file__).parents[1] / 'Assets/Welcomehome.png'
playgroundHome  = Image.open(playgroundHome)

bkgImage = Path(__file__).parents[1] / 'Assets/wireframe_backing_dark_mode.png'
bkgImage  = Image.open(bkgImage)


main_bg = "wireframe_backing_dark_mode.png"
main_bg_ext = "jpg"

#side_bg = "sample.jpg"
#side_bg_ext = "jpg"

#st.markdown(
#    f"""
#    <style>
#    .reportview-container {{
#        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
#    }}
#    </style>
##    """,
 #   unsafe_allow_html=True
#)

def app():
    st.markdown("""<style> div.stButton > button:first-child {text-align: center;position:relative;} </style>""",unsafe_allow_html=True)
    col1, col2, col3= st.columns((1,1.5,1))
    with col1:
        st.empty()
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        #st.image(playgroundHome, use_column_width=True)
        st.header('Disclaimer')
        st.write(''' 
        Olympus Playgrounds is for educational purposes only and is not an individualized recommendation. Further Olympus Playgrounds are an educational tool and should not be relied upon as the primary basis for investment, financial, tax-planning, or retirement decisions. These metrics are not tailored to the investment objectives of a specific user. This educational information neither is, nor should be construed as, investment advice, financial guidance or an offer or a solicitation or recommendation to buy, sell, or hold any security, or to engage in any specific investment strategy by Olympus Playgrounds. These metrics used herein may change at any time and Olympus Playgrounds will not notify you when such changes are made. 

        You are responsible for doing your own diligence at all times. 

        Olympus Playgrounds does not take into account nor does it provide any tax, legal or investment advice or opinion regarding the specific investment objectives or financial situation of any person. Olympus Playgrounds and its developers, related DAO members, agents, advisors, directors, officers, contractors and token holders make no representation or warranties, expressed or implied, as to the accuracy of such information and Olympus Playgrounds expressly disclaims any and all liability that may be based on such information or errors or omissions thereof. [Olympus Playgrounds reserves the right to amend or replace the information contained herein, in part or entirely, at any time, and undertakes no obligation to provide the recipient with access to the amended information or to notify the recipient thereof. Any information, representations or statements not contained herein shall not be relied upon for any purpose.

        Neither [OlympusDAO or Olympus Playgrounds] nor any of its representatives shall have any liability
        whatsoever, under contract, tort, trust or otherwise, to you or any person
        resulting from the use of the information in Olympus Playgrounds by you or any of your representatives or for omissions from the information in Olympus Playgrounds.

        Additionally, the Olympus Playgrounds undertakes no obligation to comment on the expectations of, or statements made by, third parties in respect of the information in Olympus Playgrounds.
        ''')
        #lottie_waiting = load_lottieurl('https://assets9.lottiefiles.com/packages/lf20_anre6w2q.json')
        #st_lottie(lottie_waiting, speed=1, reverse=False, loop=True, renderer='svg', height=200, key=None)
        #st.markdown(
         #   """<a style='display: block;ffont-family: Montserrat, sans-serif;font-style: normal;font-weight: 100;color:#d93c68; text-align: center;' href="https://www.example.com/">Enter</a>
          #  """,
          #  unsafe_allow_html=True,
        #)
    with col3:
        st.empty()

