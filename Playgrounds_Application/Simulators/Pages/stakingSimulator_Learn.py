"""staking learn page shown when the user enters the learn application"""
# ==============THE LIBRARIES
# region Description: Import all required libraries for this app: Staking learn page
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
#import awesome_streamlit as ast
# endregion
def app():
# region Description: All about staking
    st.title('The Staking Strategy (3,3)')
    st.write(
        '''
        **Staking is the primary value accrual strategy of Olympus**. Stakers stake their OHM on the Olympus website to earn rebase rewards. 
        The rebase rewards come from the proceed from bond sales, and can vary based on the number of OHM staked in the protocol and the reward rate set by monetary policy.
        
        **Staking is a passive, long-term strategy**. The increase in your stake of OHM translates into a constantly falling cost basis converging on zero. 
        This means even if the market price of OHM drops below your initial purchase price, given a long enough staking period, the increase in your staked OHM balance should eventually outpace the fall in price.
        
        **When you stake, you lock OHM and receive an equal amount of sOHM**. Your sOHM balance rebases up automatically at the end of every epoch. 
        sOHM is transferable and therefore composable with other DeFi protocols.
        
        **When you unstake, you burn sOHM and receive an equal amount of OHM**. Unstaking means the user will forfeit the upcoming rebase reward. 
        Note that the forfeited reward is only applicable to the unstaked amount; the remaining staked OHM (if any) will continue to receive rebase rewards.
        
        ''')
    st.title('What is (3,3) Playground? ')
    st.write(
        """
        **(3,3) Playground is a simulator for staking, and incooom strategies**.
        
        Use this simulator to:
        - Forcast ROI ar current and future reward yield percent
        - OHM growth over time
        - OHM and USD value over time
                        
        We love the incooom, use this simulator to strategize:
        - Required staked OHM to reach desired daily incooom
        - Count down until you are earning desired daily incooom
        - Required staked OHM to reach desired weekly incooom
        - Count down until you are earning desired weekly incooom
    
        Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics
    
        References to system governing equations can be found here
        [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is a the best source for due diligence and understanding
        the mechanics of Olympus protocol
        """
    )
# endregion
