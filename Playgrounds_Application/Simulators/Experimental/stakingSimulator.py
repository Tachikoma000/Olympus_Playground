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
import streamlit as st

# endregion


# region Description: Build the app
def app():
    # Data frame to hold OIP-18
    # Start by creating a dictionary
    oip18_dict = {
        'Total OHM supply range min': [
            '0', '1,000,000', '10,000,000', '100,000,000', '1,000,000,000',
            '10,000,000,000', '100,000,000,000'
        ],
        'Total OHM supply range max': [
            '1,000,000', '10,000,000', '100,000,000', '1,000,000,000',
            '10,000,000,000', '100,000,000,000', '1,000,000,000,000'
        ],
        'Min Reward Rate (%)':
            [0.3058, 0.1587, 0.1186, 0.0458, 0.0148, 0.0039, 0.0019],
        'Max Reward Rate (%)':
            [0.4583, 0.3058, 0.1587, 0.1186, 0.0458, 0.0148, 0.0039],
        'Min APY% (Assuming 90% Staked)': [10000, 1000, 500, 100, 25, 6, 3],
        'Max APY% (Assuming 90% Staked)': [100000, 10000, 1000, 500, 100, 25, 6],
    }
    # Then convert to pandas data frame
    oip18_dataFrame = pd.DataFrame(oip18_dict)
    #minOIPRate = oip18_dataFrame.min()


    with st.sidebar.expander('How to use'):
        st.write('''
                Hover your mouse over the chart trend lines to see live feedback on Total ohms accumulated vs days.
                Use the slider and number input boxes to adjust your goals and see the results displayed on the incoom charts and table. 
            ''')

    with st.sidebar.expander('Control Parameters', expanded=True):
        ohmGrowthDays = st.slider('Days', value=365, min_value=1, max_value=730, step=1)
        ohmPrice = st.text_input('Price of OHM to simulate ($)', value=500.000)
        initialOhms = st.text_input('Starting amount of OHM (Units)', value=1.0000)
        rewardYield = st.text_input('Rebase rate (%)', value=0.3928)
        minOIPRate = st.text_input('Min Reward Rate (%)', value=0.1587)
        maxOIPRate = st.text_input('Min Reward Rate (%)', value=0.3058)
        desiredUSDTarget = st.text_input('Desired OHM value (USD)', value=10000.0000,)
        desiredOHMTarget = st.text_input('Desired amount of OHMS', value=500.0000, )
        desiredDailyIncooom = st.text_input('Desired daily incooom (USD)', value=5000.0000,)
        desiredWeeklyIncooom = st.text_input('Desired weekly incooom (USD)', value=50000.000,)


        ohmGrowthDays = float(ohmGrowthDays)
        ohmPrice = float(ohmPrice)
        initialOhms = float(initialOhms)
        rewardYield = float(rewardYield)
        minOIPRate = float(minOIPRate)
        maxOIPRate = float(maxOIPRate)
        desiredUSDTarget = float(desiredUSDTarget)
        desiredOHMTarget = float(desiredOHMTarget)
        desiredDailyIncooom = float(desiredDailyIncooom)
        desiredWeeklyIncooom = float(desiredWeeklyIncooom)

    ohmGrowthResult_df = ohmGrowth_Projection(initialOhms, rewardYield, ohmGrowthDays, minOIPRate,maxOIPRate)
    roiSimulationResult_df,incooomSimulationResult_df = incooomProjection(ohmPrice,rewardYield, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom)

    dailyROI = float(roiSimulationResult_df.Percentage[0])
    fiveDayROI = float(roiSimulationResult_df.Percentage[1])
    sevenDayROI = float(roiSimulationResult_df.Percentage[2])
    oneMonthROI = float(roiSimulationResult_df.Percentage[3])
    oneYearROI = float(roiSimulationResult_df.Percentage[4])

    forcastUSDTarget = float(incooomSimulationResult_df.Results[0])
    forcastOHMTarget = float(incooomSimulationResult_df.Results[1])
    requiredOHMDailyIncooom = float(incooomSimulationResult_df.Results[2])
    forcastDailyIncooom = float(incooomSimulationResult_df.Results[3])
    requiredOHMWeeklyIncooom = float(incooomSimulationResult_df.Results[4])
    forcastWeeklyIncooom = float(incooomSimulationResult_df.Results[5])


    ohmGrowth_X = ohmGrowthResult_df.Days
    ohmGrowth_Y = ohmGrowthResult_df.Total_Ohms
    minohmGrowth_Y = ohmGrowthResult_df.Min_OhmGrowth
    maxohmGrowth_Y = ohmGrowthResult_df.Max_OhmGrowth

    ohmGrowthResult_df_Chart = go.Figure()

    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Total_Ohms, name='(3,3) ROI  ', fill=None, ))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Min_OhmGrowth, name='Min Growth Rate  ', fill=None, ))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Max_OhmGrowth, name='Max Growth Rate  ', fill='tonexty', ))

    ohmGrowthResult_df_Chart.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    ohmGrowthResult_df_Chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

    ohmGrowthResult_df_Chart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True)
    ohmGrowthResult_df_Chart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True, zeroline=False)

    st.title('Staking Playground')
    st.write("-----------------------------")

    col1, col2 = st.columns((4,1.3))
    with col1:
        st.header('OIP-18 Reward Rate Framework')
        st.table(oip18_dataFrame)
    with col2:
        st.header('Current Protocol Metrics')
        st.info(f'''
                - OHM Price: **$933.6**

                - Index: **20.7**

                - APY: **7288.2%**

                - Reward Yield: **0.3936%**

                - Supply: **2.847784e+06**
                ''')
    st.write("-----------------------------")
    col3, col4 = st.columns((4, 1.3))
    with col3:
        st.header('OHM Growth Forecast')
        st.plotly_chart(ohmGrowthResult_df_Chart,use_container_width=True)
        if ohmGrowthResult_df.Total_Ohms.max() > ohmGrowthResult_df.Max_OhmGrowth.max():
            st.write('Your simulated ohm growth deviates above max reward rate, please see the OIP-18 Frame work ')
            st.write('please see the OIP-18 Frame work and adjust accordingly: ')
        elif ohmGrowthResult_df.Total_Ohms.max() < ohmGrowthResult_df.Min_OhmGrowth.max():
            st.write('Your simulated ohm growth deviates below min reward rate ')
            st.write('please see the OIP-18 Frame work and adjust accordingly: ')
        else:
            st.write('Your simulated ohm growth is within max and min reward rate range')
    with col4:
        st.header('ROI')
        st.info(f'''
        - Daily ROI: **{dailyROI} %**
        
        - 5 Day ROI: **{fiveDayROI} %**
         
        - 7 Day ROI: **{sevenDayROI} %**
        
        - 1 Month ROI: **{oneMonthROI} %**
        
        - 1 Year ROI: **{oneYearROI} %**
        ''')
        with st.expander('Chart Explanation', expanded=True):
            st.write(f'''
            This chart shows you the ohm growth projection over **{ohmGrowthDays} days** days. Projection is calculated based on your selected rebase rate of **{rewardYield} %** and an initial **{initialOhms} ohms**.
                     ''')
    st.write("-----------------------------")

    st.header('Income Forecast')
    col5, col6 = st.columns((0.25, 0.25))
    with col5:
        st.info(f'''
        Days until desired USD value: {forcastUSDTarget}
        ''')
    with col6:
        st.info(f'''
        Days until desired OHM balance: {forcastOHMTarget}
        ''')
    col5, col6 = st.columns((0.25, 0.25))
    with col5:
        st.info(f'''
        Days until desired daily income: {forcastDailyIncooom}
        ''')
    with col6:
        st.info(f'''
        Days until desired weekly: {forcastWeeklyIncooom}
        ''')

    with st.expander("Income Breakdown"):
        st.write(f'''
                Based on your control parameters, these are the predicted outcomes assuming market stability and your parameters
                hold true. 

                - It would take **{forcastUSDTarget} days** until you accumulate enough ohms worth **$ {desiredUSDTarget}**. Keep in mind that you are also predicting 
                that the price of ohm will be **$ {ohmPrice}** on this day. 

                - It would take **{forcastOHMTarget} days** until you accumulate **{desiredOHMTarget} ohms**. Keep in mind that this prediction is calculated based on 
                    your selected rebase rate of **{rewardYield} %** and an initial of **{initialOhms} ohms** staked. Use the OIP-18 Framework to adjust your rebase rate parameter. 

                - To start earning a daily income of **$ {desiredDailyIncooom}** from staking rewards, you will need **{requiredOHMDailyIncooom} ohms**, 
                and based on the rebase rate you entered; it would take **{forcastDailyIncooom} days** to reach your goal. 
                Remember that this prediction relies on your selected rebase rate of **{rewardYield} %**, initial **{initialOhms} ohms** staked,
                and predicated price of **$ {ohmPrice}**/ohm

                - To start earning a weekly income of **$ {desiredWeeklyIncooom}** from staking rewards, you will need **{requiredOHMWeeklyIncooom} ohms**, 
                and based on the rebase rate you entered; it would take **{forcastWeeklyIncooom}** to reach your goal. 
                Remember that this prediction relies on your selected rebase rate of **{rewardYield} %**, initial **{initialOhms} ohms** staked,
                and predicated price of **$ {ohmPrice}**/ohm
                ''')
    st.write("-----------------------------")

    #st.info('Forcasts are for educational purposes alone and should not be used as financial advice')
