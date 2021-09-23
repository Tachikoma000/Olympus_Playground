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


# region Description: Build the app
def app():

    with st.sidebar.expander('How to use'):
        st.write('''
                Hover your mouse over the chart trend lines to see live feedback on Total ohms accumulated vs days.
                Use the slider and number input boxes to adjust your goals and see the results displayed on the incoom charts and table. 
            ''')

    with st.sidebar.expander('Control Parameters'):
        ohmGrowthDays = st.slider('Days', value=365, min_value=1, max_value=730, step=1)
        ohmPrice = st.text_input('Price of OHM to simulate ($)', value=500.000)
        initialOhms = st.text_input('Starting amount of OHM (Units)', value=1.0000)
        rewardYield = st.text_input('Rebase rate (%)', value=0.4583)
        desiredUSDTarget = st.text_input('Desired OHM value (USD)', value=10000.0000,)
        desiredOHMTarget = st.text_input('Desired amount of OHMS', value=500.0000, )
        desiredDailyIncooom = st.text_input('Desired daily incooom (USD)', value=5000.0000,)
        desiredWeeklyIncooom = st.text_input('Desired weekly incooom (USD)', value=50000.000,)


        ohmGrowthDays = float(ohmGrowthDays)
        ohmPrice = float(ohmPrice)
        initialOhms = float(initialOhms)
        rewardYield = float(rewardYield)
        desiredUSDTarget = float(desiredUSDTarget)
        desiredOHMTarget = float(desiredOHMTarget)
        desiredDailyIncooom = float(desiredDailyIncooom)
        desiredWeeklyIncooom = float(desiredWeeklyIncooom)

    ohmGrowthResult_df = ohmGrowth_Projection(initialOhms, rewardYield, ohmGrowthDays)
    roiSimulationResult_df,incooomSimulationResult_df = incooomProjection(ohmPrice,rewardYield, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom)
    forcastUSDTarget = float(incooomSimulationResult_df.Results[0])
    forcastOHMTarget = float(incooomSimulationResult_df.Results[1])
    requiredOHMDailyIncooom = float(incooomSimulationResult_df.Results[2])
    forcastDailyIncooom = float(incooomSimulationResult_df.Results[3])
    requiredOHMWeeklyIncooom = float(incooomSimulationResult_df.Results[4])
    forcastWeeklyIncooom = float(incooomSimulationResult_df.Results[5])

    ohmGrowthResult_df_Chart = px.scatter(ohmGrowthResult_df, x = 'Days', y = 'Total_Ohms', )
    ohmGrowthResult_df_Chart = ohmGrowthResult_df_Chart.update_traces(marker_size=2)
    ohmGrowthResult_df_Chart.update_layout(paper_bgcolor = '#fbfbfb')


    st.title('Staking playground')
    st.write("-----------------------------")

    st.header('OHM growth forcast')
    col1, col2 = st.columns((2, 1))
    with col1:
        st.plotly_chart(ohmGrowthResult_df_Chart,use_container_width=True)
    with col2:
        with st.expander('Key parameters used for forcast', expanded=True):
            st.write('''
                        [Asset allocation (OHM staked)](https://docs.olympusdao.finance/basics/staking), [APY](https://docs.olympusdao.finance/basics/basics#what-is-apy),
                        and [Rebase Rate](https://docs.olympusdao.finance/basics/basics#what-is-a-rebase) are main factors that determine returns and incooom over time.                        Play with the simulator and see how your starting OHM affects your projected accured value over time.
                        Additionally, use the incooom parameters to forcast daily and weekly incooom from (3,3) alone. 
                     ''')
        with st.expander('Forcast data'):
            st.write(ohmGrowthResult_df)
        st.write(f'''
        ### Results explanation
        This chart shows you the ohm growth projection over **{ohmGrowthDays} days**.
        Projection is calculated based on your selected rebase rate of **{rewardYield} %** and an 
        initial **{initialOhms} ohms**.
        ''')
    st.write("-----------------------------")

    st.header('Roi and incooom forcast')
    col3, col4 = st.columns((2, 1))
    with col3:
        st.write(f'''
        Based on your control parameters, these are the predicted outcomes assuming market stability and your parameters
        hold true. 
        
        - It would take **{forcastUSDTarget} days** until you accumulate enough ohms worth **$ {desiredUSDTarget}**. Keep in mind that you are also predicting 
        that the price of ohm will be **$ {ohmPrice}** on this day. 
        
        - It would take **{forcastOHMTarget} days** until you accumulate **{desiredOHMTarget} ohms**. Keep in mind that this prediction is calculated based on 
        your selected rebase rate of **{rewardYield} %** and an initial of **{initialOhms} ohms** staked. Use the OIP-18 Framework to adjust your rebase rate parameter. 
        
        - To start earning a daily incooom of **$ {desiredDailyIncooom}** from staking rewards, you will need **{requiredOHMDailyIncooom} ohms**, 
        and based on the rebase rate you entered; it would take **{forcastDailyIncooom} days** to reach your goal. 
        Remember that this prediction relies on your selected rebase rate of **{rewardYield} %**, initial **{initialOhms} ohms** staked,
         and predicated price of **$ {ohmPrice}**/ohm
         
        - To start earning a weekly incooom of **$ {desiredWeeklyIncooom}** from staking rewards, you will need **{requiredOHMWeeklyIncooom} ohms**, 
        and based on the rebase rate you entered; it would take **480 days** to reach your goal. 
        Remember that this prediction relies on your selected rebase rate of **0.4583%**, initial **1.0 ohms** staked,
         and predicated price of **$ {ohmPrice}**/ohm
         
         
        ''')
    with col4:
        st.write(roiSimulationResult_df)
    st.write("-----------------------------")

    st.info('Forcasts are for educational purposes alone and should not be used as financial advice')
