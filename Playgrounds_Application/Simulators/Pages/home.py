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
# endregion

def app():
    # region Description: All about staking
    st.title('Welcome to your Playground!')
    st.write(
        '''
        This is a simple projection calculator for Staking and bonding ohm in OlympusDAO protocol
        Welcome to Olympus Playground
        This is an interactive notebook to study, play and forcast the growth of your ohm over time. 
        This notebook is designed to work hand in hand with the awesome gitbook created by the DAO and all of Brians calcs!
        ''')