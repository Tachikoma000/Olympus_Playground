"""staking learn page shown when the user enters the learn application"""
# ==============THE LIBRARIES
# region Description: Import all required libraries for this app: Staking learn page
from pycoingecko import CoinGeckoAPI  # Coin gecko API: Pulls live data from coin gecko
import math  # Needed for basic math operations\n",
import pandas as pd  # Needed fpr dataframe creation and operations\n",
import numpy as np  # Needed for array manipulations\n",
from itertools import islice  # Needed for more complex row and coloumn slicing\n",
import matplotlib.pyplot as plt  # Needed for quickly ploting results"
import pathlib  # url management
import plotly.express as px  # cleaner graphs
import plotly.graph_objects as go  # cleaner graphs
import streamlit as st


# import awesome_streamlit as ast
# endregion
def app():
# region Description: All about staking

    st.title('The Bond, claim and stake Strategy (4,4)')
    st.write(
        '''
        Bonding is the process of locking in a fixed reward in OHM. You trade in DAI for OHM at a discount
        and the OHM is vested linearly over a period of 5 days.
    
        As a bonder, you win if price of OHM increases during your vesting period; when this happens you benefits the
        discounted on OHM and the increase in price. You also win if price remains flat during the vesting period.
        This is becuase profits are still gained from the discount.
    
        As a bonder, you loose if price of OHM decreases during your vesting period. If this happens, you will have to 
        decide between OHM and SLP (whichever is worth more). 
    
        **So what is (4,4) and what does it have to do with Bonding?** 
        The (4,4) strategy is a maximizing strategy that combines the benefits of staking (3,3) and bonding (1,1). 
        (4,4) simply means staking available OHMS during the vesting period to capture staking rewards during the vesting period.

        ''')
    st.title('What is (4,4) Playground? ')
    st.write(
        """
        **(4,4) Playground is a simulator for understanding and forecasting the bond, claim and stake**.
        
        Use this simulator to:
        - Strategize (4,4) profitability. 
        - Forecast additional gains from using (4,4) compared to (3,3)
        - Forecast additional gains from staking bonding emissions at varying epochs
        - OHM growth over time with (4,4) strategy
        """
    )

    st.info('''
    Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics

    References to system governing equations can be found here
    [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is a the best source for due diligence and understanding
    the mechanics of Olympus protocol
        ''')
# endregion