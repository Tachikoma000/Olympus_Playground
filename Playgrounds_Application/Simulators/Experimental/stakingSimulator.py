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
import requests


# endregion

stakingPlay_Logo = Path(__file__).parents[1] / 'Assets/stakingPlayground_logo.png'
stakingPlay_Logo  = Image.open(stakingPlay_Logo)

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

    @st.cache
    def run_query(q):

        # endpoint where you are making the request
        request = requests.post('https://api.thegraph.com/subgraphs/name/drondin/olympus-graph'
                                '',
                                json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

    # The Graph query... these queries are made available to us on the olympus sub graph -
    query = """

        {
        protocolMetrics(first: 1, orderBy: timestamp, orderDirection: desc) {
            timestamp
            ohmCirculatingSupply
            sOhmCirculatingSupply
            totalSupply
            ohmPrice
            marketCap
            totalValueLocked
            treasuryMarketValue
            treasuryRiskFreeValue
            runwayCurrent
            currentAPY
            nextEpochRebase
            nextDistributedOhm
          }
        }
        """
    result = run_query(query)

    # results come as a list of dictionaries, which is in a nested dictionary. so we have to extract the dictionary we care about
    dataDict = result['data']['protocolMetrics']
    protocolMetrics_df = pd.DataFrame(dataDict)
    protocolMetrics_df = protocolMetrics_df.astype(float)
    protocolMetrics_df['dateTime'] = pd.to_datetime(protocolMetrics_df.timestamp, unit='s')
    protocolMetrics_df['dateTime'] = protocolMetrics_df['dateTime'].dt.date
    protocolMetrics_df = protocolMetrics_df.set_index('dateTime')
    #st.write(protocolMetrics_df)

    currentOhmPrice = round(float(protocolMetrics_df.ohmPrice.iloc[0]),2)
    currentOCirc = round(float(protocolMetrics_df.ohmCirculatingSupply.iloc[0]), 2)
    currentSOCirc = round(float(protocolMetrics_df.sOhmCirculatingSupply.iloc[0]), 2)
    currentTSupply = round(float(protocolMetrics_df.totalSupply.iloc[0]), 2)
    currentMCap = round(float(protocolMetrics_df.marketCap.iloc[0]), 2)
    currentTVL = round(float(protocolMetrics_df.totalValueLocked.iloc[0]),2)
    currentTMV = round(float(protocolMetrics_df.treasuryMarketValue.iloc[0]), 2)
    currentTRFV = round(float(protocolMetrics_df.treasuryRiskFreeValue.iloc[0]), 2)
    currentRunway = round(float(protocolMetrics_df.runwayCurrent.iloc[0]), 2)
    currentAPY = round(float(protocolMetrics_df.currentAPY.iloc[0]), 2)
    currentEpochs = round(float(protocolMetrics_df.nextEpochRebase.iloc[0]), 4)
    currentNextDist = round(float(protocolMetrics_df.nextDistributedOhm.iloc[0]), 2)
    # assign the results to a variable called results

    with st.sidebar.expander('Welcome', expanded = True):
        st.write('**Staking playground** is designed to help predict ohm growth over time based on your selected control parameters.'
                ' Use each control section provided below to fine tune your results and generate new insight on possible staking reward outcomes ')

    with st.sidebar.expander('OHM growth simulation Controls'):
        st.info('''
        This section allows you to simulate your ohm growth over any number of days
        
        Use this section to input:
        - Number of days to simulate
        - OHM price at end of selected number of days
        - APY% throughout the simulation period (Your selected days) 
                ''')
        ohmGrowthDays = st.slider('Days', value=365, min_value=1, max_value=730, step=1)
        ohmPrice = st.text_input('Price of OHM to simulate ($)', value=500.000)
        initialOhms = st.text_input('Starting amount of OHM (Units)', value=1.0000)
        userAPY = st.text_input('Current APY%', value=7722.7)
        minAPY = st.text_input('Min APY% (Current Tier)', value=1000)
        maxAPY = st.text_input('Max APY% (Current Tier)', value=10000)

    with st.sidebar.expander('Profit taking simulation controls'):
        st.info('''
        This section allows you simulate and compare your ohm growth if you decide to take profit at certain intervals
        
        Use this section to input:
        - Profit taking intervals (Days)
        - Percent OHMS to sell on your profit taking days
                ''')

        sellDays = st.text_input('Sell Interval (Days)', value = 30)
        percentSale = st.text_input('Total OHMS to sell (%)', value = 5)

    with st.sidebar.expander('Dollar cost averaging simulation controls'):
        st.info('''
        This section allows you to simulte and compare your ohm growth if you decide to buy additional OHM at certain intervals
        
        Use this section to input:
        - Buying intervals (Days). (I.e I want to buy every 30 days)
        - Assumed price of OHM during your buy days.
        - Value of OHMs to buy on your buy days. (I.e Assuming my desired price of OHM is reached, I want to buy $xx worth) 
        
        It is difficult to predict the price of OHM in the future, so please use this section with caution
        ''')

        ohmPrice_DCA = st.text_input('Assumed OHM price ($)', value = 1000)
        valBuy = st.text_input('Value to buy ($)', value = 500)
        buyDays = st.text_input('Buy interval (Days)', value = 30)
        priceofETH = st.text_input('Price of ETH ($) (Needed for gas calculation)', value = 3000)
        gwei = st.text_input('Eth network fee', value = 40)

    with st.sidebar.expander('Staking rewards forecast simulation controls'):
        st.info('''
                This section allows you to simulate your future staking rewards.
            
                Use this section to input:
                - Your desired OHM value in USD
                - Your desired amount of OHMS
                - Your desired daily staking rewards
                - Your desired weekly staking rewards
                        ''')
        desiredUSDTarget = st.text_input('Desired OHM value (USD)', value=10000.0000,)
        desiredOHMTarget = st.text_input('Desired amount of OHMS', value=500.0000, )
        desiredDailyIncooom = st.text_input('Desired daily staking rewards (USD)', value=5000.0000,)
        desiredWeeklyIncooom = st.text_input('Desired weekly staking rewards (USD)', value=50000.000,)


        ohmGrowthDays = float(ohmGrowthDays)
        ohmPrice = float(ohmPrice)
        initialOhms = float(initialOhms)
        userAPY = float(userAPY)
        minAPY = float(minAPY)
        maxAPY = float(maxAPY)
        sellDays = float(sellDays)
        percentSale = float(percentSale)
        ohmPrice_DCA = float(ohmPrice_DCA)
        buyDays = float(buyDays)
        valBuy = float(valBuy)
        priceofETH = float(priceofETH)
        gwei = float(gwei)
        desiredUSDTarget = float(desiredUSDTarget)
        desiredOHMTarget = float(desiredOHMTarget)
        desiredDailyIncooom = float(desiredDailyIncooom)
        desiredWeeklyIncooom = float(desiredWeeklyIncooom)

    ohmGrowthResult_df,ohmGrowth_df_CSV = ohmGrowth_Projection(initialOhms, userAPY, ohmGrowthDays,minAPY,maxAPY, percentSale, sellDays, ohmPrice_DCA, valBuy, buyDays, gwei, priceofETH)
    roiSimulationResult_df,incooomSimulationResult_df,rewardYield = incooomProjection(ohmPrice,userAPY, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom)

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
    ProfitAdjusted_ohmGrowth_Y = ohmGrowthResult_df.Profit_Adjusted_Total_Ohms
    dollarCostAverage_ohmGrowth_Y = ohmGrowthResult_df.DCA_Adjusted_Total_Ohms
    minohmGrowth_Y = ohmGrowthResult_df.Min_OhmGrowth
    maxohmGrowth_Y = ohmGrowthResult_df.Max_OhmGrowth

    ohmGrowthResult_df_Chart = go.Figure()

    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Total_Ohms, name='(3,3) ROI  ', fill=None ))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Profit_Adjusted_Total_Ohms, name='(3,3) Profit adjusted ROI  '))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.DCA_Adjusted_Total_Ohms,name='(3,3) DCA adjusted ROI  '))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Min_OhmGrowth, name='Min Growth Rate  ', fill=None, ))
    ohmGrowthResult_df_Chart.add_trace(go.Scatter(x=ohmGrowthResult_df.Days, y=ohmGrowthResult_df.Max_OhmGrowth, name='Max Growth Rate  ', fill=None, ))

    ohmGrowthResult_df_Chart.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    ohmGrowthResult_df_Chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    ohmGrowthResult_df_Chart.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), xaxis_title = "Days", yaxis_title = "Total Ohms")

    ohmGrowthResult_df_Chart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True)
    ohmGrowthResult_df_Chart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True, zeroline=False)

    #st.title('Staking Playground')
    #st.write("-----------------------------")

    col1, col2 = st.columns((1,1))
    with col1:
        st.image(stakingPlay_Logo)
    st.markdown('''----''')

    col3, col4 = st.columns((4, 1.3))
    with col3:
        st.header('OHM Growth Forecast')
        st.plotly_chart(ohmGrowthResult_df_Chart,use_container_width=True)
    with col4:
        st.header('ROI')
        st.info(f'''
        - Daily ROI: **{dailyROI} %**

        - 5 Day ROI: **{fiveDayROI} %**

        - 7 Day ROI: **{sevenDayROI} %**

        - 1 Month ROI: **{oneMonthROI} %**
        ''')
        st.header('Chart Instructions')
        with st.expander('Click to view'):
            st.write('''
            The chart is designed to be interactive and allows you to view and analyze your results. Here are some cool things you can do:

            - Hide and view trend lines by clicking on the legends

            - Use the toolbar to access tools such as zoom, pan, data comparison, spike lines, and download. The tool bar is revealed when you hover your mouse on the chart''')
        st.download_button(
            "Press to download your (3,3) simulation results",
            ohmGrowth_df_CSV,
            "ohmGrowthSim.csv",
            "text/csv",
            key='browser-data'
        )
    st.write("-----------------------------")

    st.header('Results Explanation')
    with st.expander('Click to view'):
        st.write(f'''
        This chart shows you the ohm growth projection over **{ohmGrowthDays} days** days. Projection is calculated based on your selected APY of **{userAPY} %** (Equivalent to a reward yield of **{round((rewardYield*100),5)}%**)
         and an initial **{initialOhms} ohms**.
         
        The (3,3) Profit adjusted ROI trend line shows you the adjusted OHM growth if you decide to sell a Percentage of your OHM at a fixed interval (For example, 5% every 30 days).
        
        The Min Growth Rate shows you the estimated ohm growth rate if the APY was on the minimum APY of the current tier dictated by the OIP-18 Reward Rate Framework.
        
        The MAX Growth Rate shows you the estimated ohm growth rate if the APY was on the Maximum APY of the current tier dictated by OIP-18 Reward Rate Framework.
                ''')
    st.write("-----------------------------")

    st.header('Staking Rewards Forecast')
    col5, col6 = st.columns((0.25, 0.25))
    with col5:
        st.info(f'''
        Days until desired USD value: {forcastUSDTarget}
        ''')
    with col6:
        st.info(f'''
        Days until desired OHM balance: {forcastOHMTarget}
        ''')
    col7, col8 = st.columns((0.25, 0.25))
    with col7:
        st.info(f'''
        Days until desired daily staking rewards : {forcastDailyIncooom}
        ''')
    with col8:
        st.info(f'''
        Days until desired weekly staking rewards: {forcastWeeklyIncooom}
        ''')
    with st.expander("Staking Rewards Forcast Breakdown"):
        st.write(f'''
                Based on your control parameters, these are the predicted outcomes assuming market stability and your parameters
                hold true. 

                - It would take **{forcastUSDTarget} days** until you accumulate enough OHMS worth **$ {desiredUSDTarget}**. Keep in mind that you are also predicting 
                that the price of ohm will be **$ {ohmPrice}** on this day. 

                - It would take **{forcastOHMTarget} days** until you accumulate **{desiredOHMTarget} OHMS**. Keep in mind that this prediction is calculated based on 
                    your selected APY% of **{userAPY} %** and an initial of **{initialOhms} OHMS** staked. Use the OIP-18 Framework to adjust your APY% parameter. 

                - To start earning daily rewards of **$ {desiredDailyIncooom}**, you will need **{requiredOHMDailyIncooom} OHMS**, 
                and based on the APY% you entered; it would take **{forcastDailyIncooom} days** to reach your goal. 
                Remember that this prediction relies on your selected APY% of **{userAPY} %**, initial **{initialOhms} OHMS** staked,
                and predicated price of **$ {ohmPrice}**/OHMS

                - To start earning weekly reward of **$ {desiredWeeklyIncooom}**, you will need **{requiredOHMWeeklyIncooom} OHMS**, 
                and based on the APY% you entered; it would take **{forcastWeeklyIncooom} days** to reach your goal. 
                Remember that this prediction relies on your selected APY% of **{userAPY} %**, initial **{initialOhms} OHMS** staked,
                and predicated price of **$ {ohmPrice}**/OHMS
                ''')
    st.write("-----------------------------")

    st.header('OIP-18 Reward Rate Framework')
    with st.expander('Click to view'):
        st.write(
            '''
            The OIP-18 Framework is a tool used by the policy team to control the staking rewards based on the total supply of OHM. 
            Using this Framework, the policy team can make more predictable and refined decisions when balancing bonding emissions and staking rewards emissions. 
            Additionally, the Framework is a powerful tool for community members to adjust reward expectations when forecasting future performance. 

            Using this Framework with playgrounds is quite simple, determine the current total supply of OHM and, based on where it falls on the supply ranges on the table, choose the appropriate Min and Max APY% for the controls parameter section (Located on the sidebar). 
            The Min and Max APY% will create a "band" around your predicted OHM growth. The purpose of this band is to visually measure/compare your predicted total ohm growth against the maximum and minimum possible APYs. 
        ''')
        st.table(oip18_dataFrame)
        st.info('''
                - Learn more about OIP-18 Reward Rate Framework and why it's important here: https://forum.olympusdao.finance/d/77-oip-18-reward-rate-framework-and-reduction'
                - Gain deeper insight on the OIP-18 Frame work and view some tier transition predictions here: https://dune.xyz/pottedmeat/Emissions-Predictions
                ''')

    st.write("-----------------------------")

    st.info('''
    Learn more here: https://docs.olympusdao.finance/protocol-internals/market-dynamics

    References to system governing equations can be found here
    [OlympusDAO Gitbook:](https://docs.olympusdao.finance/) The gitbook is the best source for due diligence and understanding
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

    #st.info('Forcasts are for educational purposes alone and should not be used as financial advice')
# end region


# region Description: Function to calculate ohm growth over time
def ohmGrowth_Projection(initialOhms, userAPY, ohmGrowthDays, minAPY, maxAPY,percentSale, sellDays, ohmPrice_DCA, valBuy, buyDays, gwei, priceofETH):

    # Data frame to hold all required data point. Data required would be Epochs since rebase are distributed every Epoch
    ohmGrowthEpochs = (ohmGrowthDays * 3)+1
    sellEpochs = sellDays * 3
    buyEpochs = buyDays * 3
    cadenceConst = sellEpochs
    cadenceConst_BUY = buyEpochs
    dcaAmount = valBuy/ohmPrice_DCA
    percentSale = percentSale/100
    userAPY = userAPY/100
    minAPY = minAPY/100
    maxAPY = maxAPY/100

    gwei = 100
    priceofETH = 4000
    stakingGasFee = 179123 * ((gwei * priceofETH) / (10 ** 9))
    stakingGasFee_OHMAmount = stakingGasFee/ohmPrice_DCA
    #unstakingGasFee = 89654 * ((gwei * priceofETH) / (10 ** 9))


    rewardYield = ((1+userAPY)**(1/float(1095)))-1
    minOIPYield = ((1 + minAPY) ** (1 / float(1095))) - 1
    maxOIPYield = ((1 + maxAPY) ** (1 / float(1095))) - 1


    ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])  # In this case let's consider 1096 Epochs which is 365 days
    ohmGrowth_df['Days'] = ohmGrowth_df.Epochs / 3  # There are 3 Epochs per day so divide by 3 to get Days

    profitAdjusted_ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])
    profitAdjusted_ohmGrowth_df['Days'] = profitAdjusted_ohmGrowth_df.Epochs / 3

    dollarCostAVG_ohmGrowth_df = pd.DataFrame(np.arange(ohmGrowthEpochs),columns=['Epochs'])
    dollarCostAVG_ohmGrowth_df['Days'] = profitAdjusted_ohmGrowth_df.Epochs / 3

    # To Calculate the ohm growth over 3000 Epochs or 1000 days, we loop through the exponential ohm growth equation every epoch
    totalOhms = []  # create an empty array that will hold the componded rewards
    pA_totalOhms = []
    dcA_totalOhms = []

    rewardYield = round(rewardYield, 5)
    ohmStakedGrowth = initialOhms  # Initial staked ohms used to project growth over time
    pA_ohmStakedGrowth = initialOhms
    dcA_ohmStakedGrowth = initialOhms


    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms.append(ohmStakedGrowth)  # populate the empty array with calclated values each iteration
        pA_totalOhms.append(pA_ohmStakedGrowth)
        dcA_totalOhms.append(dcA_ohmStakedGrowth)


        ohmStakedGrowth = ohmStakedGrowth * (1 + rewardYield)  # compound the total amount of ohms
        pA_ohmStakedGrowth = pA_ohmStakedGrowth * (1 + rewardYield)
        dcA_ohmStakedGrowth = dcA_ohmStakedGrowth * (1 + rewardYield)

        if elements == sellEpochs:
            sellEpochs = sellEpochs + cadenceConst
            #print(totalOhms[-1] - (totalOhms[-1] * percentSale))
            pA_ohmStakedGrowth = pA_totalOhms[-1] - (pA_totalOhms[-1]*percentSale)
        else:
            pass

        if elements == buyEpochs:
            buyEpochs = buyEpochs + cadenceConst_BUY
            #print(dcA_ohmStakedGrowth)
            dcA_ohmStakedGrowth = (dcA_ohmStakedGrowth + (dcaAmount-stakingGasFee_OHMAmount))
            #st.write(stakingGasFee_OHMAmount)
            #print(dcA_ohmStakedGrowth)
        else:
            pass

    ohmGrowth_df['Total_Ohms'] = totalOhms  # Clean up and add the new array to the main data frame
    ohmGrowth_df['Profit_Adjusted_Total_Ohms'] = pA_totalOhms
    ohmGrowth_df['DCA_Adjusted_Total_Ohms'] = dcA_totalOhms
    ohmGrowth_df.Days = np.around( ohmGrowth_df.Days, decimals=1)  # Python is funny so let's round up our numbers . 1 decimal place for days",
    ohmGrowth_df.Total_Ohms = np.around( ohmGrowth_df.Total_Ohms, decimals=3 )  # Python is funny so let's round up our numbers . 3 decimal place for ohms"
    ohmGrowth_df.Profit_Adjusted_Total_Ohms = np.around(ohmGrowth_df.Profit_Adjusted_Total_Ohms, decimals=3)
    ohmGrowth_df.DCA_Adjusted_Total_Ohms = np.around(ohmGrowth_df.DCA_Adjusted_Total_Ohms, decimals=3)


    totalOhms_minOIPRate = []
    minOIPYield = round(minOIPYield, 5)
    ohmStakedGrowth_minOIPRate = initialOhms  # Initial staked ohms used to project growth over time
    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms_minOIPRate.append(
            ohmStakedGrowth_minOIPRate)  # populate the empty array with calclated values each iteration
        ohmStakedGrowth_minOIPRate = ohmStakedGrowth_minOIPRate * (1 + minOIPYield)  # compound the total amount of ohms
    ohmGrowth_df['Min_OhmGrowth'] = totalOhms_minOIPRate  # Clean up and add the new array to the main data frame

    totalOhms_maxOIPRate = []
    maxOIPYield = round(maxOIPYield, 5)
    ohmStakedGrowth_maxOIPRate = initialOhms  # Initial staked ohms used to project growth over time
    # Initialize the for loop to have loops equal to number of rows or number of epochs
    for elements in ohmGrowth_df.Epochs:
        totalOhms_maxOIPRate.append(
            ohmStakedGrowth_maxOIPRate)  # populate the empty array with calclated values each iteration
        ohmStakedGrowth_maxOIPRate = ohmStakedGrowth_maxOIPRate * (1 + maxOIPYield)  # compound the total amount of ohms
    ohmGrowth_df['Max_OhmGrowth'] = totalOhms_maxOIPRate  # Clean up and add the new array to the main data frame

    ohmGrowth_df_CSV = ohmGrowth_df.to_csv().encode('utf-8')
    # ================================================================================


    return ohmGrowth_df,ohmGrowth_df_CSV
# end region

# region Description: Function to calculate income forcast
def incooomProjection(ohmPrice,userAPY, initialOhms, desiredUSDTarget,desiredOHMTarget, desiredDailyIncooom,desiredWeeklyIncooom):

    ohmStakedInit = initialOhms
    userAPY = userAPY / 100
    rewardYield = ((1 + userAPY) ** (1 / float(1095))) - 1
    rewardYield = round(rewardYield, 5)
    rebaseConst = 1 + rewardYield
    # current staking %APY. Need to make this read from a source or user entry
    #currentAPY = 17407 / 100

    # Let's get some ROI Outputs starting with the daily
    dailyROI = (1+rewardYield)**3 -1  # Equation to calculate your daily ROI based on reward Yield
    dailyROI_P = round(dailyROI * 100, 1)  # daily ROI in Percentage
    # ================================================================================

    # 5 day ROI
    fivedayROI = (1+rewardYield)**(5*3)-1   # Equation to calculate your 5 day ROI based on reward Yield
    fivedayROI_P = round(fivedayROI * 100, 1)  # 5 day ROI in Percentage
    # ================================================================================

    # 7 day ROI
    sevendayROI = (1+rewardYield)**( 7 * 3)-1  # Equation to calculate your 7 day ROI based on reward Yield
    sevendayROI_P = round(sevendayROI * 100, 1)  # 7 day ROI in Percentage
    # ================================================================================

    # 30 day ROI
    monthlyROI = (1+rewardYield)**( 30 *3)-1  # Equation to calculate your 30 day ROI based on reward Yield
    monthlyROI_P = round(monthlyROI * 100, 1)  # 30 day ROI in Percentage
    # ================================================================================

    # Annual ROI
    annualROI = (1+rewardYield)**( 365 *3)-1  # Equation to calculate your annual ROI based on reward Yield
    annualROI_P = round(annualROI * 100, 1)  # Equation to calculate your annual ROI based on reward Yield
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

    return roiTabulated_df,incooomForcastData_df, rewardYield
# end region
