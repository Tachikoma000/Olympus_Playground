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
import plotly.figure_factory as ff
import altair as alt
import streamlit as st
# endregion

# ================THE APP
# region Description: Build the app
def app():

    with st.sidebar.expander('How to use'):
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

        ohmPrice = st.text_input('Price of OHM to simulate ($)', value=600.000)
        priceofETH = st.text_input('Price of ETH to simulate ($)', value=3000.000)
        #usdBonded = st.text_input('Amount to bond ($)', value=5000.000)
        initialOhms = st.text_input('Starting amount of OHM (Units)', value=100.0000)
        bondROI = st.text_input('Bond ROI (%)', value=6.000)
        rewardYield = st.text_input('Rebase rate (%)', value=0.3928)
        gwei = st.text_input('Highest network gas fee (gwei)', value=40.0000, )

        ohmPrice = float(ohmPrice)
        priceofETH = float(priceofETH)
        #usdBonded = float(usdBonded)
        initialOhms = float(initialOhms)
        bondROI = float(bondROI)
        rewardYield = float(rewardYield)
        gwei = float(gwei)


    bondingSimulationResults_ROI_df, bondingSimulationResults_ohmGrowth_df, stakingSimulationResults_ROI_df, stakingSimulationResults_ohmGrowth_df,\
    discountedOhmPrice,claimGasFee, remainingGasFee, stakingGasFee, unstakingGasFee, swappingGasFee, bondingGasFee, stakingRate_P,currentAPY_P = bondingSimulation(ohmPrice,priceofETH,initialOhms,bondROI,rewardYield,gwei)

    roiCharts = go.Figure()

    roiCharts.add_trace(go.Scatter(x = bondingSimulationResults_ROI_df['Epochs'], y = bondingSimulationResults_ROI_df['Bonding_ROI_5Days'],
                                                       mode = 'lines+markers',
                                                       name = '(4,4) Roi'))
    roiCharts.update_layout(xaxis_title='Epochs', yaxis_title='ROI', height=500)
    roiCharts.data[0].update(line_color='teal')


    roiCharts.add_trace(go.Scatter(x = stakingSimulationResults_ROI_df['Epochs'], y = stakingSimulationResults_ROI_df['Staking_ROI_5Days'],
                                                       mode = 'lines+markers',
                                                       name = '(3,3) Roi'))
    roiCharts.data[1].update(line_color='red')

    #roiCharts.update_layout(paper_bgcolor='#fbfbfb')


    bondingGrowthChart = go.Figure()

    bondingGrowthChart.add_trace(go.Scatter(x = bondingSimulationResults_ohmGrowth_df['Epochs'],
                                            y = bondingSimulationResults_ohmGrowth_df['Accumulated_Ohms_Bonding'],
                                            mode = 'lines+markers',
                                            name = '(4,4)'))
    bondingGrowthChart.update_layout(xaxis_title='Epochs', yaxis_title='OHM Accumulated', height=500)
    bondingGrowthChart.data[0].update(line_color='teal')

    bondingGrowthChart.add_trace(go.Scatter(x=stakingSimulationResults_ohmGrowth_df['Epochs'],
                                            y=stakingSimulationResults_ohmGrowth_df['Accumulated_Ohms_Staking'],
                                            mode='lines+markers',
                                            name='(3,3)'))
    bondingGrowthChart.data[1].update(line_color='red')
    #bondingGrowthChart.update_layout(paper_bgcolor='#fbfbfb')


    st.title('Bonding playground')
    st.write("-----------------------------")

    col1, col2 = st.columns((4,1.25))
    with col1:
        st.header('(4,4) and (3,3) ROI Comparisons')
        st.plotly_chart(roiCharts, use_container_width=True)
    with col2:
        st.header('Fees')
        st.info(f'''
        - Claim and Stake Fees: **$ {claimGasFee}**
        
        - Staking Fees: **$ {stakingGasFee}**
        
        - Unstaking Fees: **$ {unstakingGasFee}**
        
        - Swapping Fees: **$ {swappingGasFee}**
        
        - Bonding Fees: **$ {bondingGasFee}**
        ''')
        with st.expander('Chart Explanation', expanded=False):
            st.write('''
            The chart compares the ROI from (3,3) alone and (4,4) with varying claiming and staking frequency 
            over the 5 day vesting period. 

            -The red trend line is the 5 day ROI if you were to (3,3) alone

            -The blue trend line is the ROI based claiming and staking frequency during the 5 day 
            vesting period

            For example, tick 6 on the x - axis means you only claimed and staked during the 6 epochs
            of the total 15 epochs (5 days)
            ''')
    st.write("-----------------------------")

    col3, col4 = st.columns((4, 1.25))
    with col3:
        st.header('(4,4) and (3,3) Ohm Growth Comparison')
        st.plotly_chart(bondingGrowthChart, use_container_width=True)
    with col4:
        st.header('Rates Comparison')
        st.info(f'''
        - 5 Day ROI (3,3): **{stakingRate_P} %**
        - 5 Day ROI (4,4): **{bondROI} %**
        - APY (3,3): **{currentAPY_P} %**
            ''')
        with st.expander('Chart Explanation', expanded=False):
            st.write('''
            This chart shows you the ohm growth over the 5 day period if you were to claim and stake at 
            each epoch. 
            
            Similar to the ROI chart, the x-axis represents the claiming and staking frequency. 
            ''')
    st.write("-----------------------------")
