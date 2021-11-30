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
from PIL import Image
from pathlib import Path
# import awesome_stream lit as ast
# endregion

learnStaking_logo = Path(__file__).parents[1] / 'Assets/LEARN_STAKING_2.png'
learnStaking_logo  = Image.open(learnStaking_logo)

learnStaking = Path(__file__).parents[1] / 'Assets/three.png'
learnStaking  = Image.open(learnStaking)

learnStaking_33 = Path(__file__).parents[1] / 'Assets/33_curve.png'
learnStaking_33  = Image.open(learnStaking_33)


def app():
# region Description: All about staking

    col1,col2 = st.columns((0.6,1))
    with col1:
        st.image(learnStaking_logo)
    st.markdown('''----''')
    st.title('The Staking Strategy')
    col3,col4 = st.columns((2.5,1.4))
    with col3:
        stakeLearnExpander = st.expander(label='Click to view Staking Strategy', expanded=True)
        with stakeLearnExpander:
            st.write(
                '''
                **Staking is the primary value accrual strategy of Olympus, we call staking (3,3)**. Stakers stake their OHM on the Olympus website to earn rebase rewards. 
                The rebase rewards come from the proceeds of bond sales, and can vary based on the number of OHM staked in the protocol and the reward rate set by the protocol.
        
                **Staking is a passive, long-term strategy**. The increase in your stake of OHM translates into a constantly falling cost basis converging on zero. 
                This means even if the market price of OHM drops below your initial purchase price, given a long enough staking period, the increase in your staked OHM balance should eventually outpace the fall in price.
        
                **When you stake, you lock OHM and receive an equal amount of sOHM**. Your sOHM balance compounds  automatically at the end of every epoch. 
                sOHM is transferable and therefore composable with other DeFi protocols such as Rari or Abracadabra. 
                sOHM continues to rebase while being used in other DeFi protocols or even in your hardware wallet.
        
                **When you unstake, you burn sOHM and receive an equal amount of OHM**. Unstaking means the user will forfeit the upcoming rebase reward.
                 Note that the forfeited reward is only applicable to the unstaked amount; the remaining staked OHM (if any) will continue to receive rebase rewards.
                ''')
    st.markdown('''----''')
    with col4:
        st.image(learnStaking)
    st.title('What is (3,3) Playground? ')
    col5,col6 = st.columns((1,1))
    with col5:
        st.image(learnStaking_33)
    with col6:
        threeThreeLearnExpander = st.expander(label='Click to view (3,3) Strategy', expanded=True)
        with threeThreeLearnExpander:
            st.write(
                """
                **(3,3) Playground is a simulator for staking and reward strategies**

                Use this simulator to forecast:
                - ROI at current and future reward yield percent
                - OHM growth over time
                - OHM and USD value over time
                """)
            st.write("""---""")

            st.write(
                """    
                Also, use this simulator to strategize:
                - Required staked OHM to reach desired daily staking rewards
                - Time until you are earning your desired daily staking rewards
                - Required staked OHM to reach desired weekly staking rewards
                - Time until you are earning your desired weekly staking rewards
                """)
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
