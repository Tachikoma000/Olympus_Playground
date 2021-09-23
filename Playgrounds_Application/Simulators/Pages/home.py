# ==============THE LIBRARIES
# region Description: Import all required libraries for this simulator
from pycoingecko import CoinGeckoAPI # Coin gecko API: Pulls live data from coin gecko
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
# endregion


data_metrics_vision = Path(__file__).parents[1] / 'Assets/data_metrics_vision.png'
data_metrics_vision  = Image.open(data_metrics_vision)

def app():
    # region Description: All about staking
    st.title('Welcome to your Playground!')
    st.write(
        '''
        This is an interactive projection calculator for Staking and bonding ohm in OlympusDAO protocol.
        Educational material and equations in this app are designed to work hand in hand with the awesome gitbook created by the DAO. 
        
        Special thanks to the Data and Metrics team! 
        ''')
    st.write('--------------')
    st.image(data_metrics_vision)
