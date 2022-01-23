# ==============THE LIBRARIES
# region Description: Import all required libraries for this simulator
from pycoingecko import CoinGeckoAPI # Coin gecko API: Pulls live data from coin gecko
import math  # Needed for basic math operations\n",
import pandas as pd  # Needed fpr dataframe creation and operations\n",
import numpy as np  # Needed for array manipulations\n",
from itertools import islice  # Needed for more complex row and coloumn slicing\n",
import matplotlib.pyplot as plt  # Needed for quickly ploting results"
import base64
from PIL import Image
import pathlib  # url management
from pathlib import Path
import plotly.express as px  # cleaner graphs
import plotly.graph_objects as go  # cleaner graphs
import plotly.figure_factory as ff
import streamlit as st

# endregion


bondingPlay_Logo = Path(__file__).parents[1] / 'Assets/bondingPlayground_logo.png'
bondingPlay_Logo  = Image.open(bondingPlay_Logo)
# ================THE APP
# region Description: Build the app
def app():

    with st.sidebar.expander('Welcome'):
        st.write('''
                Bonding simulation charts show you optimum ROI based on claiming and staking frequency over the 5 day vesting period. 
                
                The simulator takes the following fees into consideration:
                - Claim and Autostake fees
                - Staking fees
                - Bonding fees
                - Misc fees for more complex transactions
                
                Hover your mouse over the chart trend lines to see live feedback.
                Use the slider and number input boxes to adjust your goals and see the results displayed the provided charts and tables. 
            ''')

    with st.sidebar.expander('Control Parameters',expanded=True):

        ohmPrice = st.text_input('Price of OHM to simulate ($)', value=800.000)
        priceofETH = st.text_input('Price of ETH to simulate ($)', value=3500.000)
        initialOhms = st.text_input('Starting amount of OHM (Units)', value=100.0000)
        bondROI = st.text_input('Bond ROI (%)', value=6.000)
        rewardYield = st.text_input('Rebase rate (%)', value=0.3928)
        gwei = st.text_input('Highest network gas fee (gwei)', value=40.0000, )

        ohmPrice = float(ohmPrice)
        priceofETH = float(priceofETH)
        initialOhms = float(initialOhms)
        bondROI = float(bondROI)
        rewardYield = float(rewardYield)
        gwei = float(gwei)

    vestedOhms_df, stakedOhmsROI_df, stake_bond_df ,stakingGasFee,unstakingGasFee,swappingGasFee,claimGasFee,bondingGasFee,maxBondROI,stakingRewardRate_P,\
        maxStakeGrowth,maxBondGrowth,ohmGained , vestedOhms_df_CSV,stakedOhmsROI_df_CSV = bondingSimulation(ohmPrice,priceofETH,initialOhms,bondROI,rewardYield,gwei)

    #st.write(vestedOhms_df)
    #st.write(stakedOhmsROI_df)
    #st.write(stake_bond_df)
    #st.line_chart(stake_bond_df)

    # plots
    stake_bond_chart = go.Figure()

    stake_bond_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Vested_Ohms, name='(4,4) Growth',
                                          fill=None, line=dict(color='#00aff3', width=2)))
    stake_bond_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Stake_Growth, name='(3,3) Growth',
                                          line=dict(color='#ff2a0a', width=2)))

    stake_bond_chart.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    stake_bond_chart.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                   xaxis_title="Epochs (Vesting period)", yaxis_title = "Total Ohms")
    stake_bond_chart.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

    stake_bond_chart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.1, mirror=True)
    stake_bond_chart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01, mirror=True)

    bonding_hover_template = "<b>Epoch: </b> %{x} <br>"
    bonding_hover_template += "<b>Ohm: </b> %{y} <br>"
    stake_bond_chart.update_traces(hovertemplate=bonding_hover_template)

    #=============================

    stake_bond_ROIchart = go.Figure()

    stake_bond_ROIchart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Bond_ROI, name='(4,4) ROI  ',
                                             line=dict(color='#00aff3', width=2)))
    stake_bond_ROIchart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Stake_ROI, name='(3,3) ROI  ', fill=None,
                                             line=dict(color='#ff2a0a', width=2)))

    stake_bond_ROIchart.update_layout(autosize = True,showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    stake_bond_ROIchart.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                      xaxis_title = "Epochs (Vesting period)", yaxis_title = "ROI based on claim/stake frequency")
    stake_bond_ROIchart.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

    stake_bond_ROIchart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.1, mirror=True)
    stake_bond_ROIchart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01, mirror=True)

    stake_bond_ROIchart.update_traces(hovertemplate=bonding_hover_template)