# end region


# region Description: Function to calculate ohm growth over time
def ohmGrowth_Projection(initialOhms, rewardYield, ohmGrowthDays, minOIPRate, maxOIPRate):
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

    totalOhms_minOIPRate = []
    minOIPRate = round(minOIPRate / 100, 5)
    ohmStakedGrowth_minOIPRate = initialOhms  # Initial staked ohms used to project growth over time
    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms_minOIPRate.append(
            ohmStakedGrowth_minOIPRate)  # populate the empty array with calclated values each iteration
        ohmStakedGrowth_minOIPRate = ohmStakedGrowth_minOIPRate * (1 + minOIPRate)  # compound the total amount of ohms
    ohmGrowth_df['Min_OhmGrowth'] = totalOhms_minOIPRate  # Clean up and add the new array to the main data frame

    totalOhms_maxOIPRate = []
    maxOIPRate = round(maxOIPRate / 100, 5)
    ohmStakedGrowth_maxOIPRate = initialOhms  # Initial staked ohms used to project growth over time
    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms_maxOIPRate.append(
            ohmStakedGrowth_maxOIPRate)  # populate the empty array with calclated values each iteration
        ohmStakedGrowth_maxOIPRate = ohmStakedGrowth_maxOIPRate * (1 + maxOIPRate)  # compound the total amount of ohms
    ohmGrowth_df['Max_OhmGrowth'] = totalOhms_maxOIPRate  # Clean up and add the new array to the main data frame

    # ================================================================================
    return ohmGrowth_df
