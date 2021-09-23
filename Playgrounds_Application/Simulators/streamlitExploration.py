import streamlit as st
import numpy as np
import matplotlib as plt


st.sidebar.title("Learn: (3,3) Strategy")
st.sidebar.info(
    ''' 
        (3,3) Playground is a simulator for staking, and incooom strategies.
        Use this simulator to:
        - Forcast ROI ar current and future reward yield percent
        - OHM growth over time
        - OHM and USD value over time

        We love the incooom, use this simulator to strategize:
        - Required staked OHM to reach desired daily incooom
        - Count down until you are earning desired daily incooom
        - Required staked OHM to reach desired weekly incooom
        - Count down until you are earning desired weekly incooom

        Key things to understand:
        - [Market_Dynamics](https://docs.olympusdao.finance/protocol-internals/market-dynamics)
        
        Dive deeper: [Olympus Gitbook](https://docs.olympusdao.finance/)
        '''
)