# end region

# region Description: Function to calculate ohm growth over time
def bondingSimulation(ohmPrice,priceofETH,initialOhms,bondROI,rewardYield,gwei):
    # Protocol and ohm calcs:
    discountedOhmPrice = round(ohmPrice / (1 + (bondROI / 100)),4)
    initOhmValue = round(initialOhms * ohmPrice,4)
    bondedOhms = round(initOhmValue / discountedOhmPrice,4)
    bondROI = round(bondROI / 100,4)
    # ========================================================================================

    # Calculate the rebase rate and Current APY (next epoch rebase pulled from hippo data source)
    rewardRate = round(rewardYield / 100, 4)
    rebaseConst = 1 + rewardRate  # calculate a constant for use in APY calculation
    currentAPY = (rebaseConst) ** (1095)   # current APY equation
    currentAPY_P = round((currentAPY) * 100,1)  # convert to %
    # ========================================================================================

    # Calculate fees
    stakingGasFee = round(179123 * ((gwei * priceofETH) / pow(10, 9)),1)
    unstakingGasFee = round(89654 * ((gwei * priceofETH) / (10 ** 9)),1)
    swappingGasFee = round(225748 * ((gwei * priceofETH) / (10 ** 9)) + ((0.3 / 100) * initOhmValue),1)
    claimGasFee = round(80209 * ((gwei * priceofETH) / (10 ** 9)),1)
    bondingGasFee = round((258057) * ((gwei * priceofETH) / (10 ** 9)),1)
    # miscFee = 823373 * ((gwei*priceofETH)/(10**9))
    # ================================================================================

    claimStakeGasFee = stakingGasFee + claimGasFee
    remainingGasFee = bondingGasFee + unstakingGasFee + swappingGasFee
    # ================================================================================

    # (3,3)
    stakingRate = round(((rebaseConst) ** 15) - 1,4)  # staking reward rate
    stakingRate_P = round(stakingRate * 100, 2)  # staking reward rate in percentage
    stakingOhmsGained = round(((initOhmValue - stakingGasFee) * (stakingRate / initOhmValue) - 1),4)
    # ================================================================================

    # Calculate ohm roi over 5 day period for comparison
    ohmGrowthEpochs = 16
    stakingSimulationResults_ROI_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])
    stakingSimulationResults_ROI_df['Days'] = round(stakingSimulationResults_ROI_df.Epochs / 3,1)
    stakingSimulationResults_ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])
    stakingSimulationResults_ohmGrowth_df['Days'] = round(stakingSimulationResults_ohmGrowth_df.Epochs / 3,1)
    ohmStakedGrowth = bondedOhms
    accumulatedOhmsROI_Staking = []
    accumulatedOhms_Staking = []

    for elements in stakingSimulationResults_ROI_df.Epochs:
        stakingOhmsGrowth_ROI = round(((initOhmValue - stakingGasFee) * ((rebaseConst ** 15) / initOhmValue) - 1) * 100,4)
        accumulatedOhmsROI_Staking.append(stakingOhmsGrowth_ROI)
    stakingSimulationResults_ROI_df['Staking_ROI_5Days'] = accumulatedOhmsROI_Staking

    for elements in stakingSimulationResults_ohmGrowth_df.Epochs:
        accumulatedOhms_Staking.append(ohmStakedGrowth)
        ohmStakedGrowth = ohmStakedGrowth * (rebaseConst)
    stakingSimulationResults_ohmGrowth_df['Accumulated_Ohms_Staking'] = accumulatedOhms_Staking  # Clean up and add the new array to the main data frame
    stakingSimulationResults_ohmGrowth_df.Days = np.around(stakingSimulationResults_ohmGrowth_df.Days, decimals=1)  # Python is funny so let's round up our numbers . 1 decimal place for days",
    stakingSimulationResults_ohmGrowth_df.Total_Ohms = np.around(stakingSimulationResults_ohmGrowth_df.Accumulated_Ohms_Staking,decimals=3)  # Python is funny so let's round up our numbers . 3 decimal place for ohms"

    # (4,4)
    bondingRate = (round(bondROI / 100, 4))  # bonding reward rate
    bondingRate_P = bondROI
    #round(bondingRate * 100, 4)  # bonding reward rate in percentage
    # bondingOhmsGained = (usdBonded*bondingRate / discountedOhmPrice)  # ohms gained from bonding
    # ================================================================================

    # Instantiate a data frame to hold the staking only ohm growth over 5 days
    bondingSimulationResults_ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs), columns=['Epochs'])
    bondingSimulationResults_ohmGrowth_df['Days'] = round(bondingSimulationResults_ohmGrowth_df.Epochs / 3,1)

    bondingSimulationResults_ROI_df = pd.DataFrame(np.arange(ohmGrowthEpochs), columns=['Epochs'])
    bondingSimulationResults_ROI_df['Days'] = round(bondingSimulationResults_ROI_df.Epochs / 3,1)

    accumulatedOhms_Bonding = []
    accumulatedOhmsROI_Bonding = []

    for elements in bondingSimulationResults_ohmGrowth_df.Epochs:
        bondedOhmsGrowth = round(((bondedOhms/(1+elements))*((rebaseConst**15)-1))/((rebaseConst**(15/(1+elements)))-1),3)
        accumulatedOhms_Bonding.append(bondedOhmsGrowth)
    bondingSimulationResults_ohmGrowth_df['Accumulated_Ohms_Bonding'] = accumulatedOhms_Bonding

    for elements in bondingSimulationResults_ROI_df.Epochs:
        bondingOhmsGrowth_ROI = round((((bondingSimulationResults_ohmGrowth_df.Accumulated_Ohms_Bonding.iloc[elements]*ohmPrice-elements*(claimStakeGasFee)-remainingGasFee)/initOhmValue)-1)*100,3)
        accumulatedOhmsROI_Bonding.append(bondingOhmsGrowth_ROI)
    bondingSimulationResults_ROI_df['Bonding_ROI_5Days'] = accumulatedOhmsROI_Bonding
    # ================================================================================

    return bondingSimulationResults_ROI_df, bondingSimulationResults_ohmGrowth_df, stakingSimulationResults_ROI_df,\
           stakingSimulationResults_ohmGrowth_df,discountedOhmPrice,claimGasFee, remainingGasFee, stakingGasFee,\
           unstakingGasFee, swappingGasFee, bondingGasFee, stakingRate_P,currentAPY_P
# end region

