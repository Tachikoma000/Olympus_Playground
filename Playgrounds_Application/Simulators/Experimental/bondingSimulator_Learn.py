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
learnBonding_logo = Path(__file__).parents[1] / 'Assets/Learn_bonding_logo.png'
learnBonding_logo  = Image.open(learnBonding_logo)

learnBonding_strat = Path(__file__).parents[1] / 'Assets/44_learn_2.png'
learnBonding_strat  = Image.open(learnBonding_strat)

learn_44_playground = Path(__file__).parents[1] / 'Assets/PG_bond_curve_2.png'
learn_44_playground  = Image.open(learn_44_playground)


def app():
# region Description: All about staking

    col1,col2 = st.columns((0.6,1))
    with col1:
        st.image(learnBonding_logo)
    st.markdown('''----''')
    st.title('The Bonding strategy')
    col3, col4 = st.columns((1.8,1.4))
    with col3:
        st.image(learnBonding_strat)
    with col4:
        bondLearnExpander = st.expander(label = 'Click to view Bonding Strategy', expanded=True)
        with bondLearnExpander:
            st.write(
                '''
                Bonding is the process of locking in a fixed reward in OHM, i.e. a discount of current market price, we call this (1,1) .
                 You, the bonder, purchases  OHM directly from the Treasury at a discount and the OHM is vested linearly over a period of 5 days. Bonding is a short-term, active strategy.  
                 
                 There are two bond types, reserve and liquidity:
                - Reserve bonds are the primary revenue stream for Olympus. This is simply buying OHM directly from the Treasury. The profit Olympus DAO makes from bonding goes to backing OHM.
                - Liquidity bonds are how Olympus grows its liquidity. 
                In this case you sell your liquidity share to Olympus DAO. This helps to create stability during volatility by ensuring thick liquidity and makes a rug pull much less likely.
                
                As a bonder, you win if the price of OHM increases during your vesting period; when this happens you benefit from the discount on OHM and the increase in price.
                You also win if the price remains relatively the same during the vesting period. This is because profits are still gained from the discount.
    
                As a bonder, you lose if the price of OHM decreases during your vesting period.
                ''')
        st.title('The (4,4) strategy')
        fourFourLearnEpander = st.expander(label = 'click to view (4,4) Strategy', expanded=False)
        with fourFourLearnEpander:
            st.write(
                """
                (4,4) is simply a combination of staking and bonding, (3,3) + (1,1) = (4,4). We employ a (4,4) strategy by staking our vested OHM before rebases.
                 There are multiple ways to implement this strategy such as staking before every epoch or before every other epoch. The frequency would depend on the bond amount as well as gas prices.

                (4,4) has a drawback of requiring a lot of gas since it requires 15 smart contract interactions for the optimal strategy. 
                With Playground, you can simulate how often you should stake your vested OHM from your bond.
                """)
    st.markdown('''----''')

    st.title('What is (4,4) Playground? ')
    col5,col6 = st.columns((1.5,1))
    with col5:
        fourFourLearnEpander_2 = st.expander(label = 'click to view (4,4) Strategy', expanded=True)
        with fourFourLearnEpander_2:
                st.write(
                    """
                    **(4,4) Playground is a simulator for understanding and forecasting the bond, claim, and stake strategy**

                    Use this simulator to:
                    - Strategize (4,4) profitability
                    - Compare OHM growth between (3,3) and (4,4) 
                    - Compare Return on Investment between (3,3) and (4,4)
                    - Determine how often to stake your vested OHM
                    """
                )
    with col6:
        st.image(learn_44_playground)
    st.markdown('''----''')
    st.info('''
    Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics

    References to system governing equations can be found here
    [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is a the best source for due diligence and understanding
    the mechanics of Olympus protocol
    
    Forecasts are for educational purposes alone and should not be construed as financial advice
    
    **Disclaimer**
    
    Olympus Playgrounds is for educational purposes only and is not an individualized recommendation.
    Further Olympus Playgrounds are an educational tool and should not be relied upon as the primary basis for investment, financial, tax-planning, or retirement decisions.
    These metrics are not tailored to the investment objectives of a specific user.
    This educational information neither is, nor should be construed as, investment advice, financial guidance or an offer or a solicitation or recommendation to buy, sell, or hold any security, or to engage in any specific investment strategy by Olympus Playgrounds.
    These metrics used herein may change at any time and Olympus Playgrounds will not notify you when such changes are made. 
    You are responsible for doing your own diligence at all times.
        ''')
# endregion