# end region

# region Description: Function to calculate income forcast
def incooomProjection(ohmPrice,rewardYield, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom):

    ohmStakedInit = initialOhms
    rewardYield = round(rewardYield / 100, 5)
    rebaseConst = 1 + rewardYield
    # current staking %APY. Need to make this read from a source or user entry
    #currentAPY = 17407 / 100

    # Let's get some ROI Outputs starting with the daily
    dailyROI = (1+rewardYield)**3 -1  # Equation to calculate your daily ROI based on reward Yield
    dailyROI_P = round(dailyROI * 100, 2)  # daily ROI in Percentage
    # ================================================================================

    # 5 day ROI
    fivedayROI = (1+rewardYield)**(5*3)-1   # Equation to calculate your 5 day ROI based on reward Yield
    fivedayROI_P = round(fivedayROI * 100, 2)  # 5 day ROI in Percentage
    # ================================================================================

    # 7 day ROI
    sevendayROI = (1+rewardYield)**( 7 * 3)-1  # Equation to calculate your 7 day ROI based on reward Yield
    sevendayROI_P = round(sevendayROI * 100, 2)  # 7 day ROI in Percentage
    # ================================================================================

    # 30 day ROI
    monthlyROI = (1+rewardYield)**( 30 *3)-1  # Equation to calculate your 30 day ROI based on reward Yield
    monthlyROI_P = round(monthlyROI * 100, 2)  # 30 day ROI in Percentage
    # ================================================================================

    # Annual ROI
    annualROI = (1+rewardYield)**( 365 *3)-1  # Equation to calculate your annual ROI based on reward Yield
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