# end region


# region Description: Function to calculate ohm growth over time
def ohmGrowth_Projection(initialOhms, rewardYield, ohmGrowthDays):
    # Data frame to hold all required data point. Data required would be Epochs since rebase are distributed every Epoch
    ohmGrowthEpochs = ohmGrowthDays * 3
    ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])  # In this case let's consider 1096 Epochs which is 365 days
    ohmGrowth_df['Days'] = ohmGrowth_df.Epochs / 3  # There are 3 Epochs per day so divide by 3 to get Days
    # To Calculate the ohm growth over 3000 Epochs or 1000 days, we loop through the exponential ohm growth equation every epoch
    totalOhms = []  # create an empty array that will hold the componded rewards
    rewardYield = round(rewardYield / 100, 5)
    ohmStakedGrowth = initialOhms  # Initial staked ohms used to project growth over time
    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms.append(ohmStakedGrowth)  # populate the empty array with calclated values each iteration
        ohmStakedGrowth = ohmStakedGrowth * (1 + rewardYield)  # compound the total amount of ohms
    ohmGrowth_df['Total_Ohms'] = totalOhms  # Clean up and add the new array to the main data frame
    ohmGrowth_df.Days = np.around( ohmGrowth_df.Days, decimals=1)  # Python is funny so let's round up our numbers . 1 decimal place for days",
    ohmGrowth_df.Total_Ohms = np.around( ohmGrowth_df.Total_Ohms, decimals=3 )  # Python is funny so let's round up our numbers . 3 decimal place for ohms"
    # ================================================================================
    return ohmGrowth_df
# end region

