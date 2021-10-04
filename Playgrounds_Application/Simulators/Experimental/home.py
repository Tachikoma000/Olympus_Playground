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
# endregion



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
        st.image(playgroundHome, use_column_width=True)
        st.markdown(
            """<a style='display: block;ffont-family: fieldwork, sans-serif;font-style: normal;font-weight: 600;color:#d93c68; text-align: center;' href="https://www.example.com/">Enter</a>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.empty()