# end region


# Layout and object placement
    col1,col2 = st.columns((1,1))
    with col1:
        st.image(bondingPlay_Logo)
    st.markdown('''----''')
    col3,col4 = st.columns((4,1.3))
    with col3:
        st.header('(4,4) and (3,3) Ohm Growth Comparison')
        st.plotly_chart(stake_bond_chart, use_container_width=True)
    with col4:
        st.header('Results summary')
        st.info(f'''
        - Max (3,3): ** {maxStakeGrowth} OHMs**
        - Max (4,4): ** {maxBondGrowth} OHMs**
        - Bonus: ** {ohmGained} OHMs**
        ''')
        st.header('Chart Instructions')
        with st.expander('Click to view'):
            st.write('''
             The chart is designed to be interactive and allows you to view and analyze your results. Here are some cool things you can do:

             - Hide and view trend lines by clicking on the legends

             - Use the toolbar to access tools such as zoom, pan, data comparison, spike lines, and download. The tool bar is revealed when you hover your mouse on the chart''')
        #st.download_button(
        #    "Press to download your (4,4) simulation results",
        #    vestedOhms_df_CSV,
        #    "ohmGrowthSim.csv",
        #    "text/csv",
        #    key='browser-data'
        #)
    st.header('Explanation')
    with st.expander('Click to view'):
        st.write('''
                This chart contains two trend lines (3,3) OHM Growth and (4,4) OHM Growth.
                The (4,4) OHM growth trend line depicts the OHM growth based on claim/stake frequency throughout the vesting period. 
                As we have learned in the Bonding: Learn page, bonding allows to purchase OHM at a discount from the protocol. 
                Bonding provides an opportunity to acquire more OHMs when compared to market buying. 
                This opportunity could be further amplified by claiming/staking vested ohms as they become available to you. 
                Please see the ROI comparison chart for details on the effects of claiming/staking frequency.

                The (3,3) OHM growth trend line depicts OHM growth throughout the same vesting period.
                
                This chart compares simple staking (3,3) and the claim/stake (4,4) OHM growth throughout the vesting period 
                (In Olympus, the vesting period is 15 epochs, equivalent to 5 days). 
                    ''')
    st.write("-----------------------------")
    col5,col6 = st.columns((4,1.3))
    with col5:
        st.header('(4,4) and (3,3) ROI Growth Comparison')
        st.plotly_chart(stake_bond_ROIchart, use_container_width=True)
    with col6:
        st.header('Results summary')
        st.info(f'''
        - Stake (3,3) ROI: **{stakingRewardRate_P} %**
        - Bond ROI: **{bondROI} %**
        - Max (4,4) ROI: **{maxBondROI} %**
            ''')
        st.header('Chart Instructions')
        with st.expander('Click to view'):
            st.write('''
             The chart is designed to be interactive and allows you to view and analyze your results. Here are some cool things you can do:

             - Hide and view trend lines by clicking on the legends

             - Use the toolbar to access tools such as zoom, pan, data comparison, spike lines, and download. The tool bar is revealed when you hover your mouse on the chart''')

    st.header('Explanation')
    with st.expander('Click to view'):
        st.write('''
                    This chart contains two trend lines (3,3) ROI and (4,4) ROI. 

                    The (4,4) ROI trend line depicts the bonding ROI based on claim/stake frequency throughout the vesting period. 
                    For example, depending on the control parameters, the highest ROI could be achieved by claiming/staking vested OHM tokens before every epoch, halfway through, or maybe the first four epochs. There might also be scenarios where it is not profitable for you to claim/stake at all. 
                    There could be many claim/stake combinations; the chart tries to predict the best possible combination. 

                    The (3,3) ROI trend line depicts plain staking ROI throughout the same vesting period. 

                    This chart compares simple staking (3,3) and the claim/stake (4,4) ROIs throughout the vesting period 
                    (In Olympus, the vesting period is 15 epochs, equivalent to 5 days). 
                    ''')
    st.write('''---''')

    st.info('''
    Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics

    References to system governing equations can be found here
    [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is a the best source for due diligence and understanding
    the mechanics of Olympus protocol

    **Disclaimer**
    
    Olympus Playgrounds is for educational purposes only and is not an individualized recommendation.
    Further Olympus Playgrounds are an educational tool and should not be relied upon as the primary basis for investment, financial, tax-planning, or retirement decisions.
    These metrics are not tailored to the investment objectives of a specific user.
    This educational information neither is, nor should be construed as, investment advice, financial guidance or an offer or a solicitation or recommendation to buy, sell, or hold any security, or to engage in any specific investment strategy by Olympus Playgrounds.
    These metrics used herein may change at any time and Olympus Playgrounds will not notify you when such changes are made. 
    You are responsible for doing your own diligence at all times.
        ''')