# region Description: Function to calculate income forcast
def incooomProjection(ohmPrice,rewardYield, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom):

    ohmStakedInit = initialOhms
    rewardYield = round(rewardYield / 100, 5)
    rebaseConst = 1 + rewardYield
    # current staking %APY. Need to make this read from a source or user entry
    currentAPY = 17407 / 100

    # Let's get some ROI Outputs starting with the daily
    dailyROI = (1 + rewardYield)**3 - 1  # Equation to calculate your daily ROI based on reward Yield
    dailyROI_P = round(dailyROI * 100, 2)  # daily ROI in Percentage
    # ================================================================================

    # 5 day ROI
    fivedayROI = (1 + rewardYield)**(5 *3) - 1  # Equation to calculate your 5 day ROI based on reward Yield
    fivedayROI_P = round(fivedayROI * 100, 2)  # 5 day ROI in Percentage
    # ================================================================================

    # 7 day ROI
    sevendayROI = (1 + rewardYield)**( 7 * 3) - 1  # Equation to calculate your 7 day ROI based on reward Yield
    sevendayROI_P = round(sevendayROI * 100, 2)  # 7 day ROI in Percentage
    # ================================================================================

    # 30 day ROI
    monthlyROI = (1 + rewardYield)**( 30 *3) - 1  # Equation to calculate your 30 day ROI based on reward Yield
    monthlyROI_P = round(monthlyROI * 100, 2)  # 30 day ROI in Percentage
    # ================================================================================

    # Annual ROI
    annualROI = (1 + rewardYield)**( 365 *3) - 1  # Equation to calculate your annual ROI based on reward Yield
    annualROI_P = round(annualROI * 100, 2)  # Equation to calculate your annual ROI based on reward Yield
    # ================================================================================

    # Let's create a nice looking table to view the results of our calculations. The table will contain the ROIs and the percentages
    roiData = [['Daily', dailyROI_P],
               ['5 Day', fivedayROI_P],
               ['7 Day', sevendayROI_P],
               ['1 Month', monthlyROI_P],
               ['1 Year', annualROI_P]]
    roiTabulated_df = pd.DataFrame(roiData, columns=['Cadence', 'Percentage'])
    roiDataTable = roiTabulated_df.to_dict('rows')
    columns = [{'name': i,'id': i,} for i in (roiTabulated_df.columns)]
    # ================================================================================
    # Days until you reach target USD by staking only
    forcastUSDTarget = round((math.log(desiredUSDTarget / (ohmStakedInit * ohmPrice), rebaseConst) /3))
    # ================================================================================
    # Days until you reach target OHM by staking only
    forcastOHMTarget = round(math.log(desiredOHMTarget / (ohmStakedInit), rebaseConst) / 3)
    # ================================================================================
    # Daily Incooom calculations
    # Required OHMs until you are earning your desired daily incooom
    requiredOHMDailyIncooom = round((desiredDailyIncooom / dailyROI) / ohmPrice)
    # Days until you are earning your desired daily incooom from your current initial staked OHM amount
    forcastDailyIncooom = round(math.log((requiredOHMDailyIncooom / ohmStakedInit), rebaseConst) / 3)
    requiredUSDForDailyIncooom = requiredOHMDailyIncooom * ohmPrice
    # ================================================================================
    # Weekly Incooom calculations
    # Required OHMs until you are earning your desired weekly incooom
    requiredOHMWeeklyIncooom = round((desiredWeeklyIncooom / sevendayROI) / ohmPrice)
    # Days until you are earning your desired weekly incooom from your current initial staked OHM amount
    forcastWeeklyIncooom = round(math.log((requiredOHMWeeklyIncooom / ohmStakedInit), rebaseConst) / 3)
    requiredUSDForWeeklyIncooom = requiredOHMWeeklyIncooom * ohmPrice
    # ================================================================================
    # Let's create a nice looking table to view the results of our calculations. The table will contain the ROIs and the percentages
    incooomForcastData = [['USD Target($)', forcastUSDTarget],
                          ['OHM Target(OHM)', forcastOHMTarget],
                          ['Required OHM for desired daily incooom', requiredOHMDailyIncooom],
                          ['Days until desired daily incooom goal', forcastDailyIncooom],
                          ['Required OHM for weekly incooom goal', requiredOHMWeeklyIncooom],
                          ['Days until desired weekly incooom goal', forcastWeeklyIncooom]]

    incooomForcastData_df = pd.DataFrame(incooomForcastData, columns=['Forcast', 'Results'])
    incooomForcastDataDataTable = incooomForcastData_df.to_dict('rows')
    columns = [{'name': i,'id': i,} for i in (incooomForcastData_df.columns)]

    return roiTabulated_df,incooomForcastData_df
# end region
