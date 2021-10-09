"""staking learn page shown when the user enters the learn application"""
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


# import awesome_streamlit as ast
# endregion

playgroundHome = Path(__file__).parents[1] / 'Assets/44_learn_2.png'
playgroundHome  = Image.open(playgroundHome)

learn_44 = Path(__file__).parents[1] / 'Assets/44_curve.png'
learn_44  = Image.open(learn_44)


def app():
# region Description: All about staking
    st.title('Learn: Bonding and (4,4)')
    st.markdown('''----''')
    col1,col2 = st.columns((1.5,1))
    with col1:
        st.title('')
        st.image(playgroundHome)
    with col2:
        st.title('The Bonding strategy')
        bondLearnExpander = st.expander(label = 'Click to view Bonding Strategy', expanded=True)
        with bondLearnExpander:
            st.write(
                '''
                Bonding is the process of locking in a fixed reward in OHM. You trade in DAI for OHM at a discount
                and the OHM is vested linearly over a period of 5 days
                
                As a bonder, you win if the price of OHM increases during your vesting period; when this happens you benefit from the
                discount on OHM and the increase in price. You also win if price remains relatively the same during the vesting period.
                This is becuase profits are still gained from the discount
    
                As a bonder, you loose if the price of OHM decreases during your vesting period. If this happens, you will have to 
                decide between OHM and SLP (whichever is worth more)
                ''')
        st.title('The (4,4) strategy')
        fourFourLearnEpander = st.expander(label = 'click to view (4,4) Strategy', expanded=False)
        with fourFourLearnEpander:
            st.write(
                """
                The (4,4) strategy is a maximizing strategy that combines the benefits of staking (3,3) and bonding (1,1). 
                (4,4) simply means staking available OHMS during the vesting period to capture staking rewards during the vesting period
                """)
    st.markdown('''----''')

    st.title('What is (4,4) Playground? ')
    col3,col4 = st.columns((1.5,1))
    with col3:
        fourFourLearnEpander_2 = st.expander(label = 'click to view (4,4) Strategy', expanded=True)
        with fourFourLearnEpander_2:
                st.write(
                    """
                    **(4,4) Playground is a simulator for understanding and forecasting the bond, claim, and stake strategy**

                    Use this simulator to:
                    - Strategize (4,4) profitability 
                    - Forecast additional gains from using (4,4) compared to (3,3)
                    - Forecast additional gains from staking bonding emissions at varying epochs
                    - OHM growth over time with (4,4) strategy
                    """
                )
    with col4:
        st.image(learn_44)
    st.markdown('''----''')
    st.info('''
    Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics

    References to system governing equations can be found here
    [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is a the best source for due diligence and understanding
    the mechanics of Olympus protocol
    
    Forecasts are for educational purposes alone and should not be construed as financial advice
        ''')
# endregion