# region Description: Function to calculate ohm growth over time
def bondingSimulation(ohmPrice,priceofETH,initialOhms,bondROI,rewardYield,gwei):
    # Protocol and ohm calcs:
    usdBonded = ohmPrice * initialOhms
    bondROI = (bondROI/100)
    bondPrice = ohmPrice / (1 + (bondROI))
    bondedOhms = usdBonded / bondPrice
    bondedOhmsValue = bondedOhms * ohmPrice
    # ========================================================================================
    # Calculate the rebase rate and Current APY (next epoch rebase pulled from hippo data source)
    rewardYield = rewardYield / 100
    rebaseConst = 1 + rewardYield  # calculate a constant for use in APY calculation
    currentAPY = (rebaseConst) ** (1095)   # current APY equation
    currentAPY_P = (currentAPY) * 100  # convert to %
    # ========================================================================================
    # Calculate fees
    stakingGasFee = 179123 * ((gwei * priceofETH) / (10 ** 9))
    unstakingGasFee = 89654 * ((gwei * priceofETH) / (10 ** 9))
    swappingGasFee = 225748 * ((gwei * priceofETH) / (10 ** 9)) + ((0.3 / 100) * bondedOhmsValue)
    claimGasFee = 80209 * ((gwei * priceofETH) / (10 ** 9))
    bondingGasFee = 258057 * ((gwei * priceofETH) / (10 ** 9))
    # miscFee = 823373 * ((gwei*priceofETH)/(10**9))
    # ================================================================================

    claimStakeGasFee = stakingGasFee + claimGasFee
    remainingGasFee = bondingGasFee + unstakingGasFee + swappingGasFee
    # ================================================================================
    # (3,3) Rate for the 15 epochs
    stakingRewardRate = (1+rewardYield) ** 15 - 1
    stakingRewardRate_P = round(stakingRewardRate*100,2)
    #stakingOhmsGained = round(((initOhmValue - stakingGasFee) * (stakingRate / initOhmValue) - 1),4)

    # (3,3) Ohm gained after 15 epochs
    stakingOhmGrowth = stakingRewardRate * bondedOhmsValue / ohmPrice
    stakingOhmGrowth = round(stakingOhmGrowth, 4)
    # ================================================================================
    vestedOhms_df = pd.DataFrame(np.arange(1, 16), columns=['Epochs'])
    vestedOhms_df['Days'] = vestedOhms_df.Epochs / 3
    vestedOhmGrowth = np.array([], dtype=np.float64)
    bondROIGrowth = np.array([], dtype=np.float64)

    stakedOhmsROI_df = pd.DataFrame(np.arange(1, 16), columns=['Epochs'])
    stakedOhmsROI_df['Days'] = stakedOhmsROI_df.Epochs / 3
    stakedROIAdjustedGrowth = np.array([], dtype=np.float64)
    stakeROIGrowth = np.array([], dtype=np.float64)
    stakedOhmsGrowth = np.array([], dtype=np.float64)
    stakeGrowth = initialOhms

    for epochs in vestedOhms_df.Epochs:
        vestedOhm = ((bondedOhms / (1 + epochs)) * (((1+rewardYield) ** 15) - 1)) / ((1+rewardYield) ** (15 / (1 + epochs)) - 1)
        vestedOhmROI = (((vestedOhm * ohmPrice - epochs * (claimStakeGasFee) - remainingGasFee) / usdBonded) - 1) * 100
        vestedOhmGrowth = np.append(vestedOhmGrowth, vestedOhm)
        bondROIGrowth = np.append(bondROIGrowth, vestedOhmROI)
    vestedOhms_df['Vested_Ohms'] = vestedOhmGrowth
    vestedOhms_df['Bond_ROI'] = bondROIGrowth

    for epochs in stakedOhmsROI_df.Epochs:
        stakedOhmsGrowth = np.append(stakedOhmsGrowth, stakeGrowth)
        stakedROIAdjusted = ((usdBonded - stakingGasFee) * (((1+rewardYield) ** 15) / usdBonded) - 1) * 100
        stakeROI = stakingRewardRate * 100
        stakeGrowth = stakeGrowth * (1+rewardYield)
        stakedROIAdjustedGrowth = np.append(stakedROIAdjustedGrowth, stakedROIAdjusted)
        stakeROIGrowth = np.append(stakeROIGrowth, stakeROI)
    stakedOhmsROI_df['Stake_ROI'] = stakeROIGrowth
    stakedOhmsROI_df['Staked_feeAdjustedROI'] = stakedROIAdjustedGrowth
    stakedOhmsROI_df['Stake_Growth'] = stakedOhmsGrowth
    # ================================================================================

    cols_to_use = stakedOhmsROI_df.columns.difference(vestedOhms_df.columns)
    stake_bond_df = pd.merge(vestedOhms_df, stakedOhmsROI_df[cols_to_use], left_index=True, right_index=True, how='outer')
    #stake_bond_df = pd.concat([vestedOhms_df,stakedOhmsROI_df],axis = 1, join = 'inner')

    maxBondROI = round(stake_bond_df.Bond_ROI.max(),2)
    maxStakeGrowth = round(stake_bond_df.Stake_Growth.max(),2)
    maxBondGrowth = round(stake_bond_df.Vested_Ohms.max(), 2)
    ohmGained = round((stake_bond_df.Vested_Ohms.max()-stake_bond_df.Stake_Growth.max()),2)
    stakingGasFee = round(stakingGasFee,2)
    unstakingGasFee = round(unstakingGasFee,2)
    swappingGasFee = round(swappingGasFee,2)
    claimGasFee = round(claimGasFee,2)
    bondingGasFee = round(bondingGasFee,2)

    vestedOhms_df_CSV = vestedOhms_df.to_csv().encode('utf-8')
    stakedOhmsROI_df_CSV = stakedOhmsROI_df.to_csv().encode('utf-8')

    return vestedOhms_df, stakedOhmsROI_df, stake_bond_df ,stakingGasFee,unstakingGasFee,swappingGasFee,claimGasFee,bondingGasFee,maxBondROI,stakingRewardRate_P,maxStakeGrowth,maxBondGrowth,ohmGained,vestedOhms_df_CSV,stakedOhmsROI_df_CSV
# end region
